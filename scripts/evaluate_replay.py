"""Evaluate three fixed training-only methods; the existing holdout is not a new selection set."""
import csv,hashlib,json
from pathlib import Path
from statistics import mean
from firms import atomic_write

def evaluate(v):
 train=[r for r in v['monthly'] if r['year'] in v['train_years']]
 holdout=[r for r in v['monthly'] if r['year'] in v['holdout_years']]
 # Through-origin least squares on identical training months: argmin_a sum((a*V)-M)^2.
 scalar=sum(r['viirs']*r['modis'] for r in train)/sum(r['viirs']**2 for r in train)
 monthly=[]
 for r in holdout:
  values={'unadjusted':r['viirs'],'scalar':scalar*r['viirs'],'seasonal':v['factors'][str(r['season'])]*r['viirs']}
  monthly.append({**r,'values':values,'residuals':{k:x-r['modis'] for k,x in values.items()}})
 def metrics(rows):
  return {k:{'n':len(rows),'mae':mean(abs(r['residuals'][k])for r in rows),'bias':mean(r['residuals'][k]for r in rows)}for k in ['unadjusted','scalar','seasonal']}
 # Descriptive stress test defined using only benchmark activity, without looking at candidate residuals.
 peak=sorted(monthly,key=lambda r:(-r['modis'],r['month']))[:6]
 return {'schema':'ember-replay-evaluation-1','scope':'Pantanal study area [-59,-23,-54,-15] only','unit':'occupied cell-days/month','grid_degrees':v['grid_degrees'],'training_years':v['train_years'],'training_months':len(train),'holdout_years':v['holdout_years'],'cutoff':f"{max(v['train_years'])+1}-01",'scenario':'Sensor transition replay; observed MODIS remains available after the scenario cutoff.','scalar':{'factor':scalar,'objective':'Nonnegative through-origin least squares: minimize sum over training months of (a * VIIRS - MODIS)^2. a=sum(VIIRS*MODIS)/sum(VIIRS^2); training data only.','selection':'Comparison baseline only; frozen seasonal publication rule unchanged.'},'seasonal_factors':v['factors'],'metrics':metrics(monthly),'peak_selection':'Six holdout months with the largest observed MODIS occupied cell-days; descending activity, month ascending for ties. Descriptive stress test; no residual-based selection.','peak_months':[r['month']for r in peak],'peak_metrics':metrics(peak),'monthly':monthly,'evaluation_protocol':'Existing 2023–2024 holdout is evaluation evidence. No refit or method selection on it. Future method selection requires a preregistered outer holdout from newly acquired years or nested blocked-year evaluation.'}
def main():
 source=Path('web/data/validation.json');v=json.loads(source.read_text());r=evaluate(v);r['validation_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
 payload=json.dumps(r,sort_keys=True,separators=(',',':')).encode();sha=hashlib.sha256(payload).hexdigest();name='replay-evaluation-'+sha[:12]+'.json'
 atomic_write(Path('web/data')/name,payload);atomic_write(Path('web/data/replay-evaluation.json'),json.dumps({'file':name,'sha256':sha}).encode())
 rows=[{'month':r['month'],'modis':r['modis'],**{k+'_value':x for k,x in r['values'].items()},**{k+'_residual':x for k,x in r['residuals'].items()}} for r in r['monthly']]
 import io
 output=io.StringIO(newline='');w=csv.DictWriter(output,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);atomic_write(Path('web/data/replay-residuals.csv'),output.getvalue().encode())
 print(json.dumps({'factor':r['scalar']['factor'],'metrics':r['metrics'],'peak_months':r['peak_months'],'peak_metrics':r['peak_metrics']},indent=2))
if __name__=='__main__':main()
