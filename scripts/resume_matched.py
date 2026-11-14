"""Resume only uncovered UTC days in the fixed 2020–2024 evaluation domain."""
import json,os,time
from pathlib import Path
from datetime import date
from firms import DAY,fetch,windows
root=Path('data/matched');bbox='-59.0,-23.0,-54.0,-15.0'
for source in ['MODIS_SP','VIIRS_NOAA20_SP']:
 covered=set()
 for p in (root/bbox/source).glob('*.json'):
  m=json.loads(p.read_text());d=date.fromisoformat(m['start'])
  while d<=date.fromisoformat(m['end']):covered.add(d);d+=DAY
 d=date(2020,1,1)
 while d<=date(2024,12,31):
  if d in covered:d+=DAY;continue
  end=d
  while end+DAY<=date(2024,12,31) and end+DAY not in covered and (end-d).days<4:end+=DAY
  fetch(os.environ['FIRMS_MAP_KEY'],source,bbox,d,end,root)
  d=end+DAY;time.sleep(.5)
