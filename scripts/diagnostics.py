"""Grid, confidence and platform sensitivity from the pinned snapshot."""
import gzip,json,math
from collections import defaultdict
from decimal import Decimal,ROUND_FLOOR
def cell(value,size):return int((Decimal(str(value))/Decimal(str(size))).to_integral_value(rounding=ROUND_FLOOR))
from pathlib import Path
idx=json.loads(Path('web/data/latest.json').read_text());db=json.loads(gzip.decompress((Path('web/data')/idx['file']).read_bytes()));sets=defaultdict(set);counts=defaultdict(int)
for r in db['observations']:
 key=(r['date_utc'][:7],r['product'])
 counts[(key[0],key[1],r['platform'],r['daynight'])]+=1
 for size in [.025,.05,.1]:sets[(key[0],key[1],str(size),'all')].add((r['date_utc'],cell(r['latitude'],size),cell(r['longitude'],size)))
 c=r['confidence'];high=(float(c)>=80) if r['product']=='MODIS_SP' and c.replace('.','',1).isdigit() else c=='h'
 if high:sets[(key[0],key[1],'.05','high')].add((r['date_utc'],cell(r['latitude'],.05),cell(r['longitude'],.05)))
r={'note':'Descriptive sensitivity only; high-confidence thresholds are sensor-specific (MODIS >=80, VIIRS h). Decimal grid binning matches the primary pipeline. No mask-based observation coverage.','grid_confidence':[{'month':k[0],'product':k[1],'grid':k[2],'confidence':k[3],'cell_days':len(v)} for k,v in sorted(sets.items())],'platform_daynight':[{'month':k[0],'product':k[1],'platform':k[2],'daynight':k[3],'native':v} for k,v in sorted(counts.items())]}
Path('web/data/diagnostics.json').write_text(json.dumps(r,indent=2))
