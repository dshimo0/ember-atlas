"""Restore literal source flags on frozen normalized records without changing their selection."""
import hashlib,json
from collections import defaultdict
from pathlib import Path
from firms import read_csv

def identity(r,normalized=False):
 return (r['platform']if normalized else r['satellite'],r['date_utc']if normalized else r['acq_date'],(r['time_utc']if normalized else r['acq_time']).zfill(4),float(r['latitude']),float(r['longitude']))

def hydrate(rows):
 groups=defaultdict(list)
 for r in rows:groups[r['source']].append(r)
 enriched=[]
 for name,selected in groups.items():
  path=Path(name);assert path.resolve().is_relative_to(Path('data/matched').resolve()),'Unexpected frozen source reference';m=json.loads(path.read_text());payload=path.with_suffix('.csv').read_bytes();assert hashlib.sha256(payload).hexdigest()==m['sha256'];needed={identity(r,True)for r in selected};lookup={}
  for raw in read_csv(payload):
   key=identity(raw)
   if key in needed:lookup.setdefault(key,raw)
  for r in selected:
   raw=lookup[identity(r,True)];assert m['source']==r['product']
   for normalized,original in [('confidence','confidence'),('frp_mw','frp'),('daynight','daynight')]:assert r[normalized]==raw.get(original,'')
   enriched.append(dict(r,source_version=raw.get('version',''),detection_type=raw.get('type','')))
 # Preserve the original record order as well as every original field.
 by_source_identity={(r['source'],identity(r,True)):r for r in enriched}
 return [dict(r,source_version=by_source_identity[(r['source'],identity(r,True))]['source_version'],detection_type=by_source_identity[(r['source'],identity(r,True))]['detection_type'])for r in rows]

def add_attributes(rows,attributes,pantanal=False):
 for r in rows:
  for area in (['all','north'if r['latitude']>=-19 else'south']if pantanal else['all']):
   key=(r['date_utc'],r['product'],area)
   for name,field in [('source_versions','source_version'),('detection_types','detection_type')]:
    value=r.get(field)or'not provided';counts=attributes.setdefault(key,{}).setdefault(name,{});counts[value]=counts.get(value,0)+1

def diagnostic(daily,region,bounds):
 products={}
 for product in sorted({r['product']for r in daily}):
  groups={}
  for name,first,last in [('training','2020-01-01','2022-12-31'),('outer','2023-01-01','2024-12-31'),('fresh','2025-01-01','2026-07-31')]:
   versions={};types={};n=0
   for row in daily:
    if row['area']=='all'and row['product']==product and first<=row['day']<=last:
     n+=row['native']
     for field,target in [('source_versions',versions),('detection_types',types)]:
      for key,count in row.get(field,{}).items():target[key]=target.get(key,0)+count
   groups[name]={'from_utc':first,'through_utc':last,'native_detections':n,'reported_versions':versions,'reported_types':types}
  products[product]=groups
 ref=products.get('MODIS_SP',{});training=ref.get('training',{}).get('reported_versions',{});outer=ref.get('outer',{}).get('reported_versions',{})
 return {'schema':'ember-source-field-audit-1','region':region,'bounds':bounds,'products':products,'modis_reference_labels_differ_across_split':bool(training and outer and set(training)!=set(outer)),'interpretation':'Agreement is with MODIS_SP as delivered. Literal reference-version labels differ across the split; uniform reference processing and isolated sensor effects are not established. All reported thermal types are retained. Native type counts are not additive cell-day contributions.','version_mapping_independently_verified':False}
