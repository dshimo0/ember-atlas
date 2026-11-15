import {defaultState,stateURL} from './url-state.mjs';
import {escapeHTML,number} from './format.mjs';
export function regionURL(r){return stateURL('/',{...defaultState(r.datasets.sp.coverage),region:r.id,mode:'sp',view:r.id==='pantanal'?'replay':'raw'});}
export function worldMap(registry,geography){
 const x=lon=>(lon+180)*960/360,y=lat=>(90-lat)*440/180;
 const ring=coordinates=>coordinates.map((c,i)=>`${i?'L':'M'}${x(c[0]).toFixed(1)},${y(c[1]).toFixed(1)}`).join(' ')+'Z';
 const land=geography.countries.features.map(f=>{const g=f.geometry,polys=g.type==='Polygon'?[g.coordinates]:g.coordinates;return `<path d="${polys.flatMap(p=>p.map(ring)).join(' ')}" fill="#2c464d" stroke="#617477" stroke-width=".4"/>`;}).join('');
 const offsets=[[-24,14],[-30,-18],[22,-3],[-28,19],[0,0],[0,0],[0,0],[0,0]];
 const areas=registry.regions.map((r,i)=>{const [w,s,e,n]=r.bounds,cx=x((w+e)/2),cy=y((s+n)/2),[dx,dy]=offsets[i];return `<a data-route href="${regionURL(r)}" aria-label="Explore ${escapeHTML(r.name)} study area"><title>${escapeHTML(r.name)}: ${r.datasets.sp.coverage.start} to ${r.datasets.sp.coverage.end}; ${number(r.datasets.sp.observations)} SP observations</title><rect x="${x(w)}" y="${y(n)}" width="${x(e)-x(w)}" height="${y(s)-y(n)}" fill="#f3c078" fill-opacity=".12" stroke="#f3c078"/><path d="M${cx},${cy}L${cx+dx},${cy+dy}" stroke="#f3c078"/><circle cx="${cx+dx}" cy="${cy+dy}" r="10" fill="#122129" stroke="#f3c078"/><text x="${cx+dx}" y="${cy+dy+4}" text-anchor="middle" fill="#fff" font-size="12">${i+1}</text></a>`;}).join('');
 return `<svg class="world-map" viewBox="0 0 960 440" role="img" aria-label="Eight project-defined study areas on an attributed Natural Earth world map; each numbered area links to Explore">${land}${areas}</svg><p class="pitch-foot">Country context: Natural Earth, public domain. Study boxes: Ember Atlas registry v1; not biome masks.</p>`;
}
