import {loadRelease,verifiedJSON,sha256} from './data-loader.mjs';
import {number,signed,yearsLabel,escapeHTML,compact} from './format.mjs';
import {readURL,stateURL,defaultState} from './url-state.mjs';
import {evaluateValidation,referenceRows,sensitivitySummary} from './analysis.mjs';
import {barChart,timeSeries} from './charts.mjs';
import {createPitch} from './pitch.mjs';
import {createGeographicMap} from './geographic-map.mjs';
import {PRODUCTS, SENSOR_NAMES, AREAS, monthEnd, monthName, monthsBetween, selectedProducts, scope, makeIndex, aggregateMonth, adjustment, historicalBaseline, filterObservations, observationCSV, aggregateCSV} from './model.mjs';
const $ = id => document.getElementById(id);
let summary, validation, index, geography, geographicMap, selected = '2024-09', observations = [], selectionToken = 0, loadedSelection = '', ready = false;
const shardCache = new Map();
const state = () => ({area: $('area').value, sensor: $('sensor').value, start: $('start').value, end: $('end').value});
let view='reference',guideStep=1,pitchSlide=1,pitch,release,evaluation;
const currentRoute=()=>location.pathname.replace(/\/$/,'')||'/';
const allState=()=>({...state(),month:selected,view,step:guideStep,slide:pitchSlide});
const selectionKey = s => [selected, s.area, s.sensor, s.start, s.end].join('|');
function row(month, product, s = state()) { return aggregateMonth(index, month, product, s); }
function publishedMetrics() {
  const improvement = evaluation.reduction;
  $('improvement').textContent = validation.accepted && improvement !== null ? `${number(improvement, 1)}%` : 'Unavailable';
  $('resultLabel').textContent = validation.accepted ? 'lower monthly MAE against MODIS' : 'Adjustment not supported by this release';
  $('mae').textContent = `${number(validation.unadjusted.mae, 1)} → ${number(validation.adjusted.mae, 1)} cell-days/month`;
  $('split').textContent = `${validation.adjusted.n} holdout months · ${yearsLabel(validation.holdout_years)} · Full Pantanal study rectangle`;
  $('validationLink').href = '/data/' + summary.validation.file;
  $('coverage').textContent = `Aggregate and observation coverage: ${summary.coverage.start} → ${summary.coverage.end} UTC`;
  $('validation').textContent = `The ${validation.adjusted.n} matched holdout months in ${yearsLabel(validation.holdout_years)} were excluded from fitting. Training: ${yearsLabel(validation.train_years)}. MAE and signed bias were evaluated against MODIS on the same occupied cell-day scale.`;
  $('bias').textContent = `Signed monthly bias (VIIRS minus MODIS) moved from ${signed(validation.unadjusted.bias)} to ${signed(validation.adjusted.bias)} occupied cell-days. A negative value means the adjusted estimate is lower than MODIS on average. Residuals vary by season; all seasonal results are in the validation JSON.`;
  $('factors').textContent = 'Frozen quarter factors (VIIRS → MODIS reference): ' + Object.entries(validation.factors).map(([q, f]) => `Q${+q + 1}: ${number(f, 4)}`).join(' · ') + '.';
  $('provenance').textContent = `Snapshot ${summary.snapshot.file}; SHA-256 ${summary.snapshot.sha256}. ${number(summary.observation_count)} observations, ${summary.manifest_count} raw window manifests. Built ${summary.built_utc}. UI aggregates and monthly observation shards are checksum-verified derivatives of this same snapshot. Both export types cover the same released dates.`;
  $('evidenceLinks').innerHTML = `<a href="/data/${summary.validation.file}">Versioned validation JSON ↗</a><a href="/data/${summary.snapshot.file}">Original pinned snapshot ↗</a><a href="/data/monthly_comparison.csv">Full-area monthly evidence CSV ↗</a><a href="/data/diagnostics.json">Sensitivity diagnostics ↗</a><a href="/data/dashboard.json">UI provenance index ↗</a>`;
}
function calendar(s) {
  const months = monthsBetween(s.start, s.end), byYear = new Map();
  for (const m of months) { const y = m.slice(0, 4); if (!byYear.has(y)) byYear.set(y, []); byYear.get(y).push(m); }
  const header = ['<div class="calendar-corner"></div>', ...Array.from({length: 12}, (_, i) => `<div class="month-header">${new Date(Date.UTC(2024, i, 1)).toLocaleDateString('en-US', {month: 'short', timeZone: 'UTC'})}</div>`)];
  const selectedSensors = selectedProducts(s.sensor);
  for (const [year, available] of byYear) {
    const phase = validation.train_years.includes(+year) ? 'Training' : validation.holdout_years.includes(+year) ? 'Holdout' : 'Outside release';
    header.push(`<div class="calendar-year"><div class="year-label"><strong>${year}</strong><small>${phase}</small></div>`);
    for (let n = 1; n <= 12; n++) {
      const m = `${year}-${String(n).padStart(2, '0')}`;
      if (!available.includes(m)) { header.push('<div class="calendar-spacer"></div>'); continue; }
      const original = selectedSensors.map(p => row(m,p,s));
      const ref=view==='reference'&&s.area==='all';
      const viirs=row(m,'VIIRS_NOAA20_SP',s),a=adjustment(viirs,s,validation);
      const values=ref?[{...viirs,cells:a?.value??null,product:'VIIRS_NOAA20_SP'}]:original;
      const unavailable = values.every(r => !r.retrieved), partial = !unavailable && values.some(r => !r.complete);
      const symbol = unavailable ? '—' : partial ? '◐' : '✓';
      const label = `${monthName(m)}. ${phase}. ${values.map(v => `${ref?'Adjusted VIIRS':SENSOR_NAMES[v.product]}: ${v.cells === null ? 'Data unavailable' : `${number(v.cells)} cell-days, ${v.status}`}`).join('. ')}`;
      header.push(`<button class="month ${unavailable ? 'missing' : partial ? 'partial' : ''}" data-month="${m}" aria-label="${label}" aria-pressed="${m === selected}"><em class="mobile-month">${new Date(m+'-01T00:00:00Z').toLocaleDateString('en-US',{month:'short',timeZone:'UTC'})}</em>${values.map(v => `<span class="${ref?'a':v.product === 'MODIS_SP' ? 'm' : 'v'}">${ref?'▲ A':v.product === 'MODIS_SP' ? '○ M' : '◇ V'} <b>${compact(v.cells)}</b></span>`).join('')}<span class="coverage-symbol" aria-hidden="true">${symbol}</span></button>`);
    }
    header.push('</div>');
  }
  $('calendar').innerHTML = header.join('');
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
  const baselines = values.map(v => ({...v, baseline: historicalBaseline(index, selected, v.product, s, validation)}));
  const valid = baselines.every(v => v.baseline);
  if (valid) {
    const allAbove = baselines.every(v => v.baseline.difference > 0), allBelow = baselines.every(v => v.baseline.difference < 0);
    const years = yearsLabel(baselines[0].baseline.entries.map(e => e.year));
    const calendarMonth = new Date(selected+'-01T00:00:00Z').toLocaleDateString('en-US',{month:'long',timeZone:'UTC'});
    const subject = baselines.length === 2 ? 'both sensors' : SENSOR_NAMES[baselines[0].product];
    const direction = allAbove ? 'above' : allBelow ? 'below' : 'at different levels relative to';
    $('takeaway').textContent = `${monthName(selected)}: ${subject} recorded activity ${direction} the ${years} ${calendarMonth} median${baselines.length === 2 ? 's' : ''} (n = ${baselines[0].baseline.n}).`;
  } else {
    $('takeaway').textContent = values.some(v => !v.complete) ? 'Historical comparison unavailable for a partial or missing month.' : 'Historical comparison requires at least three complete prior years.';
  }
  $('baseline').innerHTML = baselines.map(v => {
    const b = v.baseline, name = SENSOR_NAMES[v.product], mark = v.product === 'MODIS_SP' ? 'modis' : 'viirs';
    return `<div class="baseline-row"><div><span><i class="mark ${mark}" aria-hidden="true"></i>${name}</span><strong>${b && b.percent !== null ? signed(b.percent, 1) + '%' : '—'}</strong></div>${b ? `<p>${number(v.cells)} cell-days vs median <b>${number(b.median, b.median % 1 ? 1 : 0)}</b> · ${signed(b.difference, 0)} cell-days</p><details><summary>Baseline ${yearsLabel(b.entries.map(e => e.year))} · n = ${b.n} prior years</summary><div class="baseline-values">${b.entries.map(e => `${e.year}: ${number(e.value)} cell-days`).join('<br>')}<br>Selected year excluded.</div></details>` : `<p>${v.status}; ${v.retrieved}/${v.expected} selected UTC days retrieved. Baseline unavailable.</p>`}</div>`;
  }).join('');
}
function comparison(s, values) {
  const v = row(selected, 'VIIRS_NOAA20_SP', s), m = row(selected, 'MODIS_SP', s), a = adjustment(v, s, validation);
  const series = values.map(r => ({name: SENSOR_NAMES[r.product] + (r.product === 'MODIS_SP' ? ' · reference' : ' · common grid'), value: r.cells, kind: r.product === 'MODIS_SP' ? 'modis' : 'viirs'}));
  if (s.sensor !== 'MODIS_SP' && a) series.push({name: 'Adjusted VIIRS · MODIS reference', value: a.value, kind: 'adjusted'});
  $('comparison').innerHTML=barChart(series);
  if (a && m.complete && s.sensor !== 'MODIS_SP') {
    const delta = a.value - m.cells, pct = m.cells ? 100 * delta / m.cells : null;
    $('adjusted').textContent = `Adjusted VIIRS is ${number(Math.abs(delta), 1)} cell-days ${delta < 0 ? 'below' : 'above'} MODIS${pct !== null ? ` (${signed(pct)}%)` : ''} this month.`;
  } else $('adjusted').textContent = 'Adjustment unavailable for this selection.';
  $('scopeNotice').classList.toggle('warning', s.area !== 'all');
  $('scopeNotice').textContent = s.area !== 'all' ? 'Adjustment unavailable: factors were validated only for the full study area.' : !v.complete ? 'No adjustment for a partial or missing month.' : s.sensor === 'MODIS_SP' ? 'MODIS reference observations.' : a ? `Quarter factor ${number(a.factor, 4)} · Training ${yearsLabel(validation.train_years)}` : 'Adjustment unavailable: this month is outside the accepted validation domain.';
  $('nativeCounts').innerHTML = `<table><thead><tr><th>Product</th><th>Native detections</th><th>Retrieval</th></tr></thead><tbody>${values.map(r => `<tr><th>${SENSOR_NAMES[r.product]}</th><td>${number(r.native)}</td><td>${r.status}<br>${r.retrieved}/${r.expected} days</td></tr>`).join('')}</tbody></table>`;
}
function map(s, rows = []) {
  if (!geographicMap) return;
  const shown = geographicMap.update(rows, {...s, month: selected});
  $('mapMonth').textContent = `${monthName(selected)} · ${s.area === 'all' ? 'Full study area' : AREAS[s.area]}`;
  if (loadedSelection === selectionKey(s)) $('mapLoading').textContent = `${number(shown)} sampled markers · ${number(rows.length)} matching observations.`;
}
async function monthObservations(month) {
  if (!summary.observation_shards[month]) return [];
  if (!shardCache.has(month)) {
    shardCache.set(month, verifiedJSON(summary.observation_shards[month], true).then(data => {
      if (data.snapshot_sha256 !== summary.snapshot.sha256 || data.month !== month) throw new Error('Observation provenance mismatch');
      return data.observations;
    }).catch(error => { shardCache.delete(month); throw error; }));
    while (shardCache.size > 2) shardCache.delete(shardCache.keys().next().value);
  }
  return shardCache.get(month);
}
async function loadObservations(s, values) {
  const token = ++selectionToken, key = selectionKey(s), month = selected;
  loadedSelection = ''; observations = []; $('download').disabled = true; $('downloadManifest').disabled=true;
  $('download').textContent = `Download ${monthName(month)} observations`;
  $('mapLoading').textContent = 'Loading observations…'; map(s);
  if (!values.some(v => v.retrieved)) {
    $('mapLoading').textContent = 'No retrieval for this selection.';
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
    $('download').disabled = !values.some(v => v.retrieved);
    $('downloadManifest').disabled=false;
    $('observationScope').textContent = `${month} · ${scope(month, s).from} → ${scope(month, s).to} UTC · ${number(observations.length)} records · selected area & sensors`;
    map(s, observations);
  } catch (error) {
    if (token !== selectionToken) return;
    $('mapLoading').textContent = 'Observation file unavailable. Aggregate data remain available.';
    $('observationScope').textContent = 'Observation export unavailable.';
  }
}
function render() {
  if (!ready) return;
  const s = state();
  if (!s.start || !s.end || s.start > s.end || (Date.parse(s.end)-Date.parse(s.start))/86400000>3660) {
    $('error').hidden = false; $('error').textContent = 'Choose a valid date range with the end on or after the start. The previous view remains visible; downloads are disabled.';
    $('download').disabled = true; $('aggregateDownload').disabled = true; $('downloadManifest').disabled=true; selectionToken++; return;
  }
  $('error').hidden = true;
  if (selected < s.start.slice(0, 7) || selected > s.end.slice(0, 7)) selected = s.start.slice(0, 7);
  const values = selectedProducts(s.sensor).map(p => row(selected, p, s)), available = values.some(v => v.retrieved), count = values.reduce((n, v) => n + (v.native ?? 0), 0), dates = scope(selected, s);
  $('monthTitle').textContent = monthName(selected);
  $('monthPhase').textContent = validation.holdout_years.includes(+selected.slice(0, 4)) ? 'Holdout year' : validation.train_years.includes(+selected.slice(0, 4)) ? 'Training year' : 'Outside release coverage';
  $('status').textContent = available ? `${count === 0 ? 'No detections recorded · ' : ''}${number(count)} observations · ${values.every(v => v.complete) ? 'Complete monthly retrieval' : 'Partial month / mixed retrieval'}` : 'Data unavailable · no retrieval for the selected month';
  $('selection').innerHTML = `<span>Month <strong>${monthName(selected)}</strong></span><span>Area <strong>${AREAS[s.area]}</strong></span><span>Sensor <strong>${s.sensor === 'both' ? 'Both sensors' : SENSOR_NAMES[s.sensor]}</strong></span><span>Records <strong>${available ? number(count) : 'Unavailable'}</strong></span><span>UTC <strong>${dates.from} → ${dates.to}</strong></span>`;
  if(s.area!=='all'||s.sensor==='MODIS_SP')view='raw';
  $('calendarView').value=view; $('calendarView').querySelector('[value=reference]').disabled=s.area!=='all'||s.sensor==='MODIS_SP';
  $('monthSelect').innerHTML=monthsBetween(s.start,s.end).map(m=>`<option value="${m}" ${m===selected?'selected':''}>${monthName(m)}</option>`).join('');
  baselineView(s, values); comparison(s, values); calendar(s); historyView(s); guideView();
  $('aggregateDownload').disabled = false;
  $('aggregateScope').textContent = `${s.start} → ${s.end} UTC · ${monthsBetween(s.start, s.end).length} months · selected area & sensors · missing values stay blank`;
  if(currentRoute()!=='/pitch')loadObservations(s, values);
}
function download(text, filename) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: filename.endsWith('.json')?'application/json':'text/csv;charset=utf-8'})); a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); }
$('download').addEventListener('click', () => { const s = state(); if (loadedSelection !== selectionKey(s)) return; download(observationCSV(observations, summary.snapshot.sha256), `ember-observations-${selected}-${s.area}-${s.sensor}.csv`); });
$('aggregateDownload').addEventListener('click', () => { const s = state(); download(aggregateCSV(index, s, validation, summary.snapshot.sha256), `ember-aggregates-${s.start}_${s.end}-${s.area}-${s.sensor}.csv`); });
function historyView(s) {
 const rows=referenceRows(index,s,validation);
 $('referenceScope').textContent=s.area==='all'?(view==='reference'?'Adjusted VIIRS on the MODIS-reference scale · complete months · full study rectangle. Separate MODIS reference; no fused record or source transition.':'Unadjusted sensor-specific activity on the common grid.'):'Regional sensor history. Full-area calibration is unavailable here; historical medians use each product’s own regional mask.';
 $('timeSeries').innerHTML=timeSeries(rows,view);
 $('seriesLegend').innerHTML=(s.sensor!=='VIIRS_NOAA20_SP'?'<span>○ MODIS reference (dashed)</span>':'')+(s.sensor!=='MODIS_SP'?`<span>${view==='reference'?'▲ Adjusted VIIRS':'◇ VIIRS common grid'} (solid)</span>`:'');
 $('seriesTable').innerHTML=`<table><thead><tr><th>Month / split</th><th>MODIS cell-days</th><th>VIIRS cell-days</th><th>Adjusted VIIRS</th><th>Adjustment status</th></tr></thead><tbody>${rows.map(r=>`<tr><th>${r.month} · ${r.phase}</th><td>${number(r.reference)}</td><td>${number(r.viirs)}</td><td>${number(r.adjusted,1)}</td><td>${r.status}</td></tr>`).join('')}</tbody></table><p class="unit">Source products: MODIS_SP reference; VIIRS_NOAA20_SP candidate. No product sum or handoff. Missing/partial monthly series values remain unavailable.</p>`;
}
function residualView() {
 const e=evaluation;
 $('residualSummary').textContent=`Holdout bias ${signed(e.before.bias)} → ${signed(e.after.bias)}; RMSE ${number(e.before.rmse,1)} → ${number(e.after.rmse,1)} cell-days/month. ${e.underperforming.length} of ${e.rows.length} months have larger absolute residual after adjustment (${e.underperforming.map(r=>r.month).join(', ')}). Positive residuals mean VIIRS exceeds MODIS. This validation is for the full study rectangle.`;
 const max=Math.max(...e.rows.flatMap(r=>[Math.abs(r.before),Math.abs(r.after)])),x=v=>450+v/max*400;
 $('residualChart').innerHTML=`<svg class="residual-svg" viewBox="0 0 920 ${e.rows.length*20+28}" role="img" aria-label="Monthly holdout residuals in occupied cell-days; cyan unadjusted, purple adjusted; left of zero is below MODIS"><path d="M450 0V${e.rows.length*20}" stroke="#aebdb7"/>${e.rows.map((r,i)=>`<text x="0" y="${i*20+14}" fill="#b4c2bd" font-size="11">${r.month}${r.underperforms?' *':''}</text>${[['before','#86d6d1'],['after','#c8b5ed']].map(([k,c],j)=>`<rect x="${Math.min(450,x(r[k]))}" y="${i*20+j*7+2}" width="${Math.max(1,Math.abs(x(r[k])-450))}" height="5" fill="${c}"><title>${r.month}: ${k} ${number(r[k],1)} cell-days</title></rect>`).join('')}`).join('')}<text x="260" y="${e.rows.length*20+19}" fill="#b4c2bd" font-size="11">Below MODIS ← 0 → Above MODIS · cyan unadjusted / purple adjusted · * underperforms</text></svg>`;
 $('residualTable').innerHTML=`<table><thead><tr><th>Holdout month</th><th>Unadjusted residual</th><th>Adjusted residual</th><th>Absolute-error change</th></tr></thead><tbody>${e.rows.map(r=>`<tr class="${r.underperforms?'underperforms':''}"><th><a data-route href="${stateURL('/demo',{...defaultState(summary.coverage),month:r.month,step:3})}">${r.month}</a></th><td>${signed(r.before)}</td><td>${signed(r.after)}</td><td>${r.underperforms?'Larger after adjustment':'Smaller after adjustment'}</td></tr>`).join('')}</tbody></table>`;
 const sensitivity=sensitivitySummary(release.diagnostics);
 $('sensitivity').innerHTML=`<p>Descriptive count sensitivity across the full released period; no alternate calibration was selected on holdout.</p><table><thead><tr><th>Product</th><th>0.025° vs 0.05°</th><th>0.1° vs 0.05°</th><th>High-confidence share at 0.05°</th></tr></thead><tbody>${sensitivity.map(r=>`<tr><th>${SENSOR_NAMES[r.product]}</th><td>${signed(r.finerPercent)}%</td><td>${signed(r.coarserPercent)}%</td><td>${number(r.highConfidencePercent,1)}%</td></tr>`).join('')}</tbody></table><p>High confidence: MODIS ≥80; VIIRS h. Thresholds are sensor-specific. Cell-area latitude dependence, timing and cloud effects remain.</p>`;
}
const steps=[['Select area and month','Choose the study rectangle or a fixed half, and inspect the real observations for a month.'],['Compare common support','Both products use the same 0.05° grid and UTC-day aggregation. Native detections remain separate.'],['Inspect adjusted VIIRS','The purple output is VIIRS scaled to the MODIS reference using training-only quarterly factors.'],['Compare prior years','Each sensor uses its own complete prior years for the same month and same regional mask.'],['Export evidence','Export the selected month, selected-period aggregates and a provenance manifest. Share the same state.']];
function guideView() {
 const active=currentRoute()==='/demo';$('walkthrough').hidden=!active;
 if(!active)return;
 $('stepTitle').textContent=steps[guideStep-1][0];$('stepDescription').textContent=steps[guideStep-1][1];
 $('stepProgress').textContent=`Step ${guideStep} of 5`;$('stepBack').disabled=guideStep===1;$('stepNext').disabled=guideStep===5;
 $('stepRail').innerHTML=steps.map((s,i)=>`<button data-guide-step="${i+1}" aria-label="Step ${i+1}: ${s[0]}" aria-current="${i+1===guideStep?'step':'false'}"><b>${i+1}</b><span>${s[0]}</span></button>`).join('');
 for(const b of $('stepRail').querySelectorAll('button'))b.onclick=()=>goStep(+b.dataset.guideStep);
 $('useFullArea').hidden=!(guideStep===3&&state().area!=='all');
 document.querySelectorAll('.guide-target').forEach(e=>e.classList.remove('guide-target'));
 const target=['.controls','.comparison-panel','.comparison-panel','#baseline','.observation-export'][guideStep-1];document.querySelector(target)?.classList.add('guide-target');
 if(guideStep===4)for(const d of $('baseline').querySelectorAll('details'))d.open=true;
}
function goStep(n) {
 guideStep=Math.max(1,Math.min(5,n));
 if(guideStep===2)$('sensor').value='both';
 if(guideStep===3&&state().area==='all')view='reference';
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
 if(state().area!=='all')view='raw';
 render();
 history.pushState(null,'',stateURL(currentRoute(),allState(),location.hash));updateLinks();
}
function applyLocation(scroll=false) {
 if(!ready)return;
 const s=readURL(location.href,summary.coverage);selected=s.month;view=s.area==='all'?s.view:'raw';guideStep=s.step;pitchSlide=s.slide;
 for(const id of ['area','sensor','start','end'])$(id).value=s[id];
 const isPitch=currentRoute()==='/pitch';document.documentElement.dataset.route=isPitch?'pitch':'analysis';document.body.dataset.page=currentRoute().slice(1)||'explore';
 $('analysisPage').hidden=isPitch;$('pitchPage').hidden=!isPitch;
 $('pageTitle').textContent=currentRoute()==='/demo'?'Explore fire activity across sensors':`Pantanal fire activity, ${summary.coverage.start.slice(0,4)}–${summary.coverage.end.slice(0,4)}`;
 $('filterFold').open=!(currentRoute()==='/demo'&&matchMedia('(max-width:700px)').matches);
 document.title=`Ember Atlas · ${isPitch?'Pitch':currentRoute()==='/demo'?'Guided demo':'Pantanal fire activity, 2020–2024'}`;
 $('pageSubtitle').textContent=currentRoute()==='/demo'?`Pantanal study rectangle · ${summary.coverage.start}–${summary.coverage.end} UTC · Standard Processing observations`:'NASA FIRMS · MODIS C6.1 SP and NOAA-20 VIIRS SP';
 if(isPitch)pitch.setSlide(pitchSlide,scroll);
 else {
  if(!geographicMap)geographicMap=createGeographicMap($('map'),geography);
  geographicMap.resize?.();render();
 }
 history.replaceState(null,'',stateURL(currentRoute(),allState(),location.hash));updateLinks();
 if(location.hash&&!isPitch)requestAnimationFrame(()=>document.getElementById(location.hash.slice(1))?.scrollIntoView());
}
for(const id of ['area','start','end','sensor'])$(id).addEventListener('change',commitSelection);
$('monthSelect').onchange=e=>{selected=e.target.value;commitSelection();};
$('calendarView').onchange=e=>{view=e.target.value;commitSelection();};
$('stepBack').onclick=()=>goStep(guideStep-1);$('stepNext').onclick=()=>goStep(guideStep+1);
$('resetDemo').onclick=()=>{history.pushState(null,'',stateURL('/demo',defaultState(summary.coverage)));applyLocation();};
$('useFullArea').onclick=()=>{$('area').value='all';view='reference';commitSelection();};
$('map').addEventListener('mapdisplaychange',e=>{if(loadedSelection===selectionKey(state()))$('mapLoading').textContent=`${number(e.detail.shown)} sampled markers · ${number(e.detail.total)} matching observations.`;});
$('shareSelection').onclick=async()=>{const url=new URL(stateURL(currentRoute(),allState()),location.origin).href;try{await navigator.clipboard.writeText(url);$('shareStatus').textContent='Selection link copied.';}catch{$('shareStatus').innerHTML=`<a href="${url}">${escapeHTML(url)}</a>`;}};
$('downloadManifest').onclick=async()=>{
 const s=state(),aggregate=aggregateCSV(index,s,validation,summary.snapshot.sha256),obs=loadedSelection===selectionKey(s)?observationCSV(observations,summary.snapshot.sha256):null;
 const manifest={schema:'ember-evidence-1',selection:allState(),url:new URL(stateURL(currentRoute(),allState()),location.origin).href,snapshot:summary.snapshot,validation:summary.validation,products:selectedProducts(s.sensor),geography:{study_rectangle_wsen:[-59,-23,-54,-15],regional_partition_latitude:-19,north_includes_partition:true},metric:{name:'occupied cell-days',grid_degrees:validation.grid_degrees,origin:'globally anchored WGS84',utc:true,method:validation.method},calibration:{geography:'full Pantanal study rectangle only',applies_to_selection:s.area==='all'&&s.sensor!=='MODIS_SP'&&!!adjustment(row(selected,'VIIRS_NOAA20_SP',s),s,validation),training_years:validation.train_years,holdout_years:validation.holdout_years,source_transition:'none; separate overlapping products'},aggregate_export:{sha256:await sha256(new TextEncoder().encode(aggregate)),months:monthsBetween(s.start,s.end)},observation_export:obs?{sha256:await sha256(new TextEncoder().encode(obs)),rows:observations.length,source_shard:summary.observation_shards[selected]}:null,observation_coverage:'unknown'};
 download(JSON.stringify(manifest,null,2),`ember-provenance-${selected}-${s.area}.json`);
};
window.addEventListener('popstate',()=>applyLocation(true));
document.addEventListener('click',event=>{
 const a=event.target.closest('a[data-route]');if(!a||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
 const u=new URL(a.href,location.href);if(u.origin!==location.origin)return;
 event.preventDefault();history.pushState(null,'',u.pathname+u.search+u.hash);applyLocation(true);if(!u.hash)window.scrollTo(0,0);
});
(async()=>{
 try {
  release=await loadRelease();({summary,validation,geography}=release);evaluation=evaluateValidation(validation);index=makeIndex(summary);ready=true;
  $('start').value=summary.coverage.start;$('end').value=summary.coverage.end;
  pitch=createPitch($('pitchPage'),release,n=>{pitchSlide=n;history.pushState(null,'',stateURL('/pitch',allState()));pitch.setSlide(n,true);updateLinks();});
  publishedMetrics();residualView();applyLocation();
 }catch(error){console.error('Release load failed',error);$('error').hidden=false;$('error').textContent='Release data could not be loaded. Reload to retry.';$('status').textContent='Data unavailable';$('pitchPage').textContent='Presentation evidence unavailable. Reload to retry.';}
})();
