import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from firms import fetch, windows
from build_calendar import aggregate


class PipelineTest(unittest.TestCase):
    def test_windows_include_final_day_without_overlap(self):
        self.assertEqual(
            list(windows(date(2024, 8, 1), date(2024, 8, 6))),
            [(date(2024, 8, 1), date(2024, 8, 5)), (date(2024, 8, 6), date(2024, 8, 6))],
        )

    def test_ingestion_cache_and_daily_grid(self):
        payload = (
            b"latitude,longitude,acq_date,acq_time,satellite\n"
            b"-19.01,-57.01,2024-08-01,0030,Terra\n"
            b"-19.02,-57.02,2024-08-01,0130,Aqua\n"
        )
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            bbox = "-59,-23,-54,-15"
            start, end = date(2024, 8, 1), date(2024, 8, 2)
            with patch("firms.download", return_value=payload) as download:
                for _ in range(2):
                    fetch("fixture", "MODIS_SP", bbox, start, end, output)
            download.assert_called_once_with(f"area/csv/fixture/MODIS_SP/{bbox}/2/{start}")
            self.assertEqual(aggregate(output), {
                (start, bbox, "MODIS_SP"): (2, 1),
                (end, bbox, "MODIS_SP"): (0, 0),
            })
            next(output.rglob("*.csv")).write_bytes(payload + b"corruption")
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                aggregate(output)

    def test_error_body_never_becomes_a_cached_extract(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            day = date(2024, 8, 1)
            with patch("firms.download", return_value=b"Invalid MAP_KEY"), self.assertRaises(ValueError):
                fetch("fixture", "MODIS_SP", "-59,-23,-54,-15", day, day, output)
            self.assertEqual(list(output.iterdir()), [])
