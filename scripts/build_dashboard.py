"""Derive versioned daily UI aggregates and monthly observation shards from a pinned snapshot.

No fitting or ingestion. Full-area monthly values must reconcile with validation.json.
"""
import calendar,gzip,hashlib,json
from collections import defaultdict
from datetime import date,timedelta
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from firms import atomic_write

ROOT=Path('web/data')
def encode(value):return json.dumps(value,separators=(',',':'),sort_keys=True).encode()
def publish(prefix,value,compressed=False):
    payload=encode(value);digest=hashlib.sha256(payload).hexdigest()
    name=f'{prefix}-{digest[:12]}.json'+('.gz' if compressed else '')
    atomic_write(ROOT/name,gzip.compress(payload,mtime=0) if compressed else payload)
    return {'file':name,'sha256':digest}
def main():
    index=json.loads((ROOT/'latest.json').read_text())
    payload=gzip.decompress((ROOT/index['file']).read_bytes())
    if hashlib.sha256(payload).hexdigest()!=index['sha256']:raise ValueError('Snapshot checksum mismatch')
    snapshot=json.loads(payload);validation=json.loads((ROOT/'validation.json').read_text())
    coverage=defaultdict(set)
    for m in snapshot['manifests']:
        d=date.fromisoformat(m['start'])
        while d<=date.fromisoformat(m['end']):coverage[m['source']].add(str(d));d+=timedelta(days=1)
    counts=defaultdict(int);cells=defaultdict(set);months=defaultdict(list)
    for r in snapshot['observations']:
        months[r['date_utc'][:7]].append(r)
        region='north' if r['latitude']>=-19 else 'south'
        cell=tuple(int((Decimal(str(r[k]))/Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR)) for k in ['latitude','longitude'])
        for area in ['all',region]:
            key=(r['date_utc'],r['product'],area);counts[key]+=1;cells[key].add(cell)
    daily=[]
    for product,days in sorted(coverage.items()):
        for day in sorted(days):
            for area in ['all','north','south']:
                key=(day,product,area)
                daily.append({'day':day,'product':product,'area':area,'native':counts[key],'cells':len(cells[key])})
    # Compare every released month, in both units, with the frozen scientific artifact.
    for m in validation['monthly']:
        for product,key in [('MODIS_SP','modis'),('VIIRS_NOAA20_SP','viirs')]:
            rows=[d for d in daily if d['area']=='all' and d['product']==product and d['day'].startswith(m['month'])]
            assert len(rows)==calendar.monthrange(m['year'],int(m['month'][5:]))[1]
            assert sum(d['cells'] for d in rows)==m[key],m['month']
            assert sum(d['native'] for d in rows)==m[key+'_native'],m['month']
    shards={month:publish('observations-'+month,{'snapshot_sha256':index['sha256'],'month':month,'observations':rows},True) for month,rows in sorted(months.items())}
    validation_ref=publish('validation',validation)
    summary={'schema':'ember-dashboard-2','metric_method':validation['method'],'grid_degrees':validation['grid_degrees'],'snapshot':index,'built_utc':snapshot['built_utc'],'validation':validation_ref,'bounds':[-59,-23,-54,-15],'daily':daily,'observation_shards':shards,'observation_count':len(snapshot['observations']),'manifest_count':len(snapshot['manifests']),'coverage':{'start':min(d['day'] for d in daily),'end':max(d['day'] for d in daily)},'observation_coverage':'unknown'}
    ref=publish('dashboard',summary)
    atomic_write(ROOT/'dashboard.json',encode(dict(ref,snapshot=index,validation=validation_ref)))
    print(json.dumps({'summary':ref,'shards':len(shards),'observations':len(snapshot['observations']),'all_released_months_reconciled':True}))
if __name__=='__main__':main()
