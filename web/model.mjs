export const PRODUCTS = ['MODIS_SP', 'VIIRS_NOAA20_SP'];
export const SENSOR_NAMES = {MODIS_SP: 'MODIS', VIIRS_NOAA20_SP: 'NOAA-20 VIIRS'};
export const AREAS = {all: 'Full Pantanal study rectangle', north: 'Northern study area', south: 'Southern study area'};
const DAY = 86400000;
export function monthEnd(month) { return new Date(Date.UTC(+month.slice(0, 4), +month.slice(5), 0)).toISOString().slice(0, 10); }
export function monthName(month) { return new Date(month + '-01T00:00:00Z').toLocaleDateString('en-US', {month: 'long', year: 'numeric', timeZone: 'UTC'}); }
export function monthsBetween(start, end) {
  const months = [];
  for (let m = start.slice(0, 7); m <= end.slice(0, 7);) {
    months.push(m);
    const d = new Date(m + '-01T00:00:00Z'); d.setUTCMonth(d.getUTCMonth() + 1); m = d.toISOString().slice(0, 7);
  }
  return months;
}
export function selectedProducts(sensor) { return sensor === 'both' ? PRODUCTS : [sensor]; }
export function scope(month, state) { return {from: month + '-01' > state.start ? month + '-01' : state.start, to: monthEnd(month) < state.end ? monthEnd(month) : state.end}; }
export function makeIndex(summary) {
  const index = new Map();
  for (const r of summary.daily) {
    const key = `${r.area}|${r.product}|${r.day.slice(0, 7)}`;
    if (!index.has(key)) index.set(key, []);
    index.get(key).push(r);
  }
  return index;
}
export function aggregateMonth(index, month, product, state) {
  const {from, to} = scope(month, state);
  const expected = from <= to ? Math.round((Date.parse(to) - Date.parse(from)) / DAY) + 1 : 0;
  const rows = (index.get(`${state.area}|${product}|${month}`) || []).filter(r => r.day >= from && r.day <= to);
  const available = rows.length > 0;
  const complete = expected > 0 && rows.length === expected && from === month + '-01' && to === monthEnd(month);
  const native = available ? rows.reduce((n, r) => n + r.native, 0) : null;
  const cells = available ? rows.reduce((n, r) => n + r.cells, 0) : null;
  return {month, product, from, to, expected, retrieved: rows.length, native, cells, complete,
    status: !available ? 'Data unavailable' : !complete ? 'Partial month' : native === 0 ? 'No detections recorded' : 'Complete month'};
}
export function adjustment(row, state, validation) {
  const released = validation.monthly.find(m => m.month === row.month);
  if (!validation.accepted || !released || !row.complete || state.area !== 'all' || row.product !== 'VIIRS_NOAA20_SP' || released.adjusted === null) return null;
  const factor = validation.factors[Math.floor((+row.month.slice(5) - 1) / 3)];
  return Number.isFinite(factor) ? {factor, value: row.cells * factor} : null;
}
export function historicalBaseline(index, month, product, state, validation) {
  // Within-sensor historical comparison uses the same spatial mask; it does not transfer calibration.
  const current = aggregateMonth(index, month, product, state);
  if (!current.complete) return null;
  const entries = [];
  const prefix = `${state.area}|${product}|`;
  const years = [...new Set([...index.keys()].filter(key => key.startsWith(prefix)).map(key => +key.split('|')[2].slice(0,4)))].sort();
  for (const year of years.filter(y => y < +month.slice(0, 4))) {
    const m = year + month.slice(4);
    const r = aggregateMonth(index, m, product, {...state, start: m + '-01', end: monthEnd(m)});
    if (r.complete) entries.push({year, value: r.cells});
  }
  if (entries.length < 3) return null;
  const sorted = entries.map(e => e.value).sort((a, b) => a - b);
  const median = (sorted[Math.floor((sorted.length - 1) / 2)] + sorted[Math.floor(sorted.length / 2)]) / 2;
  return {entries, n: entries.length, median, difference: current.cells - median, percent: median ? 100 * (current.cells / median - 1) : null};
}
export function filterObservations(rows, month, state) {
  const {from, to} = scope(month, state);
  return rows.filter(r => r.date_utc >= from && r.date_utc <= to && r.longitude >= -59 && r.longitude <= -54 && r.latitude >= -23 && r.latitude <= -15 &&
    (state.area === 'all' || (state.area === 'north' ? r.latitude >= -19 : r.latitude < -19)) && (state.sensor === 'both' || r.product === state.sensor));
}
export function gridCell(value) { return Math.floor(Math.round(value * 1e6) / 50000); }
export function csv(headers, rows) { return [headers, ...rows].map(row => row.map(v => '"' + String(v ?? '').replaceAll('"', '""') + '"').join(',')).join('\r\n'); }
export const OBSERVATION_COLUMNS = ['latitude', 'longitude', 'date_utc', 'time_utc', 'product', 'platform', 'confidence', 'frp_mw', 'daynight', 'source', 'snapshot_sha256'];
export function observationCSV(rows, snapshot) { return csv(OBSERVATION_COLUMNS, rows.map(r => OBSERVATION_COLUMNS.map(k => k === 'snapshot_sha256' ? snapshot : r[k]))); }
export function aggregateCSV(index, state, validation, snapshot) {
  const columns = ['month','area','product','from_utc','through_utc','native_detections','occupied_cell_days','retrieved_days','selected_days','retrieval_status','complete_month','metric','unit','method','observation_coverage','calibration','factor','adjusted_modis_reference_cell_days','snapshot_sha256'];
  const rows = [];
  for (const month of monthsBetween(state.start, state.end)) for (const product of selectedProducts(state.sensor)) {
    const r = aggregateMonth(index, month, product, state), a = adjustment(r, state, validation);
    rows.push([month,state.area,product,r.from,r.to,r.native,r.cells,r.retrieved,r.expected,r.status,r.complete,'occupied cells per UTC day summed over selected dates','cell-days',validation.method,'unknown',a ? 'supported full study area' : 'unavailable',a?.factor,a?.value,snapshot]);
  }
  return csv(columns, rows);
}
