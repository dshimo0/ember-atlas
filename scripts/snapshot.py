"""Publish a content-addressed, checksum-verified snapshot with original observations."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from build_calendar import aggregate
from firms import atomic_write, read_csv

def build(raw, output):
    days=aggregate(raw)  # verify every checksum/window before publishing anything
    observations=[]; manifests=[]
    for path in sorted(raw.rglob('*.json')):
        meta=json.loads(path.read_text()); manifests.append(meta)
        seen=set()
        for row in read_csv(path.with_suffix('.csv').read_bytes()):
            key=tuple(sorted(row.items()))
            if key in seen: continue
            seen.add(key)
            observations.append({**row,'source':meta['source'],'bbox':meta['bbox'],'source_sha256':meta['sha256']})
    payload={'method_version':'ember-grid-v1','observation_coverage':'unknown','manifests':manifests,'daily':[dict(zip(['date_utc','bbox','source','raw_detections','occupied_cells_0_05deg'],[str(k[0]),k[1],k[2],*v])) for k,v in sorted(days.items())],'observations':observations}
    b=json.dumps(payload,separators=(',',':')).encode(); identity=hashlib.sha256(b).hexdigest()
    atomic_write(output/f'{identity}.json',b)
    atomic_write(output/'latest.json',json.dumps({'snapshot':f'{identity}.json','sha256':identity}).encode())
    return identity
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('raw',type=Path); p.add_argument('output',type=Path); a=p.parse_args(); print(build(a.raw,a.output))
