import json,os,csv,io
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];out=root/'submission/calendar-continuity';out.mkdir(exist_ok=True)
base=os.environ.get('BASE_URL','http://127.0.0.1:8932');report={'url':base,'checks':[]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']] if os.environ.get('EMBER_BROWSER_CA_SPKI') else []))
 for device,w,h in [('desktop',1440,1000),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for route in ['/','/demo','/methods','/about','/pitch']:
   page.goto(base+route);page.reload();page.wait_for_load_state('networkidle');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(device,route)
   if route in ['/','/demo']:
    page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
    assert page.locator('#history').evaluate('(e)=>e.nextElementSibling.classList.contains("dashboard-grid")')
   report['checks'].append({'device':device,'route':route,'refresh':True,'overflow':False})
  page.goto(base+'/?encoding=anomaly&month=2024-09&theme=light&lang=en');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
  assert page.locator('#calendarEncoding').input_value()=='anomaly'
  title=page.locator('#calendar [data-month="2024-09"]').get_attribute('title');assert 'n=4' in title and 'earlier median' in title,title
  assert 'baseline unavailable' in page.locator('#calendar [data-month="2020-09"]').get_attribute('title')
  page.locator('#calendar [data-month="2024-08"]').click();page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('#monthSelect').input_value()=='2024-08'
  with page.expect_download()as dl:page.locator('#download').click()
  rows=list(csv.DictReader(io.StringIO(Path(dl.value.path()).read_text())));assert rows and all(r['date_utc'].startswith('2024-08')for r in rows)
  page.locator('#basemapMode').select_option('local');page.wait_for_timeout(400);assert 'local' in page.locator('#basemapMode').input_value()
  if os.environ.get('AXE_SCRIPT'):
   page.add_script_tag(path=os.environ['AXE_SCRIPT']);violations=page.evaluate("async()=>{let r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(x=>({id:x.id,nodes:x.nodes.map(n=>n.target)}))}");assert not violations,violations
  page.screenshot(path=str(out/f'{device}-light-anomaly.png'),full_page=True)
  page.evaluate('window.scrollTo(0,0)');page.screenshot(path=str(out/f'{device}-first-viewport.png'))
  page.locator('#interfaceLanguage').select_option('pt-BR');page.locator('#interfaceTheme').click();page.wait_for_timeout(300);page.screenshot(path=str(out/f'{device}-dark-pt.png'),full_page=True)
  page.locator('#filterFold').evaluate('(e)=>e.open=true');page.locator('#area').select_option('north');page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('#calendarView').input_value()=='raw'
  page.locator('#timeSeries').locator('xpath=ancestor::details[1]').evaluate('(e)=>e.open=true');page.locator('#timeSeries [data-plot-month="2023-01"]').press('Enter');assert page.locator('#monthSelect').input_value()=='2023-01'
  assert not errors,errors
  report['checks'].append({'device':device,'anomaly_prior_n':4,'export_month':'2024-08','csv_rows':len(rows),'local_basemap':True,'subregion_raw':True,'keyboard_chart':True,'pageerrors':errors})
  c.close()
 b.close()
(root/'submission/calendar-continuity-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
