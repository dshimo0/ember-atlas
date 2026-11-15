"""Refresh small source diagnostics from verified daily snapshots; do not refit or rewrite points."""
import json
from pathlib import Path
from source_attributes import diagnostic
from build_dashboard import publish,encode
from firms import atomic_write
ROOT=Path('web/data')
def apply(summary):
 audit=diagnostic(summary['daily'],summary['region'],summary['bounds']);ref=publish(summary['region']+'-source-field-audit',audit);summary['source_field_audit']=ref
 summary['calibration']['reference_versions']={k:v['reported_versions']for k,v in audit['products'].get('MODIS_SP',{}).items()};return ref

def main():
 registry=json.loads((ROOT/json.loads((ROOT/'regions.json').read_text())['file']).read_text())
 for r in registry['regions']:
  sp_ref=None;versions=None
  for mode,ref in r['datasets'].items():
   s=json.loads((ROOT/ref['file']).read_text())
   if mode=='sp':sp_ref=apply(s);versions=s['calibration']['reference_versions']
   else:s['source_field_audit']=sp_ref;s['calibration']['reference_versions']=versions
   updated=publish(r['id']+'-'+mode+'-dashboard',s);r['datasets'][mode]=dict(ref,**updated,calibration=s['calibration'],source_field_audit=sp_ref)
 ref=publish('regions',registry);atomic_write(ROOT/'regions.json',encode(ref));print(ref)
if __name__=='__main__':main()
