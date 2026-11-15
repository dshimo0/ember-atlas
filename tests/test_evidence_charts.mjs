import assert from 'node:assert/strict';
import {activityPlot,diagnosticPlots} from '../web/evidence-charts.mjs';
const chart=activityPlot([{month:'2022-12',phase:'Training',reference:5,viirs:7},{month:'2023-01',phase:'Holdout',reference:null,viirs:null},{month:'2023-02',phase:'Holdout',reference:0,viirs:0}],'raw',{selected:'2023-02'});
assert.match(chart,/data-plot-month="2023-01" aria-label="2023-01 · Data unavailable"/);
assert.match(chart,/2023-02 · MODIS: 0.0 · VIIRS: 0.0/);
assert.doesNotMatch(chart,/NaN|undefined/);
assert.match(chart,/M75,.* M1075,/); // Missing observation breaks a line; zero remains a real point.
const d=diagnosticPlots({rows:[{month:'2023-01',modis:0,viirs:2,adjusted:1,residuals:{unadjusted:2,scalar:null,seasonal:1}}]});assert.doesNotMatch(d,/NaN|undefined/);
