import subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class BackfillGate(unittest.TestCase):
    def test_unverified_generators_cannot_publish_or_require_optional_packages(self):
        for script in ['harmonize.py','build_site.py']:
            with self.subTest(script=script),tempfile.TemporaryDirectory() as folder:
                result=subprocess.run([sys.executable,str(ROOT/'backfill'/script)],cwd=folder,text=True,capture_output=True)
                self.assertNotEqual(result.returncode,0)
                self.assertIn('blocked',result.stderr.lower())
                self.assertEqual(list(Path(folder).iterdir()),[])
