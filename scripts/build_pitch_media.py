from pathlib import Path
from playwright.sync_api import sync_playwright
import subprocess,json,os
R=Path(__file__).resolve().parents[1];out=R/'submission/discover-after';out.mkdir(exist_ok=True);report=[];base=os.environ.get('BASE_URL','http://127.0.0.1:8000')
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']] if os.environ.get('EMBER_BROWSER_CA_SPKI') else []));c=b.new_context(viewport={'width':1440,'height':900});page=c.new_page()
 page.goto(base+'/explore');page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000);page.screenshot(path=str(R/'web/assets/dashboard-view.png'))
 for lang in ['en','pt-BR']:
  page.goto(base+'/pitch?lang='+lang+'&theme=light');page.wait_for_selector('.pitch-slide.active')
  for i in range(1,8):
   page.locator(f'[data-slide-jump="{i}"]').click();fits=page.locator(f'#slide-{i}').evaluate('(e)=>({height:e.clientHeight,content:e.scrollHeight})');assert fits['content']<=fits['height']+2,(lang,i,fits);report.append({'lang':lang,'slide':i,**fits})
  page.emulate_media(media='print');page.pdf(path=str(out/f'pitch-{lang}.pdf'),prefer_css_page_size=True,print_background=True);page.emulate_media(media='screen')
 c.close();b.close()
for lang in ['en','pt-BR']:
 info=subprocess.check_output(['pdfinfo',str(out/f'pitch-{lang}.pdf')],text=True);assert 'Pages:           7'in info,info
(R/'web/assets/ember-atlas-pitch.pdf').write_bytes((out/'pitch-en.pdf').read_bytes());(R/'submission/ember-atlas-pitch.pdf').write_bytes((out/'pitch-en.pdf').read_bytes());(out/'pitch-fit.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
