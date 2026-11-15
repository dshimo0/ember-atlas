from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];out=R/'submission/discover-after';out.mkdir(exist_ok=True);results=[];base=os.environ.get('BASE_URL','http://127.0.0.1:8000')
with sync_playwright()as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']+(['--ignore-certificate-errors-spki-list='+os.environ['EMBER_BROWSER_CA_SPKI']]if os.environ.get('EMBER_BROWSER_CA_SPKI')else[]))
 for name,w,h in [('desktop',1440,900),('mobile',390,844)]:
  c=b.new_context(viewport={'width':w,'height':h});page=c.new_page()
  for route in ['/','/explore','/about']:
   page.goto(base+route+'?theme=light&lang=pt-BR');page.wait_for_timeout(1700)
   if route=='/':page.wait_for_function("document.body.dataset.evidence==='ready'")
   if route=='/explore':page.wait_for_function("!document.querySelector('#download').disabled",timeout=120000)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth');page.screenshot(path=str(out/f'{name}-{route.strip("/")or"discover"}-light-pt.png'))
   page.add_script_tag(path=os.environ['AXE_SCRIPT']);v=page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(x=>({id:x.id,nodes:x.nodes.map(n=>n.target)}))}");results.append({'device':name,'route':route,'axe':v});assert not v,(name,route,v);print(name,route,v,flush=True)
  page.goto(base+'/explore');page.wait_for_function("!document.querySelector('#download').disabled");page.locator('.masthead nav a[href="/"]').click();page.wait_for_url(base+'/');assert page.locator('#discoverMain').count()==1;page.go_back();page.wait_for_function("!document.querySelector('#download').disabled");assert '/explore'in page.url
  c.close()
 b.close()
(R/'submission/discover-extra-check.json').write_text(json.dumps(results,indent=2)+'\n')
