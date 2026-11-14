import calendar
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from harmonize import evaluate,MODIS,VIIRS

def rows(years,zero=False):
    return [dict(date_utc=f'{y}-08-{d:02}',bbox='-59,-23,-54,-15',source=s,raw_detections=str(v),occupied_cells_0_05deg=str(v)) for y in years for d in range(1,32) for s,v in [(MODIS,0 if zero else 10),(VIIRS,0 if zero else 20)]]

class HarmonizationTest(unittest.TestCase):
    def test_frozen_transfer(self):
        r=evaluate(rows(range(2019,2024)),[2019,2020,2021],[2022,2023])
        self.assertTrue(r['accepted']);self.assertEqual(r['adjusted']['mae'],0);self.assertEqual(r['baseline']['mae'],310)
    def test_missing_is_excluded_zero_is_valid(self):
        r=evaluate(rows(range(2019,2024),True),[2019,2020,2021],[2022,2023])
        self.assertFalse(r['accepted']);self.assertEqual(r['holdout_months'],2)
        r=evaluate(rows(range(2019,2024))[:-1],[2019,2020,2021],[2022,2023])
        self.assertEqual(r['holdout_months'],1);self.assertFalse(r['accepted'])
    def test_overlap_and_mixed_areas_rejected(self):
        with self.assertRaises(ValueError):evaluate(rows([2020]),[2020],[2020])
        r=rows([2020]);r[0]['bbox']='other'
        with self.assertRaises(ValueError):evaluate(r,[2019],[2020])
