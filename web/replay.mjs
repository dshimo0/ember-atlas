import {aggregateMonth,adjustment,monthsBetween,monthEnd,csv} from './model.mjs';
export const replayCutoff=v=>`${Math.max(...v.train_years)+1}-01`;
export const supportsReplay=s=>(!s.region||s.region==='pantanal')&&s.area==='all'&&s.mode!=='nrt';
export function replayMonth(index,month,s,v){
 const cutoff=replayCutoff(v),before=month<cutoff,source=before?'MODIS_SP':'VIIRS_NOAA20_SP';
 const observed=aggregateMonth(index,month,source,s),benchmark=aggregateMonth(index,month,'MODIS_SP',s),a=before?null:adjustment(observed,s,v);
 const supported=supportsReplay(s),value=supported&&observed.complete?(before?observed.cells:a?.value??null):null;
 return {month,value,source,adjustment:before?'none; observed MODIS':a&&supported?'frozen seasonal factor':'unavailable',factor:before?1:a&&supported?a.factor:null,from:observed.from,to:observed.to,retrieved:observed.retrieved,expected:observed.expected,complete:observed.complete,status:!observed.retrieved?'Data unavailable':!observed.complete?'Partial month':value===null?'Adjustment unavailable':'Complete retrieval',benchmark:!before&&benchmark.complete?benchmark.cells:null,phase:v.train_years.includes(+month.slice(0,4))?'Training':v.holdout_years.includes(+month.slice(0,4))?'Holdout':'Archive',cutoff};
}
export function replayRows(index,s,v){return monthsBetween(s.start,s.end).map(m=>replayMonth(index,m,s,v));}
export function replayBaseline(index,month,s,v){
 if(!supportsReplay(s))return null;const current=replayMonth(index,month,s,v);if(current.value===null)return null;
 const years=[...new Set([...index.keys()].filter(k=>k.startsWith('all|')).map(k=>+k.split('|')[2].slice(0,4)))].sort((a,b)=>a-b),entries=[];
 for(const year of years.filter(y=>y<+month.slice(0,4)&&y>=Math.min(...v.train_years))){const m=year+month.slice(4),r=replayMonth(index,m,{...s,start:m+'-01',end:monthEnd(m)},v);if(r.value!==null)entries.push({year,value:r.value,source:r.source,adjustment:r.adjustment,factor:r.factor});}
 if(entries.length<3)return null;const values=entries.map(e=>e.value).sort((a,b)=>a-b),median=(values[Math.floor((values.length-1)/2)]+values[Math.floor(values.length/2)])/2;
 return {entries,n:entries.length,median,difference:current.value-median,percent:median?100*(current.value/median-1):null};
}
export function replayCSV(index,s,v,snapshot){
 const headers=['month','region','area','scenario_cutoff','scenario','source_product','adjustment','factor','reference_scale_cell_days','benchmark_modis_cell_days','from_utc','through_utc','retrieved_days','selected_days','status','snapshot_sha256'];
 return csv(headers,replayRows(index,s,v).map(r=>[r.month,s.region||'pantanal',s.area,r.cutoff,'sensor transition replay; not actual source availability',r.source,r.adjustment,r.factor,r.value,r.benchmark,r.from,r.to,r.retrieved,r.expected,r.status,snapshot]));
}
export function compareMethods(v){
 const train=v.monthly.filter(r=>v.train_years.includes(r.year)),holdout=v.monthly.filter(r=>v.holdout_years.includes(r.year));
 const scalar=train.reduce((n,r)=>n+r.viirs*r.modis,0)/train.reduce((n,r)=>n+r.viirs**2,0);
 const rows=holdout.map(r=>({...r,residuals:{unadjusted:r.viirs-r.modis,scalar:r.viirs*scalar-r.modis,seasonal:r.viirs*v.factors[r.season]-r.modis}}));
 const metrics=rows=>Object.fromEntries(['unadjusted','scalar','seasonal'].map(k=>[k,{n:rows.length,mae:rows.reduce((n,r)=>n+Math.abs(r.residuals[k]),0)/rows.length,bias:rows.reduce((n,r)=>n+r.residuals[k],0)/rows.length}]));
 const peak=[...rows].sort((a,b)=>b.modis-a.modis||a.month.localeCompare(b.month)).slice(0,6);
 return {scalar,rows,metrics:metrics(rows),peak_months:peak.map(r=>r.month),peak_metrics:metrics(peak)};
}
