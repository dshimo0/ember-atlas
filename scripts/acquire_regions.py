"""Acquire bounded SP/NRT snapshots and earlier Pantanal MODIS using the existing downloader."""
import argparse,concurrent.futures,json,os,time
from datetime import date
from pathlib import Path
from firms import fetch,windows,bounds,atomic_write
from source_archives import unpack

def main():
 p=argparse.ArgumentParser()
 p.add_argument('--history',action='store_true')
 p.add_argument('--region',action='append',help='Restrict archive acquisition to a region ID. Repeat for multiple regions.')
 p.add_argument('--archive-start',type=date.fromisoformat)
 p.add_argument('--archive-end',type=date.fromisoformat)
 p.add_argument('--workers',type=int,default=4)
 p.add_argument('--respect-quota',action='store_true')
 a=p.parse_args()
 key=os.environ.get('FIRMS_MAP_KEY','')
 if not key:p.error('Set FIRMS_MAP_KEY in the environment before downloading.')
 defs=json.loads(Path('data/region-definitions-v1.json').read_text())['regions']
 known={r['id'] for r in defs}
 if a.region and not set(a.region)<=known:p.error('Unknown region ID; see data/region-definitions-v1.json.')
 custom_archive=a.archive_start is not None or a.archive_end is not None
 if custom_archive and (not a.archive_start or not a.archive_end or a.archive_start>a.archive_end):
  p.error('Supply both archive dates in ascending order.')
 if a.history and (a.region or custom_archive):p.error('--history uses the existing Pantanal-only archive window.')
 if a.region and not custom_archive:p.error('--region requires an explicit archive date range.')
 unpack()
 jobs=[]
 if a.history:
  jobs=[('pantanal','MODIS_SP',r,s,e,Path('data/history'))for r in [bounds('-59,-23,-54,-15')] for s,e in windows(date(2000,11,1),date(2019,12,31))]
 else:
  for r in defs:
   if a.region and r['id'] not in a.region:continue
   if custom_archive and r['id']=='pantanal':continue
   bbox=bounds(','.join(map(str,r['bounds'])))
   archive_start=a.archive_start or date(2024,9,1)
   archive_end=a.archive_end or date(2024,9,30)
   for product in ['MODIS_SP','VIIRS_NOAA20_SP']:
    if r['id']!='pantanal':
     jobs.extend((r['id'],product,bbox,s,e,Path('data/regions')/r['id']/'sp')for s,e in windows(archive_start,archive_end))
   if not custom_archive:
    for product in ['MODIS_NRT','VIIRS_NOAA20_NRT']:
     jobs.extend((r['id'],product,bbox,s,e,Path('data/regions')/r['id']/'nrt')for s,e in windows(date(2026,11,8),date(2026,11,14)))
 if not jobs:p.error('Custom archive acquisition is for the seven additional regions.')
 failures=[]
 def run(job):
  region,product,bbox,start,end,out=job
  try:
   for attempt in range(65):
    try:
     cached=(out/bbox/product/(str(start)+'_'+str(end)+'.json')).exists()
     fetch(key,product,bbox,start,end,out)
     if a.respect_quota and not cached:time.sleep(1.5)
     return None
    except ValueError as error:
     if a.respect_quota and ('quota exceeded' in str(error) or 'HTTP 400' in str(error)):
      print('FIRMS quota pause; source files remain unchanged.',flush=True);time.sleep(30)
     else:raise
   raise ValueError('FIRMS quota remained unavailable after bounded retries')
  except Exception as error:return {'region':region,'product':product,'start':str(start),'end':str(end),'error':str(error).replace(key,'[redacted]')}
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:
  for i,result in enumerate(pool.map(run,jobs),1):
   if result:failures.append(result)
   if i%100==0:print(f'Progress: {i}/{len(jobs)}; failed {len(failures)}',flush=True)
 record={'planned_windows':len(jobs),'failed':failures,'history':a.history}
 report='acquisition-history.json' if a.history else 'acquisition-regions.json'
 if custom_archive:report='acquisition-regional-archive.json'
 atomic_write(Path('data')/report,json.dumps(record,indent=2).encode());print(json.dumps(record))
if __name__=='__main__':main()
