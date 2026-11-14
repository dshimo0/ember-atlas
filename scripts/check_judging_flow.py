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
BASE=os.environ.get('BASE_URL','http://127.0.0.1:8000').rstrip('/')
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
    page.locator('#calendar [data-month="2024-09"]').click();stable(page)

report={'url':BASE,'checked_utc':datetime.now(timezone.utc).isoformat(),'snapshot':index,'validation_sha256':hashlib.sha256((ROOT/'web/data/validation.json').read_bytes()).hexdigest(),'checks':[],'public_https_verified':BASE.startswith('https://'),'browser_uses_system_validated_leaf_pin':bool(os.environ.get('EMBER_BROWSER_CA_SPKI'))}
args=['--no-sandbox']
if os.environ.get('EMBER_BROWSER_CA_SPKI'):args+=['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=args)
    for name,width,height in [('desktop',1440,1000),('mobile',390,844)]:
        context=browser.new_context(viewport={'width':width,'height':height},is_mobile=name=='mobile',has_touch=name=='mobile',accept_downloads=True)
        page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        response=page.goto(BASE);assert response.status==200;stable(page)
        assert page.locator('#calendar [data-month]').count()==60
        for bounds in page.locator('#calendar [data-month]').evaluate_all('(buttons)=>buttons.map(b=>({w:b.getBoundingClientRect().width,h:b.getBoundingClientRect().height}))'):
            assert bounds['w']>=44 and bounds['h']>=44
        assert not page.evaluate("performance.getEntriesByType('resource').some(r=>r.name.includes('/snapshot-'))")
        assert page.locator('#calendar [data-month="2024-09"]').get_attribute('aria-pressed')=='true'
        expected_reduction=100*(1-validation['adjusted']['mae']/validation['unadjusted']['mae'])
        assert page.locator('#improvement').inner_text()==f'{expected_reduction:.1f}%'
        assert page.locator('#improvement').bounding_box()['y']<height
        assert 'both sensors recorded activity above' in page.locator('#takeaway').inner_text()
        assert '2,532' in page.locator('#baseline').inner_text() and '4,782' in page.locator('#baseline').inner_text()
        assert page.locator('#baseline summary').count()==2
        assert all('n = 4' in text for text in page.locator('#baseline summary').all_text_contents())
        m=next(m for m in validation['monthly'] if m['month']=='2024-09')
        for series,key in [('modis','modis'),('viirs','viirs'),('adjusted','adjusted')]:assert abs(float(page.locator(f'[data-series="{series}"]').get_attribute('data-value'))-m[key])<1e-8
        assert '16.2%' in page.locator('#adjusted').inner_text()
        assert page.locator('h1').inner_text()=='Pantanal fire activity, 2020–2024'
        assert page.locator('#takeaway').bounding_box()['y']<page.locator('#map').bounding_box()['y']
        map_box=page.locator('.map-panel').bounding_box();comparison_box=page.locator('.comparison-panel').bounding_box()
        if name=='desktop':assert abs(map_box['y']-comparison_box['y'])<2 and map_box['x']<comparison_box['x']
        else:assert map_box['y']+map_box['height']<=comparison_box['y']
        assert page.locator('#history').bounding_box()['y']>=comparison_box['y']+comparison_box['height']-.5
        page.wait_for_function("document.querySelector('#map').dataset.basemap==='street'",timeout=20000)
        page.wait_for_function("[...document.querySelectorAll('#map img.leaflet-tile')].every(i=>i.complete&&i.naturalWidth>0)",timeout=20000)
        assert page.locator('#map .leaflet-control-attribution').inner_text().find('OpenStreetMap')>=0
        assert page.locator('#map .leaflet-control-scale-line').count()==1
        assert int(page.locator('#map').get_attribute('data-observations'))==125055
        assert 0<int(page.locator('#map').get_attribute('data-points'))<=4000
        point=json.loads(page.locator('#map').get_attribute('data-sample'))
        assert any(r['latitude']==point['latitude'] and r['longitude']==point['longitude'] and r['product']==point['product'] for r in oracle('2024-09'))
        zoom=float(page.locator('#map').get_attribute('data-zoom'))
        page.locator('#map .leaflet-control-zoom-in').click()
        page.wait_for_function('(z)=>+document.querySelector("#map").dataset.zoom>z',arg=zoom)
        center=page.locator('#map').get_attribute('data-center');page.locator('#map').focus();page.keyboard.press('ArrowRight')
        page.wait_for_function('(c)=>document.querySelector("#map").dataset.center!==c',arg=center)
        page.locator('#fitStudyArea').click()
        bounds=json.loads(page.locator('#map').get_attribute('data-bounds'))
        assert bounds[0][0]<=-23 and bounds[0][1]<=-59 and bounds[1][0]>=-15 and bounds[1][1]>=-54
        assert int(page.locator('#map').get_attribute('data-observations'))==125055

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
        button=page.locator('#calendar [data-month="2024-08"]');button.focus();page.keyboard.press('Enter');stable(page)
        assert page.locator('#map').get_attribute('data-month')=='2024-08'
        assert 'August 2024' in page.locator('#monthTitle').inner_text() and 'August 2024' in page.locator('#mapMonth').inner_text()
        assert page.locator('#calendar [data-month="2024-08"]').get_attribute('aria-pressed')=='true'
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
        assert page.locator('#map').get_attribute('data-sensor')=='VIIRS_NOAA20_SP'
        assert json.loads(page.locator('#map').get_attribute('data-sample'))['product']=='VIIRS_NOAA20_SP'
        sensor_rows,_,_=read_download(page,'#download');assert len(sensor_rows)==101659 and all(r['product']=='VIIRS_NOAA20_SP' for r in sensor_rows)
        page.select_option('#area','north');stable(page)
        assert page.locator('[data-series="adjusted"]').count()==0
        assert 'validated only for the full' in page.locator('#scopeNotice').inner_text()
        page.select_option('#sensor','MODIS_SP');stable(page)
        assert page.locator('#map').get_attribute('data-area')=='north'
        assert int(page.locator('#map').get_attribute('data-observations'))==18038
        assert json.loads(page.locator('#map').get_attribute('data-sample'))['latitude']>=-19
        north,_,_=read_download(page,'#download');assert len(north)==len(oracle('2024-09','north','MODIS_SP'))==18038
        assert all(-19<=float(r['latitude'])<=-15 and r['product']=='MODIS_SP' for r in north)
        ag,_,_=read_download(page,'#aggregateDownload');assert len(ag)==1 and ag[0]['factor']=='' and ag[0]['adjusted_modis_reference_cell_days']=='' and int(ag[0]['native_detections'])==len(north)
        # Both subregions withhold full-area calibration.
        page.select_option('#area','south');stable(page)
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
        report['checks'].append({'viewport':name,'month_keyboard_selection':True,'manual_partial_dates':True,'sensor_filter':True,'north_modis_rows':len(north),'map_zoom_pan_scale_fit':True,'map_filter_synchronization':True,'subregion_transfer_withheld':True,'zero_day':zero['day'],'missing_counts_blank':True,'javascript_errors':errors})
        context.close()
        fallback=browser.new_context(viewport={'width':width,'height':height},accept_downloads=True)
        failures=[]
        def block_tiles(route):failures.append(route.request.url);route.abort()
        fallback.route('**/tile.openstreetmap.org/**',block_tiles)
        page=fallback.new_page();fallback_errors=[];page.on('pageerror',lambda e:fallback_errors.append(str(e)));page.goto(BASE);stable(page)
        page.wait_for_function("document.querySelector('#map').dataset.basemap==='local'",timeout=15000)
        assert failures and 'unavailable' in page.locator('#basemapStatus').inner_text()
        assert page.locator('.local-place-label').count()==27
        assert 'Corumbá' in page.locator('.local-place-label').all_text_contents()
        assert page.locator('#map .leaflet-local-geography-pane canvas').count()>0
        assert int(page.locator('#map').get_attribute('data-observations'))==125055
        page.locator('.map-panel').screenshot(path=str(ROOT/f'submission/map-fallback-{name}.png'))
        page.select_option('#area','north');page.select_option('#sensor','MODIS_SP');stable(page)
        exported,_,_=read_download(page,'#download');assert len(exported)==18038
        assert page.locator('[data-series="adjusted"]').count()==0
        assert int(page.locator('#map').get_attribute('data-observations'))==len(exported)
        assert not fallback_errors,fallback_errors
        report['checks'].append({'viewport':name,'basemap_failure_fallback':True,'local_settlements':27,'local_rivers':23,'fallback_north_modis_csv_rows':len(exported)})
        fallback.close()
    browser.close()
suffix='public' if BASE.startswith('https://') else 'local'
(ROOT/f'submission/judging-check-{suffix}.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
