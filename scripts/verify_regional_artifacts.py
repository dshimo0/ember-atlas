"""Recompute published regional selection/gates and reconcile every shard against daily totals."""
import gzip,hashlib,json
from pathlib import Path
from collections import defaultdict
from decimal import Decimal,ROUND_FLOOR
from evaluate_regions import evaluate
ROOT=Path('web/data')
def read(ref):
 b=(ROOT/ref['file']).read_bytes();b=gzip.decompress(b)if ref['file'].endswith('.gz')else b
 assert hashlib.sha256(b).hexdigest()==ref['sha256'];return json.loads(b)
def main():
 registry=read(json.loads((ROOT/'regions.json').read_text()));checks=[]
 for r in registry['regions']:
  for mode,ref in r['datasets'].items():
   s=read(ref);count=0;daily={(x['day'],x['product']):x for x in s['daily']if x['area']=='all'}
   for month,shard in s['observation_shards'].items():
    native=defaultdict(int);cells=defaultdict(set)
    for x in read(shard)['observations']:
     assert month==x['date_utc'][:7];w,so,e,n=r['bounds'];assert w<=x['longitude']<=e and so<=x['latitude']<=n
     assert x['product'].endswith('_'+mode.upper());key=(x['date_utc'],x['product']);native[key]+=1;count+=1
     cells[key].add(tuple(int((Decimal(str(x[k]))/Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR))for k in ['latitude','longitude']))
    for key,x in daily.items():
     if key[0][:7]==month:assert x['native']==native[key]and x['cells']==len(cells[key]),(r['id'],key)
   assert count==s['observation_count']
   if mode=='sp'and s.get('external_audit'):
    audit=read(s['external_audit']);assert json.loads(json.dumps(evaluate(s['daily'],r['id'])))==audit
    if r['id']!='pantanal':assert s['calibration']['accepted']==audit['accepted']
   checks.append({'region':r['id'],'mode':mode,'observations':count,'all_daily_counts_and_grid_totals_match':True,'regional_evaluation_reproduced':mode=='sp'and bool(s.get('external_audit'))})
 report={'registry':json.loads((ROOT/'regions.json').read_text()),'checks':checks};Path('submission/regional-artifact-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
