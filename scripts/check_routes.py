"""Signed-out route, guided state, evidence manifest and presentation checks."""
import hashlib,json,os,subprocess,math
from pathlib import Path
from datetime import datetime,timezone
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8930').rstrip('/')
report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':[]}
args=['--no-sandbox']
if os.environ.get('EMBER_BROWSER_CA_SPKI'):args+=['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]
def stable(page):page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
def download(page,selector):
 with page.expect_download() as event:page.locator(selector).click()
 return Path(event.value.path()).read_bytes()
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,w,h in [('desktop',1440,1000),('mobile',390,844)]:
  context=b.new_context(viewport={'width':w,'height':h},has_touch=name=='mobile',is_mobile=name=='mobile',accept_downloads=True)
  page=context.new_page();errors=[];network=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.on('requestfailed',lambda r:network.append({'url':r.url,'failure':r.failure}))
  page.on('response',lambda r:network.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
  for route in ['/','/demo','/pitch']:
   assert page.goto(BASE+route).status==200
   if route=='/pitch':page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 1 of 9'")
   else:stable(page)
   page.reload()
   if route=='/pitch':page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 1 of 9'")
   else:stable(page)
  page.goto(BASE+'/demo');stable(page)
  assert 'Step 1 of 5' in page.locator('#stepProgress').inner_text()
  assert page.locator('#calendar .a').count()==60
  for n in range(2,6):
   page.locator('#stepNext').click();stable(page);assert page.locator('#stepProgress').inner_text()==f'Step {n} of 5';assert f'step={n}' in page.url
   if n==4:assert all(page.locator('#baseline details').evaluate_all('(ds)=>ds.map(d=>d.open)'))
  obs=download(page,'#download');ag=download(page,'#aggregateDownload');manifest=json.loads(download(page,'#downloadManifest'))
  assert manifest['observation_export']['rows']==125055
  assert manifest['observation_export']['sha256']==hashlib.sha256(obs).hexdigest()
  assert manifest['aggregate_export']['sha256']==hashlib.sha256(ag).hexdigest()
  assert manifest['calibration']['applies_to_selection'] is True and manifest['observation_coverage']=='unknown'
  # Open a real rendered marker, using its published map coordinates.
  page.locator('#map').scroll_into_view_if_needed()
  point=json.loads(page.locator('#map').get_attribute('data-sample'));bounds=json.loads(page.locator('#map').get_attribute('data-bounds'));box=page.locator('#map').bounding_box()
  merc=lambda lat:math.log(math.tan(math.pi/4+math.radians(lat)/2))
  x=box['x']+box['width']*(point['longitude']-bounds[0][1])/(bounds[1][1]-bounds[0][1])
  y=box['y']+box['height']*(merc(bounds[1][0])-merc(point['latitude']))/(merc(bounds[1][0])-merc(bounds[0][0]))
  page.mouse.click(x,y);page.wait_for_selector('.leaflet-popup-content')
  popup=page.locator('.leaflet-popup-content').inner_text()
  assert all(label in popup for label in ['Product:','Acquired:','UTC','FRP (MW):','Confidence:','Source:'])
  page.locator('.leaflet-popup-close-button').click()
  # Map layer visibility is explicitly display-only.
  page.locator('#layerViirs').uncheck();page.wait_for_timeout(100)
  assert int(page.locator('#map').get_attribute('data-observations'))==125055
  assert int(page.locator('#map').get_attribute('data-points'))<4000
  assert download(page,'#download')==obs
  page.locator('#layerModis').uncheck();assert page.locator('#map').get_attribute('data-points')=='0'
  page.locator('#layerViirs').check();page.locator('#layerModis').check()
  page.locator('#resetDemo').click();stable(page);assert 'step=1' in page.url
  page.locator('#shareSelection').click();page.wait_for_function("document.querySelector('#shareStatus').textContent.length>0")
  if name=='mobile':page.locator('#filterFold>summary').click()
  page.select_option('#area','north');stable(page)
  assert page.locator('#calendarView').input_value()=='raw'
  assert page.locator('#comparison [data-series=adjusted]').count()==0
  assert page.locator('#baseline summary').count()==2
  assert 'n = 4' in page.locator('#baseline').inner_text()
  page.select_option('#sensor','MODIS_SP');stable(page)
  page.select_option('#monthSelect','2024-08');stable(page)
  assert json.loads(download(page,'#downloadManifest'))['calibration']['applies_to_selection'] is False
  shared=page.url
  page.reload();stable(page)
  assert page.locator('#area').input_value()=='north' and page.locator('#sensor').input_value()=='MODIS_SP'
  assert page.locator('#map').get_attribute('data-month')=='2024-08'
  assert page.locator('#calendar .v').count()==0
  page.select_option('#monthSelect','2024-09');stable(page)
  page.go_back();stable(page);assert page.locator('#monthSelect').input_value()=='2024-08'
  page.go_forward();stable(page);assert page.locator('#monthSelect').input_value()=='2024-09'
  page.locator('.masthead a[href*="/pitch?"]').click();page.wait_for_function("!document.querySelector('#pitchPage').hidden")
  assert page.locator('.presenter-notes:visible').count()==0
  if name=='desktop':
   assert page.locator('.pitch-slide:visible').count()==1
   page.keyboard.press('ArrowRight');assert page.locator('#pitchCounter').inner_text()=='Slide 2 of 9'
   page.keyboard.press('End');assert page.locator('#pitchCounter').inner_text()=='Slide 9 of 9'
   page.keyboard.press('Home');assert page.locator('#pitchCounter').inner_text()=='Slide 1 of 9'
   page.locator('#pitchFullscreen').click();assert page.evaluate('!!document.fullscreenElement');page.keyboard.press('Escape')
  else:assert page.locator('.pitch-slide:visible').count()==9
  page.locator('#pitchNext').click();assert page.locator('#pitchCounter').inner_text()=='Slide 2 of 9'
  page.locator('#pitchNotes').check();assert page.locator('.active .presenter-notes').is_visible();page.locator('#pitchNotes').uncheck()
  page.reload();page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 2 of 9'")
  if name=='mobile':
   page.wait_for_function("document.querySelector('#slide-2').getBoundingClientRect().top>=90&&document.querySelector('#slide-2').getBoundingClientRect().top<250")
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.screenshot(path=str(ROOT/f'submission/pitch-{name}.png'))
  if name=='desktop':
   page.emulate_media(media='print');page.pdf(path=str(ROOT/'submission/ember-atlas-pitch.pdf'),prefer_css_page_size=True,print_background=True)
   info=subprocess.check_output(['pdfinfo',str(ROOT/'submission/ember-atlas-pitch.pdf')],text=True)
   assert 'Pages:           9' in info,info;page.emulate_media(media='screen')
  page.goto(BASE+'/demo');stable(page)
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.screenshot(path=str(ROOT/f'submission/demo-{name}.png'),full_page=True)
  if name=='desktop' and not BASE.startswith('https://'):page.locator('.dashboard-grid').screenshot(path=str(ROOT/'web/assets/dashboard-view.png'))
  assert not errors,errors
  assert not network,network
  report['checks'].append({'viewport':name,'direct_load_refresh_all_routes':True,'guided_steps_reset':True,'regional_baseline_n':4,'no_regional_adjustment':True,'manifest_export_hashes_match':True,'map_visibility_display_only':True,'observation_tooltip_source_time_fields':True,'share_url':shared,'back_forward_restore':True,'pitch_navigation_notes':True,'pitch_print_pages':9 if name=='desktop' else None,'unexpected_http_errors':network,'javascript_errors':errors})
  context.close()
 b.close()
suffix='public' if BASE.startswith('https://') else 'local'
(ROOT/f'submission/routes-check-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
