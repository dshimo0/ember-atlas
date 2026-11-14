from playwright.sync_api import sync_playwright
from pathlib import Path
import csv,json,time
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},record_video_dir='/tmp/ember-video',record_video_size={'width':1440,'height':1000},accept_downloads=True)
 page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:8000');page.wait_for_function("document.querySelector('#status').textContent.includes('observations selected')",timeout=120000)
 assert page.locator('#calendar button').count()==2
 page.get_by_role('button',name='2024-09',exact=False).click();page.wait_for_function("document.querySelector('#monthTitle').textContent.startsWith('2024-09')");assert '5819' in page.locator('#comparison').inner_text()
 page.screenshot(path='submission/dashboard.png',full_page=True)
 page.select_option('#area','north');page.select_option('#sensor','MODIS_SP')
 print(page.locator('#monthTitle').inner_text(),page.locator('#start').input_value(),page.locator('#end').input_value(),flush=True)
 with page.expect_download() as d:page.locator('#download').click()
 d.value.save_as('/tmp/ember-export.csv');rows=list(csv.DictReader(open('/tmp/ember-export.csv')))
 assert rows and all(r['product']=='MODIS_SP' and r['date_utc'].startswith('2024-09') and -19<=float(r['latitude'])<= -15 for r in rows)
 page.select_option('#area','all');page.select_option('#sensor','both');page.locator('summary').click();page.screenshot(path='submission/methodology.png',full_page=True)
 page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')
 page.screenshot(path='submission/mobile.png',full_page=True)
 assert not errors,errors
 Path('submission/browser-check.json').write_text(json.dumps({'url':'http://127.0.0.1:8000','calendar_months':2,'filtered_csv_rows':len(rows),'csv_area_sensor_month_verified':True,'mobile_no_horizontal_overflow':True,'javascript_errors':errors,'public_https_verified':False},indent=2))
 page.wait_for_timeout(3000)
 context.close();browser.close()
