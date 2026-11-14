"""Signed-out desktop/mobile verification against the original pinned observations.

Set BASE_URL to the target. Chromium may use EMBER_BROWSER_CA_SPKI for a leaf
key independently validated by the system CA store in a proxied Cloud runtime.
"""
import csv,gzip,hashlib,io,json,os
from datetime import datetime,timezone
from decimal import Decimal,ROUND_FLOOR
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8910').rstrip('/')
index=json.loads((ROOT/'web/data/latest.json').read_text())
payload=gzip.decompress((ROOT/'web/data'/index['file']).read_bytes())
assert hashlib.sha256(payload).hexdigest()==index['sha256']
db=json.loads(payload);del payload
validation=json.loads((ROOT/'web/data/validation.json').read_text())
summary_ref=json.loads((ROOT/'web/data/dashboard.json').read_text())
summary=json.loads((ROOT/'web/data'/summary_ref['file']).read_text())
PRODS=['MODIS_SP','VIIRS_NOAA20_SP']

def oracle(month,area='all',sensor='both',start=None,end=None):
    start=start or month+'-01';end=end or month+'-31'
    return [r for r in db['observations'] if r['date_utc'].startswith(month) and start<=r['date_utc']<=end and (sensor=='both' or r['product']==sensor) and (area=='all' or (r['latitude']>=-19 if area=='north' else r['latitude']< -19))]

def cells(rows):
    return len({(r['date_utc'],*(int((Decimal(str(r[k]))/Decimal('.05')).to_integral_value(rounding=ROUND_FLOOR)) for k in ['latitude','longitude'])) for r in rows})

def read_download(page,button):
    with page.expect_download() as pending:page.locator(button).click()
    download=pending.value
    content=Path(download.path()).read_bytes()
    return list(csv.DictReader(io.StringIO(content.decode('utf-8')))),download.suggested_filename,hashlib.sha256(content).hexdigest()

def stable(page):
    page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)

def dates(page,start,end):
    # Change both input values before dispatch so the tested range is deliberate.
    page.evaluate("([a,b])=>{document.querySelector('#start').value=a;document.querySelector('#end').value=b;document.querySelector('#end').dispatchEvent(new Event('change',{bubbles:true}))}",[start,end])

def set_default(page):
    page.select_option('#area','all');page.select_option('#sensor','both');dates(page,'2020-01-01','2024-12-31')
    page.locator('[data-month="2024-09"]').click();stable(page)

