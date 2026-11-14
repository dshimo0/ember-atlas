"""Compatibility entry point for the current signed-out judging workflow."""
from pathlib import Path
import os
import runpy

if __name__ == '__main__':
    runpy.run_path(str(Path(__file__).with_name('check_judging_flow.py')), run_name='__main__')
    suffix = 'public' if os.environ.get('BASE_URL', '').startswith('https://') else 'local'
    artifacts = Path(__file__).resolve().parents[1] / 'submission'
    (artifacts / 'browser-check.json').write_bytes((artifacts / f'judging-check-{suffix}.json').read_bytes())
