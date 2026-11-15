"""Apply preregistered inner selection and independent publication gates to each full area."""
import calendar,hashlib,json,math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from build_dashboard import publish

PROTOCOL=Path('data/regional-evaluation-protocol-v1.json')
def scalar(rows):
 d=sum(r['viirs']**2 for r in rows)
 return sum(r['viirs']*r['modis']for r in rows)/d if d else None

def quarterly(rows):
 d=sum(r['viirs']for r in rows);pooled=sum(r['modis']for r in rows)/d if d else None;factors={}
 for q in range(4):
  part=[r for r in rows if r['season']==q];denom=sum(r['viirs']for r in part)
  factors[q]=sum(r['modis']for r in part)/denom if len(part)>=6 and denom>=100 else pooled
 return factors

def errors(rows,factor):
 residuals=[(factor(r)*r['viirs']-r['modis'])for r in rows if factor(r)is not None]
 return {'n':len(residuals),'mae':mean(map(abs,residuals))if residuals else None,'bias':mean(residuals)if residuals else None,'rmse':math.sqrt(mean(x*x for x in residuals))if residuals else None}

def paired(daily):
 months=defaultdict(lambda:defaultdict(list))
 for r in daily:
  if r['area']=='all'and r['product']in ['MODIS_SP','VIIRS_NOAA20_SP']:months[r['day'][:7]][r['product']].append(r)
 rows=[];excluded=[]
 for m,products in sorted(months.items()):
  n=calendar.monthrange(int(m[:4]),int(m[5:]))[1]
  if any(len(products[p])!=n or len({r['day']for r in products[p]})!=n for p in ['MODIS_SP','VIIRS_NOAA20_SP']):excluded.append(m);continue
  rows.append({'month':m,'year':int(m[:4]),'season':(int(m[5:])-1)//3,'modis':sum(r['cells']for r in products['MODIS_SP']),'viirs':sum(r['cells']for r in products['VIIRS_NOAA20_SP']),'modis_native':sum(r['native']for r in products['MODIS_SP']),'viirs_native':sum(r['native']for r in products['VIIRS_NOAA20_SP'])})
 return rows,excluded

def better(candidate,baseline):return candidate['n']==baseline['n']and candidate['mae']is not None and candidate['mae']<baseline['mae']and abs(candidate['bias'])<=abs(baseline['bias'])

def evaluate(daily,region):
 protocol=json.loads(PROTOCOL.read_text());rows,excluded=paired(daily)
 training=[r for r in rows if r['year']in protocol['training_years']];inner=[r for r in rows if r['year']in protocol['inner_training_years']];iv=[r for r in rows if r['year']==2022]
 inner_scalar=scalar(inner);inner_q=quarterly(inner);inner_metrics={'scalar':errors(iv,lambda r:inner_scalar),'seasonal':errors(iv,lambda r:inner_q[r['season']])}
 chosen='scalar'if inner_metrics['scalar']['mae']is not None and(inner_metrics['seasonal']['mae']is None or inner_metrics['scalar']['mae']<=inner_metrics['seasonal']['mae']+1e-9)else'seasonal'
 if len(inner)!=24 or len(iv)!=12 or all(m['mae']is None for m in inner_metrics.values()):chosen=None
 sf=scalar(training);qf=quarterly(training);factors={q:sf for q in range(4)}if chosen=='scalar'else qf if chosen=='seasonal'else{q:None for q in range(4)}
 methods={'unadjusted':lambda r:1,'scalar':lambda r:sf,'seasonal':lambda r:qf[r['season']]}
 parts={'outer':[r for r in rows if r['year']in [2023,2024]],'outer_excluding_known':[r for r in rows if r['year']in[2023,2024]and r['month']!='2024-09'],'external':[r for r in rows if '2025-01'<=r['month']<='2026-07']}
 metrics={part:{name:errors(rs,fn)for name,fn in methods.items()}for part,rs in parts.items()}
 support=len(training)==36 and len(iv)==12 and len(inner)==24 and len(parts['outer'])==24 and len(parts['external'])==19
 gates={part:bool(chosen and better(m[chosen],m['unadjusted']))for part,m in metrics.items()};accepted=support and all(gates.values())and region!='pantanal'
 monthly=[]
 for r in rows:monthly.append(dict(r,adjusted=r['viirs']*factors[r['season']]if accepted and factors[r['season']]is not None else None))
 peaks={part:[r['month']for r in sorted(rs,key=lambda r:(-r['modis'],r['month']))[:6]]for part,rs in parts.items()}
 residuals={part:[{'month':r['month'],'modis':r['modis'],'viirs':r['viirs'],'values':{k:fn(r)*r['viirs']if fn(r)is not None else None for k,fn in methods.items()},'residuals':{k:fn(r)*r['viirs']-r['modis']if fn(r)is not None else None for k,fn in methods.items()}}for r in rs]for part,rs in parts.items()}
 return {'schema':'ember-regional-validation-1','region':region,'method':'regional-inner-1 '+(chosen or'unavailable'),'selected_method':chosen,'grid_degrees':.05,'train_years':[2020,2021,2022],'holdout_years':[2023,2024],'factors':factors,'seasonal_factors':qf,'scalar_factor':sf,'accepted':accepted,'reason':'All preregistered gates passed'if accepted else'Pantanal frozen publication retained; 19 fresh months are below the required 24'if region=='pantanal'else'Incomplete support or a preregistered independent gate failed','minimum_support':{'training_months':36,'outer_months':24,'external_months':19},'selection':{'fit_years':[2020,2021],'selection_year':2022,'metrics':inner_metrics,'chosen':chosen,'never_selected_using_outer':True},'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),'protocol_commit':'17403f3','unadjusted':metrics['outer']['unadjusted'],'adjusted':metrics['outer'][chosen]if chosen else errors(parts['outer'],lambda r:None),'partitions':metrics,'gates':gates,'support_complete':support,'monthly':monthly,'residuals':residuals,'peak_months':peaks,'excluded_months':excluded,'publication_domain':{'start':'2020-01-01','end':'2026-07-31','area':'full study area'}if accepted else None,'unit':'occupied cell-days/month','observation_coverage':'unknown; no usable masks or ground truth'}

def comparison_document(v):
 rows=v['residuals']['outer'];peak=v['peak_months']['outer'];peak_metrics={}
 for k in ['unadjusted','scalar','seasonal']:
  values=[r['residuals'][k]for r in rows if r['month']in peak and r['residuals'][k]is not None]
  peak_metrics[k]={'n':len(values),'mae':mean(map(abs,values))if values else None,'bias':mean(values)if values else None}
 return {'schema':'ember-regional-comparison-1','region':v['region'],'scope':v['region']+' full study area only','cutoff':'2023-01','scalar':{'factor':v['scalar_factor']},'metrics':v['partitions']['outer'],'monthly':rows,'peak_months':peak,'peak_metrics':peak_metrics,'selection':v['selection'],'external':v['partitions']['external']}

def publish_residuals(v):
 import csv,io
 from firms import atomic_write
 output=io.StringIO(newline='');writer=csv.writer(output,lineterminator='\n');writer.writerow(['region','evaluation_partition','month','method','modis_reference_cell_days','viirs_common_grid_cell_days','candidate_cell_days','residual_cell_days','purpose','unit','protocol_sha256'])
 for partition,rows in v['residuals'].items():
  for r in rows:
   for method in ['unadjusted','scalar','seasonal']:writer.writerow([v['region'],partition,r['month'],method,r['modis'],r['viirs'],r['values'][method],r['residuals'][method],'evaluation candidate; publication is controlled separately','occupied cell-days/month',v['protocol_sha256']])
 payload=output.getvalue().encode();digest=hashlib.sha256(payload).hexdigest();name=v['region']+'-candidate-residuals-'+digest[:12]+'.csv';atomic_write(Path('web/data')/name,payload);return {'file':name,'sha256':digest}
