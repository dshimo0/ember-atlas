import {aggregateMonth,adjustment,monthsBetween,evaluationPhase} from './model.mjs';
export function evaluateValidation(v) {
 const rows=v.monthly.filter(r=>v.holdout_years.includes(r.year)).map(r=>{const factor=v.factors[r.season],value=Number.isFinite(factor)?r.viirs*factor:null,before=r.viirs-r.modis,after=value===null?null:value-r.modis;return {...r,adjusted:value,before,after,underperforms:after!==null&&Math.abs(after)>Math.abs(before)};});
 function metrics(k){const values=rows.map(r=>r[k]).filter(x=>x!==null),n=values.length;return{n,mae:n?values.reduce((s,x)=>s+Math.abs(x),0)/n:null,bias:n?values.reduce((s,x)=>s+x,0)/n:null,rmse:n?Math.sqrt(values.reduce((s,x)=>s+x*x,0)/n):null};}
 const before=metrics('before'),after=metrics('after');
 for(const [a,b]of[[before,v.unadjusted],[after,v.adjusted]])for(const k of['n','mae','bias'])if((a[k]===null)!==(b[k]===null)||a[k]!==null&&Math.abs(a[k]-b[k])>1e-7)throw new Error('Validation evidence does not reconcile');
 return{before,after,rows,reduction:before.mae>0&&after.mae!==null?100*(1-after.mae/before.mae):null,underperforming:rows.filter(r=>r.underperforms)};
}
export function referenceRows(index,s,v) {
  return monthsBetween(s.start,s.end).map(month=>{
    const m=aggregateMonth(index,month,s.mode==='nrt'?'MODIS_NRT':'MODIS_SP',s),r=aggregateMonth(index,month,s.mode==='nrt'?'VIIRS_NOAA20_NRT':'VIIRS_NOAA20_SP',s),a=adjustment(r,s,v);
    return {reference_versions:m.source_versions,viirs_versions:r.source_versions,month,reference:s.sensor!=='VIIRS_NOAA20_SP'&&m.retrieved?m.cells:null,viirs:s.sensor!=='MODIS_SP'&&r.retrieved?r.cells:null,adjusted:s.sensor!=='MODIS_SP'?(a?.value??null):null,status:!r.retrieved?'Data unavailable':!r.complete?'Partial month':a?'Supported':'Adjustment unavailable',phase:evaluationPhase(month,s,v),source:'VIIRS_NOAA20_SP',reference_source:'MODIS_SP'};
  });
}
export function sensitivitySummary(d) {
  return ['MODIS_SP','VIIRS_NOAA20_SP'].map(product=>{
    const total=(grid,confidence)=>d.grid_confidence.filter(r=>r.product===product&&r.grid===grid&&r.confidence===confidence).reduce((s,r)=>s+r.cell_days,0);
    const baseline=total('0.05','all');
    return {product,baseline,finerPercent:100*(total('0.025','all')/baseline-1),coarserPercent:100*(total('0.1','all')/baseline-1),highConfidencePercent:100*total('.05','high')/baseline};
  });
}
