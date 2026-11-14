import './vendor/leaflet/leaflet.js';
const L = globalThis.L;
const STUDY = [[-23, -59], [-15, -54]];
const AREA_BOUNDS = {all: STUDY, north: [[-19, -59], [-15, -54]], south: [[-23, -59], [-19, -54]]};
const credit = '<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>';

export function createGeographicMap(element, geography) {
  const map = L.map(element, {preferCanvas: true, scrollWheelZoom: false, minZoom: 3, maxZoom: 17, zoomControl: true});
  map.createPane('local-geography'); map.getPane('local-geography').style.zIndex = 180;
  map.createPane('local-labels'); map.getPane('local-labels').style.zIndex = 185;
  L.control.scale({imperial: false, maxWidth: 100}).addTo(map);
  map.attributionControl.addAttribution('<a href="https://www.naturalearthdata.com/about/terms-of-use/">Local: Natural Earth</a>');
  L.geoJSON(geography.countries, {pane: 'local-geography', interactive: false, style: {color: '#9baea3', weight: 1, fillColor: '#edf0e4', fillOpacity: 1}}).addTo(map);
  L.geoJSON(geography.rivers, {pane: 'local-geography', interactive: false, style: {color: '#63a0bc', weight: 1.5, opacity: .9}}).addTo(map);
  const countries = new Set(['Brazil', 'Bolivia', 'Paraguay']);
  for (const feature of geography.countries.features) if (countries.has(feature.properties.ADMIN)) {
    L.tooltip({permanent: true, pane: 'local-labels', className: 'local-country-label', direction: 'center'})
      .setLatLng([feature.properties.LABEL_Y, feature.properties.LABEL_X]).setContent(feature.properties.ADMIN).addTo(map);
  }
  const labeledRivers = new Set();
  for (const feature of geography.rivers.features) {
    const name = feature.properties.name_en || feature.properties.name;
    if (!name || !['Paraguay', 'Paraná', 'Parana'].includes(name) || labeledRivers.has(name)) continue;
    const line = feature.geometry.type === 'LineString' ? feature.geometry.coordinates : feature.geometry.coordinates[0];
    if (!line?.length) continue;
    const position = line[Math.floor(line.length / 2)];
    L.tooltip({permanent: true, pane: 'local-labels', className: 'local-river-label', direction: 'left'})
      .setLatLng([position[1], position[0]]).setContent(name).addTo(map);
    labeledRivers.add(name);
  }
  L.geoJSON(geography.places, {pane: 'local-geography', interactive: false, pointToLayer(feature, latlng) {
    return L.circleMarker(latlng, {pane: 'local-geography', radius: 2, color: '#344e58', weight: 1, fillOpacity: 1})
      .bindTooltip(feature.properties.name, {permanent: true, pane: 'local-labels', direction: 'right', className: 'local-place-label'});
  }}).addTo(map);
  const study = L.rectangle(STUDY, {color: '#8e3a19', weight: 2.5, dashArray: '8 4', fill: false, interactive: false}).addTo(map);
  let areaLayer = null, pointLayer = L.layerGroup().addTo(map), tileLayer = null, timer = null, generation = 0, lastArea = 'all';
  const modeSelect = document.getElementById('basemapMode'), status = document.getElementById('basemapStatus');
  function local(unavailable = false) {
    generation++; clearTimeout(timer);
    if (tileLayer) {map.removeLayer(tileLayer); tileLayer = null;}
    element.dataset.basemap = 'local'; modeSelect.value = 'local';
    status.textContent = unavailable ? 'Local map · basemap unavailable' : 'Local map · Natural Earth';
  }
  function street() {
    local(); const active = ++generation;
    element.dataset.basemap = 'loading'; modeSelect.value = 'street'; status.textContent = 'Loading street map…';
    tileLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: credit, maxZoom: 17, crossOrigin: true});
    tileLayer.on('tileload', () => {
      if (active !== generation) return;
      clearTimeout(timer); element.dataset.basemap = 'street'; status.textContent = 'Street map · OpenStreetMap';
    });
    // A failed tile or slow provider leaves a complete local map, not blank geography.
    tileLayer.on('tileerror', () => {if (active === generation) local(true);});
    tileLayer.addTo(map);
    timer = setTimeout(() => {if (active === generation && element.dataset.basemap !== 'street') local(true);}, 7000);
  }
  modeSelect.addEventListener('change', () => modeSelect.value === 'street' ? street() : local());
  function publishView() {
    element.dataset.zoom = String(map.getZoom());
    element.dataset.center = JSON.stringify([map.getCenter().lat, map.getCenter().lng]);
    element.dataset.bounds = JSON.stringify([[map.getBounds().getSouth(), map.getBounds().getWest()], [map.getBounds().getNorth(), map.getBounds().getEast()]]);
  }
  map.on('moveend zoomend', publishView);
  function fit() {map.fitBounds(STUDY, {padding: [20, 20], animate: false});}
  document.getElementById('fitStudyArea').addEventListener('click', fit);
  fit(); street();
  new ResizeObserver(() => map.invalidateSize({pan: false})).observe(element);
  element.setAttribute('tabindex', '0');
  element.setAttribute('aria-label', 'Study area map. Arrow keys pan; plus and minus zoom.');
  return {
    update(rows, selection) {
      pointLayer.clearLayers();
      const stride = Math.max(1, Math.ceil(rows.length / 4000));
      for (let i = 0; i < rows.length; i += stride) {
        const r = rows[i], modis = r.product === 'MODIS_SP';
        L.circleMarker([r.latitude, r.longitude], {radius: modis ? 2.7 : 3, color: modis ? '#6e3b16' : '#15677c', weight: modis ? .6 : 1.1, fillColor: modis ? '#e6802a' : '#66c9da', fillOpacity: modis ? .85 : .28, product: r.product})
          .bindTooltip(`${modis ? 'MODIS' : 'NOAA-20 VIIRS'} · ${r.date_utc} ${r.time_utc.slice(0,2)}:${r.time_utc.slice(2)} UTC`).addTo(pointLayer);
      }
      if (areaLayer) {map.removeLayer(areaLayer); areaLayer = null;}
      if (selection.area !== 'all') areaLayer = L.rectangle(AREA_BOUNDS[selection.area], {color: '#183d6a', weight: 2.5, fillColor: '#5c9dc1', fillOpacity: .08, interactive: false}).addTo(map);
      study.bringToFront();
      if (selection.area !== lastArea) {map.fitBounds(AREA_BOUNDS[selection.area], {padding: [25,25], animate: false}); lastArea = selection.area;}
      const layers = pointLayer.getLayers(), first = layers[0];
      element.dataset.points = String(layers.length); element.dataset.observations = String(rows.length);
      element.dataset.area = selection.area; element.dataset.sensor = selection.sensor; element.dataset.month = selection.month;
      element.dataset.sample = first ? JSON.stringify({latitude: first.getLatLng().lat, longitude: first.getLatLng().lng, product: first.options.product}) : '';
      return layers.length;
    }
  };
}
