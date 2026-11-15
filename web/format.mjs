export const number=(value,decimals=0)=>value===null||value===undefined?'—':Number(value).toLocaleString('en-US',{minimumFractionDigits:decimals,maximumFractionDigits:decimals});
export const signed=(value,decimals=1)=>value===null||value===undefined||!Number.isFinite(value)?'—':(value>0?'+':value<0?'−':'')+number(Math.abs(value),decimals);
export const yearsLabel=years=>years.length>1?`${years[0]}–${years.at(-1)}`:String(years[0]);
export const escapeHTML=value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

export const compact=value=>value===null||value===undefined||!Number.isFinite(value)?'—':new Intl.NumberFormat('en-US',{notation:'compact',maximumFractionDigits:1}).format(value).toLowerCase();
