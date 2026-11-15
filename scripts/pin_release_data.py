"""Pin only new observation shards to an immutable public Git commit; keep old URLs local."""
import argparse,json,re,subprocess
from pathlib import Path
from build_dashboard import publish,encode
from firms import atomic_write
ROOT=Path('web/data')
BASELINE='3e28f40526fbed518383e9af0e9a071da9113035'
def pin(commit):
 if not re.fullmatch('[0-9a-f]{40}',commit):raise ValueError('Full data commit required')
 files=set(subprocess.check_output(['git','ls-tree','-r','--name-only',commit,'web/data'],text=True).splitlines())
 old=set(subprocess.check_output(['git','ls-tree','-r','--name-only',BASELINE,'web/data'],text=True).splitlines())
 pointer=json.loads((ROOT/'regions.json').read_text());registry=json.loads((ROOT/pointer['file']).read_text());external=set()
 for region in registry['regions']:
  for mode,ref in list(region['datasets'].items()):
   summary=json.loads((ROOT/ref['file']).read_text())
   for shard in summary['observation_shards'].values():
    path='web/data/'+shard['file']
    if path not in old:
     if path not in files:raise ValueError('Shard missing from data commit: '+path)
     original=subprocess.check_output(['git','show',commit+':'+path])
     if original!=(ROOT/shard['file']).read_bytes():raise ValueError('Data commit content differs')
     shard['url']='https://raw.githubusercontent.com/dshimo0/ember-atlas/'+commit+'/'+path;external.add(path)
   updated=publish(region['id']+'-'+mode+'-dashboard',summary)
   region['datasets'][mode]=dict(ref,**updated)
 ref=publish('regions',registry);atomic_write(ROOT/'regions.json',encode(ref))
 ignore=Path('.vercelignore');text=ignore.read_text().split('# Pinned expansion shards')[0].rstrip()+'\n# Pinned expansion shards (old public URLs remain local).\n'
 # Exclude every new gzip, including superseded build shards, to enforce the actual upload limit.
 external.update(str(p)for p in ROOT.glob('*.gz')if str(p)not in old)
 text+='\n'.join('/'+p for p in sorted(external))+'\n';ignore.write_text(text)
 atomic_write(Path('data/pinned-data-release.json'),encode({'schema':'ember-pinned-data-1','data_commit':commit,'registry':ref,'origin':'https://raw.githubusercontent.com','integrity':'Uncompressed SHA-256 checked before use; no API key','preserved_local_baseline':BASELINE}))
 print(json.dumps({'registry':ref,'external_shards':len(external),'data_commit':commit}))
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('commit');pin(parser.parse_args().commit)
