"""Pin expanded observations to immutable Git bytes and retain every published local data URL."""
import argparse,json,re,subprocess
from pathlib import Path
from build_dashboard import publish,encode
from firms import atomic_write
ROOT=Path('web/data')
BASELINE='a792e07c78066fcd4a6308fa3f3dd7acca7f93c7'
CATALOG=Path('data/published-static-data.json')
def local_dependencies(ref,seen=None):
 seen=set()if seen is None else seen
 def walk(value):
  if isinstance(value,dict):
   name=value.get('file')
   if name and not value.get('url'):
    assert isinstance(name,str)and Path(name).name==name
    path=ROOT/name;key=str(path)
    if key not in seen:
     seen.add(key)
     if name.endswith('.json'):walk(json.loads(path.read_text()))
   for child in value.values():walk(child)
  elif isinstance(value,list):
   for child in value:walk(child)
 walk(ref);return seen

def pin(commit):
 if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full data commit required')
 files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'web/data'],text=True).splitlines())
 old=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,'web/data'],text=True).splitlines())
 protected=old|set(json.loads(CATALOG.read_text())['paths']if CATALOG.exists()else[])
 pointer=json.loads((ROOT/'regions.json').read_text());registry=json.loads((ROOT/pointer['file']).read_text());remote=set()
 for region in registry['regions']:
  for mode,ref in list(region['datasets'].items()):
   summary=json.loads((ROOT/ref['file']).read_text())
   for month,shard in summary['observation_shards'].items():
    path='web/data/'+shard['file']
    if path not in old:
     if path not in files:raise ValueError('Shard missing from data commit: '+path)
     if subprocess.check_output(['git','show',commit+':'+path])!=(ROOT/shard['file']).read_bytes():raise ValueError('Data commit content differs')
     if path in protected or(region['id']=='pantanal'and mode=='sp'and month=='2024-09'):shard.pop('url',None)
     else:shard['url']='https://raw.githubusercontent.com/dshimo0/ember-atlas/'+commit+'/'+path;remote.add(path)
   updated=publish(region['id']+'-'+mode+'-dashboard',summary);region['datasets'][mode]=dict(ref,**updated)
 ref=publish('regions',registry);atomic_write(ROOT/'regions.json',encode(ref))
 served=protected|local_dependencies(ref)|{'web/data/regions.json'}
 # Superseded unpublished metadata stays in Git, outside the constrained Vercel upload.
 excluded=sorted(str(p)for p in ROOT.iterdir()if p.is_file()and str(p)not in served)
 ignore=Path('.vercelignore');header=ignore.read_text().split('# Pinned expansion data')[0].split('# Pinned expansion shards')[0].rstrip()
 ignore.write_text(header+'\n# Pinned expansion data; original public paths remain local.\n'+'\n'.join('/'+p for p in excluded)+'\n')
 atomic_write(CATALOG,encode({'schema':'ember-published-static-data-1','preserved_baseline':BASELINE,'paths':sorted(served)}))
 atomic_write(Path('data/pinned-data-release.json'),encode({'schema':'ember-pinned-data-1','data_commit':commit,'registry':ref,'origin':'https://raw.githubusercontent.com','integrity':'Uncompressed SHA-256 checked before use; no API key','preserved_local_baseline':BASELINE,'remote_observation_shards':len(remote),'preserved_local_paths':len(served)}))
 print(json.dumps({'registry':ref,'remote_shards':len(remote),'excluded_unpublished_files':len(excluded),'data_commit':commit}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('commit');pin(parser.parse_args().commit)
