import {loadRelease} from './data-loader.mjs';
import {compareMethods} from './replay.mjs';
import {comparisonPlot} from './evidence-charts.mjs';
import {number,signed} from './format.mjs';
try{
 const release=await loadRelease(),v=release.validation,methods=compareMethods(v),s=v.monthly.find(r=>r.month==='2024-09'),m=methods.metrics;
 document.querySelector('#discoverComparison').innerHTML=comparisonPlot([{name:'MODIS reference',kind:'modis',value:s.modis},{name:'VIIRS · common grid',kind:'viirs',value:s.viirs},{name:'Adjusted VIIRS · MODIS scale',kind:'adjusted',value:s.adjusted}])+`<p>Occupied cell-days · full Pantanal study area. Adjusted VIIRS is ${number(100*(s.adjusted/s.modis-1),1)}% relative to MODIS this month.</p>`;
 document.querySelector('#discoverResult').textContent=`${number(100*(1-m.seasonal.mae/m.unadjusted.mae),1)}% lower monthly MAE against MODIS`;
 document.querySelector('#discoverScope').textContent=`Compared with raw common-grid VIIRS · ${m.unadjusted.n} paired holdout months · ${v.holdout_years.join('–')} · full Pantanal study area. Training: ${v.train_years.join(', ')}.`;
 document.querySelector('#discoverLimit').textContent=`Quarterly signed bias: ${signed(m.seasonal.bias)} cell-days/month. The scalar baseline performs better on this holdout; no replacement is selected using it. MODIS is a reference, not ground truth.`;
 document.querySelector('#discoverMetrics').innerHTML=Object.entries(m).map(([k,x])=>`<div><span>${k==='unadjusted'?'Raw common grid':k==='scalar'?'Training-only scalar':'Frozen quarterly factors'}</span><strong>${number(x.mae,1)}</strong><small>MAE · cell-days/month</small></div>`).join('');
 const rows=v.monthly.filter(r=>v.holdout_years.includes(r.year)),max=Math.max(1,...rows.map(r=>r.modis));
 document.querySelector('#discoverCalendar').innerHTML=`<p>Observed MODIS · occupied cell-days · holdout years</p><div class="preview-months">${rows.map(r=>`<a href="/explore?region=pantanal&month=${r.month}&view=raw&sensor=MODIS_SP" style="--activity:${r.modis/max}" aria-label="${r.month}: ${number(r.modis)} observed MODIS occupied cell-days"><span>${r.month}</span><strong>${number(r.modis)}</strong></a>`).join('')}</div><p>Colour relative to the largest displayed MODIS value. Open a month for retrieval status and source versions.</p>`;
 document.body.dataset.evidence='ready';
}catch(e){document.querySelector('#discoverError').hidden=false;document.body.dataset.evidence='unavailable';}
