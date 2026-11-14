"""Frozen seasonal transfer; monthly occupied cell-days, never ground truth."""
import argparse
import calendar
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from firms import atomic_write

MODIS, VIIRS = 'MODIS_SP', 'VIIRS_NOAA20_SP'
VERSION = 'ember-seasonal-v1'

def evaluate(rows, train, holdout):
    train, holdout = set(train), set(holdout)
    if not train or not holdout or train & holdout:
        raise ValueError('Require nonempty disjoint training and holdout years')
    if len({r['bbox'] for r in rows}) != 1:
        raise ValueError('Require exactly one AOI')
    grouped = defaultdict(dict)
    for r in rows:
        if r['source'] not in (MODIS, VIIRS):
            continue
        key = (r['date_utc'][:7], r['source'])
        day = int(r['date_utc'][8:10])
        if day in grouped[key]:
            raise ValueError('Duplicate product/day')
        grouped[key][day] = (int(r['raw_detections']), int(r['occupied_cells_0_05deg']))
    months, exclusions = [], []
    for month in sorted({k[0] for k in grouped}):
        y, m = map(int, month.split('-'))
        expected = set(range(1, calendar.monthrange(y,m)[1]+1))
        values = {s:grouped.get((month,s),{}) for s in (MODIS,VIIRS)}
        if any(set(v) != expected for v in values.values()):
            exclusions.append({'month':month,'reason':'Incomplete paired retrieval'})
            continue
        out = {'month':month,'year':y,'season':(m%12)//3,'split':'train' if y in train else 'holdout' if y in holdout else 'other'}
        for s,v in values.items():
            out[s] = sum(a[1] for a in v.values())
            out[s+'_native'] = sum(a[0] for a in v.values())
        months.append(out)
    training = [r for r in months if r['split']=='train']
    testing = [r for r in months if r['split']=='holdout']
    support = len({r['year'] for r in training})>=3 and len({r['year'] for r in testing})>=2
    denominator = sum(r[VIIRS] for r in training)
    pooled = sum(r[MODIS] for r in training)/denominator if support and denominator else None
    factors = {}
    for season in range(4):
        subset = [r for r in training if r['season']==season]
        den = sum(r[VIIRS] for r in subset)
        enough = len(subset)>=6 and len({r['year'] for r in subset})>=3 and den>=100
        factors[str(season)] = {'factor':sum(r[MODIS] for r in subset)/den if support and enough else pooled,'rule':'seasonal' if support and enough else 'pooled fallback'}
    valid = bool(testing) and all(factors[str(r['season'])]['factor'] is not None for r in testing)
    def metrics(adjust):
        errors = [r[VIIRS]*(factors[str(r['season'])]['factor'] if adjust else 1)-r[MODIS] for r in testing]
        return {'mae':mean(map(abs,errors)), 'signed_bias':mean(errors),'n_months':len(errors)} if errors else None
    baseline = metrics(False)
    adjusted = metrics(True) if valid else None
    accepted = bool(valid and adjusted['mae'] < baseline['mae'] and abs(adjusted['signed_bias']) <= abs(baseline['signed_bias']))
    for r in months:
        r['factor'] = factors[str(r['season'])]['factor'] if accepted else None
        r['adjusted_viirs'] = r[VIIRS]*r['factor'] if accepted else None
    return {'method_version':VERSION,'unit':'occupied cell-days','grid':'globally anchored WGS84 0.05 degree; floor coordinate/0.05','bbox':rows[0]['bbox'], 'products':[MODIS,VIIRS], 'train_years':sorted(train),'holdout_years':sorted(holdout),'support_rule':'3 training and 2 holdout years; seasonal >=6 months, >=3 years, >=100 VIIRS cell-days; otherwise pooled', 'acceptance_rule':'Strictly lower holdout monthly MAE and no greater absolute signed bias','factors':factors,'baseline':baseline,'adjusted':adjusted,'accepted':accepted,'reason':'Passed frozen criterion' if accepted else 'Insufficient overlap or failed improvement criterion','training_months':len(training),'holdout_months':len(testing),'exclusions':exclusions,'months':months,'limitations':['MODIS is a reference, not truth','Observation coverage unknown without swath masks','No uncertainty interval: too few independent years','Transfer restricted to fitted AOI, months and product pair']}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path); p.add_argument('output',type=Path)
    p.add_argument('--train',required=True); p.add_argument('--holdout',required=True)
    a=p.parse_args()
    rows=list(csv.DictReader(a.input.open()))
    result=evaluate(rows,map(int,a.train.split(',')),map(int,a.holdout.split(',')))
    result['input_sha256']=hashlib.sha256(a.input.read_bytes()).hexdigest()
    a.output.mkdir(parents=True,exist_ok=True)
    atomic_write(a.output/'validation.json',json.dumps(result,indent=2).encode())
    import io
    b=io.StringIO(); w=csv.DictWriter(b,fieldnames=list(result['months'][0]) if result['months'] else ['month']); w.writeheader(); w.writerows(result['months'])
    atomic_write(a.output/'monthly_comparison.csv',b.getvalue().encode())

if __name__=='__main__': main()
