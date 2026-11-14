from playwright.sync_api import sync_playwright
from pathlib import Path
import csv,json,time,os
base_url=os.environ.get("BASE_URL","http://127.0.0.1:8000")
browser_args=['--no-sandbox']
if os.environ.get('EMBER_BROWSER_CA_SPKI'):browser_args.append('--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI'])
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=browser_args)
 context=browser.new_context(viewport={'width':1440,'height':1000},record_video_dir='/tmp/ember-video',record_video_size={'width':1440,'height':1000},accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 response=page.goto(base_url);assert response and response.status==200;page.wait_for_function("document.querySelector('#status').textContent.includes('observations selected')",timeout=120000)
 assert page.locator('#calendar button').count()==2
 page.get_by_role('button',name='2024-09',exact=False).click();page.wait_for_function("document.querySelector('#monthTitle').textContent.startsWith('2024-09')");assert '5819' in page.locator('#comparison').inner_text()
 page.screenshot(path='submission/dashboard.png',full_page=True)
 page.select_option('#area','north');page.select_option('#sensor','MODIS_SP')
 print(page.locator('#monthTitle').inner_text(),page.locator('#start').input_value(),page.locator('#end').input_value(),flush=True)
 with page.expect_download() as d:page.locator('#download').click()
 d.value.save_as('/tmp/ember-export.csv');rows=list(csv.DictReader(open('/tmp/ember-export.csv')))
 assert rows and all(r['product']=='MODIS_SP' and r['date_utc'].startswith('2024-09') and -19<=float(r['latitude'])<= -15 for r in rows)
 with page.expect_download() as aggregate_download:page.locator('#aggregateDownload').click()
 aggregate_download.value.save_as('/tmp/ember-aggregates.csv')
 aggregates=list(csv.DictReader(open('/tmp/ember-aggregates.csv')))
 assert len(aggregates)==1 and aggregates[0]['product']=='MODIS_SP' and int(aggregates[0]['native_detections'])==len(rows) and aggregates[0]['calibration']=='unavailable'
 page.select_option('#area','all');page.select_option('#sensor','both');
 validation=page.evaluate("fetch('data/validation.json').then(r=>r.json())")
 if validation['accepted']:assert 'Adjusted NOAA-20:' in page.locator('#adjusted').inner_text()
 page.locator('summary').click();page.screenshot(path='submission/methodology.png',full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='submission/mobile.png',full_page=True)
 assert not errors,errors
 Path('submission/browser-check.json').write_text(json.dumps({'url':base_url,'calendar_months':2,'filtered_csv_rows':len(rows),'csv_area_sensor_month_verified':True,'mobile_no_horizontal_overflow':True,'javascript_errors':errors,'public_https_verified':base_url.startswith('https://'),'browser_uses_system_validated_leaf_pin':bool(os.environ.get('EMBER_BROWSER_CA_SPKI'))},indent=2))
 page.wait_for_timeout(3000)
 context.close();browser.close()
