"""Build immutable regional summaries/shards from verified extracts without changing the frozen fit."""
import calendar,gzip,hashlib,json,tempfile
from collections import defaultdict
from datetime import date,datetime,timezone
from pathlib import Path
from firms import atomic_write,read_csv,DAY
from build_calendar import grid_cell
from build_dashboard import publish,encode
from source_archives import unpack
from stream_region import stream_inputs
from evaluate_regions import evaluate,comparison_document

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

def build(region,mode,base,validation_ref,previous=None,regional_validation=None):
 is_pantanal=region['id']=='pantanal';bbox=region['bounds']
 directory=Path('data/regions')/region['id']/mode
 directories=[Path('data/history'),directory]if is_pantanal and mode=='sp'else[directory]
 with tempfile.TemporaryDirectory(prefix='ember-months-')as tmp:
  spool=Path(tmp);daily,manifests,covered,observation_count=stream_inputs(directories,bbox,mode.upper(),spool,is_pantanal)
  if not covered and not(is_pantanal and mode=='sp'):return None
  inputs={'schema':'ember-region-evidence-2','region':region['id'],'bounds':bbox,'processing_class':mode.upper(),'grid_degrees':.05,'manifests':manifests,'normalization':'Deduplicate within nonoverlapping source windows by product/platform/UTC time/coordinates; preserve source; occupied global 0.05-degree cells/UTC day.'}
  archive_index=Path('data/source-archives/index.json')
  if archive_index.exists():
   payload=archive_index.read_bytes();digest=hashlib.sha256(payload).hexdigest();version=archive_index.with_name('index-'+digest[:12]+'.json');atomic_write(version,payload)
   inputs['raw_archive_index']={'path':str(version),'sha256':digest,'url':'https://github.com/dshimo0/ember-atlas/blob/work/'+str(version)}
  if is_pantanal and mode=='sp':inputs['base_snapshot']=base['snapshot']
  inventory=publish(region['id']+'-'+mode+'-evidence',inputs)
  shards={};months=sorted({day[:7]for days in covered.values()for day in days})
  for month in months:
   path=spool/(month+'.jsonl');rows=[json.loads(line)for line in path.open()]if path.exists()else[]
   obs_hash=hashlib.sha256(encode(rows)).hexdigest();old=previous.get('observation_shards',{}).get(month)if previous else None
   if old:
    old_hash=old.get('observations_sha256')
    if not old_hash:
     old_data=json.loads(gzip.decompress((ROOT/old['file']).read_bytes()));old_hash=hashlib.sha256(encode(old_data['observations'])).hexdigest()
    if old_hash==obs_hash:
     shards[month]=dict(old,observations_sha256=obs_hash);continue
   shards[month]=dict(publish(region['id']+'-'+mode+'-observations-'+month,{'snapshot_sha256':inventory['sha256'],'month':month,'observations':rows},True),dataset_sha256=inventory['sha256'],observations_sha256=obs_hash)
  manifest_count=len(manifests);latest=max((m['retrieved_at']for m in manifests),default=base['built_utc'])
  if is_pantanal and mode=='sp':
   occupied={(r['day'],r['product'],r['area'])for r in daily};assert not any((r['day'],r['product'],r['area'])in occupied for r in base['daily'])
   daily+=base['daily'];shards.update({m:dict(ref,dataset_sha256=base['snapshot']['sha256'])for m,ref in base['observation_shards'].items()});observation_count+=base['observation_count'];manifest_count+=base['manifest_count']
  products=sorted({r['product']for r in daily});coverage={'start':min(r['day']for r in daily),'end':max(r['day']for r in daily)}
  product_coverage={p:{'start':min(r['day']for r in daily if r['product']==p),'end':max(r['day']for r in daily if r['product']==p),'retrieved_days':sum(1 for r in daily if r['product']==p and r['area']=='all')}for p in products}
  audit_ref=None;comparison_ref=None;selected_ref=validation_ref;validation=None
  if mode=='sp':
   validation=evaluate(daily,region['id']);audit_ref=publish(region['id']+'-regional-validation',validation);comparison_ref=publish(region['id']+'-regional-comparison',comparison_document(validation))
   if not is_pantanal:selected_ref=audit_ref
  elif regional_validation:
   selected_ref=regional_validation['validation'];audit_ref=regional_validation.get('external_audit');comparison_ref=regional_validation.get('comparison')
  accepted=mode=='sp'and(is_pantanal or bool(validation and validation['accepted']))
  calibration={'evaluated':accepted,'accepted':accepted,'geography':region['name']+' full study area only','period':{'start':'2020-01-01','end':'2024-12-31'}if is_pantanal and mode=='sp'else validation['publication_domain']if validation and validation['accepted']else None,'selected_method':'frozen seasonal'if is_pantanal else validation['selected_method']if validation else None,'reason':validation['reason']if validation else'SP calibration is not applied to NRT'}
  summary={'schema':'ember-regional-dashboard-2','region':region['id'],'name':region['name'],'bounds':bbox,'processing_class':mode.upper(),'metric_method':'ember-1','grid_degrees':.05,'snapshot':inventory,'validation':selected_ref,'external_audit':audit_ref,'comparison':comparison_ref,'built_utc':latest,'daily':sorted(daily,key=lambda r:(r['day'],r['product'],r['area'])),'observation_shards':dict(sorted(shards.items())),'observation_count':observation_count,'manifest_count':manifest_count,'coverage':coverage,'product_coverage':product_coverage,'products':products,'observation_coverage':'unknown; no usable swath/cloud masks','calibration':calibration}
  if is_pantanal:summary['comparison']=None
  ref=publish(region['id']+'-'+mode+'-dashboard',summary)
  compact=dict(ref,coverage=coverage,products=products,observations=observation_count,last_retrieval_utc=latest,calibration=calibration,validation=selected_ref,external_audit=audit_ref,comparison=summary['comparison'])
  if validation:compact['evaluation_summary']={'selected_method':validation['selected_method'],'accepted':validation['accepted'],'outer':validation['partitions']['outer'],'external':validation['partitions']['external'],'gates':validation['gates']}
  return compact

