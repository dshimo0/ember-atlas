import {occupiedDays} from './model.mjs';
import './vendor/leaflet/leaflet.js';
const L = globalThis.L;
const STUDY = [[-23, -59], [-15, -54]];
const AREA_BOUNDS = {all: STUDY, north: [[-19, -59], [-15, -54]], south: [[-23, -59], [-19, -54]]};
const credit = '<a href="https://www.openstreetmap.org/copyright">© OpenStreetMap contributors</a>';

const DiamondCanvas=L.Canvas.extend({
  _updateDiamond(layer){
    if(!this._drawing||layer._empty())return;
    const p=layer._point,r=layer._radius,ctx=this._ctx;
    ctx.beginPath();ctx.moveTo(p.x,p.y-r);ctx.lineTo(p.x+r,p.y);ctx.lineTo(p.x,p.y+r);ctx.lineTo(p.x-r,p.y);ctx.closePath();this._fillStroke(ctx,layer);
  }
});
const DiamondMarker=L.CircleMarker.extend({_updatePath(){this._renderer._updateDiamond(this);}});
export function createGeographicMap(element, geography) {
  const map = L.map(element, {preferCanvas: true, scrollWheelZoom: true, minZoom: 1, maxZoom: 17, zoomControl: true});
  map.createPane('local-geography'); map.getPane('local-geography').style.zIndex = 180;
  map.createPane('local-labels'); map.getPane('local-labels').style.zIndex = 185;
  L.control.scale({imperial: false, maxWidth: 100}).addTo(map);
  map.attributionControl.addAttribution('<a href="https://www.naturalearthdata.com/about/terms-of-use/">Local: Natural Earth</a>');
  L.geoJSON(geography.countries, {pane: 'local-geography', interactive: false, style: {color: '#9baea3', weight: 1, fillColor: '#edf0e4', fillOpacity: 1}}).addTo(map);
  L.geoJSON(geography.rivers, {pane: 'local-geography', interactive: false, style: {color: '#63a0bc', weight: 1.5, opacity: .9}}).addTo(map);
  const countries = new Set(geography.countries.features.map(f=>f.properties.ADMIN));
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
  map.createPane('observations');map.getPane('observations').style.zIndex=450;
  map.createPane('study-bounds');map.getPane('study-bounds').style.zIndex=470;
  const sensorRenderer=new DiamondCanvas({padding:.2,pane:'observations'});
  let lastRows=[],lastSelection=null;
  let studyBounds=STUDY;
  const study = L.rectangle(STUDY, {pane:'study-bounds',color: '#8e3a19', weight: 2.5, dashArray: '8 4', fill: false, interactive: false}).addTo(map);
  let areaLayer = null, pointLayer = L.layerGroup().addTo(map), tileLayer = null, timer = null, generation = 0, lastArea = 'pantanal|all';
  const modeSelect = document.getElementById('basemapMode'), status = document.getElementById('basemapStatus');
  function local(unavailable = false) {
    generation++; clearTimeout(timer);
    if (tileLayer) {map.removeLayer(tileLayer); tileLayer = null;}
    element.dataset.basemap = 'local'; modeSelect.value = 'local';
    status.textContent = unavailable ? 'Local map · basemap unavailable' : 'Local map · Natural Earth';
  }
  function street(kind = 'street') {
    local(); const active = ++generation;
    element.dataset.basemap = 'loading'; modeSelect.value = kind; status.textContent = 'Loading basemap…';
    tileLayer = L.tileLayer(kind === 'satellite' ? 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}' : 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: kind === 'satellite' ? 'Imagery © Esri, Maxar, Earthstar Geographics, and the GIS User Community · contextual mosaic' : credit, maxZoom: 17, crossOrigin: true});
    tileLayer.on('load', () => {
      if (active !== generation) return;
      clearTimeout(timer); element.dataset.basemap = kind; status.textContent = kind === 'satellite' ? 'Satellite imagery · Esri · dates vary; not selected-month observations' : 'Street map · OpenStreetMap';
    });
    // A failed tile or slow provider leaves a complete local map, not blank geography.
    tileLayer.on('tileerror', () => {if (active === generation) local(true);});
    tileLayer.addTo(map);
    timer = setTimeout(() => {if (active === generation && element.dataset.basemap === 'loading') local(true);}, 12000);
  }
  modeSelect.addEventListener('change', () => modeSelect.value === 'local' ? local() : street(modeSelect.value));
  function publishView() {
    element.dataset.zoom = String(map.getZoom());
    element.dataset.center = JSON.stringify([map.getCenter().lat, map.getCenter().lng]);
    element.dataset.bounds = JSON.stringify([[map.getBounds().getSouth(), map.getBounds().getWest()], [map.getBounds().getNorth(), map.getBounds().getEast()]]);
  }
  map.on('moveend zoomend', publishView);
  function fit() {map.fitBounds(studyBounds, {padding: [20, 20], animate: false});}
  document.getElementById('fitStudyArea').addEventListener('click', fit);
  fit(); street();
  new ResizeObserver(() => map.invalidateSize({pan: false})).observe(element);
  element.setAttribute('tabindex', '0');
  element.setAttribute('aria-label', 'Study area map. Arrow keys pan; plus and minus zoom.');
  function update(rows, selection) {
      lastRows=rows;lastSelection=selection;
      const bounds=selection.bounds||[-59,-23,-54,-15];studyBounds=[[bounds[1],bounds[0]],[bounds[3],bounds[2]]];study.setBounds(studyBounds);
      pointLayer.clearLayers();
      const stride = Math.max(1, Math.ceil(rows.length / 4000));
      for (let i = 0; i < rows.length; i += stride) {
        const r = rows[i], modis = r.product.startsWith('MODIS');
        if(!document.getElementById('showPoints').checked)continue;
        if(!(modis?document.getElementById('layerModis').checked:document.getElementById('layerViirs').checked))continue;
        const marker=(modis?L.circleMarker:(latlng,options)=>new DiamondMarker(latlng,options));
        const tooltip=document.createElement('div');
        for(const [label,value] of [['Product',r.product],['Platform',r.platform],['Acquired',r.date_utc+' '+r.time_utc.slice(0,2)+':'+r.time_utc.slice(2)+' UTC'],['FRP (MW)',r.frp_mw],['Confidence',r.confidence],['Reported source version',r.source_version||'Not provided'],['Reported thermal type',r.detection_type||'Not provided'],['Day/night',r.daynight],['Coordinates',r.latitude+', '+r.longitude],['Source',r.source]]){const line=document.createElement('div');line.textContent=label+': '+(value??'Unavailable');tooltip.append(line);}
        marker([r.latitude, r.longitude], {renderer:sensorRenderer,radius: modis ? 2.7 : 3.5, color: modis ? '#6e3b16' : '#15677c', weight: modis ? .6 : 1.1, fillColor: modis ? '#e6802a' : '#66c9da', fillOpacity: modis ? .85 : .28, product: r.product})
          .bindTooltip(tooltip,{className:'observation-tooltip'}).bindPopup(tooltip.cloneNode(true)).addTo(pointLayer);
      }
      const pointCount=pointLayer.getLayers().length;
      const product=document.getElementById('mapProduct').value.replace('_SP',selection.mode==='nrt'?'_NRT':'_SP');
      const grid=occupiedDays(rows,product),gridAvailable=selection.retrieved_products?selection.retrieved_products.includes(product):true;
      if(document.getElementById('showGrid').checked)for(const c of grid){
        L.rectangle([[c.lat*.05,c.lon*.05],[(c.lat+1)*.05,(c.lon+1)*.05]],{renderer:sensorRenderer,color:product.startsWith('MODIS')?'#8a5718':'#147185',weight:.25,fillColor:(product.startsWith('MODIS')?['#ffd166','#fca636','#ed6925','#c13b13','#7f230b']:['#a4e8e0','#56c5cc','#169db6','#087692','#034c67'])[Math.min(4,Math.floor((c.occupied_days-1)/Math.max(1,(selection.period_days||31)/5)))],fillOpacity:.85})
         .bindTooltip(`${product}: ${c.occupied_days} occupied UTC days in this 0.05° cell. ${c.dates.join(', ')}. Observed occupancy, no spatial adjustment.`).addTo(pointLayer);
      }
      if (areaLayer) {map.removeLayer(areaLayer);areaLayer=null;}
      const selectedBounds=selection.area==='all'?studyBounds:AREA_BOUNDS[selection.area];
      if(selection.area!=='all')areaLayer=L.rectangle(selectedBounds,{pane:'study-bounds',color:'#183d6a',weight:2.5,fill:false,interactive:false}).addTo(map);
      study.bringToFront();const areaKey=(selection.region||'pantanal')+'|'+selection.area;
      if(areaKey!==lastArea){map.fitBounds(selectedBounds,{padding:[25,25],animate:false});lastArea=areaKey;}
      const layers = pointLayer.getLayers(), first = pointCount?layers[0]:null;
      element.dataset.points = String(pointCount); element.dataset.observations = String(rows.length);
      element.dataset.region=selection.region||'pantanal';element.dataset.gridCells=String(grid.length);element.dataset.gridAvailable=String(gridAvailable);element.dataset.cellDays=!gridAvailable?'':String(grid.reduce((n,c)=>n+c.occupied_days,0));element.dataset.gridProduct=product;
      element.dataset.area = selection.area; element.dataset.sensor = selection.sensor; element.dataset.month = selection.month;
      element.dataset.sample = first ? JSON.stringify({latitude: first.getLatLng().lat, longitude: first.getLatLng().lng, product: first.options.product}) : '';
      element.dispatchEvent(new CustomEvent('mapdisplaychange',{detail:{shown:pointCount,total:rows.length,gridCells:grid.length,cellDays:grid.reduce((n,c)=>n+c.occupied_days,0),product,periodDays:selection.period_days||31,gridAvailable:gridAvailable}}));
      return pointCount;
  }
  for(const id of ['layerModis','layerViirs','showGrid','showPoints','mapProduct'])document.getElementById(id).addEventListener('change',()=>{if(lastSelection)update(lastRows,lastSelection);});
  return {update,resize(){map.invalidateSize({pan:false});}};
}
