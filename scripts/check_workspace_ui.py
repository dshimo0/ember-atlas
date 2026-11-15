"""Verify the evidence workspace in two languages and themes against released observations."""
import os,json,csv,io
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('BASE_URL','http://127.0.0.1:8932');OUT=ROOT/'submission/workspace-ui';OUT.mkdir(exist_ok=True)
args=['--no-sandbox'];pins=os.environ.get('EMBER_BROWSER_CA_SPKI');
if pins:args.append('--ignore-certificate-errors-spki-list='+pins)
report={'url':BASE,'checks':[]}
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,w,h in [('desktop',1440,1000),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},reduced_motion='reduce',accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  for theme in ['dark','light']:
   for lang in ['en','pt-BR']:
    for route in ['','demo','methods','about','pitch?slide=5']:
     page.goto(BASE+'/'+route+('&'if '?'in route else'?')+f'theme={theme}&lang={lang}');page.wait_for_function('(x)=>document.documentElement.lang===x',arg=lang)
     if route in ['','demo']:page.wait_for_function("document.querySelector('#download')&&!document.querySelector('#download').disabled",timeout=120000)
     if route=='methods':page.wait_for_selector('#diagnosticPlots svg')
     if route.startswith('pitch'):page.wait_for_selector('.pitch-slide.active')
     page.wait_for_function('document.fonts.status==="loaded"');assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(name,theme,lang,route)
     assert page.locator('.masthead nav a').first.inner_text()==('Explorar'if lang=='pt-BR'else'Explore')
     assert page.evaluate('document.documentElement.dataset.theme')==theme
     page.screenshot(path=str(OUT/f'{name}-{theme}-{lang}-{route.split("?")[0]or"explore"}.png'))
     if os.environ.get('AXE_SCRIPT'):
      page.add_script_tag(path=os.environ['AXE_SCRIPT']);violations=page.evaluate("async()=>{let r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(x=>({id:x.id,nodes:x.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))}")
      report['checks'].append({'viewport':name,'theme':theme,'lang':lang,'route':route or'/','axe':violations});print(name,theme,lang,route,'axe',len(violations),flush=True)
  page.goto(BASE+'/?lang=en&theme=light');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
  assert float(page.locator('#comparison [data-series=modis]').get_attribute('data-value'))==5819
  page.locator('.historical-trend').evaluate('(e)=>e.open=true')
  page.locator('#timeSeries [data-plot-month="2023-01"]').focus();page.keyboard.press('Enter');page.wait_for_function("document.querySelector('#map').dataset.month==='2023-01'&&!document.querySelector('#download').disabled",timeout=120000);assert page.locator('#monthSelect').input_value()=='2023-01'
  with page.expect_download()as d:page.locator('#download').click()
  csv_en=Path(d.value.path()).read_bytes();rows=list(csv.DictReader(io.StringIO(csv_en.decode())));assert rows and all(r['date_utc'].startswith('2023-01')for r in rows)
  page.select_option('#interfaceLanguage','pt-BR');page.wait_for_function("document.documentElement.lang==='pt-BR'")
  with page.expect_download()as d:page.locator('#download').click()
  assert Path(d.value.path()).read_bytes()==csv_en
  page.select_option('#area','north')if page.locator('#area').is_visible()else None
  page.goto(BASE+'/?area=north&month=2024-09&lang=pt-BR&theme=light');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000);assert not page.locator('#comparison [data-series=adjusted]').count();assert page.locator('#downloadReplay').is_disabled()
  assert not errors,errors;c.close()
 b.close()
report['axe_violation_count']=sum(len(x['axe'])for x in report['checks']);
report['chart_selection_and_csv_scope']=True;report['language_preserves_export_bytes']=True;report['subregion_adjustment_withheld']=True
suffix='public'if BASE.startswith('https')else'local';(ROOT/f'submission/workspace-ui-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print('completed')
