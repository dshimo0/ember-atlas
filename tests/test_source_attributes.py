import hashlib,json,os,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source_attributes import hydrate,add_attributes,diagnostic
class SourceAttributesTests(unittest.TestCase):
 def test_literal_flags_restore_without_changing_frozen_records(self):
  cwd=Path.cwd()
  with tempfile.TemporaryDirectory()as tmp:
   try:
    os.chdir(tmp);p=Path('data/matched/sample.json');p.parent.mkdir(parents=True);payload=b'latitude,longitude,acq_date,acq_time,satellite,confidence,frp,daynight,version,type\n38,-120,2024-09-01,0030,Terra,90,12.5,D,6.03,0\n39,-120,2024-09-01,0030,Terra,90,2.0,D,61.03,2\n';p.with_suffix('.csv').write_bytes(payload);p.write_text(json.dumps({'source':'MODIS_SP','sha256':hashlib.sha256(payload).hexdigest()}))
    original=[{'latitude':38.0,'longitude':-120.0,'date_utc':'2024-09-01','time_utc':'0030','product':'MODIS_SP','platform':'Terra','confidence':'90','frp_mw':'12.5','daynight':'D','source':str(p)}];rows=hydrate(original)
    self.assertEqual({k:rows[0][k]for k in original[0]},original[0]);self.assertEqual(rows[0]['source_version'],'6.03');self.assertEqual(rows[0]['detection_type'],'0')
    attributes={};add_attributes(rows,attributes);self.assertEqual(attributes[('2024-09-01','MODIS_SP','all')]['detection_types'],{'0':1})
    p.with_suffix('.csv').write_bytes(payload+b'changed')
    with self.assertRaises(AssertionError):hydrate(original)
   finally:os.chdir(cwd)
 def test_reference_version_split_is_reported_without_changing_counts(self):
  rows=[{'day':'2022-01-01','product':'MODIS_SP','area':'all','native':1,'cells':1,'source_versions':{'6.03':1},'detection_types':{'0':1}},{'day':'2023-01-01','product':'MODIS_SP','area':'all','native':1,'cells':1,'source_versions':{'61.03':1},'detection_types':{'0':1}}];before=json.dumps(rows);r=diagnostic(rows,'pantanal',[-59,-23,-54,-15]);self.assertTrue(r['modis_reference_labels_differ_across_split']);self.assertFalse(r['version_mapping_independently_verified']);self.assertEqual(json.dumps(rows),before)
if __name__=='__main__':unittest.main()
