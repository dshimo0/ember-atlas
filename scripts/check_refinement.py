"""Verify visible map base selection, failure fallback, current charts and public disclosure."""
from pathlib import Path
import os,json,csv,io
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];base=os.environ.get('BASE_URL','http://127.0.0.1:8943');out=R/'submission/refinement';out.mkdir(exist_ok=True);report={'base':base,'checks':[]}
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]if os.environ.get('EMBER_BROWSER_CA_SPKI')else []))
 for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(base+'/explore?month=2024-09&theme=light');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
  page.locator('#basemapMode').select_option('satellite');page.wait_for_function("['satellite','local'].includes(document.querySelector('#map').dataset.basemap)")
  satellite=page.locator('#map').get_attribute('data-basemap');assert satellite=='satellite',satellite
  page.screenshot(path=str(out/(name+'-satellite.png')))
  with page.expect_download()as d:page.locator('#download').click()
  rows=list(csv.DictReader(io.StringIO(Path(d.value.path()).read_text())));assert len(rows)==125055 and all(r['date_utc'].startswith('2024-09')for r in rows)
  page.route('**/tile.openstreetmap.org/**',lambda r:r.abort());page.locator('#basemapMode').select_option('street');page.wait_for_function("document.querySelector('#map').dataset.basemap==='local'")
  assert int(page.locator('#map').get_attribute('data-observations'))==len(rows)
  page.screenshot(path=str(out/(name+'-fallback.png')))
  page.locator('#history').evaluate('(e)=>e.open=true');cell=page.locator('#calendar [data-month="2024-09"]');assert '✓'not in cell.inner_text()and '○'not in cell.inner_text();assert 'Adjusted'in cell.inner_text()
  for route in ['/credits.html','/pitch?slide=5&theme=light','/methods?theme=light','/?theme=light']:
   page.goto(base+route)
   if route.startswith('/pitch'):page.wait_for_selector('.pitch-slide.active video');assert page.locator('.pitch-slide').count()==7
   if route.startswith('/methods'):page.wait_for_selector('#diagnosticPlots svg');assert page.locator('.methods-grid details').count()==0
   if route.startswith('/?'):page.wait_for_function("document.body.dataset.evidence==='ready'")
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,route)
   page.screenshot(path=str(out/(name+'-'+('credits'if route.startswith('/credits')else 'product'if route.startswith('/pitch')else 'methods'if route.startswith('/methods')else 'discover')+'.png')))
  assert not errors,errors
  report['checks'].append({'viewport':name,'satellite':satellite,'forced_street_failure':'local','matching_csv_rows':len(rows),'calendar_full_labels':True,'methods_open_sections':True,'embedded_product':True,'pageerrors':errors});c.close()
 b.close()
(out/'checks.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
