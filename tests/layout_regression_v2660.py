#!/usr/bin/env python3
import os,sys
from playwright.sync_api import sync_playwright
BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
PAGES=['wissensdatenbank/','wissensdatenbank/endress-hauser-promass-einbaulage/','werkstoffdatenbank/','werkstoffdatenbank/?material=1-4404']
try:
 with sync_playwright() as p:
  b=p.chromium.launch(executable_path=os.environ.get('SK_CHROMIUM_EXECUTABLE') or '/opt/pw-browsers/chromium-1208/chrome-linux64/chrome')
  for w,h in ((320,740),(390,844),(768,1024),(1440,1000)):
   c=b.new_context(viewport={'width':w,'height':h},is_mobile=w<=430,has_touch=w<=768);page=c.new_page()
   for route in PAGES:
    page.goto(BASE+route,wait_until='networkidle');m=page.evaluate('()=>[document.documentElement.scrollWidth,document.documentElement.clientWidth]');assert m[0]<=m[1]+2,(w,route,m)
    if 'wissensdatenbank/'==route:assert page.locator('.knowledge-tile').count()==5
    if route=='werkstoffdatenbank/':page.wait_for_selector('.material-tile');assert page.locator('.material-tile').count()==10
   c.close()
  b.close()
 print('PASS · kein horizontaler Überlauf · 320/390/768/1440 · Wissens- und Werkstoffansichten')
except Exception as e:print('FAIL',e);sys.exit(1)
