import {escapeHTML,number} from './format.mjs';
export const scenes=[
 ['Observe the Earth','A satellite reports a thermal anomaly at a place and time. Begin with the selected study area; a detection is not a confirmed independent fire.','Explore the selected map'],
 ['Read the historical record','Select a month to connect the historical series, map and exports. Gaps remain unavailable; complete earlier months provide the historical baseline.','Inspect the activity calendar'],
 ['Meet the sensors','MODIS and VIIRS differ in resolution, sensitivity and acquisition time. The common grid counts occupied cells once per product per UTC day.','Compare the observed products'],
 ['Harmonize the observations','Training-only factors put VIIRS on the MODIS-reference scale. Reveal continuing MODIS observations as a separate benchmark, and inspect the remaining error.','Inspect the reference comparison'],
 ['Understand the evidence','A reproducible comparison includes its sources, time window, method and limitations. Export the selected evidence or inspect the full methodology.','Go to selected exports']
];
export function sourceCards(summary){
 return Object.entries(summary.product_coverage).map(([product,c])=>`<article class="source-card"><p class="eyebrow">${escapeHTML(product)}</p><h3>${product.startsWith('MODIS')?'MODIS · Terra + Aqua':'VIIRS · NOAA-20'}</h3><p>${product.startsWith('MODIS')?'Nominal 1 km thermal product':'Nominal 375 m thermal product'} · ${escapeHTML(summary.processing_class)}</p><strong>${c.start} → ${c.end}</strong><p>${number(c.retrieved_days)} retrieved UTC days. Physical footprints, sensitivity and observation opportunities differ.</p><a href="https://www.earthdata.nasa.gov/data/tools/firms">NASA FIRMS source ↗</a></article>`).join('');
}
