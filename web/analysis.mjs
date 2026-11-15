import {aggregateMonth,adjustment,monthsBetween} from './model.mjs';
export function evaluateValidation(v) {
  const rows=v.monthly.filter(r=>v.holdout_years.includes(r.year)).map(r=>{
    const value=r.viirs*v.factors[r.season],before=r.viirs-r.modis,after=value-r.modis;
    return {...r,adjusted:value,before,after,underperforms:Math.abs(after)>Math.abs(before)};
  });
  function metrics(key){return {n:rows.length,mae:rows.reduce((s,r)=>s+Math.abs(r[key]),0)/rows.length,bias:rows.reduce((s,r)=>s+r[key],0)/rows.length,rmse:Math.sqrt(rows.reduce((s,r)=>s+r[key]**2,0)/rows.length)};}
  const before=metrics('before'),after=metrics('after');
  for(const [a,b] of [[before,v.unadjusted],[after,v.adjusted]])for(const key of ['n','mae','bias'])if(Math.abs(a[key]-b[key])>1e-7)throw new Error('Validation evidence does not reconcile');
  return {before,after,rows,reduction:100*(1-after.mae/before.mae),underperforming:rows.filter(r=>r.underperforms)};
}
export function referenceRows(index,s,v) {
  return monthsBetween(s.start,s.end).map(month=>{
    const m=aggregateMonth(index,month,'MODIS_SP',s),r=aggregateMonth(index,month,'VIIRS_NOAA20_SP',s),a=adjustment(r,s,v);
    return {month,reference:s.sensor!=='VIIRS_NOAA20_SP'&&m.complete?m.cells:null,viirs:s.sensor!=='MODIS_SP'&&r.complete?r.cells:null,adjusted:s.sensor!=='MODIS_SP'?(a?.value??null):null,status:!r.retrieved?'Data unavailable':!r.complete?'Partial month':a?'Supported':'Adjustment unavailable',phase:v.train_years.includes(+month.slice(0,4))?'Training':v.holdout_years.includes(+month.slice(0,4))?'Holdout':'Outside release',source:'VIIRS_NOAA20_SP',reference_source:'MODIS_SP'};
  });
}
export function sensitivitySummary(d) {
  return ['MODIS_SP','VIIRS_NOAA20_SP'].map(product=>{
    const total=(grid,confidence)=>d.grid_confidence.filter(r=>r.product===product&&r.grid===grid&&r.confidence===confidence).reduce((s,r)=>s+r.cell_days,0);
    const baseline=total('0.05','all');
    return {product,baseline,finerPercent:100*(total('0.025','all')/baseline-1),coarserPercent:100*(total('0.1','all')/baseline-1),highConfidencePercent:100*total('.05','high')/baseline};
  });
}
