"""Resume matched SP histories and retain available NRT without overlapping cached windows."""
import argparse,concurrent.futures,hashlib,json,os,time
from datetime import date
from pathlib import Path
from firms import DAY,fetch,bounds,atomic_write
from source_archives import unpack

def coverage(roots,product,bbox):
 days=set()
 for root in roots:
  for path in (root/bbox/product).glob('*.json'):
   m=json.loads(path.read_text());assert hashlib.sha256(path.with_suffix('.csv').read_bytes()).hexdigest()==m['sha256']
   d=date.fromisoformat(m['start'])
   while d<=date.fromisoformat(m['end']):days.add(d);d+=DAY
 return days

def uncovered(start,end,covered):
 d=start
 while d<=end:
  if d in covered:d+=DAY;continue
  last=d
  while last+DAY<=end and last+DAY not in covered and (last-d).days<4:last+=DAY
  yield d,last;d=last+DAY

def main():
 p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);p.add_argument('--mode',choices=['sp','nrt','all'],default='all');a=p.parse_args();unpack()
 definitions=json.loads(Path('data/region-definitions-v1.json').read_text())['regions'];jobs=[]
 for r in definitions:
  bbox=bounds(','.join(map(str,r['bounds'])))
  for mode in (['sp','nrt']if a.mode=='all'else[a.mode]):
   root=Path('data/regions')/r['id']/mode
   for sensor in ['MODIS','VIIRS_NOAA20']:
    product=sensor+'_'+mode.upper();roots=[root]
    if r['id']=='pantanal'and mode=='sp':roots.append(Path('data/matched'))
    covered=coverage(roots,product,bbox)
    start=date(2020,1,1)if mode=='sp'else date(2026,9,1)if sensor=='MODIS'else date(2026,8,1)
    end=date(2026,7,31)if mode=='sp'else date(2026,11,14)
    jobs.extend((r['id'],product,bbox,s,e,root)for s,e in uncovered(start,end,covered))
 failures=[];completed=0
 def run(job):
  region,product,bbox,start,end,root=job
  for attempt in range(80):
   try:
    fetch(os.environ['FIRMS_MAP_KEY'],product,bbox,start,end,root);time.sleep(.35);return None
   except ValueError as e:
    if 'quota exceeded' in str(e)or'HTTP 400'in str(e):
     print('Source request temporarily unavailable; preserving files and backing off.',flush=True);time.sleep(30)
    else:return {'region':region,'product':product,'start':str(start),'end':str(end),'error':str(e).replace(os.environ['FIRMS_MAP_KEY'],'[redacted]')}
   except Exception as e:return {'region':region,'product':product,'start':str(start),'end':str(end),'error':type(e).__name__}
  return {'region':region,'product':product,'start':str(start),'end':str(end),'error':'Bounded retries exhausted'}
 print('Planned uncovered windows:',len(jobs),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers)as pool:
  for result in pool.map(run,jobs):
   completed+=1
   if result:failures.append(result)
   if completed%50==0:
    record={'planned':len(jobs),'completed':completed,'failed':failures,'mode':a.mode};atomic_write(Path('data/expansion-progress.json'),json.dumps(record,indent=2).encode());print('Completed',completed,'of',len(jobs),'failures',len(failures),flush=True)
 record={'planned':len(jobs),'completed':completed,'failed':failures,'mode':a.mode};atomic_write(Path('data/expansion-acquisition.json'),json.dumps(record,indent=2).encode());print(json.dumps(record))
if __name__=='__main__':main()
