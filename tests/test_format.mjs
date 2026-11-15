import test from 'node:test';
import assert from 'node:assert/strict';
import {signed,number} from '../web/format.mjs';
test('unavailable residuals are not presented as signed zero',()=>{
 for(const value of [null,undefined,NaN])assert.equal(signed(value),'—');
 assert.equal(signed(0),'0.0');assert.equal(number(null),'—');assert.equal(signed(-2),'−2.0');
});
import {datasetDefaults} from '../web/url-state.mjs';
import {evaluationPhase} from '../web/model.mjs';
test('defaults use the published domain; missing future adjustment is not missing retrieval',()=>{
 const ref={coverage:{start:'2000-11-01',end:'2026-07-31'},calibration:{accepted:true,period:{start:'2020-01-01',end:'2024-12-31'}}};
 const s=datasetDefaults(ref,'pantanal');assert.equal(s.end,'2024-12-31');assert.equal(s.month,'2024-09');
 const v={train_years:[2020,2021,2022],holdout_years:[2023,2024],accepted:false};assert.equal(evaluationPhase('2023-01',{area:'all',mode:'sp'},v),'Holdout');assert.equal(evaluationPhase('2025-01',{area:'all',mode:'sp'},v),'External evaluation');
 const nrt=datasetDefaults({coverage:{start:'2026-08-01',end:'2026-11-14'}},'siberia','nrt');assert.equal(nrt.start,'2026-11-08');assert.equal(nrt.view,'raw');
});
import {makeIndex,aggregateMonth,aggregateCSV,observationCSV} from '../web/model.mjs';
test('literal source version/type counts follow UTC clipping; type zero is retained',()=>{
 const daily=[{day:'2024-09-01',product:'MODIS_SP',area:'all',native:2,cells:2,source_versions:{'6.03':2},detection_types:{'0':1,'2':1}},{day:'2024-09-02',product:'MODIS_SP',area:'all',native:1,cells:1,source_versions:{'61.03':1},detection_types:{'2':1}}],index=makeIndex({daily}),s={area:'all',sensor:'MODIS_SP',start:'2024-09-02',end:'2024-09-02'};
 assert.deepEqual(aggregateMonth(index,'2024-09','MODIS_SP',s).source_versions,{'61.03':1});
 const csv=observationCSV([{source_version:'6.03',detection_type:'0'}],'sha');assert(csv.includes('"source_version","detection_type"'));assert(csv.endsWith('"6.03","0"'));
});
