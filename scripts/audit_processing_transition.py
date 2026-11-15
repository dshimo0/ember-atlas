"""Audit actual SP/NRT overlap; never infer a processing join across an unobserved gap."""
import csv,hashlib,json
from datetime import date
from pathlib import Path
from build_dashboard import publish,encode
from firms import atomic_write

def audit(availability):
 by_id={r['data_id']:r for r in availability};sensors=[]
 for sensor in ['MODIS','VIIRS_NOAA20']:
  sp=by_id[sensor+'_SP'];nrt=by_id[sensor+'_NRT'];start=max(sp['min_date'],nrt['min_date']);end=min(sp['max_date'],nrt['max_date']);days=max(0,(date.fromisoformat(end)-date.fromisoformat(start)).days+1)
  sensors.append({'sensor':sensor,'sp_start':sp['min_date'],'sp_end':sp['max_date'],'nrt_start':nrt['min_date'],'nrt_end':nrt['max_date'],'overlap_days':days,'join_enabled':False})
 return {'schema':'ember-processing-overlap-1','sensors':sensors,'join_enabled':False,'status':'No coincident SP/NRT acquisition window is currently served'if not any(r['overlap_days']for r in sensors)else'Overlap exists but processing equivalence has not been evaluated','metrics':None,'reason':'A temporal gap cannot identify processing-level bias separately from changing fire activity. No equivalence or adjustment is inferred.','unblock':'When SP includes retained NRT acquisition windows, re-extract the same sensor/geometry/dates, compare versions, raw and occupied-cell counts and daily cell-set agreement, then preregister independent processing-transition evaluation.','historical_vintages':'Preserve raw NRT replies and exact retrieval times; current SP reprocessing is not a reconstruction of past publication latency.'}

def main():
 path=Path('data/source-availability-expansion.csv');r=audit(list(csv.DictReader(path.open())));r['source_availability_sha256']=hashlib.sha256(path.read_bytes()).hexdigest();r['source']='NASA FIRMS availability, retrieved in this execution; key omitted'
 ref=publish('processing-transition',r);atomic_write(Path('web/data/processing-transition.json'),encode(ref));print(json.dumps(r,indent=2))
if __name__=='__main__':main()
