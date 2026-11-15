import sys
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from regional_calibration import daily_rows, regions, fetch_with_quota_retry


class LocalCalibrationTests(unittest.TestCase):
    @patch('regional_calibration.time.sleep')
    @patch('regional_calibration.fetch')
    def test_quota_retries_but_other_failures_do_not(self, fetch_mock, sleep_mock):
        fetch_mock.side_effect = [ValueError('FIRMS transaction quota exceeded'), None]
        fetch_with_quota_retry('secret', 'MODIS_SP', 'bbox', None, None, None)
        self.assertEqual(fetch_mock.call_count, 2)
        self.assertEqual(sleep_mock.call_count, 11)
        fetch_mock.reset_mock()
        fetch_mock.side_effect = ValueError('FIRMS returned HTTP 403')
        with self.assertRaises(ValueError):
            fetch_with_quota_retry('secret', 'MODIS_SP', 'bbox', None, None, None)
        self.assertEqual(fetch_mock.call_count, 1)

    def test_missing_days_stay_missing_and_cell_occupancy_is_deduplicated(self):
        detection = {'date_utc': '2024-07-01', 'product': 'MODIS_SP',
                     'latitude': -29.2, 'longitude': -67.5}
        observations = {'2024-07': [detection, dict(detection)]}
        rows = daily_rows(observations,
                          {'MODIS_SP': {'2024-07-01', '2024-07-02'}}, '-68,-30,-67,-29')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['raw_detections'], 2)
        self.assertEqual(rows[0]['occupied_cells_0_05deg'], 1)
        self.assertEqual(rows[1]['raw_detections'], 0)
        self.assertNotIn('2024-07-03', [r['date_utc'] for r in rows])

    def test_chilecito_extends_existing_eight(self):
        self.assertEqual(len(regions()), 9)
        self.assertEqual(regions()['chilecito']['bounds'], [-68, -30, -67, -29])


if __name__ == '__main__':
    unittest.main()
