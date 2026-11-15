import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import zlib from 'node:zlib';
import {makeIndex,adjustment,aggregateMonth,occupiedDays,filterObservations} from '../web/model.mjs';
import {compareMethods,replayMonth,replayBaseline,replayCSV} from '../web/replay.mjs';
const p=JSON.parse(fs.readFileSync('web/data/dashboard.json')),summary=JSON.parse(fs.readFileSync('web/data/'+p.file)),v=JSON.parse(fs.readFileSync('web/data/'+p.validation.file));
const index=makeIndex(summary),s={region:'pantanal',mode:'sp',area:'all',sensor:'both',start:'2020-01-01',end:'2024-12-31'};
test('replay changes sources only at January 2023 and retains separate observed benchmark',()=>{
 const before=replayMonth(index,'2022-12',s,v),after=replayMonth(index,'2023-01',s,v);
 assert.equal(before.source,'MODIS_SP');assert.equal(before.factor,1);assert.equal(before.value,aggregateMonth(index,'2022-12','MODIS_SP',s).cells);assert.equal(before.benchmark,null);
 assert.equal(after.source,'VIIRS_NOAA20_SP');assert.equal(after.value,v.monthly.find(r=>r.month==='2023-01').adjusted);assert.equal(after.benchmark,v.monthly.find(r=>r.month==='2023-01').modis);
 const text=replayCSV(index,s,v,summary.snapshot.sha256);assert(text.includes('sensor transition replay; not actual source availability'));assert.equal(text.split('\r\n').length,61);
});
test('replay leaves missing and incomplete months unavailable; no geographic or NRT transfer',()=>{
 assert.equal(replayMonth(index,'2019-12',{...s,start:'2019-12-01'},v).value,null);
 assert.equal(replayMonth(index,'2024-09',{...s,start:'2024-09-10'},v).value,null);
 for(const region of ['southern-amazon','cerrado','gran-chaco','california','southeastern-australia','iberian-peninsula','siberia'])assert.equal(replayMonth(index,'2024-09',{...s,region},v).value,null);
 assert.equal(adjustment(aggregateMonth(index,'2024-09','VIIRS_NOAA20_SP',s),{...s,mode:'nrt'},v),null);
});
test('scalar fits only training values; all methods and peak subsets match versioned evidence',()=>{
 const ref=JSON.parse(fs.readFileSync('web/data/replay-evaluation.json')),e=JSON.parse(fs.readFileSync('web/data/'+ref.file)),r=compareMethods(v);
 assert(Math.abs(r.scalar-e.scalar.factor)<1e-12);assert.deepEqual(r.peak_months,e.peak_months);
 for(const key of ['unadjusted','scalar','seasonal'])for(const f of ['mae','bias','n']){assert(Math.abs(r.metrics[key][f]-e.metrics[key][f])<1e-9);assert(Math.abs(r.peak_metrics[key][f]-e.peak_metrics[key][f])<1e-9);}
 const changed=structuredClone(v);changed.monthly.filter(r=>v.holdout_years.includes(r.year)).forEach(r=>r.modis*=100);assert.equal(compareMethods(changed).scalar,r.scalar);
});
test('replay baseline uses earlier months and keeps each month source and adjustment inspectable',()=>{
 const b=replayBaseline(index,'2024-09',s,v);assert.equal(b.n,4);assert.deepEqual(b.entries.map(e=>e.year),[2020,2021,2022,2023]);assert.equal(b.entries.at(-1).source,'VIIRS_NOAA20_SP');assert.equal(b.entries[0].source,'MODIS_SP');
 const changed=new Map(index);changed.set('all|MODIS_SP|2024-09',[]);assert.equal(replayBaseline(changed,'2023-09',s,v).median,replayBaseline(index,'2023-09',s,v).median);
});
test('full-data occupied-day map exactly reconciles common-grid monthly totals',()=>{
 const ref=summary.observation_shards['2024-09'],payload=JSON.parse(zlib.gunzipSync(fs.readFileSync('web/data/'+ref.file)));
 for(const product of ['MODIS_SP','VIIRS_NOAA20_SP']){const cells=occupiedDays(payload.observations,product);assert.equal(cells.reduce((n,c)=>n+c.occupied_days,0),aggregateMonth(index,'2024-09',product,s).cells);assert(cells.every(c=>c.occupied_days<=30));}
});
test('regional masks are not the Pantanal bounding box and preserve NRT product identifiers',()=>{
 const row={date_utc:'2026-11-09',latitude:38,longitude:-120,product:'MODIS_NRT'};
 assert.equal(filterObservations([row],'2026-11',{...s,region:'california',mode:'nrt',sensor:'MODIS_SP',bounds:[-125,32,-114,42.5],start:'2026-11-08',end:'2026-11-14'}).length,1);
 assert.equal(filterObservations([row],'2026-11',{...s,start:'2026-11-08',end:'2026-11-14'}).length,0);
});
