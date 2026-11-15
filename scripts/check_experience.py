"""Regression evidence for the P0/P1 presentation changes against real release snapshots."""
import json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('BASE_URL','http://127.0.0.1:8932').rstrip('/');OUT=ROOT/'submission'/'experience';OUT.mkdir(exist_ok=True)
args=['--no-sandbox'];pins=os.environ.get('EMBER_BROWSER_CA_SPKI')
if pins:args.append('--ignore-certificate-errors-spki-list='+pins)
report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':[],'axe_version':'4.10.3'if os.environ.get('AXE_SCRIPT')else None}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,w,h in [('desktop',1440,1000),('tablet',768,1024),('mobile',375,812)]:
  c=b.new_context(viewport={'width':w,'height':h},is_mobile=name=='mobile',has_touch=name=='mobile',reduced_motion='reduce',accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)));findings=[]
  def ready():page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
  def capture(label):page.screenshot(path=str(OUT/f'{label}-{name}.png'))
  def axe(label):
   if not os.environ.get('AXE_SCRIPT'):return
   page.add_script_tag(path=os.environ['AXE_SCRIPT']);v=page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,failure:n.failureSummary})).slice(0,10)}))}");findings.append({'page':label,'violations':v});assert not v,(name,label,v)
  for label,route in [('explore','/'),('demo','/demo'),('methods','/methods'),('about','/about'),('pitch','/pitch')]:
   assert page.goto(BASE+route).status==200
   if label in ['explore','demo']:ready()
   if label=='methods':page.wait_for_selector('#sourceCards article')
   if label=='pitch':page.wait_for_selector('.pitch-slide.active')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,label)
   if label=='about':assert page.locator('#creator-name').inner_text()=='Diego Shimohama';assert page.locator('a[href="https://dshimo.vercel.app/"]').count()>0
   capture(label);axe(label)
   if label in ['methods','about','pitch']:page.reload()
   if label=='methods':page.wait_for_selector('#sourceCards article')
  page.goto(BASE+'/');ready();assert page.locator('#monthSelect').input_value()=='2024-09'
  map_top=page.locator('#map').bounding_box()['y'];assert map_top<h,(name,map_top)
  assert page.locator('#calendar [data-month]').evaluate_all('es=>es.every(e=>e.scrollWidth<=e.clientWidth+1)'),name
  page.locator('#calendar').screenshot(path=str(OUT/f'calendar-{name}.png'))
  page.locator('.inspection-controls > summary').click();page.locator('#layerOpacity').focus();page.keyboard.press('Home');assert page.locator('#opacityValue').inner_text()=='20%';assert page.locator('.leaflet-observations-pane').evaluate('(e)=>e.style.opacity')=='0.2';assert page.locator('.leaflet-study-bounds-pane').evaluate('(e)=>e.style.opacity')=='';page.keyboard.press('End')
  page.locator('#mapFullscreen').click();page.wait_for_function('!!document.fullscreenElement');page.locator('#mapFullscreen').click();page.wait_for_function('!document.fullscreenElement')
  method=page.locator('.masthead a').filter(has_text='Methods & data')
  if name=='mobile':method.tap()
  else:method.click()
  page.wait_for_function("document.body.dataset.page==='methods'");assert '/methods'in page.url;page.wait_for_selector('#sourceCards article');page.reload();page.wait_for_selector('#sourceCards article')
  page.goto(BASE+'/#methodology');page.wait_for_function("location.pathname==='/methods'");page.wait_for_selector('#sourceCards article')
  page.goto(BASE+'/');ready();page.locator('#monthScrubber').focus();page.keyboard.press('ArrowRight');ready();assert page.locator('#monthSelect').input_value()==page.locator('#map').get_attribute('data-month')
  page.locator('#scientificMode').click();assert page.locator('#methodsPage').is_visible();assert 'detail=scientific'in page.url;page.reload();ready();assert page.locator('#methodsPage').is_visible();page.locator('#scientificMode').click();assert page.locator('#methodsPage').is_hidden()
  page.goto(BASE+'/demo');ready();assert page.locator('#walkthrough').bounding_box()['y']<h
  for n in range(1,6):
   page.locator(f'[data-guide-step="{n}"]').click();ready();assert page.locator('#stepProgress').inner_text()==f'Step {n} of 5';assert page.locator('#stepDescription').is_visible()
   if n==2:assert page.locator('#history').evaluate("e=>e.parentElement.id==='explore'")
   if n==3:assert page.locator('#calendarView').input_value()=='raw'
   if n==4:assert page.locator('#showBenchmark').is_checked();assert 'ground truth'in page.locator('#sceneEvidence').inner_text()
   page.locator('#walkthrough').scroll_into_view_if_needed();capture(f'demo-step{n}')
  page.locator('#resetDemo').click();ready();assert page.locator('#stepProgress').inner_text()=='Step 1 of 5'
  page.locator('[data-guide-step="1"]').focus();page.keyboard.press('ArrowRight');assert page.locator('#stepProgress').inner_text()=='Step 2 of 5'
  assert page.locator('#skipDemo').is_visible()
  page.goto(BASE+'/pitch?slide=5');page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 5 of 9'");capture('pitch-evidence');page.goto(BASE+'/pitch?slide=9');page.wait_for_function("document.querySelector('#pitchCounter')?.textContent==='Slide 9 of 9'");assert page.locator('#slide-9 table').count()==0;capture('pitch-closing')
  if name=='mobile':
   page.goto(BASE+'/pitch');page.wait_for_selector('#slide-5');page.locator('#slide-5').scroll_into_view_if_needed();page.wait_for_function("document.querySelector('#pitchCounter').textContent==='Slide 5 of 9'");assert 'slide=5'in page.url;capture('pitch-scroll-synced')
  if name=='desktop':
   page.goto(BASE+'/pitch');page.wait_for_selector('.pitch-slide.active');page.keyboard.press('ArrowRight');assert page.locator('#pitchCounter').inner_text()=='Slide 2 of 9'
   for i in range(1,10):
    page.goto(BASE+f'/pitch?slide={i}');page.wait_for_function(f"document.querySelector('#pitchCounter')?.textContent==='Slide {i} of 9'");assert page.locator(f'#slide-{i}').evaluate('(e)=>e.scrollHeight<=e.clientHeight+2'),i
   page.emulate_media(media='print');page.pdf(path=str(OUT/'pitch.pdf'),prefer_css_page_size=True,print_background=True);page.emulate_media(media='screen')
  assert not errors,errors;report['checks'].append({'viewport':name,'width':w,'height':h,'map_top':map_top,'all_five_routes_load_refresh':True,'legacy_methods_anchor':True,'menu_navigation':True,'calendar_no_numeric_overflow':True,'slider_map_synchronized':True,'scientific_detail_url_restored':True,'five_scenes_and_reset':True,'guide_keyboard':True,'pitch_keyboard_or_scroll_progress':True,'no_page_overflow':True,'unexpected_page_errors':errors,'accessibility':findings});c.close();print(name+' passed',flush=True)
 b.close()
info=subprocess.check_output(['pdfinfo',str(OUT/'pitch.pdf')],text=True);assert 'Pages:           9'in info;report['pdf_pages']=9
suffix='public'if BASE.startswith('https://')else'local';(ROOT/f'submission/experience-check-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
