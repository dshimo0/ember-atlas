"""Preserve byte-exact new FIRMS inputs in deterministic, reviewable source archives."""
import gzip,hashlib,io,json,tarfile
from collections import defaultdict
from pathlib import Path
from firms import atomic_write
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'data/source-archives/index.json'
def unpack():
 if not INDEX.exists():return
 for ref in json.loads(INDEX.read_text())['archives']:
  payload=(ROOT/ref['path']).read_bytes();assert hashlib.sha256(payload).hexdigest()==ref['sha256']
  with tarfile.open(fileobj=io.BytesIO(payload),mode='r:gz')as archive:
   for member in archive.getmembers():
    assert member.isfile() and member.name in ref['members']
    path=(ROOT/member.name).resolve();assert path.is_relative_to(ROOT/'data/history')or path.is_relative_to(ROOT/'data/regions')
    content=archive.extractfile(member).read();assert hashlib.sha256(content).hexdigest()==ref['members'][member.name]
    if path.exists():assert path.read_bytes()==content,'Existing source changed; refusing overwrite: '+str(path)
    else:atomic_write(path,content)
def pack():
 groups=defaultdict(list)
 for name in ['history','regions']:
  for path in sorted((ROOT/'data'/name).rglob('*')):
   if path.is_file()and path.suffix in ['.json','.csv']:
    key='pantanal-history-'+path.stem[:4]if name=='history'else'-'.join(path.relative_to(ROOT/'data/regions').parts[:2])
    groups[key].append(path)
 refs=[]
 for key,paths in sorted(groups.items()):
  output=io.BytesIO();members={}
  with tarfile.open(fileobj=output,mode='w',format=tarfile.PAX_FORMAT)as archive:
   for path in paths:
    name=str(path.relative_to(ROOT));content=path.read_bytes();members[name]=hashlib.sha256(content).hexdigest()
    info=tarfile.TarInfo(name);info.size=len(content);info.mtime=0;info.mode=0o644;archive.addfile(info,io.BytesIO(content))
  payload=gzip.compress(output.getvalue(),mtime=0);name='data/source-archives/'+key+'.tar.gz';atomic_write(ROOT/name,payload)
  refs.append({'path':name,'sha256':hashlib.sha256(payload).hexdigest(),'members':members})
 record={'schema':'ember-source-archives-1','license':'NASA FIRMS observations; see submission/RESOURCES.md','extraction':'python scripts/source_archives.py unpack; byte-exact files restored to recorded source-reference paths','archives':refs}
 atomic_write(INDEX,json.dumps(record,indent=2,sort_keys=True).encode());print('Packed',sum(len(r['members'])for r in refs),'source files in',len(refs),'verified archives.')
if __name__=='__main__':
 import sys
 if len(sys.argv)>1 and sys.argv[1]=='pack':pack()
 else:unpack()
