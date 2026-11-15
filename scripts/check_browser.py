"""Compatibility entry point for the current eight-region release acceptance suite."""
import runpy
from pathlib import Path
if __name__=='__main__':
    runpy.run_path(str(Path(__file__).with_name('check_eight_regions.py')),run_name='__main__')
