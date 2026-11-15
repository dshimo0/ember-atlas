const validDate=s=>/^\d{4}-\d{2}-\d{2}$/.test(s||'')&&Number.isFinite(Date.parse(s))&&new Date(s).toISOString().slice(0,10)===s;
export function defaultState(coverage={start:'2020-01-01',end:'2024-12-31'}) {return {area:'all',sensor:'both',start:coverage.start<'2020-01-01'?'2020-01-01':coverage.start,end:coverage.end,month:coverage.start<='2024-09-01'&&coverage.end>='2024-09-30'?'2024-09':coverage.end.slice(0,7),region:'pantanal',mode:'sp',view:'replay',benchmark:false,step:1,slide:1};}
export function readURL(url,coverage) {
  const u=new URL(url,'https://ember-atlas-opal.vercel.app'),p=u.searchParams,s=defaultState(coverage);
  if(['pantanal','southern-amazon','cerrado','gran-chaco','california','southeastern-australia','iberian-peninsula','siberia'].includes(p.get('region')))s.region=p.get('region');
  if(p.get('mode')==='nrt')s.mode='nrt';s.benchmark=p.get('benchmark')==='1';
  if(['all','north','south'].includes(p.get('area')))s.area=p.get('area');
  if(['both','MODIS_SP','VIIRS_NOAA20_SP'].includes(p.get('sensor')))s.sensor=p.get('sensor');
  if(validDate(p.get('start')))s.start=p.get('start');if(validDate(p.get('end')))s.end=p.get('end');
  if(s.start>s.end||(Date.parse(s.end)-Date.parse(s.start))/86400000>12000){s.start=coverage?.start||'2020-01-01';s.end=coverage?.end||'2024-12-31';}
  if(/^\d{4}-(0[1-9]|1[0-2])$/.test(p.get('month')||''))s.month=p.get('month');
  if(s.month<s.start.slice(0,7)||s.month>s.end.slice(0,7))s.month=s.start.slice(0,7);
  if(['raw','reference','replay'].includes(p.get('view')))s.view=p.get('view');
  s.step=Math.max(1,Math.min(5,parseInt(p.get('step'),10)||1));s.slide=Math.max(1,Math.min(9,parseInt(p.get('slide'),10)||1));
  return s;
}
export function stateURL(path,s,hash='') {
  const p=new URLSearchParams({region:s.region||'pantanal',mode:s.mode||'sp',benchmark:s.benchmark?'1':'0',month:s.month,area:s.area,sensor:s.sensor,start:s.start,end:s.end,view:s.view});
  if(path==='/demo')p.set('step',String(s.step||1));if(path==='/pitch')p.set('slide',String(s.slide||1));
  return path+'?'+p.toString()+hash;
}
