"""Render the eight-row coverage inventory from the published registry, never from assumptions."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'web/data'
p=json.loads((DATA/'regions.json').read_text());r=json.loads((DATA/p['file']).read_text())
rows=['| Study area (W/S/E/N) | Observed SP coverage | Recent NRT UTC window | Adjustment |','| --- | --- | --- | --- |']
for region in r['regions']:
 s=json.loads((DATA/region['datasets']['sp']['file']).read_text());n=json.loads((DATA/region['datasets']['nrt']['file']).read_text());nrt_coverage='; '.join(f"{k}: {v['start']}–{v['end']} ({v['retrieved_days']} retrieved days)"for k,v in n['product_coverage'].items());coverage='; '.join(f"{k}: {v['start']}–{v['end']} ({v['retrieved_days']} retrieved days)"for k,v in s['product_coverage'].items())
 rows.append(f"| {region['name']} ({', '.join(map(str,region['bounds']))}) | {coverage} | {nrt_coverage} | {'Evaluated full area, SP 2020–2024 only'if region['id']=='pantanal'else ('Evaluated '+str(s['calibration']['selected_method'])+', full area SP through '+s['calibration']['period']['end'] if s['calibration'].get('accepted') else s['calibration'].get('reason','Unavailable; regional evaluation pending'))} |")
text='\n'.join(rows)
for name in ['README.md','docs/challenge-traceability.md']:
 p=ROOT/name;s=p.read_text();start=s.index('<!-- COVERAGE:START -->')+len('<!-- COVERAGE:START -->');end=s.index('<!-- COVERAGE:END -->');p.write_text(s[:start]+'\n'+text+'\n'+s[end:])
(ROOT/'submission/eight-region-coverage.md').write_text('# Released data coverage\n\n'+text+'\n\nAll geometries are project-defined study rectangles. Missing retrieval is not zero. SP and NRT remain separate. Product dates describe published retrieval, not full NASA service availability.\n')
print(text)
