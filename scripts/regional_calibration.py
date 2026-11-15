"""Isolated local FIRMS acquisition and regional evaluation; never publishes models."""
import argparse
import csv
import hashlib
import io
import json
import os
import time
from collections import defaultdict
from datetime import date
from pathlib import Path

from firms import atomic_write, bounds, fetch, windows
from build_regions import read_inputs
from build_calendar import grid_cell
from harmonize import analyze
from evaluate_replay import evaluate

ROOT = Path(__file__).resolve().parents[1]
CHILECITO = {'id': 'chilecito', 'name': 'Chilecito study area',
             'bounds': [-68, -30, -67, -29]}


def fetch_with_quota_retry(key, product, bbox, start, end, raw):
    for attempt in range(4):
        try:
            return fetch(key, product, bbox, start, end, raw)
        except ValueError as error:
            if 'quota exceeded' not in str(error).lower() or attempt == 3:
                raise
            print(f'FIRMS quota exceeded. Waiting 11 minutes before retry {attempt + 1}/3. '
                  'Keep this terminal open; Ctrl+C stops safely.', flush=True)
            for minute in range(11):
                time.sleep(60)
                print(f'Quota pause: {minute + 1}/11 minutes elapsed.', flush=True)


def regions():
    entries = json.loads((ROOT / 'data/region-definitions-v1.json').read_text(encoding='utf-8'))['regions']
    return {r['id']: r for r in entries + [CHILECITO]}


def daily_rows(observations, covered, bbox):
    counts, cells = defaultdict(int), defaultdict(set)
    for observations_in_month in observations.values():
        for r in observations_in_month:
            key = (r['date_utc'], r['product'])
            counts[key] += 1
            cells[key].add(grid_cell(str(r['latitude']), str(r['longitude'])))
    return [{'bbox': bbox, 'date_utc': day, 'source': product,
             'raw_detections': counts[day, product],
             'occupied_cells_0_05deg': len(cells[day, product])}
            for product, days in sorted(covered.items()) for day in sorted(days)]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['plan', 'fetch', 'evaluate'])
    p.add_argument('--region', choices=list(regions()), default='chilecito')
    p.add_argument('--start', type=date.fromisoformat, default=date(2020, 1, 1))
    p.add_argument('--end', type=date.fromisoformat, default=date(2024, 12, 31))
    p.add_argument('--sources', default='MODIS_SP,VIIRS_NOAA20_SP',
                   choices=['MODIS_SP,VIIRS_NOAA20_SP', 'MODIS_SP', 'MODIS_NRT,VIIRS_NOAA20_NRT'])
    p.add_argument('--train', default='2020,2021,2022')
    p.add_argument('--holdout', default='2023,2024')
    p.add_argument('--pause', type=float, default=2.0)
    p.add_argument('--out', type=Path, default=ROOT / 'data/local-calibration')
    a = p.parse_args()
    if a.end < a.start or a.pause < 0:
        p.error('Dates must be ascending and pause nonnegative.')
    r = regions()[a.region]
    bbox = bounds(','.join(map(str, r['bounds'])))
    # Date-specific folders prevent overlapping acquisition runs from silently merging.
    base = a.out / a.region / f'{a.start}_{a.end}'
    raw = base / ('nrt' if 'NRT' in a.sources else 'sp')
    jobs = [(product, start, end) for start, end in windows(a.start, a.end)
            for product in a.sources.split(',')]
    protocol = {'region': r, 'start': str(a.start), 'end': str(a.end),
                'sources': a.sources, 'train': a.train, 'holdout': a.holdout,
                'requests': len(jobs), 'geometry': 'project-defined exploratory rectangle',
                'publication_approved': False}
    if a.command == 'plan':
        print(json.dumps(protocol, indent=2))
        return
    key = os.environ.get('FIRMS_MAP_KEY', '')
    try:
        if a.command == 'fetch':
            if not key:
                raise ValueError('Set FIRMS_MAP_KEY in the environment.')
            atomic_write(base / 'acquisition-plan.json', json.dumps(protocol, indent=2).encode())
            failures = []
            for product, start, end in jobs:
                try:
                    fetch_with_quota_retry(key, product, bbox, start, end, raw)
                except (OSError, ValueError) as error:
                    failures.append({'product': product, 'start': str(start), 'end': str(end),
                                     'error': str(error).replace(key, '[redacted]')})
                    # Stop on first error to avoid thousands of quota/unavailable requests.
                    break
                time.sleep(a.pause)
            atomic_write(base / 'acquisition-status.json', json.dumps({'plan': protocol,
                         'failures': failures, 'complete': not failures}, indent=2).encode())
            if failures:
                raise ValueError('Acquisition stopped; inspect acquisition-status.json and rerun the same command to resume.')
            return
        if a.sources != 'MODIS_SP,VIIRS_NOAA20_SP':
            raise ValueError('Evaluation requires the paired SP products; NRT and historical MODIS remain separate.')
        obs, manifests, covered = read_inputs(raw, r['bounds'], 'SP')
        rows = daily_rows(obs, covered, bbox)
        if not rows:
            raise ValueError('No verified input files. Run fetch first.')
        buf = io.StringIO(newline='')
        writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        payload = buf.getvalue().encode()
        result = analyze(rows, list(map(int, a.train.split(','))), list(map(int, a.holdout.split(','))))
        result.update(region=r, input_sha256=hashlib.sha256(payload).hexdigest(),
                      publication_approved=False, protocol=protocol,
                      source_manifests=manifests)
        atomic_write(base / 'daily.csv', payload)
        atomic_write(base / 'validation.json', json.dumps(result, indent=2).encode())
        if result['unadjusted']['n'] < 24 or len([m for m in result['monthly'] if m['year'] in result['train_years']]) < 36:
            raise ValueError('Insufficient complete paired months; see validation.json. No model approved.')
        # Round-trip converts factor keys to strings expected by the existing evaluator.
        evidence = evaluate(json.loads(json.dumps(result)))
        evidence['scope'] = f"{r['name']} {r['bounds']} only"
        evidence['publication_approved'] = False
        atomic_write(base / 'comparison.json', json.dumps(evidence, indent=2).encode())
        print(json.dumps({'output': str(base), 'legacy_gate_passed': result['accepted'],
                          'metrics': evidence['metrics'], 'publication_approved': False}, indent=2))
    except (OSError, ValueError, AssertionError, ZeroDivisionError) as error:
        message = str(error)
        if key:
            message = message.replace(key, '[redacted]')
        p.exit(1, message + '\n')


if __name__ == '__main__':
    main()
