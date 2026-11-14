import {PRODUCTS, SENSOR_NAMES, AREAS, monthEnd, monthName, monthsBetween, selectedProducts, scope, makeIndex, aggregateMonth, adjustment, historicalBaseline, filterObservations, observationCSV, aggregateCSV} from './model.mjs';
const $ = id => document.getElementById(id);
const number = (value, decimals = 0) => value === null || value === undefined ? '—' : Number(value).toLocaleString('en-US', {minimumFractionDigits: decimals, maximumFractionDigits: decimals});
const compact = value => value === null ? '—' : value >= 1000 ? (value / 1000).toFixed(1) + 'k' : String(value);
const signed = (value, decimals = 1) => (value > 0 ? '+' : value < 0 ? '−' : '') + number(Math.abs(value), decimals);
let summary, validation, index, geography, selected = '2024-09', observations = [], selectionToken = 0, loadedSelection = '', ready = false;
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
  $('resultLabel').textContent = validation.accepted ? 'lower monthly error in the holdout' : 'Adjustment not supported by this release';
  $('mae').textContent = `${number(validation.unadjusted.mae, 1)} → ${number(validation.adjusted.mae, 1)}`;
  $('split').innerHTML = `<span>TRAIN ${yearsLabel(validation.train_years)}</span><span>HOLDOUT ${yearsLabel(validation.holdout_years)} · ${validation.adjusted.n} paired months</span>`;
  $('validationLink').href = 'data/' + summary.validation.file;
  const showcase = summary.coverage.end.slice(0, 4) === '2024' ? '2024-09' : selected;
  const showcaseState = {...state(), start: summary.coverage.start, end: summary.coverage.end, area: 'all'};
  const showcaseAbove = PRODUCTS.every(product => historicalBaseline(index, showcase, product, showcaseState, validation)?.difference > 0);
  $('heroFinding').textContent = showcaseAbove ? `${monthName(showcase)}: both products recorded activity above their own same-month historical medians.` : 'Explore the sensor-specific historical record below.';
  $('coverage').textContent = `Aggregates + observation exports: ${summary.coverage.start} → ${summary.coverage.end} UTC`;
  $('validation').textContent = `The ${validation.adjusted.n} matched holdout months in ${yearsLabel(validation.holdout_years)} were excluded from fitting. Training: ${yearsLabel(validation.train_years)}. The frozen rule ${validation.accepted ? 'passed' : 'did not pass'}. These errors measure agreement with MODIS in the full Pantanal study area, not accuracy against ground truth.`;
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
    const phase = validation.train_years.includes(+year) ? 'TRAIN' : validation.holdout_years.includes(+year) ? 'HOLDOUT' : 'OUTSIDE RELEASE';
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
      const columns = matchMedia('(max-width:600px)').matches ? 4 : 12;
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
    const direction = baselines.every(v => v.baseline.difference > 0) ? 'above' : baselines.every(v => v.baseline.difference < 0) ? 'below' : 'on different sides of';
    $('findingTitle').textContent = direction === 'above' ? 'More activity in both records.' : direction === 'below' ? 'Less activity in both records.' : 'Read each sensor separately.';
    if (baselines.length === 1) $('findingTitle').textContent = `${SENSOR_NAMES[baselines[0].product]} seasonal comparison`;
    $('takeaway').textContent = `${baselines.length === 2 ? 'Both products recorded' : SENSOR_NAMES[baselines[0].product] + ' recorded'} activity ${direction} ${baselines.length === 2 ? 'their respective' : 'its'} same-month historical median${baselines.length === 2 ? 's' : ''} in ${monthName(selected)}.`;
  } else {
    $('findingTitle').textContent = 'Inspect the observed activity.';
    $('takeaway').textContent = s.area !== 'all' ? 'Historical anomalies are not validated for this subregion. The sensor-specific observations remain available.' : values.some(v => !v.complete) ? 'A complete selected month is required for a historical comparison. Missing retrieval is not zero activity.' : 'At least three complete prior years for this calendar month are required. This release has an insufficient historical baseline for the selection.';
  }
  $('baseline').innerHTML = baselines.map(v => {
    const b = v.baseline, name = SENSOR_NAMES[v.product], mark = v.product === 'MODIS_SP' ? 'modis' : 'viirs';
    return `<div class="baseline-row"><div><span><i class="mark ${mark}" aria-hidden="true"></i>${name}</span><strong>${b ? signed(b.percent, 1) + '%' : '—'}</strong></div>${b ? `<p>${number(v.cells)} cell-days vs median <b>${number(b.median, b.median % 1 ? 1 : 0)}</b> · ${signed(b.difference, 0)} cell-days</p><details><summary>Baseline ${yearsLabel(b.entries.map(e => e.year))} · n = ${b.n} prior years</summary><div class="baseline-values">${b.entries.map(e => `${e.year}: ${number(e.value)} cell-days`).join('<br>')}<br>Selected year excluded.</div></details>` : `<p>${v.status}; ${v.retrieved}/${v.expected} selected UTC days retrieved. Baseline unavailable.</p>`}</div>`;
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
    $('adjusted').textContent = `Adjusted VIIRS is ${number(Math.abs(delta), 1)} cell-days ${delta < 0 ? 'below' : 'above'} MODIS${pct !== null ? ` (${signed(pct)}%)` : ''} this month. The adjustment ${Math.abs(delta) < Math.abs(v.cells - m.cells) ? 'moved VIIRS closer to' : 'did not move VIIRS closer to'} the reference.`;
  } else $('adjusted').textContent = 'The selected observations are shown separately by sensor. No adjusted estimate is applied to this view.';
  $('scopeNotice').classList.toggle('warning', s.area !== 'all');
  $('scopeNotice').textContent = s.area !== 'all' ? 'Adjustment unavailable: the seasonal factors were validated only for the full Pantanal study area. A subregion needs its own independent fit and evaluation.' : !v.complete ? 'Adjustment unavailable for a missing or partial month. Counts reflect only retrieved dates inside your selected range.' : s.sensor === 'MODIS_SP' ? 'MODIS is the reference; select both sensors to inspect the VIIRS adjustment.' : a ? `Factor ${number(a.factor, 4)}, fit on ${yearsLabel(validation.train_years)}. Comparison is agreement with MODIS, not ground-truth accuracy.` : 'Adjustment unavailable: this month is outside the accepted validation domain.';
  $('nativeCounts').innerHTML = `<table><thead><tr><th>Product</th><th>Native detections</th><th>Retrieval</th></tr></thead><tbody>${values.map(r => `<tr><th>${SENSOR_NAMES[r.product]}</th><td>${number(r.native)}</td><td>${r.status}<br>${r.retrieved}/${r.expected} days</td></tr>`).join('')}</tbody></table>`;
}
function project(lon, lat) { return [20 + (lon + 66) / 18 * 580, 20 + (-10 - lat) / 16 * 440]; }
function geometryPath(geometry) {
  const polygons = geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates;
  return polygons.map(polygon => polygon.map(ring => ring.map((c, i) => `${i ? 'L' : 'M'}${project(c[0], c[1]).map(n => n.toFixed(2)).join(',')}`).join('') + 'Z').join('')).join('');
}
function map(s, rows = []) {
  let shapes = '<defs><clipPath id="mapClip"><rect x="20" y="20" width="580" height="440"/></clipPath></defs><g clip-path="url(#mapClip)">';
  if (geography) for (const country of geography.features) shapes += `<path d="${geometryPath(country.geometry)}" fill="#20383c" stroke="#6c8581" stroke-width=".8"/>`;
  for (const lon of [-65, -60, -55, -50]) { const [x] = project(lon, -10); shapes += `<path d="M${x},20V460" stroke="#527077" stroke-opacity=".22"/>`; }
  for (const lat of [-10, -15, -20, -25]) { const [, y] = project(-66, lat); shapes += `<path d="M20,${y}H600" stroke="#527077" stroke-opacity=".22"/>`; }
  const stride = Math.max(1, Math.ceil(rows.length / 4000)), sampled = rows.filter((r, i) => i % stride === 0);
  for (const r of sampled) { const [x, y] = project(r.longitude, r.latitude); shapes += r.product === 'MODIS_SP' ? `<circle cx="${x}" cy="${y}" r="1.8" fill="#f3c078" opacity=".7"/>` : `<path d="M${x},${y - 2}l2,2l-2,2l-2,-2Z" fill="#86d6d1" opacity=".65"/>`; }
  const [x, y] = project(-59, -15), [right, bottom] = project(-54, -23), middle = project(-59, -19)[1];
  shapes += `<rect x="${x}" y="${y}" width="${right - x}" height="${bottom - y}" fill="none" stroke="#f4d7a0" stroke-width="2" stroke-dasharray="7 3"/>`;
  for (const area of ['north', 'south']) {
    const top = area === 'north' ? y : middle, height = area === 'north' ? middle - y : bottom - middle;
    shapes += `<g class="map-area" role="button" tabindex="0" data-area="${area}" aria-label="Select ${AREAS[area]}"><title>Select ${AREAS[area]}</title><rect x="${x}" y="${top}" width="${right - x}" height="${height}" fill="${s.area === area ? '#e9d398' : '#ffffff'}" fill-opacity="${s.area === area ? '.12' : '.001'}" stroke="${s.area === area ? '#fff1bb' : 'none'}" stroke-width="2"/></g>`;
  }
  shapes += '</g>';
  for (const name of ['Brazil', 'Bolivia', 'Paraguay']) {
    const f = geography?.features.find(f => f.properties.ADMIN === name);
    if (f) { const [tx, ty] = project(f.properties.LABEL_X, f.properties.LABEL_Y); shapes += `<text x="${tx}" y="${ty}" font-size="11" fill="#d7e2d5" text-anchor="middle" letter-spacing="2">${name.toUpperCase()}</text>`; }
  }
  for (const lon of [-65, -60, -55, -50]) shapes += `<text x="${project(lon, -10)[0]}" y="14" font-size="9" fill="#9db2ad" text-anchor="middle">${Math.abs(lon)}°W</text>`;
  for (const lat of [-15, -20, -25]) shapes += `<text x="4" y="${project(-66, lat)[1]}" font-size="9" fill="#9db2ad" transform="rotate(-90 10 ${project(-66, lat)[1]})">${Math.abs(lat)}°S</text>`;
  $('map').innerHTML = shapes;
  for (const button of $('map').querySelectorAll('[data-area]')) {
    const choose = () => { $('area').value = button.dataset.area; render(); };
    button.addEventListener('click', choose); button.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); choose(); } });
  }
  $('mapMonth').textContent = `${monthName(selected)} · ${AREAS[s.area]} · ${s.sensor === 'both' ? 'Both sensors' : SENSOR_NAMES[s.sensor]}`;
  if (loadedSelection === selectionKey(s)) $('mapLoading').textContent = `${number(sampled.length)} of ${number(rows.length)} matching observations shown. The CSV contains all ${number(rows.length)} records.`;
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
  $('mapLoading').textContent = 'Loading checksum-verified observations for this month…'; map(s);
  if (!values.some(v => v.retrieved)) {
    $('mapLoading').textContent = 'Data unavailable: no retrieval for this selection. No observations are inferred.';
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
    $('mapLoading').textContent = 'Observation file unavailable. Aggregates remain accessible; observation export is disabled. Reload to retry.';
    $('observationScope').textContent = 'Observation export unavailable; no data were substituted.';
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
  $('monthPhase').textContent = validation.holdout_years.includes(+selected.slice(0, 4)) ? 'HOLDOUT YEAR · NOT USED TO FIT THE FACTORS' : validation.train_years.includes(+selected.slice(0, 4)) ? 'TRAINING YEAR' : 'OUTSIDE RELEASE COVERAGE';
  $('status').textContent = available ? `${count === 0 ? 'No detections recorded · ' : ''}${number(count)} observations selected · ${values.every(v => v.complete) ? 'Complete monthly retrieval' : 'Partial month / mixed retrieval'} · observation coverage unknown` : 'Data unavailable · no retrieval for the selected month';
  $('selection').innerHTML = `<span>MONTH <strong>${monthName(selected)}</strong></span><span>AREA <strong>${AREAS[s.area]}</strong></span><span>SENSOR <strong>${s.sensor === 'both' ? 'Both sensors' : SENSOR_NAMES[s.sensor]}</strong></span><span>OBSERVATIONS <strong>${available ? number(count) : 'Unavailable'}</strong></span><span>UTC <strong>${dates.from} → ${dates.to}</strong></span>`;
  baselineView(s, values); comparison(s, values); calendar(s);
  $('aggregateDownload').disabled = false;
  $('aggregateScope').textContent = `${s.start} → ${s.end} UTC · ${monthsBetween(s.start, s.end).length} months · selected area & sensors · missing values stay blank`;
  loadObservations(s, values);
}
function download(text, filename) { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([text], {type: 'text/csv;charset=utf-8'})); a.download = filename; a.click(); setTimeout(() => URL.revokeObjectURL(a.href), 1000); }
$('download').addEventListener('click', () => { const s = state(); if (loadedSelection !== selectionKey(s)) return; download(observationCSV(observations, summary.snapshot.sha256), `ember-observations-${selected}-${s.area}-${s.sensor}.csv`); });
$('aggregateDownload').addEventListener('click', () => { const s = state(); download(aggregateCSV(index, s, validation, summary.snapshot.sha256), `ember-aggregates-${s.start}_${s.end}-${s.area}-${s.sensor}.csv`); });
for (const id of ['area', 'start', 'end', 'sensor']) $(id).addEventListener('change', render);
$('resetArea').addEventListener('click', () => { $('area').value = 'all'; render(); });
(async () => {
  try {
    const pointer = await (await fetch('data/dashboard.json')).json();
    [summary, validation, geography] = await Promise.all([verifiedJSON(pointer), verifiedJSON(pointer.validation), fetch('assets/geography.json').then(r => r.json())]);
    if (summary.snapshot.sha256 !== pointer.snapshot.sha256) throw new Error('Release index mismatch');
    index = makeIndex(summary); ready = true;
    $('start').value = summary.coverage.start; $('end').value = summary.coverage.end;
    if (!summary.observation_shards[selected]) selected = summary.coverage.end.slice(0, 7);
    publishedMetrics(); render();
  } catch (error) {
    $('error').hidden = false; $('error').textContent = 'The verified release could not be loaded. Please reload. No substitute data are shown.';
    $('status').textContent = 'Data unavailable';
  }
})();
