"""Frozen-year, complete-month seasonal transfer. MODIS is a reference, not truth."""
import argparse,calendar,csv,hashlib,json
from collections import defaultdict
from pathlib import Path
from statistics import mean

def analyze(rows,train,holdout):
    if set(train)&set(holdout): raise ValueError('Training and holdout years overlap')
    if len({r['bbox'] for r in rows})>1: raise ValueError('Mixed AOIs')
    months=defaultdict(dict)
    for r in rows:
        m=r['date_utc'][:7]; s=r['source']; v=months[m].setdefault(s,{'days':set(),'native':0,'cells':0})
        if r['date_utc'] in v['days']: raise ValueError('Duplicate day')
        v['days'].add(r['date_utc']);v['native']+=int(r['raw_detections']);v['cells']+=int(r['occupied_cells_0_05deg'])
    for year in sorted(set(train+holdout)):
        for month in range(1,13):months.setdefault(f'{year}-{month:02}', {})
    pairs=[];excluded=[]
    for m,s in sorted(months.items()):
        n=calendar.monthrange(int(m[:4]),int(m[5:]))[1]
        if any(len(s.get(p,{}).get('days',[]))!=n for p in ['MODIS_SP','VIIRS_NOAA20_SP']): excluded.append(m);continue
        pairs.append({'month':m,'year':int(m[:4]),'season':(int(m[5:])-1)//3,'modis':s['MODIS_SP']['cells'],'viirs':s['VIIRS_NOAA20_SP']['cells'],'modis_native':s['MODIS_SP']['native'],'viirs_native':s['VIIRS_NOAA20_SP']['native']})
    tr=[r for r in pairs if r['year'] in train]; ho=[r for r in pairs if r['year'] in holdout]
    enough=len({r['year'] for r in tr})>=3 and len({r['year'] for r in ho})>=2 and len(tr)>=36 and len(ho)>=24
    denom=sum(r['viirs'] for r in tr);pool=sum(r['modis'] for r in tr)/denom if denom else None
    factors={}
    for s in range(4):
        a=[r for r in tr if r['season']==s];d=sum(r['viirs'] for r in a)
        factors[s]=sum(r['modis'] for r in a)/d if len(a)>=6 and d>=100 else pool
    def errors(adjust):
        e=[r['viirs']*(factors[r['season']] if adjust else 1)-r['modis'] for r in ho if not adjust or factors[r['season']] is not None]
        return {'n':len(e),'mae':mean(map(abs,e)) if e else None,'bias':mean(e) if e else None}
    base,adj=errors(False),errors(True)
    seasonal={}
    for season in range(4):
        part=[r for r in ho if r['season']==season]
        seasonal[season]={'n':len(part)}
        for name,adjust in [('unadjusted',False),('adjusted',True)]:
            ee=[r['viirs']*(factors[season] if adjust else 1)-r['modis'] for r in part if not adjust or factors[season] is not None]
            seasonal[season][name]={'mae':mean(map(abs,ee)) if ee else None,'bias':mean(ee) if ee else None}
    accepted=bool(enough and adj['n']==base['n'] and adj['mae'] is not None and adj['mae']<base['mae'] and abs(adj['bias'])<=abs(base['bias']))
    for r in pairs:r['adjusted']=r['viirs']*factors[r['season']] if accepted else None
    return {'method':'ember-1','grid_degrees':.05,'train_years':train,'holdout_years':holdout,'minimum_support':'36 training months in 3 years, 24 holdout months in 2 years; seasonal >=6 months and 100 VIIRS cell-days, otherwise pooled','acceptance_rule':'lower monthly holdout MAE and no worse absolute bias; identical months','factors':factors,'unadjusted':base,'adjusted':adj,'accepted':accepted,'reason':'Holdout criterion passed' if accepted else 'Insufficient overlap or holdout criterion failed','excluded_months':excluded,'seasonal_holdout':seasonal,'paired_months':len(pairs),'monthly':pairs,'unit':'occupied cell-days','observation_coverage':'unknown; no swath or usable-observation masks'}

def main():
    p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('--train',default='2020,2021,2022');p.add_argument('--holdout',default='2023,2024');a=p.parse_args()
    r=analyze(list(csv.DictReader(a.input.open())),list(map(int,a.train.split(','))),list(map(int,a.holdout.split(','))))
    r['input_sha256']=hashlib.sha256(a.input.read_bytes()).hexdigest();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2))
    with a.output.with_name('monthly_comparison.csv').open('w') as f:
        if r['monthly']:
            w=csv.DictWriter(f,fieldnames=list(r['monthly'][0]));w.writeheader();w.writerows(r['monthly'])
if __name__=='__main__':main()
