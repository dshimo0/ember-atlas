"""Reuse one bounded South America query for four unchanged analysis masks; respect FIRMS quotas."""
import argparse,concurrent.futures,hashlib,json,os,time
from datetime import date,datetime,timezone
from pathlib import Path
from acquire_expansion import coverage,uncovered
from firms import DAY,fetch,bounds,atomic_write
from source_masks import subset
from source_archives import unpack
SOUTH=['pantanal','southern-amazon','cerrado','gran-chaco']
COVER=[-66,-32,-44,-5]

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);a=p.parse_args();unpack();regions=json.loads(Path('data/region-definitions-v1.json').read_text())['regions'];jobs=[];covered={}
 for mode in ['sp','nrt']:
  for sensor in ['MODIS','VIIRS_NOAA20']:
   product=sensor+'_'+mode.upper();start=date(2020,1,1)if mode=='sp'else date(2026,9,1)if sensor=='MODIS'else date(2026,8,1);end=date(2026,7,31)if mode=='sp'else date(2026,11,14)
   for r in regions:
    box=bounds(','.join(map(str,r['bounds'])));root=Path('data/regions')/r['id']/mode;roots=[root]+([Path('data/matched')]if r['id']=='pantanal'and mode=='sp'else[])
    covered[(r['id'],product)]=coverage(roots,product,box)
   common=set.intersection(*(covered[(id,product)]for id in SOUTH));parent_root=Path('data/covering')/mode;parent_box=bounds(','.join(map(str,COVER)))
   for s,e in uncovered(start,end,common):jobs.append(('covering',product,parent_box,s,e,parent_root,mode))
   for r in regions:
    if r['id']in SOUTH:continue
    box=bounds(','.join(map(str,r['bounds'])));root=Path('data/regions')/r['id']/mode
    jobs.extend((r['id'],product,box,s,e,root,mode)for s,e in uncovered(start,end,covered[(r['id'],product)]))
 def run(job):
  id,product,box,start,end,root,mode=job
  for attempt in range(120):
   try:
    fetch(os.environ['FIRMS_MAP_KEY'],product,box,start,end,root);break
   except ValueError as error:
    if 'quota exceeded'in str(error)or'HTTP 400'in str(error):print('FIRMS quota backoff; original inputs preserved.',flush=True);time.sleep(30)
    else:return {'id':id,'product':product,'start':str(start),'error':str(error).replace(os.environ['FIRMS_MAP_KEY'],'[redacted]')}
  else:return {'id':id,'product':product,'start':str(start),'error':'Quota retry budget exhausted'}
  if id=='covering':
   parent=root/box/product/(str(start)+'_'+str(end)+'.json');meta=json.loads(parent.read_text());payload=parent.with_suffix('.csv').read_bytes()
   for r in regions:
    if r['id']not in SOUTH:continue
    region_box=bounds(','.join(map(str,r['bounds'])));target_root=Path('data/regions')/r['id']/mode/region_box/product
    for first,last in uncovered(start,end,covered[(r['id'],product)]):
     content,n=subset(payload,r['bounds'],str(first),str(last));target=target_root/('filtered_'+str(first)+'_'+str(last)+'.csv')
     derived={'source':product,'bbox':region_box,'start':str(first),'end':str(last),'retrieved_at':meta['retrieved_at'],'sha256':hashlib.sha256(content).hexdigest(),'rows':n,'pipeline_version':'ember-covering-mask-1','processing_class':mode.upper(),'derived_from':{'reference':str(parent),'sha256':meta['sha256'],'server_bbox':meta['bbox'],'source_delivered_rows':meta['rows']},'rule':'Inclusive WGS84 bbox/date filter; original field values retained; original covering CSV preserved.'}
     atomic_write(target,content);atomic_write(target.with_suffix('.json'),json.dumps(derived,indent=2).encode())
  time.sleep(.6);return None
 def safe_run(job):
  try:return run(job)
  except Exception as error:
   failure={'id':job[0],'product':job[1],'start':str(job[3]),'end':str(job[4]),'error':type(error).__name__+': '+str(error).replace(os.environ['FIRMS_MAP_KEY'],'[redacted]')};print('Window failed safely:',json.dumps(failure),flush=True);return failure
 print('Planned missing covering/direct windows:',len(jobs),flush=True);failures=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers)as pool:
  for i,result in enumerate(pool.map(safe_run,jobs),1):
   if result:failures.append(result)
   if i%25==0:
    status={'planned':len(jobs),'completed':i,'failed':failures,'shared_query_masks':SOUTH};atomic_write(Path('data/shared-acquisition-progress.json'),json.dumps(status,indent=2).encode());print('Completed',i,'of',len(jobs),'failed',len(failures),flush=True)
 atomic_write(Path('data/shared-acquisition.json'),json.dumps({'planned':len(jobs),'completed':len(jobs),'failed':failures},indent=2).encode())
if __name__=='__main__':main()