def main():
 unpack()
 definitions=json.loads(Path('data/region-definitions-v1.json').read_text());p=json.loads((ROOT/'dashboard.json').read_text());base=json.loads((ROOT/p['file']).read_text());regions=[]
 previous_registry=json.loads((ROOT/json.loads((ROOT/'regions.json').read_text())['file']).read_text())if (ROOT/'regions.json').exists()else{'regions':[]}
 previous={r['id']:r for r in previous_registry['regions']}
 for region in definitions['regions']:
  r=dict(region,geometry_type='bounding box',source=definitions['geometry_source'],source_url=definitions['source_url'])
  w,s,e,n=r['bounds'];r['geometry']={'type':'Polygon','coordinates':[[[w,s],[e,s],[e,n],[w,n],[w,s]]]}
  r['datasets']={}
  for mode in ['sp','nrt']:
   old_ref=previous.get(region['id'],{}).get('datasets',{}).get(mode);old=json.loads((ROOT/old_ref['file']).read_text())if old_ref else None
   ref=build(region,mode,base,p['validation'],old,r['datasets'].get('sp'))
   if ref:r['datasets'][mode]=ref
  r['available_products']=sorted({product for d in r['datasets'].values()for product in d['products']});regions.append(r)
  print(r['id'],{k:v['observations']for k,v in r['datasets'].items()},flush=True)
 registry={'schema':'ember-regions-1','crs':definitions['crs'],'definition_sha256':hashlib.sha256(Path('data/region-definitions-v1.json').read_bytes()).hexdigest(),'regions':regions}
 ref=publish('regions',registry);atomic_write(ROOT/'regions.json',encode(ref));print(json.dumps(ref))
if __name__=='__main__':main()
