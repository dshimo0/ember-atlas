import json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from pin_release_data import pin,BASELINE
class PinDataTests(unittest.TestCase):
 def test_only_new_committed_bytes_move_to_the_pinned_origin(self):
  original=Path.cwd()
  with tempfile.TemporaryDirectory()as tmp:
   try:
    os.chdir(tmp);root=Path('web/data');root.mkdir(parents=True);Path('.vercelignore').write_text('/data/**\n');(root/'old.gz').write_bytes(b'old');(root/'new.gz').write_bytes(b'new')
    (root/'summary.json').write_text(json.dumps({'observation_shards':{'2024-09':{'file':'old.gz'},'2025-01':{'file':'new.gz'}}}));(root/'registry.json').write_text(json.dumps({'regions':[{'id':'california','datasets':{'sp':{'file':'summary.json'}}}]}));(root/'regions.json').write_text(json.dumps({'file':'registry.json'}))
    def git(args,**kwargs):
     if args[1]=='ls-tree':return 'web/data/old.gz\n'if args[4]==BASELINE else'web/data/old.gz\nweb/data/new.gz\n'
     return b'new'
    with patch('pin_release_data.subprocess.check_output',side_effect=git):pin('a'*40)
    ref=json.loads((root/'regions.json').read_text());r=json.loads((root/ref['file']).read_text());s=json.loads((root/r['regions'][0]['datasets']['sp']['file']).read_text());shards=s['observation_shards']
    self.assertNotIn('url',shards['2024-09']);self.assertIn('/'+'a'*40+'/',shards['2025-01']['url']);self.assertIn('/web/data/new.gz',Path('.vercelignore').read_text());self.assertNotIn('/web/data/old.gz',Path('.vercelignore').read_text())
   finally:os.chdir(original)
 def test_mutable_or_abbreviated_commit_is_rejected(self):
  for commit in ['work','123abcd','a'*39]:
   with self.assertRaises(ValueError):pin(commit)
if __name__=='__main__':unittest.main()
