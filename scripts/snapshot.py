"""Publish checksum-verified observations and manifest inventory without credentials."""
import csv,hashlib,json,sys,gzip
from pathlib import Path
from datetime import datetime,timezone
sys.path.insert(0,str(Path(__file__).parent))
from build_calendar import aggregate
from firms import read_csv
root=Path(sys.argv[1]);out=Path('web/data');out.mkdir(parents=True,exist_ok=True)
aggregate(root)
observations=[];manifests=[];seen=set()
for p in sorted(root.rglob('*.json')):
 m=json.loads(p.read_text());ref=str(p);manifests.append(dict(m,reference=ref))
 for r in read_csv(p.with_suffix('.csv').read_bytes()):
  identity=(m['source'],r['satellite'],r['acq_date'],r['acq_time'],r['latitude'],r['longitude'])
  if identity in seen:continue
  seen.add(identity)
  observations.append({'latitude':float(r['latitude']),'longitude':float(r['longitude']),'date_utc':r['acq_date'],'time_utc':r['acq_time'].zfill(4),'product':m['source'],'platform':r['satellite'],'confidence':r.get('confidence',''),'frp_mw':r.get('frp',''),'daynight':r.get('daynight',''),'source':ref})
payload=json.dumps({'version':'ember-1','built_utc':datetime.now(timezone.utc).isoformat(),'observations':observations,'manifests':manifests},separators=(',',':')).encode();h=hashlib.sha256(payload).hexdigest();name='snapshot-'+h[:12]+'.json.gz';(out/name).write_bytes(gzip.compress(payload,mtime=0));(out/'latest.json').write_text(json.dumps({'file':name,'sha256':h}))
print(name,len(observations))
