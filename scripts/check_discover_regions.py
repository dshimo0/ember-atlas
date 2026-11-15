"""Verify the map-first region presets against their pinned September observations."""
import os,json,csv,io,gzip,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('BASE_URL','http://127.0.0.1:8940');report={'base':BASE,'checks':[]}
def ref(x):
 b=(ROOT/'web/data'/x['file']).read_bytes();b=gzip.decompress(b)if x['file'].endswith('.gz')else b
 assert hashlib.sha256(b).hexdigest()==x['sha256'];return json.loads(b)
registry=ref(json.loads((ROOT/'web/data/regions.json').read_text()))
args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]if os.environ.get('EMBER_BROWSER_CA_SPKI')else[])
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=args)
 for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h},accept_downloads=True);page=c.new_page()
  for r in registry['regions']:
   page.goto(BASE+'/explore?region='+r['id']+'&month=2024-09');page.wait_for_function("r=>!document.querySelector('#download').disabled&&document.querySelector('#map').dataset.region===r",arg=r['id'],timeout=120000)
   source=ref(ref(r['datasets']['sp'])['observation_shards']['2024-09'])['observations']
   with page.expect_download()as event:page.locator('#download').click()
   rows=list(csv.DictReader(io.StringIO(Path(event.value.path()).read_text())));assert len(rows)==len(source)>0
   wst,sth,est,nth=r['bounds'];bounds=json.loads(page.locator('#map').get_attribute('data-bounds'));assert bounds[0][0]<=sth and bounds[0][1]<=wst and bounds[1][0]>=nth and bounds[1][1]>=est
   assert all(wst<=float(x['longitude'])<=est and sth<=float(x['latitude'])<=nth and x['date_utc'].startswith('2024-09')for x in rows)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth')
   report['checks'].append({'viewport':name,'region':r['id'],'month':'2024-09','csv_rows':len(rows),'matches_snapshot_count':True,'geometry_fit':True});print(name,r['id'],len(rows),flush=True)
  # Recent view stays separate and a single sensor controls map and download.
  page.locator('#dataMode').select_option('nrt');page.wait_for_function("!document.querySelector('#download').disabled");assert page.locator('#dataMode').input_value()=='nrt';assert page.locator('#calendarView').input_value()=='raw'
  page.locator('#filterFold').evaluate('(e)=>e.open=true');page.locator('#sensor').select_option('MODIS_SP');page.wait_for_function("!document.querySelector('#download').disabled")
  with page.expect_download()as e:page.locator('#download').click()
  rows=list(csv.DictReader(io.StringIO(Path(e.value.path()).read_text())));assert rows and all(x['product']=='MODIS_NRT'for x in rows)
  report['checks'].append({'viewport':name,'separate_nrt':True,'single_sensor_csv':True});c.close()
 b.close()
(ROOT/'submission/discover-regions-check.json').write_text(json.dumps(report,indent=2)+'\n')
