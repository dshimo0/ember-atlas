"""Stream verified source windows into bounded-memory monthly spools and daily counts."""
import hashlib,json
from collections import defaultdict
from datetime import date
from pathlib import Path
from firms import DAY,read_csv
from build_calendar import grid_cell
from source_masks import subset

def stream_inputs(directories,bbox,processing,spool,pantanal=False):
 manifests=[];covered=defaultdict(set);daily=[];total=0
 paths=sorted(path for directory in directories for path in directory.rglob('*.json'))
 for path in paths:
  m=json.loads(path.read_text());payload=path.with_suffix('.csv').read_bytes()
  assert hashlib.sha256(payload).hexdigest()==m['sha256'],path
  assert list(map(float,m['bbox'].split(',')))==bbox,path
  if m.get('derived_from'):
   parent=Path(m['derived_from']['reference']);upstream=json.loads(parent.read_text());original=parent.with_suffix('.csv').read_bytes();assert hashlib.sha256(original).hexdigest()==upstream['sha256']==m['derived_from']['sha256'];expected,n=subset(original,bbox,m['start'],m['end']);assert expected==payload and n==m['rows'];assert upstream['source']==m['source'];ub=list(map(float,upstream['bbox'].split(',')));assert ub[0]<=bbox[0]and ub[1]<=bbox[1]and ub[2]>=bbox[2]and ub[3]>=bbox[3];assert upstream['start']<=m['start']<=m['end']<=upstream['end'];assert upstream['processing_class']==processing
  assert m['processing_class']==processing and m['source'].endswith('_'+processing),path
  start,end=date.fromisoformat(m['start']),date.fromisoformat(m['end']);d=start;days=[]
  while d<=end:
   assert str(d)not in covered[m['source']],'Overlapping source windows'
   covered[m['source']].add(str(d));days.append(str(d));d+=DAY
  counts=defaultdict(int);cells=defaultdict(set);seen=set();month_rows=defaultdict(list);delivered=0
  for r in read_csv(payload):
   delivered+=1;assert str(start)<=r['acq_date']<=str(end)
   lat,lon=float(r['latitude']),float(r['longitude']);assert bbox[0]<=lon<=bbox[2]and bbox[1]<=lat<=bbox[3]
   t=r['acq_time'].zfill(4);assert len(t)==4 and t.isdecimal()and int(t[:2])<24 and int(t[2:])<60
   key=(r['satellite'],r['acq_date'],t,lat,lon)
   if key in seen:continue
   seen.add(key);total+=1
   if spool is not None:
    out={'latitude':lat,'longitude':lon,'date_utc':r['acq_date'],'time_utc':t,'product':m['source'],'platform':r['satellite'],'confidence':r.get('confidence',''),'frp_mw':r.get('frp',''),'daynight':r.get('daynight',''),'source':str(path),'source_version':r.get('version',''),'detection_type':r.get('type','')}
    month_rows[r['acq_date'][:7]].append(json.dumps(out,separators=(',',':')))
   for area in (['all','north'if lat>=-19 else'south']if pantanal else['all']):
    k=(r['acq_date'],area);counts[k]+=1;cells[k].add(grid_cell(str(lat),str(lon)))
  assert delivered==m['rows'],path
  for month,rows in month_rows.items():
   with (spool/(month+'.jsonl')).open('a')as f:f.write('\n'.join(rows)+'\n')
  for day in days:
   for area in (['all','north','south']if pantanal else['all']):daily.append({'day':day,'product':m['source'],'area':area,'native':counts[(day,area)],'cells':len(cells[(day,area)])})
  manifests.append(dict(m,reference=str(path)))
 return daily,manifests,covered,total
