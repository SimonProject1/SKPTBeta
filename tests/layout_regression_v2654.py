#!/usr/bin/env python3
"""V2.6.5.4-Beta: vollständiger Positionsabgleich von App-Rahmen, Header, Inhalt und Footer."""
from __future__ import annotations
import glob, os, sys
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
checks=0;failures=[]
def check(value,message):
    global checks
    checks+=1
    if not value: failures.append(message)
def close(a,b,tol=1.25): return abs(a-b)<=tol
def rect_stable(a,b,tol=.75): return all(abs(a[k]-b[k])<=tol for k in ('x','y','width','height'))

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for profile,width,height,has_touch,is_mobile in PROFILES:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=has_touch,is_mobile=is_mobile)
            page=context.new_page()
            expected_header=None
            for route in ROUTES:
                errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
                response=page.goto(urljoin(BASE,route),wait_until='networkidle')
                label=f'{profile} {route or "/"}'
                check(response and response.ok,f'{label}: HTTP nicht OK')
                check(not errors,f'{label}: JavaScript-Fehler {errors}')
                state=page.evaluate("""()=>{
                  const home=document.body.dataset.skPage==='start';
                  const frame=document.querySelector(home?'.pct-home-screen':'.sk-app-frame');
                  const header=document.querySelector(home?'.pct-home-head':'.sk-global-header');
                  const content=document.querySelector(home?'#pctHomeGrid':'.sk-app-scroll');
                  const footer=document.querySelector(home?'.pct-home-footer':'.sk-footer');
                  const controls=[...header.querySelectorAll(home?'.pct-home-search-trigger,.pct-home-quick-actions>.sk-favorites-trigger':'.pct-header-actions>.pct-control')];
                  const logo=header.querySelector(home?'.pct-home-brand-mark img':'.sk-header-logo');
                  const release=header.querySelector(home?'.pct-home-release-module':'.sk-header-release-module');
                  const rect=n=>n?.getBoundingClientRect().toJSON();
                  const center=n=>{const r=n.getBoundingClientRect();return r.top+r.height/2};
                  return {home,version:document.body.dataset.skVersion,frame:rect(frame),header:rect(header),content:rect(content),footer:rect(footer),
                    controls:controls.map(rect),controlCenters:controls.map(center),logo:rect(logo),logoCenter:logo?center(logo):null,release:rect(release),releaseCenter:release?center(release):null,
                    headerCenter:center(header),frameContains:frame.contains(header)&&frame.contains(content)&&frame.contains(footer),
                    documentOverflow:document.documentElement.scrollWidth-innerWidth,bodyOverflow:document.body.scrollWidth-innerWidth,
                    frameOverflow:frame.scrollWidth-frame.clientWidth,contentOverflow:content.scrollWidth-content.clientWidth,
                    footerPosition:getComputedStyle(footer).position,contentOverflowY:getComputedStyle(content).overflowY,
                    headerTransform:getComputedStyle(header).transform,footerTransform:getComputedStyle(footer).transform,
                    broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)};
                }""")
                check(state['version']==VERSION,f'{label}: Version {state["version"]}')
                check(state['frameContains'],f'{label}: Header/Inhalt/Footer nicht im Standardrahmen')
                check(state['frame'] and state['header'] and state['content'] and state['footer'],f'{label}: Layoutknoten fehlen')
                if not all(state[x] for x in ('frame','header','content','footer')): continue
                fr,hr,cr,rr=state['frame'],state['header'],state['content'],state['footer']
                check(fr['left']>=-1 and fr['right']<=width+1 and fr['top']>=-1 and fr['bottom']<=height+1,f'{label}: Rahmen außerhalb Viewport {fr}')
                check(close(hr['top'],fr['top'],3) and hr['left']>=fr['left']-1 and hr['right']<=fr['right']+1,f'{label}: Header ohne gemeinsame obere Referenz {hr}/{fr}')
                check(cr['top']>=hr['bottom']-1 and cr['bottom']<=rr['top']+1,f'{label}: Inhalt überlappt Header/Footer {hr}/{cr}/{rr}')
                check(rr['left']>=fr['left']-1 and rr['right']<=fr['right']+1 and close(rr['bottom'],fr['bottom'],3),f'{label}: Footer ohne gemeinsame untere Referenz {rr}/{fr}')
                expected_header=expected_header or hr['height']
                check(close(hr['height'],expected_header,.75),f'{label}: Headerhöhe {hr["height"]} statt {expected_header}')
                check(all(abs(value-state['headerCenter'])<=2.25 for value in state['controlCenters']),f'{label}: Headerbuttons nicht auf Mittellinie {state}')
                check(state['logoCenter'] is not None and abs(state['logoCenter']-state['headerCenter'])<=2.25,f'{label}: Logo nicht auf Mittellinie')
                check(state['releaseCenter'] is not None and abs(state['releaseCenter']-state['headerCenter'])<=2.25,f'{label}: Versionsmodul nicht auf Mittellinie')
                check(state['documentOverflow']<=1 and state['bodyOverflow']<=1 and state['frameOverflow']<=1 and state['contentOverflow']<=1,f'{label}: horizontaler Überlauf {state}')
                flow_ok=state['contentOverflowY']=='hidden' if state['home'] else state['contentOverflowY'] in ('auto','scroll')
                check(state['footerPosition']=='relative' and flow_ok,f'{label}: Footer/Scrollfluss falsch {state}')
                check(state['headerTransform']=='none' and state['footerTransform']=='none',f'{label}: Header/Footer transformiert')
                check(not state['broken'],f'{label}: defekte Bilder {state["broken"]}')

                controls=page.locator('.pct-home-quick-actions>button:visible' if state['home'] else '.pct-header-actions>.pct-control:visible')
                if controls.count():
                    control=controls.first;base=control.bounding_box();control.hover();hover=control.bounding_box();control.focus();focus=control.bounding_box();
                    control.dispatch_event('pointerdown',{'pointerId':77,'pointerType':'mouse','buttons':1,'bubbles':True});pressed=control.bounding_box();control.dispatch_event('pointerup',{'pointerId':77,'pointerType':'mouse','buttons':0,'bubbles':True})
                    check(rect_stable(base,hover) and rect_stable(base,focus) and rect_stable(base,pressed),f'{label}: Headercontrol bewegt sich bei Interaktion')
            context.close()
    finally:
        browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Positionsprüfungen')
    for failure in failures: print('-',failure)
    sys.exit(1)
print(f'PASS · {checks} Positionsprüfungen · 16 Routen · 5 Profile · Header/Footer/Content · Interaktionsstabilität · Reflow')
