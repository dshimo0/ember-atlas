"""Write a single artifact-derived regional evaluation table into the release documents."""
import json
from pathlib import Path
ROOT=Path('web/data')
def read(ref):return json.loads((ROOT/ref['file']).read_text())
def write():
 registry=read(json.loads((ROOT/'regions.json').read_text()));rows=['| Study area | Inner choice | Outer MAE: raw → choice (n) | Fresh MAE: raw → choice (n) | Fresh signed bias | Published adjustment |','| --- | --- | ---: | ---: | ---: | --- |'];evidence=[]
 def n(x):return '—'if x is None else f'{x:,.1f}'
 for r in registry['regions']:
  s=read(r['datasets']['sp']);a=read(s['external_audit']);method=a['selected_method'];o=a['partitions']['outer'];fresh=a['partitions']['external'];c=s['calibration'];om=o.get(method,{'mae':None,'n':0});fm=fresh.get(method,{'mae':None,'bias':None,'n':0});publication=c['selected_method']+' through '+c['period']['end']if c['accepted']else'Withheld'
  rows.append(f"| {r['name']} | {method} | {n(o['unadjusted']['mae'])} → {n(om['mae'])} ({om['n']}) | {n(fresh['unadjusted']['mae'])} → {n(fm['mae'])} ({fm['n']}) | {n(fm['bias'])} | {publication} |")
  evidence.append({'region':r['id'],'audit':s['external_audit'],'selected_method':method,'accepted':c['accepted'],'domain':c['period'],'gates':a['gates'],'support_complete':a['support_complete']})
 text='\n'.join(rows)+'\n\nUnits: occupied cell-days/month; full named study rectangle, SP only. Inner choice uses 2022 after fitting 2020–2021; refit uses 2020–2022. Outer: 2023–2024, including the previously published September 2024; the artifact also reports the sensitivity excluding that month. Fresh: January 2025–July 2026, excluded from fitting and selection. Pantanal retains the original publication regardless of the new audit. A failed regional gate withholds adjustment. MODIS is the comparison reference, not ground truth.\n'
 Path('submission/regional-evaluation.md').write_text('# Regional evaluation\n\n'+text)
 Path('submission/regional-evaluation-index.json').write_text(json.dumps({'registry':json.loads((ROOT/'regions.json').read_text()),'regions':evidence},indent=2)+'\n')
 for path in ['README.md','docs/methodology.md','docs/challenge-traceability.md']:
  p=Path(path);body=p.read_text();start='<!-- REGIONAL-EVALUATION:START -->';end='<!-- REGIONAL-EVALUATION:END -->'
  if start not in body:body+='\n## Regional evaluation\n\n'+start+'\n'+end+'\n'
  a=body.index(start)+len(start);b=body.index(end);p.write_text(body[:a]+'\n'+text+body[b:])
 print(text)
if __name__=='__main__':write()
