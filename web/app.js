import {scenes,sourceCards} from './experience.mjs';
import {replayCutoff,supportsReplay,replayMonth,replayRows,replayBaseline,replayCSV,compareMethods} from './replay.mjs';
import {loadRelease,loadDataset,verifiedJSON,sha256} from './data-loader.mjs';
import {number,signed,yearsLabel,escapeHTML,compact} from './format.mjs';
import {readURL,stateURL,defaultState,datasetDefaults} from './url-state.mjs';
import {evaluateValidation,referenceRows,sensitivitySummary} from './analysis.mjs';
import {activityPlot,diagnosticPlots,comparisonPlot} from './evidence-charts.mjs';
import {createPitch} from './pitch.mjs';
import {createGeographicMap} from './geographic-map.mjs';
import {PRODUCTS, SENSOR_NAMES, AREAS, monthEnd, monthName, monthsBetween, selectedProducts, scope, makeIndex, aggregateMonth, adjustment, historicalBaseline, filterObservations, observationCSV, aggregateCSV,cellCSV,evaluationPhase} from './model.mjs';
const $ = id => document.getElementById(id);
let summary, validation, index, geography, geographicMap, selected = '2024-09', observations = [], selectionToken = 0, loadedSelection = '', ready = false;
const shardCache = new Map();
const state = () => ({region:$('region').value||'pantanal',mode:$('dataMode').value,bounds:summary?.bounds,calibrationAvailable:!!validation?.accepted&&(validation.region||'pantanal')===summary?.region,area: $('area').value, sensor: $('sensor').value, start: $('start').value, end: $('end').value});
let datasetToken=0,currentComparison,externalAudit;
let view='replay',guideStep=1,pitchSlide=1,pitch,release,evaluation,detail='general';
const currentRoute=()=>location.pathname.replace(/\/$/,'')||'/';
const allState=()=>({...state(),month:selected,view,encoding:$('calendarEncoding').value,benchmark:$('showBenchmark').checked,step:guideStep,slide:pitchSlide,detail});
const selectionKey = s => [s.region,s.mode,selected, s.area, s.sensor, s.start, s.end].join('|');
function row(month, product, s = state()) { return aggregateMonth(index, month, product, s); }
function publishedMetrics() {
  const improvement = evaluation.reduction;
  $('validationQuick').innerHTML=`<strong>${validation.accepted&&improvement!==null?number(improvement,1)+'% lower monthly MAE vs raw VIIRS':'Adjustment unavailable'}</strong><span>Against MODIS · ${validation.adjusted.n} holdout months · ${yearsLabel(validation.holdout_years)} · ${release.registry.regions.find(r=>r.id===(validation.region||'pantanal'))?.name||'Pantanal'} full study area, SP</span>`;
  const versions=summary.calibration?.reference_versions;$('referenceVersions').href=summary.source_field_audit?'/data/'+summary.source_field_audit.file:'#methodology';$('referenceVersions').title='Reported training → holdout version labels. Uniform reference processing and isolated sensor effects are unverified.';$('referenceVersions').textContent=versions?`MODIS version: ${Object.keys(versions.training||{}).join(', ')} → ${Object.keys(versions.outer||{}).join(', ')}; continuity unverified.`:'';
  $('improvement').textContent = validation.accepted && improvement !== null ? `${number(improvement, 1)}%` : 'Unavailable';
  $('resultLabel').textContent = validation.accepted ? 'lower monthly MAE against MODIS' : 'Adjustment not supported by this release';
  $('mae').textContent = `${number(validation.unadjusted.mae, 1)} → ${number(validation.adjusted.mae, 1)} cell-days/month`;
  $('split').textContent = `${validation.adjusted.n} holdout months · ${yearsLabel(validation.holdout_years)} · ${release.registry.regions.find(r=>r.id===(validation.region||'pantanal'))?.name||'Pantanal'} SP only`;
  $('validationLink').href = '/data/' + summary.validation.file;
  $('coverage').textContent = `Aggregate and observation coverage: ${summary.coverage.start} → ${summary.coverage.end} UTC`;
  $('validation').textContent = `The ${validation.adjusted.n} matched holdout months in ${yearsLabel(validation.holdout_years)} were excluded from fitting. Training: ${yearsLabel(validation.train_years)}. MAE and signed bias were evaluated against MODIS on the same occupied cell-day scale.`;
  $('bias').textContent = `Signed monthly bias (VIIRS minus MODIS) moved from ${signed(validation.unadjusted.bias)} to ${signed(validation.adjusted.bias)} occupied cell-days. A negative value means the adjusted estimate is lower than MODIS on average. Residuals vary by season; all seasonal results are in the validation JSON.`;
  $('factors').textContent = (validation.selected_method==='scalar'?'Inner-selected scalar (repeated per quarter): ':validation.region?(validation.selected_method==='seasonal'?'Inner-selected quarter factors: ':'Regional fit unavailable: '):'Frozen quarter factors (VIIRS → MODIS reference): ') + Object.entries(validation.factors).map(([q, f]) => `Q${+q + 1}: ${number(f, 4)}`).join(' · ') + '.';
  $('provenance').textContent = `Snapshot ${summary.snapshot.file}; SHA-256 ${summary.snapshot.sha256}. ${number(summary.observation_count)} observations, ${summary.manifest_count} raw window manifests. Built ${summary.built_utc}. UI aggregates and monthly observation shards are checksum-verified derivatives of this same snapshot. Both export types cover the same released dates.`;
  $('evidenceLinks').innerHTML = `<a href="/data/${summary.validation.file}">Versioned validation JSON →</a><a href="/data/${summary.snapshot.file}">Original pinned snapshot →</a><a href="/data/monthly_comparison.csv">Full-area monthly evidence CSV →</a><a href="/data/diagnostics.json">Sensitivity diagnostics →</a><a href="/data/dashboard.json">UI provenance index →</a>`;
}
function calendar(s) {
  const months = monthsBetween(s.start, s.end), byYear = new Map();
  for (const m of months) { const y = m.slice(0, 4); if (!byYear.has(y)) byYear.set(y, []); byYear.get(y).push(m); }
  const header = ['<div class="calendar-corner"></div>', ...Array.from({length: 12}, (_, i) => `<div class="month-header">${new Date(Date.UTC(2024, i, 1)).toLocaleDateString('en-US', {month: 'short', timeZone: 'UTC'})}</div>`)];
  const selectedSensors = selectedProducts(s.sensor,s.mode);
  const activityMax=Math.max(1,...months.flatMap(m=>{if(view==='replay'&&supportsReplay(s))return[replayMonth(index,m,s,validation).value??0];if(view==='reference')return[adjustment(row(m,'VIIRS_NOAA20_SP',s),s,validation)?.value??0];return selectedSensors.map(p=>row(m,p,s).cells??0);}));
  for (const [year, available] of byYear) {
    const phase=evaluationPhase(year+'-01',s,validation);
    header.push(`<div class="calendar-year"><div class="year-label"><strong>${year}</strong><small>${phase}</small></div>`);
    for (let n = 1; n <= 12; n++) {
      const m = `${year}-${String(n).padStart(2, '0')}`;
      if (!available.includes(m)) { header.push('<div class="calendar-spacer"></div>'); continue; }
      const original = selectedSensors.map(p => row(m,p,s));
      const ref=view==='reference'&&s.area==='all';
      const viirs=row(m,'VIIRS_NOAA20_SP',s),a=adjustment(viirs,s,validation),replayed=replayMonth(index,m,s,validation);
      const replay=view==='replay'&&supportsReplay(s);
      const values=replay?[{...replayed,cells:replayed.value,product:replayed.source}]:ref?[{...viirs,cells:a?.value??null,product:'VIIRS_NOAA20_SP'}]:original;
      const unavailable = values.every(r => !r.retrieved), partial = !unavailable && values.some(r => !r.complete);
      const unsupported=!unavailable&&!partial&&values.every(v=>v.cells===null);
      const symbol = unavailable ? '—' : partial ? '◐' : unsupported?'⊘':'✓';
      const baselines=values.map(v=>{const b=replay?replayBaseline(index,m,s,validation):historicalBaseline(index,m,v.product,s,validation);return ref&&b&&a?{...b,median:b.median*a.factor,entries:b.entries.map(e=>({...e,value:e.value*a.factor}))}:b;});
      const anomaly=$('calendarEncoding').value==='anomaly';
      const validBaseline=!partial&&!unsupported&&baselines.every(b=>b&&b.percent!==null);
      const delta=validBaseline?baselines.reduce((sum,b)=>sum+b.percent,0)/baselines.length:null;
      const baselineLabel=anomaly?' '+baselines.map((b,i)=>`${values[i].product}: ${b?`earlier median ${number(b.median,1)} cell-days; years ${yearsLabel(b.entries.map(e=>e.year))}; n=${b.n}; difference ${b.percent===null?'undefined (zero median)':signed(b.percent)+'%'}`:'historical baseline unavailable'}`).join('. '):'';
      const label = `${monthName(m)}. ${phase}. ${values.map(v => `${replay?SENSOR_NAMES[v.product]+' · '+replayed.adjustment:ref?'Adjusted VIIRS':SENSOR_NAMES[v.product]}: ${v.cells === null ? (v.retrieved?'Adjustment unavailable; source data retrieved':'Data unavailable') : `${number(v.cells,v.cells%1?1:0)} cell-days, ${v.status}`}`).join('. ')}${baselineLabel}`;
      header.push(`<button class="month ${anomaly?'anomaly-month':''} ${unavailable ? 'missing' : partial ? 'partial' : ''}" data-month="${m}" data-source="${replay?replayed.source:values.map(v=>v.product).join(',')}" data-adjustment="${replay?replayed.adjustment:ref?(validation.selected_method||'frozen seasonal'):'none'}" title="${label}" style="${anomaly?`--anomaly-color:${delta===null?'var(--soft)':delta<0?'#236a91':delta>0?'#9b4c27':'var(--soft)'};`: ""}--activity:${Math.max(0,...values.map(v=>(v.cells??0)/activityMax))}" aria-label="${label}" aria-pressed="${m === selected}"><em class="mobile-month">${new Date(m+'-01T00:00:00Z').toLocaleDateString('en-US',{month:'short',timeZone:'UTC'})}</em>${values.map(v => `<span class="${replay?(replayed.source==='MODIS_SP'?'m':'a'):ref?'a':v.product.startsWith('MODIS')?'m':'v'}">${replay?(replayed.source==='MODIS_SP'?'○ M':'▲ A'):ref?'▲ A':v.product.startsWith('MODIS')?'○ M':'◇ V'} <b>${compact(v.cells)}</b></span>`).join('')}${anomaly?`<small class="anomaly-value">${delta===null?'— baseline':signed(delta)+'%'}</small>`:''}<span class="coverage-symbol" aria-hidden="true">${symbol}</span></button>`);
    }
    header.push('</div>');
  }
  $('calendar').innerHTML = header.join('');
  $('calendarEncodingNote').textContent=$('calendarEncoding').value==='anomaly'?'Colour: blue below, brown above the earlier same-month median; neutral means no supported baseline or equal activity. Raw multi-sensor cells use the mean of supported sensor percentage differences; individual baselines are in each month tooltip. At least three complete prior years; zero medians have no percentage. Adjusted-only values use their own sensor baseline on the same seasonal scale.':'Colour: activity relative to the largest displayed monthly value. Values and source products remain inspectable.';
  document.querySelector('.calendar-scale').hidden=$('calendarEncoding').value==='anomaly';
  for (const button of $('calendar').querySelectorAll('[data-month]')) {
    button.addEventListener('click', () => { selected = button.dataset.month; commitSelection(); $('calendar').querySelector(`[data-month="${selected}"]`)?.focus({preventScroll: true}); });
    button.addEventListener('keydown', event => {
      const columns = matchMedia('(max-width:700px)').matches ? 4 : 12;
      const delta = {ArrowRight: 1, ArrowLeft: -1, ArrowDown: columns, ArrowUp: -columns}[event.key];
      if (!delta) return;
      event.preventDefault(); const buttons = [...$('calendar').querySelectorAll('[data-month]')], i = buttons.indexOf(button);
      buttons[Math.max(0, Math.min(buttons.length - 1, i + delta))].focus();
    });
  }
}
function baselineView(s, values) {
  if(view==='replay'&&supportsReplay(s)){
   const r=replayMonth(index,selected,s,validation),b=replayBaseline(index,selected,s,validation);
   $('findingTitle').textContent='Earlier reported activity';
   $('takeaway').textContent=b?`${monthName(selected)}: reference-scale activity is ${b.percent===null?number(Math.abs(b.difference),1)+' cell-days':number(Math.abs(b.percent),1)+'%'} ${b.difference>=0?'above':'below'} its earlier same-month median (${yearsLabel(b.entries.map(e=>e.year))}, n = ${b.n}).`:r.complete&&r.value===null?'No published reference-scale adjustment is available for this month. Raw observations remain available.':'Reference-scale historical comparison requires a complete selected month and at least three complete earlier same-month values.';
   $('baseline').innerHTML=b?`<div class="baseline-row"><strong>${number(r.value,1)} vs median ${number(b.median,1)} cell-days</strong><p>${signed(b.difference)} cell-days · ${b.n} complete prior months. Earlier complete matched-domain months only (${Math.min(...validation.train_years)}–${validation.publication_domain?.end.slice(0,4)||'2024'}); older MODIS is archive context. Missing/partial periods excluded.</p><details><summary>Baseline ${yearsLabel(b.entries.map(e=>e.year))} · n = ${b.n} · sources</summary>${b.entries.map(e=>`${e.year}: ${number(e.value,1)} · ${e.source} · ${e.adjustment} · versions ${Object.keys(e.source_versions||{}).map(escapeHTML).join(', ')||'not provided'}`).join('<br>')}</details></div>`:'<p>Incomplete months and unavailable reference-scale values are excluded. No later years are used.</p>';
   return;
  }
  $('findingTitle').textContent='Historical comparison · within-sensor observations';

  const baselines = values.map(v => ({...v, baseline: historicalBaseline(index, selected, v.product, s, validation)}));
  const valid = baselines.every(v => v.baseline);
  if (valid) {
    const allAbove = baselines.every(v => v.baseline.difference > 0), allBelow = baselines.every(v => v.baseline.difference < 0);
    const sameBaseline=baselines.every(v=>JSON.stringify(v.baseline.entries.map(e=>e.year))===JSON.stringify(baselines[0].baseline.entries.map(e=>e.year)));
    const years = yearsLabel(baselines[0].baseline.entries.map(e => e.year));
    const calendarMonth = new Date(selected+'-01T00:00:00Z').toLocaleDateString('en-US',{month:'long',timeZone:'UTC'});
    const subject = baselines.length === 2 ? 'both sensors' : SENSOR_NAMES[baselines[0].product];
    const direction = allAbove ? 'above' : allBelow ? 'below' : 'at different levels relative to';
    $('takeaway').textContent = `${monthName(selected)}: ${subject} recorded activity ${direction} ${sameBaseline?'the '+years+' '+calendarMonth+' median'+(baselines.length===2?'s':'')+' (n = '+baselines[0].baseline.n+')':'their respective earlier '+calendarMonth+' medians; years and sample sizes are listed below'}.`;
  } else {
    $('takeaway').textContent = values.some(v => !v.complete) ? 'Historical comparison unavailable for a partial or missing month.' : 'Historical comparison requires at least three complete prior years.';
  }
  $('baseline').innerHTML = baselines.map(v => {
    const b = v.baseline, name = SENSOR_NAMES[v.product], mark = v.product.startsWith('MODIS') ? 'modis' : 'viirs';
    return `<div class="baseline-row"><div><span><i class="mark ${mark}" aria-hidden="true"></i>${name}</span><strong>${b && b.percent !== null ? signed(b.percent, 1) + '%' : '—'}</strong></div>${b ? `<p>${number(v.cells)} cell-days vs median <b>${number(b.median, b.median % 1 ? 1 : 0)}</b> · ${signed(b.difference, 0)} cell-days</p><details><summary>Baseline ${yearsLabel(b.entries.map(e => e.year))} · n = ${b.n} prior years</summary><div class="baseline-values">${b.entries.map(e => `${e.year}: ${number(e.value)} cell-days`).join('<br>')}<br>Selected year excluded.</div></details>` : `<p>${v.status}; ${v.retrieved}/${v.expected} selected UTC days retrieved. Baseline unavailable.</p>`}</div>`;
  }).join('');
}
function comparison(s, values) {
  const v = row(selected, s.mode==='nrt'?'VIIRS_NOAA20_NRT':'VIIRS_NOAA20_SP', s), m = row(selected, s.mode==='nrt'?'MODIS_NRT':'MODIS_SP', s), a = adjustment(v, s, validation);
  const series = values.map(r => ({name: SENSOR_NAMES[r.product] + (r.product.startsWith('MODIS') ? ' · reference' : ' · common grid'), value: r.cells, kind: r.product.startsWith('MODIS') ? 'modis' : 'viirs'}));
  if (s.sensor !== 'MODIS_SP' && a) series.push({name: 'Adjusted VIIRS · MODIS reference', value: a.value, kind: 'adjusted'});
  $('comparison').innerHTML=comparisonPlot(series);
  if (a && m.complete && s.sensor !== 'MODIS_SP') {
    const delta = a.value - m.cells, pct = m.cells ? 100 * delta / m.cells : null;
    $('adjusted').textContent = `Adjusted VIIRS is ${number(Math.abs(delta), 1)} cell-days ${delta < 0 ? 'below' : 'above'} MODIS${pct !== null ? ` (${signed(pct)}%)` : ''} this month.`;
  } else $('adjusted').textContent = 'Adjustment unavailable for this selection.';
  $('scopeNotice').classList.toggle('warning', !supportsReplay(s));
  $('scopeNotice').textContent = !supportsReplay(s) ? 'Adjustment unavailable: the selected processing level, region or mask has no published adjustment.' : !v.complete ? 'No adjustment for a partial or missing month.' : s.sensor === 'MODIS_SP' ? 'MODIS reference observations.' : a ? `${validation.selected_method==='scalar'?'Scalar':'Quarter'} factor ${number(a.factor, 4)} · Training ${yearsLabel(validation.train_years)}` : 'Adjustment unavailable: this month is outside the accepted validation domain.';
  $('nativeCounts').innerHTML = `<table><thead><tr><th>Product</th><th>Native detections</th><th>Retrieval</th></tr></thead><tbody>${values.map(r => `<tr><th>${SENSOR_NAMES[r.product]}</th><td>${number(r.native)}</td><td>${r.status}<br>${r.retrieved}/${r.expected} days</td></tr>`).join('')}</tbody></table>`;
  $('sourceFlags').innerHTML=values.map(r=>`<p><strong>${SENSOR_NAMES[r.product]}</strong><br>Literal version / native detections: ${Object.entries(r.source_versions).map(([v,n])=>escapeHTML(v)+': '+number(n)).join('; ')||'No record-level value'}<br>Reported type / native detections: ${Object.entries(r.detection_types).map(([v,n])=>escapeHTML(v)+': '+number(n)).join('; ')||'No record-level value'}</p>`).join('')+'<p>All reported thermal types are included. Counts by type describe native records, not shares of occupied cell-days. Source-version and type transitions are not independently harmonized. The MODIS comparison reference is the SP archive as delivered.</p>';
}
function map(s, rows = []) {
  if (!geographicMap) return;
  document.querySelector('.occupancy-key').hidden=loadedSelection!==selectionKey(s);
  const shown = geographicMap.update(rows, {...s, month:selected,retrieved_products:loadedSelection===selectionKey(s)?selectedProducts('both',s.mode).filter(p=>row(selected,p,s).retrieved>0):[],period_days:Math.round((Date.parse(scope(selected,s).to)-Date.parse(scope(selected,s).from))/86400000)+1,mapProduct:$('mapProduct').value});
  $('mapMonth').textContent = `${monthName(selected)} · ${s.area === 'all' ? summary.name+' study area' : AREAS[s.area]}`;

}
async function monthObservations(month) {
  if (!summary.observation_shards[month]) return [];
  const ref=summary.observation_shards[month],cacheKey=ref.file;
  if (!shardCache.has(cacheKey)) {
    shardCache.set(cacheKey, verifiedJSON(summary.observation_shards[month], true).then(data => {
      if (data.snapshot_sha256 !== (ref.dataset_sha256||summary.snapshot.sha256) || data.month !== month) throw new Error('Observation provenance mismatch');
      return data.observations;
    }).catch(error => { shardCache.delete(cacheKey); throw error; }));
    while (shardCache.size > 2) shardCache.delete(shardCache.keys().next().value);
  }
  return shardCache.get(cacheKey);
}
async function loadObservations(s, values) {
  const token = ++selectionToken, key = selectionKey(s), month = selected;
  loadedSelection = ''; observations = []; $('download').disabled = true; $('downloadCells').disabled=true; $('downloadManifest').disabled=true;
  $('download').textContent = `Download ${monthName(month)} observations`;
  $('mapLoading').textContent='Loading observations…';$('gridLegend').textContent='Loading selected sensor occupancy…';map(s);
  if (!values.some(v => v.retrieved)) {
    $('mapLoading').textContent='No retrieval for this selection.';$('gridLegend').textContent='Occupied days unavailable: no retrieval in the selected UTC scope.';
    $('observationScope').textContent = 'Observation export unavailable: no retrieved data for this month.';
    $('downloadManifest').disabled=false;
    return;
  }
  try {
    const all = await monthObservations(month);
    if (token !== selectionToken) return;
    observations = filterObservations(all, month, s); loadedSelection = key;
    const expected = values.reduce((n, v) => n + (v.native ?? 0), 0);
    if (observations.length !== expected) throw new Error('Selected observations do not match released aggregates');
    $('download').disabled = !values.some(v => v.retrieved);$('downloadCells').disabled=$('download').disabled;
    $('downloadManifest').disabled=false;
    $('observationScope').textContent = `${month} · ${scope(month, s).from} → ${scope(month, s).to} UTC · ${number(observations.length)} records · selected area & sensors`;
    map(s, observations);
  } catch (error) {
    if (token !== selectionToken) return;
    $('mapLoading').textContent = 'Observation file unavailable. Aggregate data remain available.';
    $('gridLegend').textContent='Occupancy unavailable: the observation file could not be loaded.';$('downloadManifest').disabled=false;
    $('observationScope').textContent = 'Observation export unavailable.';
  }
}
function render() {
  if (!ready) return;
  const s = state();
  if (!s.start || !s.end || s.start > s.end || (Date.parse(s.end)-Date.parse(s.start))/86400000>12000) {
    $('error').hidden = false; $('error').textContent = 'Choose a valid date range with the end on or after the start. The previous view remains visible; downloads are disabled.';
    $('download').disabled=true;$('downloadCells').disabled=true;$('downloadReplay').disabled=true;$('aggregateDownload').disabled=true;$('downloadManifest').disabled=true; selectionToken++; return;
  }
  $('error').hidden = true;
  if (selected < s.start.slice(0, 7) || selected > s.end.slice(0, 7)) selected = s.start.slice(0, 7);
  const values = selectedProducts(s.sensor,s.mode).map(p => row(selected, p, s)), available = values.some(v => v.retrieved), count = values.reduce((n, v) => n + (v.native ?? 0), 0), dates = scope(selected, s);
  $('monthTitle').textContent = monthName(selected);
  $('monthPhase').textContent=evaluationPhase(selected,s,validation);
  $('status').textContent = available ? `${count === 0 ? 'No detections recorded · ' : ''}${number(count)} observations · ${values.every(v => v.complete) ? 'Complete monthly retrieval' : 'Partial month / mixed retrieval'}` : 'Data unavailable · no retrieval for the selected month';
  $('selection').innerHTML = `<span>Month <strong>${monthName(selected)}</strong></span><span>Area <strong>${s.area==='all'?summary.name+' study area':AREAS[s.area]}</strong></span><span>Sensor <strong>${s.sensor === 'both' ? 'Both sensors' : SENSOR_NAMES[s.sensor]}</strong></span><span>Records <strong>${available ? number(count) : 'Unavailable'}</strong></span><span>UTC <strong>${dates.from} → ${dates.to}</strong></span>`;
  if(!supportsReplay(s)||s.sensor==='MODIS_SP')view='raw';
  if(view==='replay'&&s.sensor!=='both')view='reference';
  $('calendarView').value=view; $('calendarView').querySelector('[value=reference]').disabled=!supportsReplay(s)||s.sensor==='MODIS_SP'; $('calendarView').querySelector('[value=replay]').disabled=!supportsReplay(s)||s.sensor!=='both';
  if(s.sensor!=='both')$('mapProduct').value=s.sensor;
  else if(view==='replay')$('mapProduct').value=selected<replayCutoff(validation)?'MODIS_SP':'VIIRS_NOAA20_SP';
  for(const o of $('mapProduct').options)o.disabled=s.sensor!=='both'&&o.value!==s.sensor;
  $('monthSelect').innerHTML=monthsBetween(s.start,s.end).map(m=>`<option value="${m}" ${m===selected?'selected':''}>${monthName(m)}</option>`).join('');
  datasetLabels();replayView(s);baselineView(s, values); comparison(s, values); calendar(s); historyView(s); guideView();experienceView(s);
  $('aggregateDownload').disabled = false;
  $('aggregateScope').textContent = `${s.start} → ${s.end} UTC · ${monthsBetween(s.start, s.end).length} months · selected area & sensors · missing values stay blank`;
  if(['/', '/demo'].includes(currentRoute()))loadObservations(s, values);
}
function datasetLabels(){
 const r=release.registry.regions.find(r=>r.id===state().region),mode=state().mode;
 $('pageTitle').textContent=currentRoute()==='/demo'?'Explore fire activity across sensors':`${r.name} fire activity`;
 $('pageSubtitle').textContent=mode==='nrt'?'NASA FIRMS · Recent detections (NRT), separate from the Standard Processing archive':'NASA FIRMS · Standard Processing archive';
 $('datasetSummary').textContent=`${mode.toUpperCase()} coverage ${summary.coverage.start}–${summary.coverage.end} UTC · data details`;
 $('datasetCoverage').textContent=`${mode.toUpperCase()} retrieved acquisition dates: ${summary.coverage.start} → ${summary.coverage.end} UTC · ${Object.entries(summary.product_coverage).map(([p,c])=>p+': '+c.start+' → '+c.end+' ('+number(c.retrieved_days)+' retrieved UTC days)').join('; ')} · last retrieval ${summary.built_utc}. Usable satellite observation coverage: unknown.`;
 $('mapBounds').textContent=`Study bounds W/S/E/N: ${r.bounds.join(', ')} · WGS84 rectangle; not a biome mask.`;
 $('extent').textContent=`${r.name} study area · W/S/E/N ${r.bounds.join(', ')} (WGS84). ${r.extent_note}`;
 $('coverage').textContent=`Available ${mode.toUpperCase()} archive: ${summary.coverage.start} → ${summary.coverage.end} UTC; missing retrievals remain blank.`;
 $('area').querySelector('[value=all]').textContent=r.name+' study area';
 for(const option of $('area').querySelectorAll('option:not([value=all])'))option.disabled=r.id!=='pantanal';
 $('provenance').textContent=`Dataset ${summary.snapshot.file}; SHA-256 ${summary.snapshot.sha256}. ${number(summary.observation_count)} observations; ${summary.manifest_count} source manifests. Product coverage and retrieval inventory are linked below. Observation coverage remains unknown.`;
 $('evidenceLinks').innerHTML=`<a href="/data/${summary.snapshot.file}">Selected dataset manifests</a><a href="/data/${release.registryRef.file}">Versioned region registry</a><a href="/data/${summary.validation.file}">SP calibration evidence</a>${summary.source_field_audit?`<a href="/data/${summary.source_field_audit.file}">Source-version split and native type audit</a>`:''}<a href="/data/${(summary.comparison||release.replayRef).file}">Three-method evaluation</a><a href="/data/${summary.residual_csv?.file||'replay-residuals.csv'}">${summary.residual_csv?'Selected-region SP candidate residual CSV':'Pantanal holdout residual CSV'}</a>`;
 $('validationLink').href='/data/'+(summary.comparison||summary.validation).file;
 $('processingTransition').innerHTML=`<p>${release.transitionAudit.status}. SP/NRT joining is disabled.</p><ul>${release.transitionAudit.sensors.map(x=>`<li>${x.sensor}: SP ends ${x.sp_end}; NRT starts ${x.nrt_start}; ${x.overlap_days} overlapping acquisition days.</li>`).join('')}</ul><p>${release.transitionAudit.unblock}</p><a href="/data/${release.transitionRef.file}">Versioned availability audit</a>`;
}
function replayView(s){
 const available=supportsReplay(s),r=replayMonth(index,selected,s,validation);
 $('replayIntro').hidden=!available||view!=='replay';
 $('replayDescription').textContent=`Scenario cutoff ${replayCutoff(validation)}: observed MODIS → ${validation.selected_method==='scalar'?'scalar-adjusted':'seasonally adjusted'} VIIRS. Observed MODIS continues and can be revealed as a holdout benchmark.`;
 $('selectedSource').textContent=available&&view==='replay'?`Replay: ${r.month<r.cutoff?'observed MODIS':'adjusted NOAA-20 VIIRS'} · cutoff ${r.cutoff}`:'';
 $('replaySource').textContent=`${monthName(selected)} · source ${r.source} · ${r.adjustment}${r.factor!==null?' · factor '+number(r.factor,4):''} · ${r.status}. Units: occupied cell-days.`;
 $('downloadReplay').disabled=!available||view!=='replay';
}
function download(text, filename) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: filename.endsWith('.json')?'application/json':'text/csv;charset=utf-8'})); a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); }
$('download').addEventListener('click', () => { const s = state(); if (loadedSelection !== selectionKey(s)) return; download(observationCSV(observations, summary.snapshot.sha256), `ember-observations-${s.region}-${s.mode}-${scope(selected,s).from}_${scope(selected,s).to}-${s.area}-${s.sensor}.csv`); });
$('aggregateDownload').addEventListener('click', () => { const s = state(); download(aggregateCSV(index, s, validation, summary.snapshot.sha256), `ember-aggregates-${s.region}-${s.mode}-${s.start}_${s.end}-${s.area}-${s.sensor}.csv`); });
function historyView(s) {
 if(view==='replay'&&supportsReplay(s)){
 const rows=replayRows(index,s,validation);
 $('referenceScope').textContent=`Replay scenario · cutoff ${replayCutoff(validation)} · MODIS before; adjusted VIIRS after. Simulated transition, not actual source availability. Older MODIS is observed archive context; calibration publication ends ${validation.publication_domain?.end||'2024-12-31'}.`;
 $('timeSeries').innerHTML=activityPlot(rows.map(r=>({...r,replay_modis:r.source==='MODIS_SP'?r.value:null,replay_adjusted:r.source==='VIIRS_NOAA20_SP'?r.value:null,benchmark:$('showBenchmark').checked?r.benchmark:null})), 'replay',{cutoff:replayCutoff(validation),selected});
 $('seriesLegend').innerHTML='<span>○ Observed MODIS before cutoff</span><span>▲ Adjusted VIIRS after cutoff</span><span>Dashed: observed holdout MODIS benchmark (optional)</span>';
 $('seriesTable').innerHTML=`<table><thead><tr><th>Month / split</th><th>Source</th><th>Adjustment / factor</th><th>Reported source versions</th><th>Cell-days</th><th>Retrieval</th></tr></thead><tbody>${rows.map(r=>`<tr><th>${r.month} · ${r.phase}</th><td>${r.source}</td><td>${r.adjustment} / ${number(r.factor,4)}</td><td>${Object.keys(r.source_versions||{}).map(escapeHTML).join(", ")||"Not provided"}</td><td>${number(r.value,1)}</td><td>${r.retrieved}/${r.expected} days · ${r.status}</td></tr>`).join('')}</tbody></table>`;return;}
 const rows=referenceRows(index,s,validation);
 $('referenceScope').textContent=s.mode==='nrt'?'Recent detections in the selected partial UTC window. NRT and Standard Processing are not joined; historical comparison requires independent evaluation.':s.area==='all'?(view==='reference'?'Adjusted VIIRS on the MODIS-reference scale · complete months · full study rectangle. Separate MODIS reference; no fused record or source transition.':'Unadjusted sensor-specific activity on the common grid.'):'Regional sensor history. Full-area calibration is unavailable here; historical medians use each product’s own regional mask.';
 $('timeSeries').innerHTML=activityPlot(rows,view,{selected});
 $('seriesLegend').innerHTML=(s.sensor!=='VIIRS_NOAA20_SP'?'<span>○ MODIS reference (dashed)</span>':'')+(s.sensor!=='MODIS_SP'?`<span>${view==='reference'?'▲ Adjusted VIIRS':'◇ VIIRS common grid'} (solid)</span>`:'');
 $('seriesTable').innerHTML=`<table><thead><tr><th>Month / split</th><th>MODIS cell-days</th><th>VIIRS cell-days</th><th>Adjusted VIIRS</th><th>Adjustment status</th><th>MODIS / VIIRS reported versions</th></tr></thead><tbody>${rows.map(r=>`<tr><th>${r.month} · ${r.phase}</th><td>${number(r.reference)}</td><td>${number(r.viirs)}</td><td>${number(r.adjusted,1)}</td><td>${r.status}</td><td>${Object.keys(r.reference_versions||{}).map(escapeHTML).join(", ")||"—"} / ${Object.keys(r.viirs_versions||{}).map(escapeHTML).join(", ")||"—"}</td></tr>`).join('')}</tbody></table><p class="unit">Source products: ${summary.products.join(' / ')}. Raw values cover the selected UTC dates; partial windows are labeled. No SP/NRT join. Adjustment is unavailable for partial or unsupported periods.</p>`;
}
function residualView() {
 const e=evaluation,methods=compareMethods(validation),artifact=currentComparison||release.replayEvaluation,calibrationName=release.registry.regions.find(r=>r.id===(validation.region||'pantanal'))?.name||'Pantanal';
 $('diagnosticPlots').innerHTML=diagnosticPlots(methods);
 $('methodsPage').querySelector('.methods-intro').after($('diagnosticPlots'));
 for(const k of ['unadjusted','scalar','seasonal'])for(const field of ['mae','bias','n'])if(Math.abs(methods.metrics[k][field]-artifact.metrics[k][field])>1e-7)throw new Error('Three-method evidence mismatch');
 $('scalarSummary').textContent=`Scalar MAE ${number(methods.metrics.scalar.mae,1)} vs seasonal ${number(methods.metrics.seasonal.mae,1)}; ${validation.selected_method?'inner-selected '+validation.selected_method:validation.region?'regional selection unavailable':'frozen method retained'}.`;
 $('methodComparison').innerHTML=`<table class="method-table"><caption>Identical ${methods.metrics.unadjusted.n} complete paired holdout months · ${calibrationName} study area · occupied cell-days/month</caption><thead><tr><th>Method</th><th>MAE</th><th>Signed bias</th></tr></thead><tbody>${Object.entries(methods.metrics).map(([k,m])=>`<tr data-method="${k}"><th>${k==='unadjusted'?'Unadjusted common-grid VIIRS':k==='scalar'?'Training-only single scalar':'Quarterly training factors'}</th><td>${number(m.mae,1)}</td><td>${signed(m.bias)}</td></tr>`).join('')}</tbody></table><p>Scalar ${number(methods.scalar,6)} minimizes training sum of squared monthly residuals through the origin. Fit only on 2020–2022. ${validation.region&&!validation.selected_method?"Inner selection is unavailable until 24 inner-fit and 12 selection months are complete. No adjustment is published.":validation.selected_method?"The method was chosen using 2022 only, after fitting 2020–2021, and refitted on 2020–2022. Outer and external results cannot switch this choice.":"It is an evaluation baseline; the Pantanal seasonal publication rule is unchanged. Future method selection requires separate evaluation."}</p>`;
 $('peakComparison').textContent=`Peak stress test: six holdout months ranked by observed MODIS activity (${methods.peak_months.join(', ')}), never by residual. MAE / bias: unadjusted ${number(methods.peak_metrics.unadjusted.mae,1)} / ${signed(methods.peak_metrics.unadjusted.bias)}; scalar ${number(methods.peak_metrics.scalar.mae,1)} / ${signed(methods.peak_metrics.scalar.bias)}; seasonal ${number(methods.peak_metrics.seasonal.mae,1)} / ${signed(methods.peak_metrics.seasonal.bias)} cell-days/month.`;
 $('residualSummary').textContent=!e.after.n?'No complete inner selection is available. Only unadjusted bars are shown; candidate diagnostics do not establish a publishable fit.':`Holdout bias ${signed(e.before.bias)} → ${signed(e.after.bias)}; RMSE ${number(e.before.rmse,1)} → ${number(e.after.rmse,1)} cell-days/month. ${e.underperforming.length} of ${e.rows.length} months have larger absolute residual after adjustment (${e.underperforming.map(r=>r.month).join(', ')}). Positive residuals mean VIIRS exceeds MODIS. This SP validation is for the full ${validation.region||'pantanal'} study area only.`;
 const max=Math.max(1,...e.rows.flatMap(r=>[Math.abs(r.before||0),Math.abs(r.after||0)])),x=v=>450+v/max*400;
 $('residualChart').innerHTML=`<svg class="residual-svg" viewBox="0 0 920 ${e.rows.length*20+28}" role="img" aria-label="Monthly holdout residuals in occupied cell-days; cyan unadjusted, purple adjusted; left of zero is below MODIS"><path d="M450 0V${e.rows.length*20}" stroke="#aebdb7"/>${e.rows.map((r,i)=>`<text x="0" y="${i*20+14}" fill="#b4c2bd" font-size="11">${r.month}${r.underperforms?' *':''}</text>${[['before','#86d6d1'],['after','#c8b5ed']].map(([k,c],j)=>r[k]===null?'':`<rect x="${Math.min(450,x(r[k]))}" y="${i*20+j*7+2}" width="${Math.max(1,Math.abs(x(r[k])-450))}" height="5" fill="${c}"><title>${r.month}: ${k} ${number(r[k],1)} cell-days</title></rect>`).join('')}`).join('')}<text x="260" y="${e.rows.length*20+19}" fill="#b4c2bd" font-size="11">Below MODIS ← 0 → Above MODIS · cyan unadjusted / purple adjusted · * underperforms</text></svg>`;
 $('residualTable').innerHTML=`<table><thead><tr><th>Month</th><th>MODIS benchmark</th><th>Unadjusted residual</th><th>Scalar residual</th><th>Seasonal residual</th></tr></thead><tbody>${methods.rows.map(r=>`<tr><th><a data-route href="${stateURL('/demo',{...allState(),month:r.month,view:supportsReplay(state())?'replay':'raw',benchmark:true})}">${r.month}</a></th><td>${number(r.modis)}</td><td>${signed(r.residuals.unadjusted)}</td><td>${signed(r.residuals.scalar)}</td><td>${signed(r.residuals.seasonal)}</td></tr>`).join('')}</tbody></table>`;
 const sensitivity=sensitivitySummary(release.diagnostics);
 $('sensitivity').parentElement.hidden=summary.region!=='pantanal';
 $('sensitivity').innerHTML=`<p>Descriptive count sensitivity for the original paired Pantanal 2020–2024 release only; no alternate calibration was selected on holdout.</p><table><thead><tr><th>Product</th><th>0.025° vs 0.05°</th><th>0.1° vs 0.05°</th><th>High-confidence share at 0.05°</th></tr></thead><tbody>${sensitivity.map(r=>`<tr><th>${SENSOR_NAMES[r.product]}</th><td>${signed(r.finerPercent)}%</td><td>${signed(r.coarserPercent)}%</td><td>${number(r.highConfidencePercent,1)}%</td></tr>`).join('')}</tbody></table><p>High confidence: MODIS ≥80; VIIRS h. Thresholds are sensor-specific. Cell-area latitude dependence, timing and cloud effects remain.</p>`;
}
function externalView(){
 const panel=$('externalEvidence');panel.hidden=!externalAudit;
 const scope=release.registry.regions.find(r=>r.id===(validation.region||'pantanal'))?.name||'Pantanal';
 $('residualSection').querySelector('h2').textContent=scope+' SP validation: three methods';
 $('methodContract').textContent=validation.region?'Regional selection uses 2022 after fitting 2020–2021, then refits on 2020–2022. Publication requires complete support and lower MAE with no worse absolute bias on 2023–2024, on those years excluding the previously published September 2024, and on January 2025–July 2026. MODIS is a comparison reference, not ground truth. Full study area and complete SP months only.': 'The frozen Pantanal rule requires lower monthly MAE and no worse absolute signed bias on 24 holdout months in 2023–2024 after fitting 36 months in 2020–2022. The publication domain remains 2020–2024, full study area and complete SP months only. MODIS is a comparison reference, not ground truth.';
 if(!externalAudit)return;const a=externalAudit,metrics=a.partitions.external;
 panel.innerHTML=`<h3>New out-of-time evidence · ${summary.name}</h3><p>January 2025–July 2026 · ${metrics.unadjusted.n} complete paired SP months · excluded from fitting and method selection.</p><table><thead><tr><th>Method</th><th>MAE</th><th>Signed bias</th></tr></thead><tbody>${Object.entries(metrics).map(([name,m])=>`<tr><th>${name}</th><td>${number(m.mae,1)}</td><td>${signed(m.bias)}</td></tr>`).join('')}</tbody></table><p>Complete paired support: ${a.monthly.filter(r=>a.train_years.includes(r.year)).length}/36 training months; ${a.selection.metrics.scalar.n}/12 inner-selection months; ${a.partitions.outer.unadjusted.n}/24 outer months; ${metrics.unadjusted.n}/19 fresh months.</p><p>Inner selection: ${a.selected_method||'unavailable (incomplete inner support)'}, using 2022 after fitting 2020–2021. Publication: ${a.accepted?'all regional gates passed':a.reason}. Gate results: ${Object.entries(a.gates).map(([k,p])=>k+': '+(p?'passed':'failed')).join('; ')}.</p><details><summary>All external monthly residuals</summary><table><thead><tr><th>Month</th><th>Unadjusted</th><th>Scalar</th><th>Quarterly</th></tr></thead><tbody>${a.residuals.external.map(r=>`<tr><th>${r.month}</th><td>${signed(r.residuals.unadjusted)}</td><td>${signed(r.residuals.scalar)}</td><td>${signed(r.residuals.seasonal)}</td></tr>`).join('')}</tbody></table></details><p><a href="/data/${summary.external_audit.file}">Versioned regional audit</a> · <a href="https://github.com/dshimo0/ember-atlas/blob/work/data/regional-evaluation-protocol-v1.json">Preregistered protocol</a></p>`;
}
function experienceView(s){
 const months=monthsBetween(s.start,s.end),position=months.indexOf(selected);
 $('activeScope').textContent=`${s.area==='all'?summary.name+' study area':AREAS[s.area]} · ${s.sensor==='both'?'Both sensors':SENSOR_NAMES[selectedProducts(s.sensor,s.mode)[0]]} · UTC`;
 $('monthScrubber').max=String(Math.max(0,months.length-1));$('monthScrubber').value=String(Math.max(0,position));$('monthScrubber').setAttribute('aria-valuetext',monthName(selected));$('scrubberMonth').textContent=monthName(selected);$('previousMonth').disabled=position<=0;$('nextMonth').disabled=position>=months.length-1;
 document.body.dataset.detail=detail;$('scientificMode').setAttribute('aria-pressed',String(detail==='scientific'));$('scientificMode').textContent=detail==='scientific'?'Scientific detail: on':'Scientific detail';
 if(currentRoute()!=='/methods')$('methodsPage').hidden=detail!=='scientific';
 $('methodsScope').textContent=`${summary.name} study area · ${s.mode.toUpperCase()} · selected ${monthName(selected)} · full-area SP calibration is separately scoped below.`;
 $('sourceCards').innerHTML=sourceCards(summary);$('methodExplore').href=stateURL('/',allState());
 const v=row(selected,s.mode==='nrt'?'VIIRS_NOAA20_NRT':'VIIRS_NOAA20_SP',s),a=s.sensor==='MODIS_SP'?null:adjustment(v,s,validation);
 $('methodSelectedAdjustment').innerHTML=`<div><small>Observed VIIRS · common grid</small><strong>${number(v.cells)}</strong><span>occupied cell-days</span></div><div><small>${a?'Training-only factor':'Adjustment'}</small><strong>${a?'× '+number(a.factor,4):'Unavailable'}</strong><span>${a?'applied to this complete month':'selected scope is unsupported'}</span></div><div><small>Adjusted VIIRS · MODIS scale</small><strong>${number(a?.value??null,1)}</strong><span>occupied cell-days · derived estimate</span></div>`;
}
function guideView(){
 const active=currentRoute()==='/demo';$('walkthrough').hidden=!active;const disclosure=$('validationDisclosure');if(active)$('analysisPage').append(disclosure);else document.querySelector('.page-heading').after(disclosure);
 document.body.dataset.step=String(guideStep);
 // Reorder the same calendar, never create a second analytical state.
 const history=$('history'),explore=$('explore');if(currentRoute()==='/'||active)explore.insertBefore(history,explore.querySelector('.dashboard-grid'));else if(history.parentElement===explore)explore.after(history);
 if(!active)return;
 const scene=scenes[guideStep-1],s=state(),m=row(selected,s.mode==='nrt'?'MODIS_NRT':'MODIS_SP',s),v=row(selected,s.mode==='nrt'?'VIIRS_NOAA20_NRT':'VIIRS_NOAA20_SP',s),a=s.sensor==='MODIS_SP'?null:adjustment(v,s,validation);
 $('stepTitle').textContent=scene[0];$('stepDescription').textContent=scene[1];$('stepProgress').textContent=`Step ${guideStep} of 5`;$('stepBack').disabled=guideStep===1;$('stepNext').disabled=guideStep===5;
 $('stepRail').innerHTML=scenes.map((x,i)=>`<button data-guide-step="${i+1}" aria-label="Step ${i+1}: ${x[0]}" aria-current="${i+1===guideStep?'step':'false'}"><b>${i+1}</b><span>${x[0]}</span></button>`).join('');
 for(const b of $('stepRail').querySelectorAll('button')){b.onclick=()=>goStep(+b.dataset.guideStep);b.onkeydown=e=>{const n={ArrowRight:guideStep+1,ArrowLeft:guideStep-1,Home:1,End:5}[e.key];if(n){e.preventDefault();goStep(n);$('stepRail').querySelector(`[data-guide-step="${guideStep}"]`)?.focus();}};}
 $('sceneImage').hidden=guideStep!==1;const image=$('sceneImage').querySelector('img'),pantanal=s.region==='pantanal';image.src=pantanal?'/assets/pantanal-modis-2024-09-01.jpg':'/assets/earth-nasa.jpg';image.alt=pantanal?'MODIS Terra true-color Pantanal context, September 1, 2024':'NASA Blue Marble composite, released October 2007';$('sceneImageCredit').textContent=pantanal?'NASA GIBS / MODIS Terra · Sep 1, 2024. Editorial context; not the monthly analytical layer.':'NASA/GSFC/Reto Stöckli · Blue Marble, 2007. Editorial Earth context; not the selected region’s observations.';
 const evidence=[`${summary.name} study area · ${monthName(selected)} · ${s.mode.toUpperCase()} observations`,`${monthName(selected)} · earlier same-month years and sample size are available with the selected comparison.`,`MODIS ${number(m.cells)} · VIIRS ${number(v.cells)} occupied cell-days on the common grid.`,a?`Adjusted VIIRS ${number(a.value,1)} cell-days · factor ${number(a.factor,4)}. MODIS remains a comparison reference, not ground truth.`:'No published adjustment for this selection. Real sensor-specific values remain available.',`${scope(selected,s).from} → ${scope(selected,s).to} UTC · selected region, mask and sensors. Missing retrieval is not zero.`];
 const sensorExplanation=guideStep===3?'<div class="scene-sensors"><div><span class="sensor-dot modis"></span><strong>MODIS · nominal 1 km</strong><small>Terra + Aqua reference</small></div><div><span class="sensor-dot viirs"></span><strong>VIIRS · nominal 375 m</strong><small>NOAA-20 comparison</small></div><div><span class="sensor-dot adjusted"></span><strong>Shared 0.05° grid</strong><small>Count each cell once per product per UTC day</small></div></div>':'';
 const sceneMetrics=guideStep===4&&a?`<p class="scene-validation"><strong>${number(evaluation.reduction,1)}% lower monthly MAE vs raw common-grid VIIRS</strong><br>${validation.adjusted.n} holdout months · ${yearsLabel(validation.holdout_years)} · full ${summary.name} SP area. Scalar MAE ${number(compareMethods(validation).metrics.scalar.mae,1)}; quarterly ${number(compareMethods(validation).metrics.seasonal.mae,1)} cell-days/month. All candidates and remaining bias are in Methods & data.<br>Reference-processing continuity and ground truth remain unverified.</p>`:'';
 $('sceneEvidence').innerHTML=`${sensorExplanation}<p>${escapeHTML(evidence[guideStep-1])}</p>${sceneMetrics}<button id="sceneJump">${scene[2]} ↓</button>`;
 const target=['.map-panel','#history','.comparison-panel','.comparison-panel','.observation-export'][guideStep-1];$('sceneJump').onclick=()=>document.querySelector(target)?.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion:reduce)').matches?'instant':'smooth'});
 $('skipDemo').href=stateURL('/',allState());$('guideMethods').href=stateURL('/methods',allState());$('useFullArea').hidden=!(guideStep===4&&!supportsReplay(s));
 if(guideStep===5)for(const d of $('baseline').querySelectorAll('details'))d.open=true;
}
function goStep(n){
 guideStep=Math.max(1,Math.min(5,n));
 if(guideStep===3){$('sensor').value='both';view='raw';}
 if(guideStep===4&&supportsReplay(state())){view='replay';$('showBenchmark').checked=true;}
 commitSelection();
}
function updateLinks() {
 for(const a of document.querySelectorAll('.masthead [data-route]')){
  const u=new URL(a.getAttribute('href'),location.origin),path=u.pathname;
  a.href=stateURL(path,allState(),u.hash);
  if(path===currentRoute()&&!u.hash)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');
 }
}
function commitSelection() {
 if(!ready)return;
 if(!supportsReplay(state()))view='raw';
 render();
 history.pushState(null,'',stateURL(currentRoute(),allState(),location.hash));updateLinks();
}
async function applyLocation(scroll=false) {
 if(!ready)return;const token=++datasetToken;
 if(currentRoute()==='/'&&location.hash==='#methodology')history.replaceState(null,'','/methods'+location.search+'#methodology');
 const preliminary=readURL(location.href),region=release.registry.regions.find(r=>r.id===preliminary.region)||release.registry.regions[0];
 $('region').value=region.id;$('dataMode').value=preliminary.mode;
 $('download').disabled=true;$('downloadCells').disabled=true;$('aggregateDownload').disabled=true;$('downloadReplay').disabled=true;$('downloadManifest').disabled=true;$('status').textContent='Loading selected dataset…';selectionToken++;
 try{
  const data=await loadDataset(region.id,preliminary.mode);const [v,c,a]=await Promise.all([verifiedJSON(data.validation),data.comparison?verifiedJSON(data.comparison):Promise.resolve(release.replayEvaluation),data.external_audit?verifiedJSON(data.external_audit):Promise.resolve(null)]);if(token!==datasetToken)return;summary=data;validation=v;currentComparison=c;externalAudit=a;evaluation=evaluateValidation(validation);index=makeIndex(summary);publishedMetrics();residualView();externalView();
  const s=readURL(location.href,summary.coverage),defaults=datasetDefaults(region.datasets[preliminary.mode],region.id,preliminary.mode),query=new URL(location.href).searchParams;if(!['start','end','month'].some(k=>query.has(k))){s.start=defaults.start;s.end=defaults.end;}selected=s.month;view=s.view;$('calendarEncoding').value=s.encoding||'activity';guideStep=s.step;pitchSlide=s.slide;detail=s.detail;$('showBenchmark').checked=s.benchmark;
  for(const id of ['area','sensor','start','end'])$(id).value=s[id];for(const d of document.querySelectorAll('.native-details,.source-flags,.series-table'))d.open=detail==='scientific';if(region.id!=='pantanal')$('area').value='all';
  const isPitch=currentRoute()==='/pitch',isMethods=currentRoute()==='/methods';document.documentElement.dataset.route=isPitch?'pitch':'analysis';document.body.dataset.page=currentRoute().slice(1)||'explore';
  document.querySelector('.skip').href=isPitch?'#pitchPage':isMethods?'#methodsPage':currentRoute()==='/demo'?'#walkthrough':'#explore';
  $('analysisPage').hidden=isPitch||isMethods;$('pitchPage').hidden=!isPitch;$('methodsPage').hidden=!isMethods;document.body.dataset.detail=detail;$('filterFold').open=false;
  document.title=`Ember Atlas · ${isPitch?'Pitch':isMethods?'Methods & data':region.name+' study area'}`;
  if(isPitch)pitch.setSlide(pitchSlide,scroll);else{if(!isMethods&&!geographicMap)geographicMap=createGeographicMap($('map'),geography);geographicMap?.resize?.();render();}
  history.replaceState(null,'',stateURL(currentRoute(),allState(),location.hash));updateLinks();
  if(location.hash&&!isPitch)requestAnimationFrame(()=>document.getElementById(location.hash.slice(1))?.scrollIntoView());
 }catch(error){if(token!==datasetToken)return;console.error(error);$('error').hidden=false;$('error').textContent='Selected regional dataset unavailable. No replacement observations are shown.';}
}
function recentStart(coverage){return[new Date(Date.parse(coverage.end)-6*86400000).toISOString().slice(0,10),coverage.start].sort().at(-1);}
function switchDataset(){
 const region=release.registry.regions.find(r=>r.id===$('region').value),mode=$('dataMode').value,ref=region.datasets[mode];
 const s=datasetDefaults(ref,region.id,mode);
 if(mode==='nrt')s.start=recentStart(ref.coverage);history.pushState(null,'',stateURL(currentRoute(),s));applyLocation();
}
$('region').onchange=switchDataset;$('dataMode').onchange=switchDataset;
$('showBenchmark').onchange=commitSelection;
$('scientificMode').onclick=()=>{detail=detail==='scientific'?'general':'scientific';$('validationDisclosure').open=detail==='scientific';for(const d of document.querySelectorAll('.native-details,.source-flags,.series-table'))d.open=detail==='scientific';commitSelection();};
$('monthScrubber').oninput=e=>{selected=monthsBetween(state().start,state().end)[+e.target.value];commitSelection();};
for(const [id,delta]of [['previousMonth',-1],['nextMonth',1]])$(id).onclick=()=>{const ms=monthsBetween(state().start,state().end);selected=ms[Math.max(0,Math.min(ms.length-1,ms.indexOf(selected)+delta))];commitSelection();};
$('mapFullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.querySelector('.map-panel').requestFullscreen();}catch{$('mapFullscreen').textContent='Fullscreen unavailable';}};
document.addEventListener('fullscreenchange',()=>{$('mapFullscreen').textContent=document.fullscreenElement===document.querySelector('.map-panel')?'Exit fullscreen':'Expand map';});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&document.fullscreenElement===document.querySelector('.map-panel'))document.exitFullscreen();});
$('layerOpacity').oninput=e=>{$('opacityValue').textContent=e.target.value+'%';document.querySelector('#map .leaflet-observations-pane').style.opacity=String(+e.target.value/100);};
$('fullArchive').onclick=()=>{$('start').value=summary.coverage.start;$('end').value=summary.coverage.end;commitSelection();};
$('downloadReplay').onclick=()=>download(replayCSV(index,state(),validation,summary.snapshot.sha256),`ember-replay-${state().region}-${state().start}_${state().end}.csv`);
$('downloadCells').onclick=()=>{const s=state(),dates=scope(selected,s),product=$('mapProduct').value.replace('_SP',s.mode==='nrt'?'_NRT':'_SP');download(cellCSV(observations,product,{...s,from:dates.from,to:dates.to},summary.snapshot.sha256),`ember-cells-${s.region}-${selected}-${product}.csv`);};
for(const id of ['area','start','end','sensor'])$(id).addEventListener('change',commitSelection);
$('monthSelect').onchange=e=>{selected=e.target.value;commitSelection();};
$('calendarEncoding').onchange=()=>commitSelection();
$('calendarView').onchange=e=>{view=e.target.value;commitSelection();};
$('stepBack').onclick=()=>goStep(guideStep-1);$('stepNext').onclick=()=>goStep(guideStep+1);
$('resetDemo').onclick=()=>{const ref=release.registry.regions[0].datasets.sp;history.pushState(null,'',stateURL('/demo',datasetDefaults(ref,'pantanal')));$('layerModis').checked=true;$('layerViirs').checked=true;$('showGrid').checked=true;$('showPoints').checked=false;$('mapProduct').value='VIIRS_NOAA20_SP';applyLocation().then(()=>$('fitStudyArea').click());};
$('useFullArea').onclick=()=>{$('region').value='pantanal';$('dataMode').value='sp';switchDataset();};
$('map').addEventListener('mapdisplaychange',e=>{if(loadedSelection===selectionKey(state())){$('mapLoading').textContent=!e.detail.gridAvailable?`${e.detail.product}: occupancy unavailable; no retrieval. ${number(e.detail.total)} records from other selected products.`:`${number(e.detail.gridCells)} occupied cells · ${number(e.detail.cellDays)} cell-days · ${number(e.detail.shown)} sampled detections shown / ${number(e.detail.total)} matching observations.`;$('downloadCells').disabled=!e.detail.gridAvailable;$('gridLegend').textContent=!e.detail.gridAvailable?`${e.detail.product}: occupancy unavailable; no retrieval for this sensor/window.`:`${e.detail.product} · occupied UTC days per 0.05° cell · ${e.detail.periodDays} selected UTC days; darker = more occupied days.`;$('occupancyMax').textContent=`${e.detail.periodDays} selected UTC days`;document.querySelector('.occupancy-key').hidden=!e.detail.gridAvailable;document.querySelector('.occupancy-key').dataset.sensor=e.detail.product.startsWith('MODIS')?'modis':'viirs';}});
$('shareSelection').onclick=async()=>{const url=new URL(stateURL(currentRoute(),allState()),location.origin).href;try{await navigator.clipboard.writeText(url);$('shareStatus').textContent='Selection link copied.';}catch{$('shareStatus').innerHTML=`<a href="${url}">${escapeHTML(url)}</a>`;}};
$('downloadManifest').onclick=async()=>{
 const s=state(),selection=allState(),dataset=summary,month=selected,selectedRows=observations,selectedIndex=index;
 const product=$('mapProduct').value.replace('_SP',s.mode==='nrt'?'_NRT':'_SP'),dates=scope(month,s);
 const aggregate=aggregateCSV(selectedIndex,s,validation,dataset.snapshot.sha256);
 const obs=loadedSelection===selectionKey(s)?observationCSV(selectedRows,dataset.snapshot.sha256):null;
 const cells=obs!==null&&aggregateMonth(selectedIndex,month,product,s).retrieved>0?cellCSV(selectedRows,product,{...s,from:dates.from,to:dates.to},dataset.snapshot.sha256):null;
 const replay=view==='replay'&&supportsReplay(s)?replayCSV(selectedIndex,s,validation,dataset.snapshot.sha256):null;
 const manifest={schema:'ember-evidence-2',selection,url:new URL(stateURL(currentRoute(),selection),location.origin).href,
  snapshot:dataset.snapshot,validation:dataset.validation,evaluation:dataset.comparison||release.replayRef,external_evaluation:dataset.external_audit,products:selectedProducts(s.sensor,s.mode),
  geography:{study_rectangle_wsen:dataset.bounds,mask:s.area,geometry_type:'project-defined bounding box'},
  metric:{name:'occupied cell-days',grid_degrees:.05,origin:'globally anchored WGS84',utc:true},
  calibration:{geography:(validation.region||'pantanal')+' full study area only; SP' ,publication_domain:validation.publication_domain||(!validation.region&&validation.accepted?{start:'2020-01-01',end:'2024-12-31'}:null),applies_to_selection:supportsReplay(s)&&s.sensor!=='MODIS_SP'&&!!adjustment(aggregateMonth(selectedIndex,month,'VIIRS_NOAA20_SP',s),s,validation),training_years:validation.train_years,holdout_years:validation.holdout_years,source_transition:view==='replay'?'replay scenario; '+replayCutoff(validation):'none'},
  aggregate_export:{sha256:await sha256(new TextEncoder().encode(aggregate)),months:monthsBetween(s.start,s.end)},
  observation_export:obs!==null?{sha256:await sha256(new TextEncoder().encode(obs)),rows:selectedRows.length,source_shard:dataset.observation_shards[month]}:null,
  cell_export:cells!==null?{sha256:await sha256(new TextEncoder().encode(cells)),product,from_utc:dates.from,through_utc:dates.to}:null,
  replay_export:replay!==null?{sha256:await sha256(new TextEncoder().encode(replay)),cutoff:replayCutoff(validation),scenario:true}:null,
  observation_coverage:'unknown'};
 download(JSON.stringify(manifest,null,2),`ember-provenance-${month}-${s.region}-${s.mode}.json`);
};
window.addEventListener('popstate',()=>applyLocation(true));
document.addEventListener('click',event=>{
 const a=event.target.closest('a[data-route]');if(!a||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 const u=new URL(a.getAttribute('href'),location.href);if(u.origin!==location.origin)return;
 event.preventDefault();history.pushState(null,'',u.pathname+u.search+u.hash);applyLocation(true);if(!u.hash)window.scrollTo(0,0);
});
(async()=>{
 try {
  release=await loadRelease();({summary,validation,geography}=release);evaluation=evaluateValidation(validation);index=makeIndex(summary);ready=true;
  $('region').innerHTML=release.registry.regions.map(r=>`<option value="${r.id}">${r.name}</option>`).join('');
  $('start').value=summary.coverage.start;$('end').value=summary.coverage.end;
  pitch=createPitch($('pitchPage'),release,n=>{pitchSlide=n;history.pushState(null,'',stateURL('/pitch',allState()));pitch.setSlide(n,true);updateLinks();},n=>{if(currentRoute()!=='/pitch')return;pitchSlide=n;history.replaceState(null,'',stateURL('/pitch',allState()));updateLinks();});
  publishedMetrics();residualView();applyLocation();
 }catch(error){console.error('Release load failed',error);$('error').hidden=false;$('error').textContent='Release data could not be loaded. Reload to retry.';$('status').textContent='Data unavailable';$('pitchPage').textContent='Presentation evidence unavailable. Reload to retry.';}
})();

function selectPlotMonth(e){const hit=e.target.closest('[data-plot-month]');if(!hit||e.type==='keydown'&&!['Enter',' '].includes(e.key))return;e.preventDefault();$('monthSelect').value=hit.dataset.plotMonth;$('monthSelect').dispatchEvent(new Event('change'));}
$('timeSeries').addEventListener('click',selectPlotMonth);$('timeSeries').addEventListener('keydown',selectPlotMonth);
