#!/usr/bin/env python3
"""V2.6.5.4-Beta: visuelle Einbettung von Header und Footer in die App-Fläche."""
from __future__ import annotations
import glob, os, re, sys
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
VERSION='2.6.5.4-Beta'
PROFILES=[
    ('iPhone-iOS-PWA',390,844,True,True),
    ('Smartphone',412,915,True,True),
    ('Smartphone-Querformat',844,390,True,True),
    ('Tablet',820,1180,True,False),
    ('Desktop',1440,1000,False,False),
]
ROUTES=[
    '', 'analogsignal/', 'einheitendatenbank/', 'einheitenrechner/', 'pf-rechner/',
    'pt-rechner/', 'siemens-analogwert-rechner/', 'spannungsfall-rechner/',
    'werkstoffdatenbank/', 'wissensdatenbank/',
    'wissensdatenbank/air-torque-antrieb-drehrichtung/',
    'wissensdatenbank/endress-hauser-promass-einbaulage/',
    'wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/',
    'wissensdatenbank/siemens-sps-rohwert/',
    'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/',
    'wissensdatenbank/werkstoff-nachschlagewerk/',
]
checks=0; failures=[]
def check(value,message):
    global checks
    checks+=1
    if not value: failures.append(message)
def alpha(value):
    value=(value or '').strip().lower()
    if value=='transparent': return 0.0
    m=re.fullmatch(r'rgba\([^,]+,[^,]+,[^,]+,\s*([0-9.]+)\)',value)
    if m: return float(m.group(1))
    if value.startswith('rgb('): return 1.0
    return 1.0

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for profile,width,height,has_touch,is_mobile in PROFILES:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=has_touch,is_mobile=is_mobile)
            page=context.new_page()
            for route in ROUTES:
                response=page.goto(urljoin(BASE,route),wait_until='networkidle')
                label=f'{profile} {route or "/"}'
                check(response and response.ok,f'{label}: HTTP nicht OK')
                state=page.evaluate("""()=>{
                  const home=document.body.dataset.skPage==='start';
                  const frame=document.querySelector(home?'.pct-home-screen':'.sk-app-frame');
                  const header=document.querySelector(home?'.pct-home-head':'.sk-global-header');
                  const footer=document.querySelector(home?'.pct-home-footer':'.sk-footer');
                  const css=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return {
                    bg:s.backgroundColor,bgi:s.backgroundImage,shadow:s.boxShadow,
                    top:s.borderTopColor,bottom:s.borderBottomColor,
                    rect:{left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height}}};
                  return {version:document.body.dataset.skVersion,frame:css(frame),header:css(header),footer:css(footer)};
                }""")
                check(state['version']==VERSION,f'{label}: Version {state["version"]}')
                for part in ('header','footer'):
                    item=state[part]
                    check(alpha(item['bg'])==0.0 and item['bgi']=='none',f'{label}: {part} besitzt Eigenfläche {item}')
                    check(item['shadow']=='none',f'{label}: {part} besitzt aufgesetzten Schatten {item["shadow"]}')
                check(alpha(state['header']['bottom'])<=.10,f'{label}: Header-Trennlinie zu stark {state["header"]["bottom"]}')
                check(alpha(state['footer']['top'])<=.10,f'{label}: Footer-Trennlinie zu stark {state["footer"]["top"]}')
                check(alpha(state['frame']['bg'])>=.99 or state['frame']['bgi']!='none',f'{label}: Standard-App-Rechteck ohne App-Hintergrund')
                fr,hr,rr=state['frame']['rect'],state['header']['rect'],state['footer']['rect']
                check(hr['left']>=fr['left']-1 and hr['right']<=fr['right']+1 and rr['left']>=fr['left']-1 and rr['right']<=fr['right']+1,
                      f'{label}: Header/Footer außerhalb Standard-App-Rechteck')
            context.close()
    finally:
        browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} visuelle Shell-Prüfungen')
    for failure in failures: print('-',failure)
    sys.exit(1)
print(f'PASS · {checks} visuelle Shell-Prüfungen · 16 Routen · 5 Profile · durchgängiger App-Hintergrund')
