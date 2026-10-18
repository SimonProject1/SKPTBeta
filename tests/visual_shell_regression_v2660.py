#!/usr/bin/env python3
import os,sys
from playwright.sync_api import sync_playwright
BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
def same(a,b):return all(abs(a[k]-b[k])<.6 for k in ('x','y','width','height'))
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('SK_CHROMIUM_EXECUTABLE') or '/opt/pw-browsers/chromium-1208/chrome-linux64/chrome');c=b.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True);page=c.new_page()
  for route,sel in [('wissensdatenbank/','.knowledge-tile'),('werkstoffdatenbank/','.material-tile')]:
   page.goto(BASE+route,wait_until='networkidle');page.wait_for_selector(sel);el=page.locator(sel).first;a=el.bounding_box();el.evaluate("e=>e.focus({preventScroll:true})");page.wait_for_timeout(80);d=el.bounding_box();assert same(a,d),(route,a,d);page.locator('.sk-app-frame').screenshot(path=f'/tmp/{route.split("/")[0]}-390.png')
  page.goto(BASE+'wissensdatenbank/siemens-sps-rohwert/',wait_until='networkidle');assert page.locator('.kb-context-back').is_visible();assert page.locator('.kb-hero img').get_attribute('src').endswith('v=2.6.6.0-Beta')
  c.close();b.close()
 print('PASS · ortsfeste Fokuszustände · Standard-App-Rechteck · mobile Zurück-Chips · Hero-Icons')
except Exception as e:print('FAIL',e);sys.exit(1)