report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'snapshot':index,'validation_sha256':hashlib.sha256((ROOT/'web/data/validation.json').read_bytes()).hexdigest(),'checks':[],'public_https_verified':BASE.startswith('https://'),'browser_uses_system_validated_leaf_pin':bool(os.environ.get('EMBER_BROWSER_CA_SPKI'))}
args=['--no-sandbox']
if os.environ.get('EMBER_BROWSER_CA_SPKI'):args+=['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=args)
    for name,width,height in [('desktop',1440,1000),('mobile',390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},accept_downloads=True)
        page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        response=page.goto(BASE);assert response.status==200;stable(page)
        assert page.locator('[data-month]').count()==60
        for bounds in page.locator('[data-month]').evaluate_all('(buttons)=>buttons.map(b=>({w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}))'):
            assert bounds['w']>=44 and bounds['h']>=44
        assert not page.evaluate("performance.getEntriesByType('resource').some(r=>r.name.includes('/snapshot-'))")
        assert page.locator('[data-month="2024-09"]').get_attribute('aria-pressed')=='true'
        expected_reduction=100*(1-validation['adjusted']['mae']/validation['unadjusted']['mae'])
        assert page.locator('#improvement').inner_text()==f'{expected_reduction:.1f}%'
        assert page.locator('#improvement').bounding_box()['y']<height
        assert 'Both products recorded activity above' in page.locator('#takeaway').inner_text()
        assert '2,532' in page.locator('#baseline').inner_text() and '4,782' in page.locator('#baseline').inner_text()
        assert page.locator('#baseline summary').count()==2
        assert all('n = 4' in text for text in page.locator('#baseline summary').all_text_contents())
        m=next(m for m in validation['monthly'] if m['month']=='2024-09')
        for series,key in [('modis','modis'),('viirs','viirs'),('adjusted','adjusted')]:assert abs(float(page.locator(f'[data-series="{series}"]').get_attribute('data-value'))-m[key])<1e-8
        assert '16.2%' in page.locator('#adjusted').inner_text()
        assert page.locator('#takeaway').bounding_box()['y']<page.locator('#map').bounding_box()['y']
        assert not page.evaluate('document.documentElement.scrollWidth > innerWidth')
        observations,filename,digest=read_download(page,'#download');expected=oracle('2024-09')
        assert len(observations)==len(expected)==125055
        assert {r['snapshot_sha256'] for r in observations}=={index['sha256']}
        for prod in PRODS:
            exported=[r for r in observations if r['product']==prod]
            assert cells(exported)==m['modis' if prod=='MODIS_SP' else 'viirs']
        assert {(r['product'],r['date_utc'],r['time_utc'],float(r['latitude']),float(r['longitude']),r['source']) for r in observations}=={(r['product'],r['date_utc'],r['time_utc'],r['latitude'],r['longitude'],r['source']) for r in expected}
        aggregates,_,_=read_download(page,'#aggregateDownload');assert len(aggregates)==120
        for row in aggregates:
            reference=next(m for m in validation['monthly'] if m['month']==row['month']);key='modis' if row['product']=='MODIS_SP' else 'viirs'
            assert int(row['occupied_cell_days'])==reference[key] and int(row['native_detections'])==reference[key+'_native']
        report['checks'].append({'viewport':name,'initial_month':'2024-09','calendar_months':60,'observation_rows':len(observations),'observation_csv_sha256':digest,'aggregate_rows':len(aggregates),'csv_rows_reconcile_with_snapshot':True})
        page.evaluate('scrollTo(0,0)')
        page.screenshot(path=str(ROOT/f'submission/judging-{name}.png'),full_page=True)
        if name=='desktop':page.screenshot(path=str(ROOT/'submission/judging-first-viewport.png'))
        # Calendar and keyboard selection synchronize chart, map, and observations.
        button=page.locator('[data-month="2024-08"]');button.focus();page.keyboard.press('Enter');stable(page)
        assert 'August 2024' in page.locator('#monthTitle').inner_text() and 'August 2024' in page.locator('#mapMonth').inner_text()
        assert page.locator('[data-month="2024-08"]').get_attribute('aria-pressed')=='true'
        assert float(page.locator('[data-series="modis"]').get_attribute('data-value'))==5880
        page.keyboard.press('ArrowRight');assert page.evaluate('document.activeElement.dataset.month')=='2024-09'
        page.keyboard.press('Enter');stable(page)
        # Manual date range creates a genuinely partial month, with no full-month transfer.
        dates(page,'2024-09-10','2024-09-20');stable(page)
        assert 'Partial month' in page.locator('#status').inner_text()
        assert page.locator('[data-series="adjusted"]').count()==0
        assert page.locator('.month.partial').count()==1
        partial,_,_=read_download(page,'#download');assert len(partial)==len(oracle('2024-09',start='2024-09-10',end='2024-09-20'))
        ag,_,_=read_download(page,'#aggregateDownload');assert len(ag)==2 and all(r['calibration']=='unavailable' and r['selected_days']=='11' for r in ag)
        assert sum(int(r['native_detections']) for r in ag)==len(partial)
        dates(page,'2024-09-01','2024-09-30');stable(page)
        page.select_option('#sensor','VIIRS_NOAA20_SP');stable(page)
        sensor_rows,_,_=read_download(page,'#download');assert len(sensor_rows)==101659 and all(r['product']=='VIIRS_NOAA20_SP' for r in sensor_rows)
        page.select_option('#area','north');stable(page)
        assert page.locator('[data-series="adjusted"]').count()==0
        assert 'validated only for the full' in page.locator('#scopeNotice').inner_text()
        page.select_option('#sensor','MODIS_SP');stable(page)
        north,_,_=read_download(page,'#download');assert len(north)==len(oracle('2024-09','north','MODIS_SP'))==18038
        assert all(-19<=float(r['latitude'])<=-15 and r['product']=='MODIS_SP' for r in north)
        ag,_,_=read_download(page,'#aggregateDownload');assert len(ag)==1 and ag[0]['factor']=='' and ag[0]['adjusted_modis_reference_cell_days']=='' and int(ag[0]['native_detections'])==len(north)
        # The map's keyboard-operable south selector also withholds calibration.
        page.locator('#map [data-area="south"]').focus();page.keyboard.press('Enter');stable(page)
        assert page.locator('#area').input_value()=='south' and page.locator('[data-series="adjusted"]').count()==0
        # A real retrieved zero-detection day is distinct from missing retrieval.
        page.select_option('#area','all')
        zero=next(d for d in summary['daily'] if d['area']=='all' and d['product']=='MODIS_SP' and d['native']==0)
        dates(page,zero['day'],zero['day']);stable(page)
        assert 'No detections recorded' in page.locator('#status').inner_text()
        zero_rows,_,_=read_download(page,'#download');assert zero_rows==[]
        # Outside the observed domain, counts stay null/blank and downloads are unavailable.
        dates(page,'2019-12-01','2019-12-31');page.wait_for_function("document.querySelector('#status').textContent.startsWith('Data unavailable')")
        assert page.locator('#download').is_disabled()
        assert page.locator('.month.missing').count()==1
        assert page.locator('[data-series="modis"]').get_attribute('data-value')==''
        missing,_,_=read_download(page,'#aggregateDownload');assert len(missing)==1 and missing[0]['native_detections']=='' and missing[0]['occupied_cell_days']=='' and missing[0]['retrieval_status']=='Data unavailable'
        assert not errors,errors
        report['checks'].append({'viewport':name,'month_keyboard_selection':True,'manual_partial_dates':True,'sensor_filter':True,'north_modis_rows':len(north),'map_subregion_keyboard':True,'subregion_transfer_withheld':True,'zero_day':zero['day'],'missing_counts_blank':True,'javascript_errors':errors})
        context.close()
    browser.close()
suffix='public' if BASE.startswith('https://') else 'local'
(ROOT/f'submission/judging-check-{suffix}.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
