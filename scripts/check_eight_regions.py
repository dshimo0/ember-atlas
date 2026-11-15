"""Signed-out region, replay, SP/NRT, map-cell and CSV acceptance checks."""
import csv,gzip,hashlib,io,json,os,math
from datetime import datetime,timezone
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('BASE_URL','http://127.0.0.1:8930').rstrip('/')
def readref(ref):
 p=(ROOT/'web/data'/ref['file']).read_bytes();p=gzip.decompress(p)if ref['file'].endswith('.gz')else p
 assert hashlib.sha256(p).hexdigest()==ref['sha256'];return json.loads(p)
registry=readref(json.loads((ROOT/'web/data/regions.json').read_text()))
def stable(page,region):
 page.wait_for_function("r=>!document.querySelector('#download').disabled&&document.querySelector('#map').dataset.region===r&&document.querySelector('#map').dataset.month===document.querySelector('#monthSelect').value",arg=region,timeout=120000)
def download(page,selector):
 with page.expect_download()as event:page.locator(selector).click()
 return Path(event.value.path()).read_bytes()
def csvrows(payload):return list(csv.DictReader(io.StringIO(payload.decode())))
def ids(rows):return {(r['product'],r['date_utc'],r['time_utc'],float(r['latitude']),float(r['longitude']),r['source'])for r in rows}
args=['--no-sandbox'];pins=os.environ.get('EMBER_BROWSER_CA_SPKI')
if pins:args.append('--ignore-certificate-errors-spki-list='+pins)
report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'registry':json.loads((ROOT/'web/data/regions.json').read_text()),'checks':[]}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for viewport,w,h in [('desktop',1440,1000),('mobile',390,844)]:
  context=b.new_context(viewport={'width':w,'height':h},has_touch=viewport=='mobile',is_mobile=viewport=='mobile',accept_downloads=True)
  page=context.new_page();errors=[];http_errors=[];console_errors=[];page.on('console',lambda m:console_errors.append(m.text)if m.type=='error'and 'tile.openstreetmap.org'not in m.location.get('url','')else None);page.on('response',lambda r:http_errors.append({'url':r.url,'status':r.status}) if r.url.startswith(BASE) and r.status>=400 else None);page.on('pageerror',lambda e:errors.append(str(e)))
  for r in registry['regions']:
   for mode in ['sp','nrt']:
    ref=r['datasets'][mode];summary=readref(ref);month='2024-09'if mode=='sp'else summary['coverage']['end'][:7]
    route='/demo'if r['id']=='pantanal'else'/'
    assert page.goto(BASE+route+'?region='+r['id']+'&mode='+mode).status==200;stable(page,r['id'])
    assert page.locator('#monthSelect').input_value()==month
    assert page.locator('#region option').all_text_contents()==[x['name']for x in registry['regions']]
    assert page.locator('#dataMode').input_value()==mode
    assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
    bounds=json.loads(page.locator('#map').get_attribute('data-bounds'));west,south,east,north=r['bounds']
    assert bounds[0][0]<=south and bounds[0][1]<=west and bounds[1][0]>=north and bounds[1][1]>=east,(r['id'],bounds)
    source=readref(summary['observation_shards'][month])['observations'];start=page.locator('#start').input_value();end=page.locator('#end').input_value();source=[x for x in source if start<=x['date_utc']<=end]
    rows=csvrows(download(page,'#download'));assert len(rows)==len(source)>0;assert ids(rows)==ids(source)
    assert all(west<=float(x['longitude'])<=east and south<=float(x['latitude'])<=north for x in rows)
    ag=csvrows(download(page,'#aggregateDownload'));selected=[x for x in ag if x['month']==month]
    assert sum(int(x['native_detections'])for x in selected)==len(rows)
    product=page.locator('#map').get_attribute('data-grid-product')
    product_rows=[x for x in rows if x['product']==product]
    occupied={(x['date_utc'],int((Decimal(str(x['latitude']))/Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR)),int((Decimal(str(x['longitude']))/Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR)))for x in product_rows}
    assert int(page.locator('#map').get_attribute('data-cell-days'))==len(occupied)
    cells=csvrows(download(page,'#downloadCells'));assert sum(int(x['occupied_days'])for x in cells)==len(occupied)
    assert all(x['product']==product and x['region']==r['id']for x in cells)
    if not ref.get('calibration',{}).get('accepted',r['id']=='pantanal'and mode=='sp'):
     assert page.locator('#comparison [data-series=adjusted]').count()==0
     assert page.locator('#downloadReplay').is_disabled()
     assert all(x['factor']==''and x['adjusted_modis_reference_cell_days']==''for x in ag)
    if mode=='nrt':
     page.locator('.dataset-details').evaluate('(d)=>d.open=true')
     assert all(x['product'].endswith('_NRT')for x in rows)
     assert 'Partial month' in page.locator('#status').inner_text()
     assert 'last retrieval' in page.locator('#datasetCoverage').inner_text()
    page.reload();stable(page,r['id']);assert page.locator('#dataMode').input_value()==mode
    if mode=='sp':
     page.locator('.map-panel').screenshot(path=str(ROOT/f'submission/region-{r["id"]}-{viewport}.png'))
    report['checks'].append({'viewport':viewport,'region':r['id'],'mode':mode,'rows':len(rows),'csv_matches_full_snapshot':True,'bounds_fit':True,'map_product':product,'map_cell_days':len(occupied),'cell_csv_reconciles':True,'refresh':True,'adjustment_supported':ref.get('calibration',{}).get('accepted',r['id']=='pantanal'and mode=='sp')})
  # New SP shards must work through their immutable public origin as well as original local files.
  for r in registry['regions']:
   summary=readref(r['datasets']['sp'])
   if summary['coverage']['end']<'2025-01-31':continue
   page.goto(BASE+'/demo?region='+r['id']+'&month=2025-01&start=2025-01-01&end=2025-01-31&view=replay');stable(page,r['id'])
   source=readref(summary['observation_shards']['2025-01'])['observations'];rows=csvrows(download(page,'#download'));assert ids(rows)==ids(source)
   ag=csvrows(download(page,'#aggregateDownload'));assert sum(int(x['native_detections'])for x in ag)==len(rows)
   v=readref(summary['validation']);month=next((x for x in v['monthly']if x['month']=='2025-01'),None);supported=bool(v['accepted']and month and month['adjusted']is not None)
   assert bool(page.locator('#comparison [data-series=adjusted]').count())==supported
   if supported:
    shown=float(page.locator('#comparison [data-series=adjusted]').get_attribute('data-value'));assert abs(shown-month['adjusted'])<1e-7
   page.reload();stable(page,r['id']);assert page.locator('#monthSelect').input_value()=='2025-01'
   if viewport=='mobile':page.locator('#filterFold').evaluate('(e)=>e.open=true')
   page.select_option('#sensor','VIIRS_NOAA20_SP');stable(page,r['id']);filtered=csvrows(download(page,'#download'));assert all(x['product']=='VIIRS_NOAA20_SP'for x in filtered);assert page.locator('#calendarView').input_value()!='replay';assert page.locator('#downloadReplay').is_disabled()
   page.select_option('#sensor','both');page.evaluate("()=>{document.querySelector('#start').value='2025-01-02';document.querySelector('#end').dispatchEvent(new Event('change',{bubbles:true}))}");stable(page,r['id']);partial=csvrows(download(page,'#download'));assert all(x['date_utc']>='2025-01-02'for x in partial);assert page.locator('#comparison [data-series=adjusted]').count()==0
   report['checks'].append({'viewport':viewport,'region':r['id'],'new_sp_month':'2025-01','rows':len(rows),'source_url':summary['observation_shards']['2025-01'].get('url'),'csv_matches_new_shard':True,'adjustment_supported_in_new_month':supported,'single_sensor_no_replay':True,'manual_date_clipped_and_adjustment_disabled':True,'refresh':True})
  # Replay cutoff, optional benchmark, no future baseline and exact monthly export.
  page.goto(BASE+'/demo?region=pantanal&view=replay&month=2022-12');stable(page,'pantanal')
  assert page.locator('#calendar [data-month="2022-12"]').get_attribute('data-source')=='MODIS_SP'
  assert page.locator('#calendar [data-month="2023-01"]').get_attribute('data-source')=='VIIRS_NOAA20_SP'
  assert page.locator('#replaySource').inner_text().find('none; observed MODIS')>=0
  page.select_option('#monthSelect','2023-01');stable(page,'pantanal')
  assert 'frozen seasonal factor' in page.locator('#replaySource').inner_text()
  page.locator('#showBenchmark').check();stable(page,'pantanal')
  assert 'Observed holdout MODIS benchmark' in page.locator('#timeSeries').inner_html()
  link=page.url;page.reload();stable(page,'pantanal');assert page.locator('#showBenchmark').is_checked()
  monthly_bytes=download(page,'#downloadReplay');monthly=csvrows(monthly_bytes);jan=next(x for x in monthly if x['month']=='2023-01');dec=next(x for x in monthly if x['month']=='2022-12')
  manifest=json.loads(download(page,'#downloadManifest'));assert manifest['replay_export']['sha256']==hashlib.sha256(monthly_bytes).hexdigest();assert manifest['observation_export']['sha256']==hashlib.sha256(download(page,'#download')).hexdigest();assert manifest['cell_export']['sha256']==hashlib.sha256(download(page,'#downloadCells')).hexdigest()
  assert jan['source_product']=='VIIRS_NOAA20_SP'and dec['source_product']=='MODIS_SP'and dec['factor']=='1'
  assert abs(float(jan['reference_scale_cell_days'])-float(page.locator('#comparison [data-series=adjusted]').get_attribute('data-value')))<1e-8
  page.go_back();stable(page,'pantanal');page.go_forward();stable(page,'pantanal')
  page.locator('#fullArchive').click();stable(page,'pantanal');archive_months=page.locator('#calendar [data-month]').count();coverage=registry['regions'][0]['datasets']['sp']['coverage'];assert archive_months==(int(coverage['end'][:4])-int(coverage['start'][:4]))*12+int(coverage['end'][5:7])-int(coverage['start'][5:7])+1
  page.select_option('#monthSelect','2000-11');stable(page,'pantanal')
  assert page.locator('#calendar [data-month="2000-11"]').get_attribute('data-source')=='MODIS_SP'
  old=csvrows(download(page,'#download'));assert old and all(r['product']=='MODIS_SP'for r in old)
  full=csvrows(download(page,'#aggregateDownload'));early_viirs=next(r for r in full if r['month']=='2000-11'and r['product']=='VIIRS_NOAA20_SP');assert early_viirs['native_detections']==''and early_viirs['retrieved_days']=='0'
  page.select_option('#calendarView','raw');stable(page,'pantanal');page.select_option('#mapProduct','VIIRS_NOAA20_SP');assert page.locator('#map').get_attribute('data-grid-available')=='false';assert page.locator('#map').get_attribute('data-cell-days')=='';assert page.locator('#downloadCells').is_disabled();page.select_option('#calendarView','replay');stable(page,'pantanal')
  page.select_option('#monthSelect','2023-01');stable(page,'pantanal')
  if viewport=='mobile':page.locator('#filterFold').evaluate('(e)=>e.open=true')
  page.select_option('#area','north');stable(page,'pantanal');assert page.locator('#downloadReplay').is_disabled();assert page.locator('#comparison [data-series=adjusted]').count()==0
  page.select_option('#area','all');page.select_option('#sensor','MODIS_SP');stable(page,'pantanal');assert page.locator('#map').get_attribute('data-grid-product')=='MODIS_SP'
  # Missing values stay blank; the real zero-detection day remains exportable zero.
  # This month may be present after backfill; force a pre-archive month for missingness.
  page.evaluate("()=>{document.querySelector('#start').value='1999-12-01';document.querySelector('#end').value='1999-12-31';document.querySelector('#end').dispatchEvent(new Event('change',{bubbles:true}))}")
  page.wait_for_function("document.querySelector('#download').disabled&&document.querySelector('#status').textContent.startsWith('Data unavailable')")
  missing=csvrows(download(page,'#aggregateDownload'));assert all(x['native_detections']==''and x['occupied_cell_days']==''for x in missing)
  page.evaluate("()=>{document.querySelector('#start').value='2020-01-08';document.querySelector('#end').value='2020-01-08';document.querySelector('#end').dispatchEvent(new Event('change',{bubbles:true}))}");stable(page,'pantanal');assert csvrows(download(page,'#download'))==[]
  # Direct presentation, keyboard/mobile navigation, exact world links and print.
  assert page.goto(BASE+'/pitch?slide=7').status==200;page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 7 of 9'")
  assert page.locator('.world-map a').count()==8 and page.locator('.world-regions a').count()==8
  page.reload();page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 7 of 9'")
  if viewport=='desktop':
   page.keyboard.press('ArrowLeft');assert page.locator('#pitchCounter').inner_text()=='Slide 6 of 9';page.keyboard.press('Home');assert page.locator('#pitchCounter').inner_text()=='Slide 1 of 9'
   page.emulate_media(media='print');page.pdf(path=str(ROOT/'submission/ember-atlas-pitch.pdf'),prefer_css_page_size=True,print_background=True);page.emulate_media(media='screen')
  if viewport=='mobile':assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  for i,r in enumerate(registry['regions']):
   page.goto(BASE+'/pitch?slide=7');page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 7 of 9'");page.locator('.world-map a').nth(i).focus();page.keyboard.press('Enter');stable(page,r['id']);assert page.locator('#region').input_value()==r['id']
  page.goto(BASE+'/pitch?slide=7');page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 7 of 9'")
  page.screenshot(path=str(ROOT/f'submission/transition-pitch-{viewport}.png'))
  page.goto(BASE+'/demo?view=replay&benchmark=1&month=2024-09');stable(page,'pantanal');page.screenshot(path=str(ROOT/f'submission/transition-demo-{viewport}.png'))
  if viewport=='desktop' and not BASE.startswith('https://'):page.locator('.dashboard-grid').screenshot(path=str(ROOT/'web/assets/dashboard-view.png'))
  page.locator('#history').screenshot(path=str(ROOT/f'submission/transition-calendar-{viewport}.png'))
  assert not errors,errors;assert not http_errors,http_errors;assert not console_errors,console_errors;context.close()
  # Tiles unavailable: every study area still has geographic context and observations.
  fallback=b.new_context(viewport={'width':w,'height':h});fallback.route('**/tile.openstreetmap.org/**',lambda route:route.abort());f=fallback.new_page()
  for r in registry['regions']:
   f.goto(BASE+'/?region='+r['id']);stable(f,r['id']);f.wait_for_function("document.querySelector('#map').dataset.basemap==='local'",timeout=15000)
   assert int(f.locator('#map').get_attribute('data-observations'))>0
   assert f.locator('#map .leaflet-local-geography-pane canvas').count()>0
  fallback.close()
  report['checks'].append({'viewport':viewport,'replay_cutoff_sources':True,'benchmark_shared_state':link,'replay_csv_matches_display':True,'new_export_manifest_hashes':True,'no_subarea_transfer':True,'zero_vs_missing':True,'full_modis_archive_months':archive_months,'early_unavailable_viirs_blank':True,'unretrieved_map_sensor_not_zero':True,'world_map_links':8,'world_map_keyboard_links_navigate':8,'all_regions_tile_fallback':True,'javascript_errors':errors,'application_http_errors':http_errors,'unexpected_console_errors':console_errors})
 b.close()
suffix='public'if BASE.startswith('https://')else'local';(ROOT/f'submission/eight-region-check-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
