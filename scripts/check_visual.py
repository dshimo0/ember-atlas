"""Browser checks for P2/P3 visual changes; scientific output uses existing artifacts."""
import csv,gzip,hashlib,io,json,os,urllib.parse,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('BASE_URL','http://127.0.0.1:8932').rstrip('/');OUT=ROOT/'submission/visual';OUT.mkdir(exist_ok=True)
registry=json.loads((ROOT/'web/data/regions-c06212509a51.json').read_text());images=json.loads((ROOT/'web/assets/regional-imagery.json').read_text())['images'];assert [x['id']for x in images]==[r['id']for r in registry['regions']]
for i,r in zip(images,registry['regions']):
 assert i['bounds_wsen']==r['bounds'];assert hashlib.sha256((ROOT/'web/assets'/i['file']).read_bytes()).hexdigest()==i['sha256'];q=urllib.parse.parse_qs(urllib.parse.urlparse(i['source']).query);assert q['time']==['2024-09-01'];assert q['layers']==['MODIS_Terra_CorrectedReflectance_TrueColor'];w,s,e,n=r['bounds'];assert abs(i['width']/i['height']-(e-w)/(n-s))<.02
report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'image_hashes_and_extents_verified':8,'checks':[],'unchanged_scientific_files':[]}
import subprocess
for f in ['web/model.mjs','web/analysis.mjs','web/replay.mjs','web/charts.mjs','scripts/harmonize.py','web/data/regions.json']:
 assert (ROOT/f).read_bytes()==subprocess.check_output(['git','show','5df68c7:'+f],cwd=ROOT);report['unchanged_scientific_files'].append(f)
def readref(ref):
 data=(ROOT/'web/data'/ref['file']).read_bytes();data=gzip.decompress(data)if ref['file'].endswith('.gz')else data;assert hashlib.sha256(data).hexdigest()==ref['sha256'];return json.loads(data)
pan=readref(registry['regions'][0]['datasets']['sp']);validation=readref(pan['validation']);expected=next(x for x in validation['monthly']if x['month']=='2024-09')['adjusted'];expected_rows=len(readref(pan['observation_shards']['2024-09'])['observations'])
args=['--no-sandbox'];pins=os.environ.get('EMBER_BROWSER_CA_SPKI')
if pins:args.append('--ignore-certificate-errors-spki-list='+pins)
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,w,h in [('desktop',1440,1000),('mobile',375,812)]:
  c=b.new_context(viewport={'width':w,'height':h},has_touch=name=='mobile',is_mobile=name=='mobile',reduced_motion='reduce',accept_downloads=True);page=c.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(BASE+'/about#study-areas');page.locator('#study-areas').scroll_into_view_if_needed();page.wait_for_function('document.fonts.status==="loaded"');assert page.evaluate('document.fonts.check("16px Manrope")');assert page.locator('.atlas-card').count()==8
  for i in range(8):page.locator('.atlas-card').nth(i).scroll_into_view_if_needed();page.locator('.atlas-card img').nth(i).wait_for();page.wait_for_function('(i)=>document.querySelectorAll(".atlas-card img")[i].naturalWidth>0',arg=i)
  page.locator('#study-areas').scroll_into_view_if_needed();page.screenshot(path=str(OUT/f'atlas-{name}.png'));assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
  for i,r in enumerate(registry['regions']):
   page.goto(BASE+'/about#study-areas');page.locator('.atlas-card').nth(i).get_by_text('Explore observations').click();page.wait_for_function("r=>!document.querySelector('#download').disabled&&document.querySelector('#map').dataset.region===r",arg=r['id'],timeout=120000);assert int(page.locator('#map').get_attribute('data-observations'))>0;bounds=json.loads(page.locator('#map').get_attribute('data-bounds'));west,south,east,north=r['bounds'];assert bounds[0][0]<=south and bounds[0][1]<=west and bounds[1][0]>=north and bounds[1][1]>=east
   if r['id']=='pantanal':
    with page.expect_download()as d:page.locator('#download').click()
    rows=list(csv.DictReader(io.StringIO(Path(d.value.path()).read_text())));assert len(rows)==expected_rows;assert all(x['date_utc'].startswith('2024-09')for x in rows);assert abs(float(page.locator('#comparison [data-series=adjusted]').get_attribute('data-value'))-expected)<.000001
  page.goto(BASE+'/pitch');page.wait_for_selector('[data-slide-jump="9"]');page.locator('[data-slide-jump="9"]').focus();page.keyboard.press('Enter');page.wait_for_function("document.querySelector('#pitchCounter').textContent==='Slide 9 of 9'");assert page.locator('[data-slide-jump="9"]').get_attribute('aria-current')=='step';assert 'slide=9'in page.url;assert page.locator('.slide-body').first.evaluate('(e)=>getComputedStyle(e).animationName')=='none';page.screenshot(path=str(OUT/f'pitch-{name}.png'));assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');assert not errors,errors
  report['checks'].append({'viewport':name,'atlas_links_open_real_observations':8,'pantanal_csv_rows':expected_rows,'september_adjusted_reconciles':True,'keyboard_section_selection':True,'reduced_motion':True,'no_document_overflow':True,'page_errors':errors});c.close()
 c=b.new_context(viewport={'width':375,'height':812},reduced_motion='no-preference');c.route('**/manrope-latin-variable.woff2',lambda route:route.abort());page=c.new_page();page.goto(BASE+'/about');assert page.locator('#creator-name').inner_text()=='Diego Shimohama';assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');page.screenshot(path=str(OUT/'font-fallback-mobile.png'));report['font_failure_keeps_content_readable']=True;c.close()
 c=b.new_context(reduced_motion='no-preference');page=c.new_page();page.goto(BASE+'/pitch');page.wait_for_selector('.pitch-slide.active');assert page.locator('.pitch-slide.active .slide-body').evaluate('(e)=>getComputedStyle(e).animationDuration')=='0.18s';report['optional_motion_seconds']=.18;c.close();b.close()
suffix='public'if BASE.startswith('https://')else'local';(ROOT/f'submission/visual-check-{suffix}.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
