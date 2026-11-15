"""Reuse pilot windows only where they do not overlap the canonical backfill."""
import json,shutil
from pathlib import Path
for p in Path('data/raw').rglob('*.json'):
 m=json.loads(p.read_text());dest=Path('data/matched')/m['bbox']/m['source'];existing=[json.loads(q.read_text()) for q in dest.glob('*.json')]
 if any(x['start']<=m['end'] and x['end']>=m['start'] for x in existing):continue
 dest.mkdir(parents=True,exist_ok=True)
 for ext in ['.json','.csv']:shutil.copy2(p.with_suffix(ext),dest/p.with_suffix(ext).name)
