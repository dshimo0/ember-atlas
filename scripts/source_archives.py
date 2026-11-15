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
    path=(ROOT/member.name).resolve();assert path.is_relative_to(ROOT/'data/history')or path.is_relative_to(ROOT/'data/regions')or path.is_relative_to(ROOT/'data/covering')
    content=archive.extractfile(member).read();assert hashlib.sha256(content).hexdigest()==ref['members'][member.name]
    if path.exists():assert path.read_bytes()==content,'Existing source changed; refusing overwrite: '+str(path)
    else:atomic_write(path,content)
def pack():
 refs=json.loads(INDEX.read_text())['archives']if INDEX.exists()else[]
 known={name:sha for ref in refs for name,sha in ref['members'].items()};groups=defaultdict(list)
 for family in ['history','regions','covering']:
  for path in sorted((ROOT/'data'/family).rglob('*')):
   if not path.is_file()or path.suffix not in ['.json','.csv']:continue
   name=str(path.relative_to(ROOT));content=path.read_bytes()
   if name in known:
    assert hashlib.sha256(content).hexdigest()==known[name],'Existing input changed: '+name
    continue
   if not path.with_suffix('.json').exists()or not path.with_suffix('.csv').exists():continue
   year=json.loads(path.with_suffix('.json').read_text()).get('start',path.stem)[:4]
   key='pantanal-history-'+year if family=='history'else 'covering-'+path.relative_to(ROOT/'data/covering').parts[0]+'-'+year if family=='covering'else'-'.join(path.relative_to(ROOT/'data/regions').parts[:2])+'-'+year
   groups[key].append(path)
 for key,paths in sorted(groups.items()):
  output=io.BytesIO();members={}
  with tarfile.open(fileobj=output,mode='w',format=tarfile.PAX_FORMAT)as archive:
   for path in paths:
    name=str(path.relative_to(ROOT));content=path.read_bytes();members[name]=hashlib.sha256(content).hexdigest()
    info=tarfile.TarInfo(name);info.size=len(content);info.mtime=0;info.mode=0o644;archive.addfile(info,io.BytesIO(content))
  payload=gzip.compress(output.getvalue(),mtime=0);digest=hashlib.sha256(payload).hexdigest();name='data/source-archives/'+key+'-'+digest[:12]+'.tar.gz';atomic_write(ROOT/name,payload)
  refs.append({'path':name,'sha256':digest,'members':members})
 record={'schema':'ember-source-archives-2','license':'NASA FIRMS observations; see submission/RESOURCES.md','extraction':'python scripts/source_archives.py unpack; exact original paths and bytes; no overwrite of changed work','archives':refs}
 payload=json.dumps(record,indent=2,sort_keys=True).encode();digest=hashlib.sha256(payload).hexdigest();atomic_write(INDEX,payload);atomic_write(INDEX.with_name('index-'+digest[:12]+'.json'),payload)
 print('Verified',sum(len(r['members'])for r in refs),'source files in',len(refs),'immutable archives.')
if __name__=='__main__':
 import sys
 if len(sys.argv)>1 and sys.argv[1]=='pack':pack()
 else:unpack()
