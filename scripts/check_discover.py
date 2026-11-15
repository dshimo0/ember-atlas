from pathlib import Path
import json,os,csv,io
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];out=R/'submission/discover-after';out.mkdir(exist_ok=True);base=os.environ.get('BASE_URL','http://127.0.0.1:8940');report={'base':base,'checks':[]}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']] if os.environ.get('EMBER_BROWSER_CA_SPKI') else []))
 for n,w,h in [('desktop',1440,900),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for route in ['/','/explore','/demo','/methods','/about','/pitch']:
   page.goto(base+route);page.reload()
   if route=='/':page.wait_for_function("document.body.dataset.evidence==='ready'",timeout=120000)
   if route in ['/explore','/demo']:page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
   if route=='/methods':page.wait_for_selector('#diagnosticPlots svg')
   if route=='/pitch':page.wait_for_selector('.pitch-slide.active');assert page.locator('.pitch-slide').count()==7
   if route=='/about':page.wait_for_selector('.regional-status',state='attached');assert page.locator('.regional-status').count()==8
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(n,route)
   page.screenshot(path=str(out/f'{n}-{route.strip("/")or"discover"}.png'))
   page.add_script_tag(path=os.environ['AXE_SCRIPT']);v=page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(x=>({id:x.id,nodes:x.nodes.map(n=>n.target)}))}")
   report['checks'].append({'viewport':n,'route':route,'refresh':True,'axe':v});assert not v,(n,route,v);print(n,route,v,flush=True)
  page.goto(base+'/?month=2024-08&region=pantanal&sensor=both');page.wait_for_url('**/explore?**');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000);assert page.locator('#monthSelect').input_value()=='2024-08'
  with page.expect_download()as dl:page.locator('#download').click()
  rows=list(csv.DictReader(io.StringIO(Path(dl.value.path()).read_text())));assert len(rows)==129280 and all(r['date_utc'].startswith('2024-08')for r in rows)
  page.locator('#history').evaluate('(e)=>e.open=true');page.locator('#calendar [data-month="2024-09"]').click();page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('#monthSelect').input_value()=='2024-09'
  page.locator('#filterFold').evaluate('(e)=>e.open=true');page.locator('#area').select_option('north');page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('#calendarView').input_value()=='raw'
  page.goto(base+'/demo');page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('[data-guide-step]').count()==4
  for i in range(1,5):page.locator(f'[data-guide-step="{i}"]').click();assert page.locator('#stepProgress').inner_text()==f'Step {i} of 4'
  page.goto(base+'/pitch?slide=7');page.wait_for_selector('.pitch-slide.active');assert page.locator('.pitch-slide').count()==7
  page.locator('#pitchPrev').click();assert '6 of 7' in page.locator('#pitchCounter').inner_text();page.keyboard.press('ArrowRight');assert '7 of 7'in page.locator('#pitchCounter').inner_text()
  assert not errors,errors;report['checks'].append({'viewport':n,'legacy_migration':True,'csv_rows':len(rows),'calendar_sync':True,'subregion_raw':True,'guide_steps':4,'pitch_frames':7,'pageerrors':errors});c.close()
 b.close()
(R/'submission/discover-check.json').write_text(json.dumps(report,indent=2)+'\n');print('completed')
