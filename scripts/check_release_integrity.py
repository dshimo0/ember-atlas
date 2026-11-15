"""Check frozen release inputs and credentials without exposing secret values."""
import gzip,hashlib,json,os,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
paths=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT,text=True).splitlines()
key=os.environ.get('FIRMS_MAP_KEY','').encode()
pattern=re.compile(rb'firms\.modaps\.eosdis\.nasa\.gov/api/(?:area/csv|data_availability/csv)/[a-zA-Z0-9]{20,}/')
failures=[];scanned=0
for name in paths:
 p=ROOT/name
 if not p.is_file():continue
 data=p.read_bytes();scanned+=1
 if (key and key in data)or pattern.search(data):failures.append(name)
 if name.startswith('web/') and name.endswith('.gz'):
  decoded=gzip.decompress(data)
  if (key and key in decoded)or pattern.search(decoded):failures.append(name+' (decompressed)')
assert not failures,'Credential pattern detected in: '+', '.join(failures)
frozen=['web/data/latest.json','web/data/validation.json','web/data/validation-ba55acfc7909.json','web/data/dashboard.json','data/calendar.csv','scripts/harmonize.py']
unchanged={}
for name in frozen:
 current=(ROOT/name).read_bytes();original=subprocess.check_output(['git','show','6fb056e:'+name],cwd=ROOT)
 assert current==original,name+' changed'
 unchanged[name]=hashlib.sha256(current).hexdigest()
report={'files_scanned':scanned,'credential_patterns_found':False,'known_environment_key_checked':bool(key),'decompressed_public_gzip_checked':True,'frozen_file_sha256':unchanged}
(ROOT/'submission/integrity-check.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
