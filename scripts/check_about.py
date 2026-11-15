"""Check the creator page and its links without requiring analytical data to render it."""
import json,os
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8931').rstrip('/')
args=['--no-sandbox']
if os.environ.get('EMBER_BROWSER_CA_SPKI'):args.append('--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI'])
checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,width,height in [('desktop',1440,1000),('mobile',390,844),('small-mobile',320,740)]:
  c=b.new_context(viewport={'width':width,'height':height});page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  assert page.goto(BASE+'/about').status==200
  assert page.locator('h1').inner_text()=='About the team'
  assert page.locator('#creator-name').inner_text()=='Diego Shimohama'
  assert page.locator('nav [aria-current=page]').inner_text()=='About'
  assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  page.reload();assert page.locator('#creator-name').is_visible()
  page.keyboard.press('Tab');assert page.locator('.skip').evaluate('(e)=>e===document.activeElement')
  page.keyboard.press('Enter');assert page.url.endswith('#about')
  page.screenshot(path=str(ROOT/f'submission/about-{name}.png'),full_page=True)
  if name!='small-mobile':
   page.goto(BASE+'/?region=california&month=2024-09&mode=sp');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
   assert page.locator('#region').input_value()=='california'
   page.locator('.masthead a[href="/about"]').click();assert page.locator('#creator-name').is_visible()
   page.go_back();page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
   assert page.locator('#region').input_value()=='california'
   assert page.locator('#monthSelect').input_value()=='2024-09'
   page.goto(BASE+'/pitch?slide=9');page.wait_for_function("document.querySelector('#pitchCounter').textContent==='Slide 9 of 9'",timeout=120000)
   assert page.locator('#pitchPage a[href="/about"]').count()==1
  assert not errors,errors
  checks.append({'viewport':name,'direct_load_refresh':True,'no_horizontal_overflow':True,'keyboard_skip_link':True,'analytical_state_preserved_by_browser_back':name!='small-mobile','unexpected_page_errors':errors});c.close()
 c=b.new_context(java_script_enabled=False);page=c.new_page();assert page.goto(BASE+'/about').status==200;assert page.locator('#creator-name').is_visible();c.close();b.close()
report={'url':BASE+'/about','checks':checks,'readable_without_javascript':True,'creator_confirmed_by_owner':'Diego Shimohama; sole creator'}
suffix='public'if BASE.startswith('https://')else'local';(ROOT/f'submission/about-check-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
