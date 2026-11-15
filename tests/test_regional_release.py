import copy,hashlib,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from build_regions import read_inputs
from evaluate_replay import evaluate
import source_archives
from unittest.mock import patch

class RegionalReleaseTests(unittest.TestCase):
 def fixture(self,root,processing='SP',bbox='-125,32,-114,42.5'):
  payload=b'latitude,longitude,acq_date,acq_time,satellite\n38,-120,2024-09-01,0030,Terra\n38,-120,2024-09-01,0030,Terra\n'
  p=root/'window.csv';p.write_bytes(payload)
  meta={'source':'MODIS_'+processing,'processing_class':processing,'bbox':bbox,'start':'2024-09-01','end':'2024-09-02','rows':2,'sha256':hashlib.sha256(payload).hexdigest(),'retrieved_at':'2026-11-15T00:00:00Z'}
  p.with_suffix('.json').write_text(json.dumps(meta));return p
 def test_real_empty_day_is_covered_and_records_are_deduplicated(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);self.fixture(root);obs,manifests,covered=read_inputs(root,[-125,32,-114,42.5],'SP')
   self.assertEqual(len(obs['2024-09']),1);self.assertEqual(covered['MODIS_SP'],{'2024-09-01','2024-09-02'});self.assertNotIn('2024-09-03',covered['MODIS_SP']);self.assertEqual(obs['2024-09'][0]['time_utc'],'0030')
 def test_hash_and_geography_must_match(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);p=self.fixture(root)
   with self.assertRaises(AssertionError):read_inputs(root,[-59,-23,-54,-15],'SP')
   p.write_bytes(p.read_bytes()+b'\n')
   with self.assertRaises(AssertionError):read_inputs(root,[-125,32,-114,42.5],'SP')
 def test_nrt_cannot_silently_enter_sp(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);self.fixture(root,processing='NRT')
   with self.assertRaises(AssertionError):read_inputs(root,[-125,32,-114,42.5],'SP')
 def test_scalar_and_peak_selection_are_independent_of_holdout_residuals(self):
  v=json.loads(Path('web/data/validation.json').read_text());r=evaluate(v)
  self.assertAlmostEqual(r['metrics']['scalar']['mae'],175.32928712011548)
  changed=copy.deepcopy(v)
  for m in changed['monthly']:
   if m['year']in v['holdout_years']:m['viirs']*=100
  e=evaluate(changed);self.assertEqual(e['scalar']['factor'],r['scalar']['factor']);self.assertEqual(e['peak_months'],r['peak_months'])
class SourceArchiveTests(unittest.TestCase):
 def test_roundtrip_preserves_bytes_and_is_deterministic(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);path=root/'data/history/bbox/MODIS_SP/2000-11-01_2000-11-05.csv';path.parent.mkdir(parents=True);original=b'latitude,longitude\r\n-19,-55\r\n';path.write_bytes(original);path.with_suffix('.json').write_text('{}')
   with patch.object(source_archives,'ROOT',root),patch.object(source_archives,'INDEX',root/'data/source-archives/index.json'):
    source_archives.pack();first=next((root/'data/source-archives').glob('*.tar.gz')).read_bytes();source_archives.pack();self.assertEqual(first,next((root/'data/source-archives').glob('*.tar.gz')).read_bytes());path.unlink();source_archives.unpack();self.assertEqual(path.read_bytes(),original)
 def test_unpack_refuses_to_overwrite_changed_existing_work(self):
  with tempfile.TemporaryDirectory()as t:
   root=Path(t);path=root/'data/history/bbox/MODIS_SP/2000-11-01_2000-11-05.csv';path.parent.mkdir(parents=True);path.write_bytes(b'original');path.with_suffix('.json').write_text('{}')
   with patch.object(source_archives,'ROOT',root),patch.object(source_archives,'INDEX',root/'data/source-archives/index.json'):
    source_archives.pack();path.write_bytes(b'existing changed work')
    with self.assertRaises(AssertionError):source_archives.unpack()
if __name__=='__main__':unittest.main()
