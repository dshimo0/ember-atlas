"""Build immutable regional summaries/shards from verified extracts without changing the frozen fit."""
import calendar,gzip,hashlib,json
from collections import defaultdict
from datetime import date,datetime,timezone
from pathlib import Path
from firms import atomic_write,read_csv,DAY
from build_calendar import grid_cell
from build_dashboard import publish,encode
from source_archives import unpack

ROOT=Path('web/data')
def read_inputs(directory,bbox,expected_class):
 observations=defaultdict(list);manifests=[];covered=defaultdict(set);seen=set()
 for path in sorted(directory.rglob('*.json')):
  m=json.loads(path.read_text());payload=path.with_suffix('.csv').read_bytes()
  assert hashlib.sha256(payload).hexdigest()==m['sha256'],path
  assert list(map(float,m['bbox'].split(',')))==bbox,path
  assert m['processing_class']==expected_class and m['source'].endswith('_'+expected_class),path
  rows=list(read_csv(payload));assert len(rows)==m['rows'],path
  start,end=date.fromisoformat(m['start']),date.fromisoformat(m['end']);d=start
  while d<=end:
   assert str(d) not in covered[m['source']],'Overlapping windows'
   covered[m['source']].add(str(d));d+=DAY
  for r in rows:
   assert str(start)<=r['acq_date']<=str(end),path
   lat,lon=float(r['latitude']),float(r['longitude']);assert bbox[0]<=lon<=bbox[2] and bbox[1]<=lat<=bbox[3],path
   time=r['acq_time'].zfill(4);assert len(time)==4 and time.isdecimal() and int(time[:2])<24 and int(time[2:])<60,path
   key=(m['source'],r['satellite'],r['acq_date'],time,lat,lon)
   if key in seen:continue
   seen.add(key)
   observations[r['acq_date'][:7]].append({'latitude':lat,'longitude':lon,'date_utc':r['acq_date'],'time_utc':time,'product':m['source'],'platform':r['satellite'],'confidence':r.get('confidence',''),'frp_mw':r.get('frp',''),'daynight':r.get('daynight',''),'source':str(path)})
  manifests.append(dict(m,reference=str(path)))
 return observations,manifests,covered

def build(region,mode,base,validation_ref):
 is_pantanal=region['id']=='pantanal';bbox=region['bounds']
 directory=Path('data/history') if is_pantanal and mode=='sp' else Path('data/regions')/region['id']/mode
 obs,manifests,covered=read_inputs(directory,bbox,mode.upper())
 if not covered and not(is_pantanal and mode=='sp'):return None
 inputs={'schema':'ember-region-evidence-1','region':region['id'],'bounds':bbox,'processing_class':mode.upper(),'grid_degrees':.05,'manifests':manifests,'normalization':'Deduplicate product/platform/UTC time/coordinates; retain source manifest; occupied globally anchored 0.05-degree WGS84 cells per UTC day.'}
 archive_index=Path('data/source-archives/index.json')
 if archive_index.exists():inputs['raw_archive_index']={'path':str(archive_index),'sha256':hashlib.sha256(archive_index.read_bytes()).hexdigest(),'url':'https://github.com/dshimo0/ember-atlas/blob/work/data/source-archives/index.json'}
 if is_pantanal and mode=='sp':inputs['base_snapshot']=base['snapshot']
 inventory=publish(region['id']+'-'+mode+'-evidence',inputs)
 counts=defaultdict(int);cells=defaultdict(set)
 for rows in obs.values():
  for r in rows:
   areas=['all', 'north'if r['latitude']>=-19 else 'south']if is_pantanal else ['all']
   for area in areas:
    key=(r['date_utc'],r['product'],area);counts[key]+=1;cells[key].add(grid_cell(str(r['latitude']),str(r['longitude'])))
 daily=[]
 for product,days in sorted(covered.items()):
  for day in sorted(days):
   for area in (['all','north','south']if is_pantanal else ['all']):
    key=(day,product,area);daily.append({'day':day,'product':product,'area':area,'native':counts[key],'cells':len(cells[key])})
 # Publish even a successfully retrieved empty month, with an empty observation array.
 months=sorted({day[:7]for days in covered.values()for day in days})
 shards={month:dict(publish(region['id']+'-'+mode+'-observations-'+month,{'snapshot_sha256':inventory['sha256'],'month':month,'observations':obs[month]},True),dataset_sha256=inventory['sha256'])for month in months}
 observation_count=sum(map(len,obs.values()));manifest_count=len(manifests)
 latest=max((m['retrieved_at']for m in manifests),default=base['built_utc'])
 if is_pantanal and mode=='sp':
  assert not any(r['day']>='2020-01-01'for r in daily),'History overlaps frozen release'
  daily+=base['daily'];shards.update({m:dict(ref,dataset_sha256=base['snapshot']['sha256'])for m,ref in base['observation_shards'].items()})
  observation_count+=base['observation_count'];manifest_count+=base['manifest_count']
 products=sorted({r['product']for r in daily});coverage={'start':min(r['day']for r in daily),'end':max(r['day']for r in daily)}
 product_coverage={product:{'start':min(r['day']for r in daily if r['product']==product),'end':max(r['day']for r in daily if r['product']==product),'retrieved_days':sum(1 for r in daily if r['product']==product and r['area']=='all')}for product in products}
 summary={'schema':'ember-regional-dashboard-1','region':region['id'],'name':region['name'],'bounds':bbox,'processing_class':mode.upper(),'metric_method':'ember-1','grid_degrees':.05,'snapshot':inventory,'validation':validation_ref,'built_utc':latest,'daily':sorted(daily,key=lambda r:(r['day'],r['product'],r['area'])),'observation_shards':dict(sorted(shards.items())),'observation_count':observation_count,'manifest_count':manifest_count,'coverage':coverage,'product_coverage':product_coverage,'products':products,'observation_coverage':'unknown; no usable swath/cloud masks','calibration':{'evaluated':is_pantanal and mode=='sp','geography':'Pantanal study area only','period':'2020-01-01/2024-12-31'if is_pantanal and mode=='sp'else None,'reason':None if is_pantanal and mode=='sp'else 'No independently evaluated regional SP calibration; NRT remains separate.'}}
 ref=publish(region['id']+'-'+mode+'-dashboard',summary)
 return dict(ref,coverage=coverage,products=products,observations=observation_count,last_retrieval_utc=latest)

def main():
 unpack()
 definitions=json.loads(Path('data/region-definitions-v1.json').read_text());p=json.loads((ROOT/'dashboard.json').read_text());base=json.loads((ROOT/p['file']).read_text());regions=[]
 for region in definitions['regions']:
  r=dict(region,geometry_type='bounding box',source=definitions['geometry_source'],source_url=definitions['source_url'])
  w,s,e,n=r['bounds'];r['geometry']={'type':'Polygon','coordinates':[[[w,s],[e,s],[e,n],[w,n],[w,s]]]}
  r['datasets']={}
  for mode in ['sp','nrt']:
   ref=build(region,mode,base,p['validation'])
   if ref:r['datasets'][mode]=ref
  r['available_products']=sorted({product for d in r['datasets'].values()for product in d['products']});regions.append(r)
  print(r['id'],{k:v['observations']for k,v in r['datasets'].items()},flush=True)
 registry={'schema':'ember-regions-1','crs':definitions['crs'],'definition_sha256':hashlib.sha256(Path('data/region-definitions-v1.json').read_bytes()).hexdigest(),'regions':regions}
 ref=publish('regions',registry);atomic_write(ROOT/'regions.json',encode(ref));print(json.dumps(ref))
if __name__=='__main__':main()
