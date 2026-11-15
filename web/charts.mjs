import {number,escapeHTML} from './format.mjs';
export function barChart(series) {
  const max=Math.max(1,...series.map(r=>r.value??0));
  return series.map(r=>`<div class="chart-row ${r.kind}" data-series="${r.kind}" data-value="${r.value??''}"><div class="chart-label"><i class="mark ${r.kind}" aria-hidden="true"></i><span>${escapeHTML(r.name)}</span><strong>${number(r.value,r.decimals??(r.kind==='adjusted'?1:0))}</strong></div>${r.value===null?'<p class="empty-chart">Data unavailable</p>':`<div class="bar-track" role="img" aria-label="${escapeHTML(r.name)}: ${number(r.value,1)} occupied cell-days"><div class="bar-fill" style="width:${100*r.value/max}%"></div></div>`}</div>`).join('');
}
export function timeSeries(rows,view='reference',options={}) {
  const series=view==='replay'?[['replay_modis','#f3c078','Observed MODIS before cutoff'],['replay_adjusted','#c8b5ed','Adjusted VIIRS after cutoff'],['benchmark','#edf1e9','Observed holdout MODIS benchmark']]:view==='reference'?[['reference','#f3c078','MODIS reference'],['adjusted','#c8b5ed','Adjusted VIIRS']]:[['reference','#f3c078','MODIS'],['viirs','#86d6d1','VIIRS common grid']];
  const width=960,height=220,pad=32,max=Math.max(1,...rows.flatMap(r=>series.map(([k])=>r[k]??0)));
  const x=i=>pad+i*(width-2*pad)/Math.max(1,rows.length-1),y=n=>height-pad-n/max*(height-2*pad);
  let body=`<path d="M${pad},${pad}V${height-pad}H${width-pad}" fill="none" stroke="#587078"/>`;
  body+=`<text x="4" y="${pad+4}" fill="#b4c2bd" font-size="11">${number(max)}</text><text x="10" y="${height-pad+4}" fill="#b4c2bd" font-size="11">0</text>`;
  rows.forEach((r,i)=>{if(r.month.endsWith('-01')&&(+r.month.slice(0,4)-+rows[0].month.slice(0,4))%Math.max(1,Math.ceil(rows.length/120))===0)body+=`<text x="${x(i)}" y="${height-7}" fill="#b4c2bd" font-size="11">${r.month.slice(0,4)}</text>`;});
  for(const [key,color,label] of series) {
    let path='';rows.forEach((r,i)=>{if(r[key]===null){path+=' ';return;}const prev=i>0&&rows[i-1][key]!==null;path+=`${prev?'L':'M'}${x(i)},${y(r[key])} `;});
    body+=`<path d="${path}" stroke="${color}" stroke-width="2" fill="none" ${['reference','benchmark'].includes(key)?'stroke-dasharray="5 3"':''}/>`;
    rows.forEach((r,i)=>{if(r[key]!==null)body+=`<circle cx="${x(i)}" cy="${y(r[key])}" r="2.5" fill="${color}"><title>${escapeHTML(r.month+' '+label+': '+number(r[key],1)+' cell-days; '+r.phase)}</title></circle>`;});
  }
  if(options.cutoff){const i=rows.findIndex(r=>r.month===options.cutoff);if(i>=0)body+=`<path d="M${x(i)} 15V${height-pad}" stroke="#aabdbb" stroke-dasharray="3 3"/><text x="${Math.min(x(i)+5,width-130)}" y="14" fill="#c8b5ed" font-size="11">Replay cutoff ${options.cutoff}</text>`;}
  return `<svg class="activity-series" viewBox="0 0 ${width} ${height}" role="img" aria-label="Selected-date monthly ${view==='replay'?'Sensor transition replay with separate observed benchmark':view==='reference'?'MODIS and adjusted VIIRS on MODIS-reference scale':'sensor-specific common-grid activity'}. Missing months are gaps; units are occupied cell-days.">${body}</svg>`;
}
