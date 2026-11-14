import {createGeographicMap} from './geographic-map.mjs';
import {PRODUCTS, SENSOR_NAMES, AREAS, monthEnd, monthName, monthsBetween, selectedProducts, scope, makeIndex, aggregateMonth, adjustment, historicalBaseline, filterObservations, observationCSV, aggregateCSV} from './model.mjs';
const $ = id => document.getElementById(id);
const number = (value, decimals = 0) => value === null || value === undefined ? '—' : Number(value).toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
const compact = value => value === null ? '—' : value >= 1000 ? (value / 1000).toFixed(1) + 'k' : String(value);
const signed = (value, decimals = 1) => (value > 0 ? '+' : value < 0 ? '−' : '') + number(Math.abs(value), decimals);
let summary, validation, index, geography, geographicMap, selected = '2024-09', observations = [], selectionToken = 0, loadedSelection = '', ready = false;
const shardCache = new Map();
const state = () => ({area: $('area').value, sensor: $('sensor').value, start: $('start').value, end: $('end').value});
const selectionKey = s => [selected, s.area, s.sensor, s.start, s.end].join('|');
function yearsLabel(years) { return years.length > 1 ? `${years[0]}–${years.at(-1)}` : String(years[0]); }
function sha256(bytes) { return crypto.subtle.digest('SHA-256', bytes).then(hash => [...new Uint8Array(hash)].map(v => v.toString(16).padStart(2, '0')).join('')); }
async function verifiedJSON(ref, compressed = false) {
  const response = await fetch('data/' + ref.file);
  if (!response.ok) throw new Error('Data file unavailable');
  const bytes = compressed ? await new Response(response.body.pipeThrough(new DecompressionStream('gzip'))).arrayBuffer() : await response.arrayBuffer();
  if (await sha256(bytes) !== ref.sha256) throw new Error('Data integrity check failed');
  return JSON.parse(new TextDecoder().decode(bytes));
}
function row(month, product, s = state()) { return aggregateMonth(index, month, product, s); }
function publishedMetrics() {
  const improvement = validation.unadjusted.mae > 0 ? 100 * (1 - validation.adjusted.mae / validation.unadjusted.mae) : null;
  $('improvement').textContent = validation.accepted && improvement !== null ? `${number(improvement, 1)}%` : 'Unavailable';
  $('resultLabel').textContent = validation.accepted ? 'lower monthly error against MODIS' : 'Adjustment not supported by this release';
  $('mae').textContent = `${number(validation.unadjusted.mae, 1)} → ${number(validation.adjusted.mae, 1)} cell-days/month`;
  $('split').textContent = `${validation.adjusted.n} holdout months · ${yearsLabel(validation.holdout_years)} · Full Pantanal study area`;
  $('validationLink').href = 'data/' + summary.validation.file;
  $('coverage').textContent = `Aggregate and observation coverage: ${summary.coverage.start} → ${summary.coverage.end} UTC`;
  $('validation').textContent = `The ${validation.adjusted.n} matched holdout months in ${yearsLabel(validation.holdout_years)} were excluded from fitting. Training: ${yearsLabel(validation.train_years)}. The frozen rule ${validation.accepted ? 'passed' : 'did not pass'}.`;
  $('bias').textContent = `Signed monthly bias (VIIRS minus MODIS) moved from ${signed(validation.unadjusted.bias)} to ${signed(validation.adjusted.bias)} occupied cell-days. A negative value means the adjusted estimate is lower than MODIS on average. Residuals vary by season; all seasonal results are in the validation JSON.`;
  $('factors').textContent = 'Frozen quarter factors (VIIRS → MODIS reference): ' + Object.entries(validation.factors).map(([q, f]) => `Q${+q + 1}: ${number(f, 4)}`).join(' · ') + '.';
  $('provenance').textContent = `Snapshot ${summary.snapshot.file}; SHA-256 ${summary.snapshot.sha256}. ${number(summary.observation_count)} observations, ${summary.manifest_count} raw window manifests. Built ${summary.built_utc}. UI aggregates and monthly observation shards are checksum-verified derivatives of this same snapshot. Both export types cover the same released dates.`;
  $('evidenceLinks').innerHTML = `<a href="data/${summary.validation.file}">Versioned validation JSON ↗</a><a href="data/${summary.snapshot.file}">Original pinned snapshot ↗</a><a href="data/monthly_comparison.csv">Full-area monthly evidence CSV ↗</a><a href="data/diagnostics.json">Sensitivity diagnostics ↗</a><a href="data/dashboard.json">UI provenance index ↗</a>`;
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
      const values = selectedSensors.map(p => row(m, p, s));
      const unavailable = values.every(r => !r.retrieved), partial = !unavailable && values.some(r => !r.complete);
      const symbol = unavailable ? '—' : partial ? '◐' : '✓';
      const label = `${monthName(m)}. ${phase}. ${values.map(v => `${SENSOR_NAMES[v.product]}: ${v.cells === null ? 'Data unavailable' : `${number(v.cells)} cell-days, ${v.status}`}`).join('. ')}`;
      header.push(`<button class="month ${unavailable ? 'missing' : partial ? 'partial' : ''}" data-month="${m}" aria-label="${label}" aria-pressed="${m === selected}"><em class="mobile-month">${new Date(m+'-01T00:00:00Z').toLocaleDateString('en-US',{month:'short',timeZone:'UTC'})}</em>${values.map(v => `<span class="${v.product === 'MODIS_SP' ? 'm' : 'v'}">${v.product === 'MODIS_SP' ? '○ M' : '◇ V'} <b>${compact(v.cells)}</b></span>`).join('')}<span class="coverage-symbol" aria-hidden="true">${symbol}</span></button>`);
    }
    header.push('</div>');
  }
  $('calendar').innerHTML = header.join('');
  for (const button of $('calendar').querySelectorAll('[data-month]')) {
    button.addEventListener('click', () => { selected = button.dataset.month; render(); $('calendar').querySelector(`[data-month="${selected}"]`)?.focus({preventScroll: true}); });
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
    $('takeaway').textContent = s.area !== 'all' ? 'Historical comparison unavailable for this subregion.' : values.some(v => !v.complete) ? 'Historical comparison unavailable for a partial or missing month.' : 'Historical comparison requires at least three complete prior years.';
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
  const max = Math.max(1, ...series.map(r => r.value ?? 0));
  $('comparison').innerHTML = series.map(r => `<div class="chart-row ${r.kind}" data-series="${r.kind}" data-value="${r.value ?? ''}"><div class="chart-label"><i class="mark ${r.kind}" aria-hidden="true"></i><span>${r.name}</span><strong>${number(r.value, r.kind === 'adjusted' ? 1 : 0)}</strong></div>${r.value === null ? '<p class="empty-chart">Data unavailable</p>' : `<div class="bar-track" role="img" aria-label="${r.name}: ${number(r.value, r.kind === 'adjusted' ? 1 : 0)} occupied cell-days"><div class="bar-fill" style="width:${100 * r.value / max}%"></div></div>`}</div>`).join('');
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
  if (loadedSelection === selectionKey(s)) $('mapLoading').textContent = `${number(shown)} of ${number(rows.length)} observations shown.`;
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
  loadedSelection = ''; observations = []; $('download').disabled = true;
  $('download').textContent = `Download ${monthName(month)} observations`;
  $('mapLoading').textContent = 'Loading observations…'; map(s);
  if (!values.some(v => v.retrieved)) {
    $('mapLoading').textContent = 'No retrieval for this selection.';
    $('observationScope').textContent = 'Observation export unavailable: no retrieved data for this month.';
    return;
  }
  try {
    const all = await monthObservations(month);
    if (token !== selectionToken) return;
    observations = filterObservations(all, month, s); loadedSelection = key;
    const expected = values.reduce((n, v) => n + (v.native ?? 0), 0);
    if (observations.length !== expected) throw new Error('Selected observations do not match released aggregates');
    $('download').disabled = !values.some(v => v.retrieved);
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
  if (!s.start || !s.end || s.start > s.end) {
    $('error').hidden = false; $('error').textContent = 'Choose a valid date range with the end on or after the start. The previous view remains visible; downloads are disabled.';
    $('download').disabled = true; $('aggregateDownload').disabled = true; selectionToken++; return;
  }
  $('error').hidden = true;
  if (selected < s.start.slice(0, 7) || selected > s.end.slice(0, 7)) selected = s.start.slice(0, 7);
  const values = selectedProducts(s.sensor).map(p => row(selected, p, s)), available = values.some(v => v.retrieved), count = values.reduce((n, v) => n + (v.native ?? 0), 0), dates = scope(selected, s);
  $('monthTitle').textContent = monthName(selected);
  $('monthPhase').textContent = validation.holdout_years.includes(+selected.slice(0, 4)) ? 'Holdout year' : validation.train_years.includes(+selected.slice(0, 4)) ? 'Training year' : 'Outside release coverage';
  $('status').textContent = available ? `${count === 0 ? 'No detections recorded · ' : ''}${number(count)} observations · ${values.every(v => v.complete) ? 'Complete monthly retrieval' : 'Partial month / mixed retrieval'}` : 'Data unavailable · no retrieval for the selected month';
  $('selection').innerHTML = `<span>Month <strong>${monthName(selected)}</strong></span><span>Area <strong>${AREAS[s.area]}</strong></span><span>Sensor <strong>${s.sensor === 'both' ? 'Both sensors' : SENSOR_NAMES[s.sensor]}</strong></span><span>Records <strong>${available ? number(count) : 'Unavailable'}</strong></span><span>UTC <strong>${dates.from} → ${dates.to}</strong></span>`;
  baselineView(s, values); comparison(s, values); calendar(s);
  $('aggregateDownload').disabled = false;
  $('aggregateScope').textContent = `${s.start} → ${s.end} UTC · ${monthsBetween(s.start, s.end).length} months · selected area & sensors · missing values stay blank`;
  loadObservations(s, values);
}
function download(text, filename) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: 'text/csv;charset=utf-8'})); a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); }
$('download').addEventListener('click', () => { const s = state(); if (loadedSelection !== selectionKey(s)) return; download(observationCSV(observations, summary.snapshot.sha256), `ember-observations-${selected}-${s.area}-${s.sensor}.csv`); });
$('aggregateDownload').addEventListener('click', () => { const s = state(); download(aggregateCSV(index, s, validation, summary.snapshot.sha256), `ember-aggregates-${s.start}_${s.end}-${s.area}-${s.sensor}.csv`); });
for (const id of ['area', 'start', 'end', 'sensor']) $(id).addEventListener('change', render);
(async () => {
  try {
    const pointer = await (await fetch('data/dashboard.json')).json();
    [summary, validation, geography] = await Promise.all([verifiedJSON(pointer), verifiedJSON(pointer.validation), fetch('assets/local-geography.json').then(r => r.json())]);
    if (summary.snapshot.sha256 !== pointer.snapshot.sha256) throw new Error('Release index mismatch');
    index = makeIndex(summary); geographicMap = createGeographicMap($('map'), geography); ready = true;
    $('start').value = summary.coverage.start; $('end').value = summary.coverage.end;
    if (!summary.observation_shards[selected]) selected = summary.coverage.end.slice(0, 7);
    publishedMetrics(); render();
  } catch (error) {
    $('error').hidden = false; $('error').textContent = 'Release data could not be loaded. Reload to retry.';
    $('status').textContent = 'Data unavailable';
  }
})();
