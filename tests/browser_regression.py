#!/usr/bin/env python3
"""Playwright-Browserprüfung: 16 Seiten, 3 Viewports, 6 Rechner und Offline."""
from __future__ import annotations
import os, sys, glob
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
ROUTES=['','analogsignal/','pf-rechner/','pt-rechner/','einheitenrechner/','spannungsfall-rechner/','siemens-analogwert-rechner/','einheitendatenbank/','werkstoffdatenbank/','messstellen-doku/','wissensdatenbank/','wissensdatenbank/air-torque-antrieb-drehrichtung/','wissensdatenbank/endress-hauser-promass-einbaulage/','wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','wissensdatenbank/siemens-sps-rohwert/','wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/']
VIEWPORTS=[('Smartphone',390,844),('Tablet',820,1180),('Desktop',1440,1000)]
failures=[]; checks=0

def check(condition,message):
    global checks; checks+=1
    if not condition: failures.append(message)

def goto(page,route):
    return page.goto(urljoin(BASE,route),wait_until='networkidle')

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for name,width,height in VIEWPORTS:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
            page=context.new_page()
            shared_reference=None
            for route in ROUTES:
                response=goto(page,route)
                check(response is not None and response.ok,f'{name} {route or "/"}: HTTP {response.status if response else "keine Antwort"}')
                state=page.evaluate("""()=>{const s=document.querySelector('.sk-app-scroll'),h=document.querySelector('.pct-home-head,.sk-header-inner'),f=document.querySelector('.sk-footer'),frame=document.querySelector('.pct-home-screen,.sk-app-frame'),r=n=>n?({top:n.getBoundingClientRect().top,right:n.getBoundingClientRect().right,bottom:n.getBoundingClientRect().bottom,left:n.getBoundingClientRect().left,width:n.getBoundingClientRect().width,height:n.getBoundingClientRect().height}):null,fs=f?getComputedStyle(f):null;return{doc:document.documentElement.scrollWidth>innerWidth+2,scroll:s?s.scrollWidth>s.clientWidth+2:false,h:r(h),f:r(f),frame:r(frame),footerStyle:fs?{borderTop:fs.borderTopWidth,outline:fs.outlineWidth,shadow:fs.boxShadow,background:fs.backgroundColor}:null,vw:innerWidth,vh:innerHeight}}""")
                check(not state['doc'],f'{name} {route or "/"}: horizontaler Dokumentüberlauf')
                check(not state['scroll'],f'{name} {route or "/"}: horizontaler Inhaltsüberlauf')
                check(state['h'] and state['h']['top']>=-1 and state['h']['right']<=state['vw']+1,f'{name} {route or "/"}: Header außerhalb des Viewports')
                check(state['f'] and state['f']['bottom']<=state['vh']+1 and state['f']['left']>=-1,f'{name} {route or "/"}: Footer außerhalb des Viewports')
                check(state['footerStyle'] and state['footerStyle']['borderTop']=='0px' and state['footerStyle']['outline']=='0px' and state['footerStyle']['shadow']=='none',f'{name} {route or "/"}: Footer besitzt noch Kontur/Schatten {state["footerStyle"]}')
                if shared_reference is None:
                    shared_reference={'header':state['h'],'footer':state['f'],'frame':state['frame']}
                else:
                    for area,key in (('Header','header'),('Footer','footer'),('Rahmen','frame')):
                        current=state['h'] if key=='header' else state['f'] if key=='footer' else state['frame']
                        reference=shared_reference[key]
                        check(current is not None and reference is not None and abs(current['width']-reference['width'])<=1 and abs(current['height']-reference['height'])<=1,f'{name} {route}: {area} weicht von Startseite ab ({current} statt {reference})')
            context.close()

        context=browser.new_context(viewport={'width':390,'height':844}); page=context.new_page();goto(page,'')
        home=page.evaluate("""()=>{const g=document.querySelector('#pctHomeGrid'),b=document.querySelector('#pctHomeGrid .sk-favorite-button'),t=[...document.querySelectorAll('.sk-home-app-title')];return{columns:getComputedStyle(g).gridTemplateColumns.split(' ').filter(Boolean).length,touch:b?Math.min(b.getBoundingClientRect().width,b.getBoundingClientRect().height):0,titleOverflow:t.some(x=>x.scrollWidth>x.clientWidth+2),external:document.querySelector('[data-app-id="eh-device-viewer"]')?.href}}""")
        check(home['columns']==3,f'Smartphone-Startseite: {home["columns"]} statt 3 Spalten');check(home['touch']>=44,f'Favoriten-Touchziel nur {home["touch"]} px');check(not home['titleOverflow'],'App-Titel läuft horizontal über');check(home['external']=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H-Ziel falsch')

        goto(page,'einheitendatenbank/');page.wait_for_selector('.unit-category-card')
        unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open).length,favorites:!!document.querySelector('#unitFavoritesPanel')})""")
        check(unit['open']==0,f'Einheitendatenbank: {unit["open"]} Kategorien initial geöffnet');check(unit['favorites'],'Einheiten-Favoritenbereich fehlt')
        page.fill('#unitSearch','Fahrenheit');page.wait_for_timeout(100);unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open&&!x.hidden).length,rows:[...document.querySelectorAll('#unitCategoryList .unit-row')].filter(x=>!x.hidden).length})""")
        check(unit['open']>=1 and unit['rows']>=1,'Einheitensuche öffnet Treffer nicht automatisch')

        goto(page,'werkstoffdatenbank/');page.wait_for_selector('.material-compare-table td');material=page.evaluate("""()=>({row:getComputedStyle(document.querySelector('.material-compare-table tbody tr')).display,label:document.querySelector('.material-compare-table td')?.dataset.label||''})""")
        check(material['row']=='block','Werkstoffvergleich mobil nicht gestapelt');check(bool(material['label']),'Mobile Werkstoff-Schlüssel fehlen')

        goto(page,'messstellen-doku/');mess=page.evaluate("""()=>{const n=document.querySelector('#note'),i=document.querySelector('#tag');return{note:n.getBoundingClientRect().height,input:i.getBoundingClientRect().height,version:document.querySelector('.sk-header-version')?.textContent.trim()||''}}""")
        check(mess['note']<=60,f'Messstellen-Doku: Bemerkungsfeld mit {mess["note"]} px zu hoch')
        check(mess['input']<=44,f'Messstellen-Doku: Eingabefeld mit {mess["input"]} px zu hoch')
        check(mess['version']=='V2.5.2.1-Beta','Messstellen-Doku: gemeinsamer Versionskopf fehlt')

        goto(page,'wissensdatenbank/endress-hauser-promass-einbaulage/');page.wait_for_selector('.kb-detail-group');knowledge=page.evaluate("""()=>({short:!!document.querySelector('.kb-short-answer'),closed:[...document.querySelectorAll('.kb-detail-group')].every(d=>!d.open),sources:!!document.querySelector('.kb-source-bundle'),safety:[...document.querySelectorAll('.kb-callout.danger,.kb-callout.warning')].every(n=>n.offsetParent!==null)})""")
        check(knowledge['short'],'Kurzantwort fehlt');check(knowledge['closed'],'Details nicht initial geschlossen');check(knowledge['sources'],'Quellenbündel fehlt');check(knowledge['safety'],'Sicherheitshinweis ausgeblendet')

        goto(page,'analogsignal/');check('12' in page.text_content('#out') and 'mA' in page.text_content('#out'),'Analogsignal 50 → 12 mA fehlgeschlagen');check('50' in page.text_content('#pct'),'Analogsignal 50 % fehlgeschlagen')
        goto(page,'pf-rechner/');check('0,16' in page.text_content('#k'),'P+F K=0,16 fehlgeschlagen');check(page.text_content('#n').strip()=='4','P+F Nullpunkt=4 fehlgeschlagen')
        goto(page,'pt-rechner/');check('100' in page.text_content('#out') and 'Ω' in page.text_content('#out'),'Pt100 0 °C → 100 Ω fehlgeschlagen')
        goto(page,'einheitenrechner/');check('100' in page.text_content('#out') and 'kPa' in page.text_content('#out'),'1 bar → 100 kPa fehlgeschlagen')
        goto(page,'siemens-analogwert-rechner/');check('13.824' in page.text_content('#rawResult').replace(' ',''),'Siemens 12 mA → 13.824 fehlgeschlagen');check('50' in page.text_content('#physicalResult'),'Siemens 12 mA → 50 °C fehlgeschlagen')
        goto(page,'spannungsfall-rechner/');page.fill('#current','16');page.fill('#length','35');page.click('#calculate');page.wait_for_selector('#result:not([hidden])');check('6,93' in page.text_content('#dropV'),'Spannungsfall ΔU≈6,93 V fehlgeschlagen');check('1,73' in page.text_content('#dropPercent'),'Spannungsfall ≈1,73 % fehlgeschlagen');check('393,07' in page.text_content('#loadVoltage'),'Lastspannung ≈393,07 V fehlgeschlagen')

        goto(page,'');page.evaluate("""async()=>{if('serviceWorker'in navigator)await navigator.serviceWorker.ready}""");page.wait_for_timeout(600);context.set_offline(True)
        for route in ('einheitenrechner/','wissensdatenbank/endress-hauser-promass-einbaulage/'):
            try:
                response=page.goto(urljoin(BASE,route),wait_until='domcontentloaded',timeout=15000)
                check(response is not None and response.status==200,f'Offline {route}: keine HTTP-200-Antwort');check('SK PCT Tools' in page.title(),f'Offline {route}: falsches Dokument')
            except Exception as exc: check(False,f'Offline {route}: {exc}')
        context.close()
    finally: browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Prüfungen');[print(f'- {item}') for item in failures];sys.exit(1)
print(f'PASS · {checks} Browserprüfungen · 16 Seiten × 3 Viewports · 6 Rechnerreferenzen · Offline')
