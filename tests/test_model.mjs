import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {makeIndex,aggregateMonth,adjustment,historicalBaseline,filterObservations,gridCell,aggregateCSV,observationCSV,monthsBetween} from '../web/model.mjs';
const pointer=JSON.parse(fs.readFileSync('web/data/dashboard.json'));
const summary=JSON.parse(fs.readFileSync('web/data/'+pointer.file));
const validation=JSON.parse(fs.readFileSync('web/data/'+pointer.validation.file));
const index=makeIndex(summary), state={area:'all',sensor:'both',start:'2020-01-01',end:'2024-12-31'};
test('released September reconciles with frozen reference and prior-year medians',()=>{
  const m=aggregateMonth(index,'2024-09','MODIS_SP',state),v=aggregateMonth(index,'2024-09','VIIRS_NOAA20_SP',state);
  assert.equal(m.cells,5819);assert.equal(v.cells,8809);assert.equal(m.native,23396);assert.equal(v.native,101659);
  assert.equal(adjustment(v,state,validation).value,validation.monthly.find(m=>m.month==='2024-09').adjusted);
  const b=historicalBaseline(index,'2024-09','MODIS_SP',state,validation);
  assert.equal(b.median,2532);assert.equal(b.n,4);assert.deepEqual(b.entries.map(e=>e.year),[2020,2021,2022,2023]);
  assert.equal(historicalBaseline(index,'2024-09','VIIRS_NOAA20_SP',state,validation).median,4782);
});
test('full-domain transfer never leaks into a subregion or partial month',()=>{
  for(const area of ['north','south']){const s={...state,area};assert.equal(adjustment(aggregateMonth(index,'2024-09','VIIRS_NOAA20_SP',s),s,validation),null);assert.equal(historicalBaseline(index,'2024-09','MODIS_SP',s,validation),null);}
  const s={...state,start:'2024-09-10',end:'2024-09-20'},r=aggregateMonth(index,'2024-09','VIIRS_NOAA20_SP',s);
  assert.equal(r.expected,11);assert.equal(r.retrieved,11);assert.equal(r.status,'Partial month');assert.equal(adjustment(r,s,validation),null);
});
test('missing retrieval stays null; successfully retrieved zero is zero',()=>{
  const absent=aggregateMonth(index,'2019-12','MODIS_SP',{...state,start:'2019-12-01'});assert.equal(absent.native,null);assert.equal(absent.cells,null);assert.equal(absent.status,'Data unavailable');
  const fixture=makeIndex({daily:Array.from({length:31},(_,i)=>({day:`2024-01-${String(i+1).padStart(2,'0')}`,product:'MODIS_SP',area:'all',native:0,cells:0}))});
  const zero=aggregateMonth(fixture,'2024-01','MODIS_SP',state);assert.equal(zero.native,0);assert.equal(zero.status,'No detections recorded');assert.equal(zero.complete,true);
  fixture.get('all|MODIS_SP|2024-01').pop();assert.equal(aggregateMonth(fixture,'2024-01','MODIS_SP',state).status,'Partial month');
});
test('baseline cannot include target/future years or fewer than three prior years',()=>{
  assert.equal(historicalBaseline(index,'2022-09','MODIS_SP',state,validation),null);
  assert.equal(historicalBaseline(index,'2023-09','MODIS_SP',state,validation).n,3);
});
test('latitude partition and exact negative grid edges match the primary pipeline',()=>{
  const r={date_utc:'2024-09-01',product:'MODIS_SP',longitude:-54,latitude:-19};
  assert.equal(filterObservations([r],'2024-09',{...state,area:'north'}).length,1);
  assert.equal(filterObservations([r],'2024-09',{...state,area:'south'}).length,0);
  assert.equal(filterObservations([{...r,latitude:-15}],'2024-09',state).length,1);
  assert.equal(gridCell(-19.05),-381);assert.equal(gridCell(-19.050001),-382);
});
test('period aggregate CSV contains the whole range and withholds unsupported adjustments',()=>{
  const all=aggregateCSV(index,state,validation,summary.snapshot.sha256);assert.equal(all.split('\r\n').length,121);
  const north=aggregateCSV(index,{...state,area:'north',sensor:'VIIRS_NOAA20_SP'},validation,summary.snapshot.sha256);
  assert.equal(north.split('\r\n').length,61);assert(!north.includes('supported full study area'));assert(north.includes('"unavailable","",""'));
  const missing=aggregateCSV(index,{...state,start:'2019-12-01',end:'2019-12-31'},validation,summary.snapshot.sha256);
  assert(missing.includes('"","","0","31","Data unavailable"'));
});
test('observation export keeps provenance and correctly escapes CSV',()=>{
  const text=observationCSV([{source:'file,"quoted"',time_utc:'0030'}],summary.snapshot.sha256);
  assert(text.includes('"0030"'));assert(text.includes('"file,""quoted"""'));assert(text.includes(summary.snapshot.sha256));
  assert.equal(monthsBetween(state.start,state.end).length,60);
});

test('a zero historical median keeps absolute difference and omits percentage',()=>{
  const daily=[];for(const year of [2020,2021,2022,2023])for(let day=1;day<=31;day++)daily.push({day:`${year}-01-${String(day).padStart(2,'0')}`,area:'all',product:'MODIS_SP',native:year===2023&&day===1?1:0,cells:year===2023&&day===1?1:0});
  const fake={monthly:[2020,2021,2022,2023].map(year=>({year}))};
  const b=historicalBaseline(makeIndex({daily}),'2023-01','MODIS_SP',state,fake);assert.equal(b.median,0);assert.equal(b.difference,1);assert.equal(b.percent,null);
});
