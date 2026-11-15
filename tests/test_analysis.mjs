import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {evaluateValidation,referenceRows,sensitivitySummary} from '../web/analysis.mjs';
import {defaultState,readURL,stateURL} from '../web/url-state.mjs';
import {makeIndex,historicalBaseline} from '../web/model.mjs';
const pointer=JSON.parse(fs.readFileSync('web/data/dashboard.json'));
const summary=JSON.parse(fs.readFileSync('web/data/'+pointer.file));
const validation=JSON.parse(fs.readFileSync('web/data/'+pointer.validation.file));
const index=makeIndex(summary),s=defaultState(summary.coverage);
test('holdout metrics recompute from frozen factors, including worse months',()=>{
 const e=evaluateValidation(validation);assert.equal(e.rows.length,24);
 assert(Math.abs(e.reduction-80.45433076451603)<1e-10);
 assert.deepEqual(e.underperforming.map(r=>r.month),['2023-02','2023-03']);
 assert(e.after.rmse>=e.after.mae);assert(e.before.rmse>=e.before.mae);
 const corrupt=structuredClone(validation);corrupt.adjusted.mae+=1;assert.throws(()=>evaluateValidation(corrupt),/reconcile/);
});
test('regional baselines independently reconcile daily summaries; no regional reference-scale series',()=>{
 for(const area of ['north','south'])for(const product of ['MODIS_SP','VIIRS_NOAA20_SP']){
  const values=[2020,2021,2022,2023].map(y=>summary.daily.filter(r=>r.area===area&&r.product===product&&r.day.startsWith(y+'-09')).reduce((n,r)=>n+r.cells,0)).sort((a,b)=>a-b);
  const b=historicalBaseline(index,'2024-09',product,{...s,area},validation);assert.equal(b.median,(values[1]+values[2])/2);assert.equal(b.n,4);
  assert(referenceRows(index,{...s,area},validation).every(r=>r.adjusted===null));
 }
});
test('reference-scale series preserves sources, zero, missing and sensor selection',()=>{
 const rows=referenceRows(index,s,validation);assert.equal(rows.length,60);assert.equal(rows.find(r=>r.month==='2024-09').adjusted,validation.monthly.find(r=>r.month==='2024-09').adjusted);
 assert(rows.every(r=>r.source==='VIIRS_NOAA20_SP'&&r.reference_source==='MODIS_SP'));
 assert(referenceRows(index,{...s,sensor:'MODIS_SP'},validation).every(r=>r.viirs===null&&r.adjusted===null));
 assert(referenceRows(index,{...s,sensor:'VIIRS_NOAA20_SP'},validation).every(r=>r.reference===null));
 assert.equal(referenceRows(index,{...s,start:'2019-12-01',end:'2019-12-31'},validation)[0].adjusted,null);
 assert.equal(referenceRows(index,{...s,start:'2024-09-10',end:'2024-09-20'},validation)[0].adjusted,null);
});
test('share URL roundtrips area/month/sensor/dates/view/step/slide and rejects invalid inputs',()=>{
 const selected={...s,area:'north',month:'2024-08',sensor:'MODIS_SP',step:4,slide:6,view:'raw'};
 assert.deepEqual(readURL(stateURL('/demo',selected),summary.coverage),{...selected,slide:1});
 assert.equal(readURL(stateURL('/pitch',selected),summary.coverage).slide,6);
 const invalid=readURL('/demo?area=bogus&start=2024-02-31&month=2025-99&step=100',summary.coverage);assert.equal(invalid.area,'all');assert.equal(invalid.start,s.start);assert.equal(invalid.month,'2024-09');assert.equal(invalid.step,5);
});
test('sensitivity summary uses real product-specific confidence and grid diagnostics',()=>{
 const d=JSON.parse(fs.readFileSync('web/data/diagnostics.json')),rows=sensitivitySummary(d);
 assert.equal(rows.length,2);for(const r of rows){assert(r.finerPercent>0);assert(r.coarserPercent<0);assert(r.highConfidencePercent>0&&r.highConfidencePercent<=100);}
});
