import sys,unittest,calendar
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from harmonize import analyze

def fixture():
 return [{'date_utc':f'{y}-{m:02}-{d:02}','bbox':'a','source':s,'raw_detections':str(n),'occupied_cells_0_05deg':str(n)} for y in range(2020,2025) for m in range(1,13) for d in range(1,calendar.monthrange(y,m)[1]+1) for s,n in [('MODIS_SP',2),('VIIRS_NOAA20_SP',4)]]
class HarmonizationTest(unittest.TestCase):
 def test_fixed_transfer_on_unseen_years(self):
  r=analyze(fixture(),[2020,2021,2022],[2023,2024]);self.assertTrue(r['accepted']);self.assertEqual(r['adjusted']['mae'],0);self.assertGreater(r['unadjusted']['mae'],60)
 def test_missing_day_excludes_month(self):
  r=analyze(fixture()[:-1],[2020,2021,2022],[2023,2024]);self.assertIn('2024-12',r['excluded_months']);self.assertFalse(r['accepted'])
 def test_zero_is_a_complete_month(self):
  rows=fixture()
  for r in rows:r['occupied_cells_0_05deg']='0'
  a=analyze(rows,[2020,2021,2022],[2023,2024]);self.assertEqual(a['paired_months'],60);self.assertFalse(a['accepted']);self.assertIsNone(a['factors'][0])
 def test_overlap_and_mixed_areas_rejected(self):
  with self.assertRaises(ValueError):analyze(fixture(),[2020],[2020])
  rows=fixture();rows[0]['bbox']='b'
  with self.assertRaises(ValueError):analyze(rows,[2020],[2024])
