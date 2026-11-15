import {aggregateMonth,adjustment,monthsBetween,monthEnd,csv} from './model.mjs';
export const replayCutoff=v=>`${Math.max(...v.train_years)+1}-01`;
export const supportsReplay=(s,v)=>s.area==='all'&&s.mode!=='nrt'&&(v?!!v.accepted&&(s.region||'pantanal')===(v.region||'pantanal'):typeof s.calibrationAvailable==='boolean'?s.calibrationAvailable:!s.region||s.region==='pantanal');
export function replayMonth(index,month,s,v){
 const cutoff=replayCutoff(v),before=month<cutoff,source=before?'MODIS_SP':'VIIRS_NOAA20_SP';
 const observed=aggregateMonth(index,month,source,s),benchmark=aggregateMonth(index,month,'MODIS_SP',s),a=before?null:adjustment(observed,s,v);
 const supported=supportsReplay(s,v),value=supported&&observed.complete?(before?observed.cells:a?.value??null):null;
 return {month,value,source,adjustment:before?'none; observed MODIS':a&&supported?(v.selected_method==='scalar'?'training-only scalar':v.region?'regional seasonal factor':'frozen seasonal factor'):'unavailable',factor:before?1:a&&supported?a.factor:null,from:observed.from,to:observed.to,retrieved:observed.retrieved,expected:observed.expected,complete:observed.complete,status:!observed.retrieved?'Data unavailable':!observed.complete?'Partial month':value===null?'Adjustment unavailable':'Complete retrieval',benchmark:!before&&benchmark.complete?benchmark.cells:null,phase:v.train_years.includes(+month.slice(0,4))?'Training':v.holdout_years.includes(+month.slice(0,4))?'Holdout':+month.slice(0,4)>Math.max(...v.holdout_years)?'External evaluation':'Archive',cutoff};
}
export function replayRows(index,s,v){return monthsBetween(s.start,s.end).map(m=>replayMonth(index,m,s,v));}
export function replayBaseline(index,month,s,v){
 if(!supportsReplay(s,v))return null;const current=replayMonth(index,month,s,v);if(current.value===null)return null;
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
 const denominator=train.reduce((n,r)=>n+r.viirs**2,0),scalar=denominator?train.reduce((n,r)=>n+r.viirs*r.modis,0)/denominator:null,seasonal=v.seasonal_factors||v.factors;
 const rows=holdout.map(r=>({...r,residuals:{unadjusted:r.viirs-r.modis,scalar:scalar!==null?r.viirs*scalar-r.modis:null,seasonal:Number.isFinite(seasonal[r.season])?r.viirs*seasonal[r.season]-r.modis:null}}));
 const metrics=rs=>Object.fromEntries(['unadjusted','scalar','seasonal'].map(k=>{const values=rs.map(r=>r.residuals[k]).filter(x=>x!==null);return[k,{n:values.length,mae:values.length?values.reduce((n,x)=>n+Math.abs(x),0)/values.length:null,bias:values.length?values.reduce((n,x)=>n+x,0)/values.length:null}];}));
 const peak=[...rows].sort((a,b)=>b.modis-a.modis||a.month.localeCompare(b.month)).slice(0,6);
 return {scalar,rows,metrics:metrics(rows),peak_months:peak.map(r=>r.month),peak_metrics:metrics(peak)};
}
