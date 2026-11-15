import {escapeHTML,number} from './format.mjs';
export const scenes=[
 ['Different sensors, different reports','Resolution, sensitivity and acquisition time affect what gets recorded. Compare the same region and month on a shared grid.','Compare the sensors'],
 ['Inspect the selected month','Choose a study area and a complete month. The map uses actual FIRMS observations; native detections are not independent fires.','Inspect the map'],
 ['Read the activity calendar','Select a month to connect the calendar, geography and exports. Earlier complete same-month years provide historical context.','Open the calendar'],
 ['Validate and export','Compare adjusted VIIRS with continuing MODIS observations, inspect remaining error and download matching evidence. MODIS is a reference, not ground truth.','Export selected observations']
];
export function sourceCards(summary){
 return Object.entries(summary.product_coverage).map(([product,c])=>`<article class="source-card"><p class="eyebrow">${escapeHTML(product)}</p><h3>${product.startsWith('MODIS')?'MODIS · Terra + Aqua':'VIIRS · NOAA-20'}</h3><p>${product.startsWith('MODIS')?'Nominal 1 km thermal product':'Nominal 375 m thermal product'} · ${escapeHTML(summary.processing_class)}</p><strong>${c.start} → ${c.end}</strong><p>${number(c.retrieved_days)} retrieved UTC days. Physical footprints, sensitivity and observation opportunities differ.</p><a href="https://www.earthdata.nasa.gov/data/tools/firms">NASA FIRMS source ↗</a></article>`).join('');
}
