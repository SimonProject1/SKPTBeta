#!/usr/bin/env python3
"""Playwright-Browserprüfung: 15 Seiten, 3 Viewports, Reflow, 6 Rechner und Offline."""
from __future__ import annotations
import os, sys, glob
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
ROUTES=['','analogsignal/','pf-rechner/','pt-rechner/','einheitenrechner/','spannungsfall-rechner/','siemens-analogwert-rechner/','einheitendatenbank/','werkstoffdatenbank/','wissensdatenbank/','wissensdatenbank/air-torque-antrieb-drehrichtung/','wissensdatenbank/endress-hauser-promass-einbaulage/','wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','wissensdatenbank/siemens-sps-rohwert/','wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/']
VIEWPORTS=[('Smartphone',390,844),('Tablet',820,1180),('Desktop',1440,1000)]
REFLOW_ROUTES=['','pt-rechner/','spannungsfall-rechner/','werkstoffdatenbank/','wissensdatenbank/endress-hauser-promass-einbaulage/']
EXPERIENCE_SOURCE='Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)'
failures=[]; checks=0

def check(condition,message):
    global checks; checks+=1
    if not condition: failures.append(message)

def goto(page,route): return page.goto(urljoin(BASE,route),wait_until='networkidle')

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for name,width,height in VIEWPORTS:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
            page=context.new_page(); shared_reference=None
            for route in ROUTES:
                response=goto(page,route)
                check(response is not None and response.ok,f'{name} {route or "/"}: HTTP {response.status if response else "keine Antwort"}')
                state=page.evaluate("""()=>{const s=document.querySelector('.sk-app-scroll'),h=document.querySelector('.pct-home-head,.sk-header-inner'),f=document.querySelector('.sk-footer'),frame=document.querySelector('.pct-home-screen,.sk-app-frame'),r=n=>n?({top:n.getBoundingClientRect().top,right:n.getBoundingClientRect().right,bottom:n.getBoundingClientRect().bottom,left:n.getBoundingClientRect().left,width:n.getBoundingClientRect().width,height:n.getBoundingClientRect().height}):null,fs=f?getComputedStyle(f):null,nav=[...document.querySelectorAll('.pct-header-actions img.pct-nav-graphic')];return{doc:document.documentElement.scrollWidth>innerWidth+2,scroll:s?s.scrollWidth>s.clientWidth+2:false,h:r(h),f:r(f),frame:r(frame),footerStyle:fs?{borderTop:fs.borderTopWidth,outline:fs.outlineWidth,shadow:fs.boxShadow}:null,vw:innerWidth,vh:innerHeight,h1:document.querySelectorAll('h1').length,referrer:document.querySelector('meta[name=referrer]')?.content||'',nav:{count:nav.length,png:nav.every(i=>i.src.split('?')[0].endsWith('.png')),broken:nav.some(i=>!i.complete||i.naturalWidth===0)}}}""")
                check(not state['doc'],f'{name} {route or "/"}: horizontaler Dokumentüberlauf')
                check(not state['scroll'],f'{name} {route or "/"}: horizontaler Inhaltsüberlauf')
                check(state['h'] and state['h']['top']>=-1 and state['h']['right']<=state['vw']+1,f'{name} {route or "/"}: Header außerhalb des Viewports')
                check(state['f'] and state['f']['bottom']<=state['vh']+1 and state['f']['left']>=-1,f'{name} {route or "/"}: Footer außerhalb des Viewports')
                check(state['footerStyle'] and state['footerStyle']['borderTop']=='0px' and state['footerStyle']['outline']=='0px' and state['footerStyle']['shadow']=='none',f'{name} {route or "/"}: Footer besitzt Kontur/Schatten')
                check(state['h1']==1,f'{name} {route or "/"}: {state["h1"]} H1 statt genau einer')
                check(state['referrer']=='no-referrer',f'{name} {route or "/"}: Referrer-Schutz fehlt')
                if route: check(state['nav']['count']==2 and state['nav']['png'] and not state['nav']['broken'],f'{name} {route}: interne Home-/Zurück-PNG-Navigation fehlerhaft: {state["nav"]}')
                if not route:
                    app_icons=page.evaluate("""()=>[...document.querySelectorAll('#pctHomeGrid .sk-home-app')].map(app=>{const frame=app.querySelector('.sk-home-icon'),image=app.querySelector('img.sk-nav-graphic'),star=app.querySelector('.sk-favorite-button'),fr=frame.getBoundingClientRect(),ir=image.getBoundingClientRect(),sr=star.getBoundingClientRect(),fs=getComputedStyle(frame),ring=getComputedStyle(star,'::after'),inset=parseFloat(ring.inset)||0,visible={left:sr.left+inset,top:sr.top+inset,right:sr.right-inset,bottom:sr.bottom-inset};return{fw:fr.width,fh:fr.height,iw:ir.width,ih:ir.height,border:fs.borderTopWidth,shadow:fs.boxShadow,transform:fs.transform,arc:getComputedStyle(frame,'::before').backgroundImage,starX:sr.left-fr.right,starY:sr.top-fr.top,touch:Math.min(sr.width,sr.height),visible:sr.width-2*inset,inside:visible.left>=fr.left-1&&visible.top>=fr.top-1&&visible.right<=fr.right+1&&visible.bottom<=fr.bottom+1,natural:[image.naturalWidth,image.naturalHeight],broken:!image.complete||image.naturalWidth===0}})""")
                    check(len(app_icons)==10,f'{name} Startseite: {len(app_icons)} statt 10 Icon-Rahmen')
                    if app_icons:
                        first=app_icons[0]
                        check(all(abs(x['fw']-first['fw'])<=1 and abs(x['fh']-first['fh'])<=1 and x['border']==first['border'] and x['shadow']==first['shadow'] and x['transform']==first['transform'] for x in app_icons),f'{name} Startseite: Außenmaß, Rahmen, Perspektive oder Schatten der Icons uneinheitlich')
                        check(all(abs(x['iw']-first['iw'])<=1 and abs(x['ih']-first['ih'])<=1 and x['natural']==[512,512] and not x['broken'] for x in app_icons),f'{name} Startseite: PNG-Innenmaß oder natürliche Größe uneinheitlich')
                        check(all(abs(x['starX']-first['starX'])<=1 and abs(x['starY']-first['starY'])<=1 for x in app_icons),f'{name} Startseite: Favoritensternposition uneinheitlich')
                        check(all(x['touch']>=44 and 21<=x['visible']<=23 and x['inside'] for x in app_icons),f'{name} Startseite: Favoritenkreis/Touchfläche fehlerhaft: {app_icons}')
                        check(all(x['arc']=='none' for x in app_icons),f'{name} Startseite: alte innere CSS-Rahmenlinie ist noch aktiv')
                signs=page.evaluate("""()=>[...document.querySelectorAll('button.pct-control--sign')].map(button=>{const box=button.getBoundingClientRect(),style=getComputedStyle(button),parent=button.parentElement.getBoundingClientRect();return{width:box.width,height:box.height,radius:style.borderRadius,touch:style.touchAction,center:Math.abs((box.top+box.height/2)-(parent.top+parent.height/2))}})""")
                if signs:
                    check(all(round(s['width'])==44 and round(s['height'])==44 for s in signs),f'{name} {route}: ±-Taster nicht durchgehend 44 × 44 px: {signs}')
                    check(all(s['radius'].startswith('13px') and s['touch']=='manipulation' for s in signs),f'{name} {route}: ±-Stil/Touchregel abweichend: {signs}')
                    check(all(s['center']<=1 for s in signs),f'{name} {route}: ±-Taster nicht mittig ausgerichtet: {signs}')
                if shared_reference is None: shared_reference={'header':state['h'],'footer':state['f'],'frame':state['frame']}
                else:
                    for area,key in (('Header','header'),('Footer','footer'),('Rahmen','frame')):
                        current=state['h'] if key=='header' else state['f'] if key=='footer' else state['frame']; reference=shared_reference[key]
                        check(current is not None and reference is not None and abs(current['width']-reference['width'])<=1 and abs(current['height']-reference['height'])<=1,f'{name} {route}: {area} weicht von Startseite ab')
            context.close()

        # WCAG-Reflow-Sanity: 320 CSS px entspricht der üblichen 400-%-Reflow-Prüfbreite.
        context=browser.new_context(viewport={'width':320,'height':900},device_scale_factor=1); page=context.new_page()
        for route in REFLOW_ROUTES:
            goto(page,route)
            state=page.evaluate("""()=>({doc:document.documentElement.scrollWidth,body:document.body.scrollWidth,vw:innerWidth,controls:[...document.querySelectorAll('button,a,input,select')].filter(x=>x.offsetParent!==null&&!x.closest('.sk-favorites-drawer:not(.open)')).some(x=>x.getBoundingClientRect().right>innerWidth+2||x.getBoundingClientRect().left<-2)})""")
            check(state['doc']<=state['vw']+2 and state['body']<=state['vw']+2,f'Reflow 320 px {route or "/"}: horizontaler Überlauf {state}')
            check(not state['controls'],f'Reflow 320 px {route or "/"}: Bedienelement außerhalb des Viewports')
        context.close()

        context=browser.new_context(viewport={'width':390,'height':844}); page=context.new_page();goto(page,'')
        home=page.evaluate("""()=>{const g=document.querySelector('#pctHomeGrid'),b=document.querySelector('#pctHomeGrid .sk-favorite-button'),t=[...document.querySelectorAll('.sk-home-app-title')],icons=[...document.querySelectorAll('#pctHomeGrid img.sk-nav-graphic')],boxes=[...document.querySelectorAll('#pctHomeGrid .sk-home-icon')],forbidden=/RECHNER|WISSEN|EXTERN|MATERIAL|PCT|PIPING/i,ring=b?getComputedStyle(b,'::after'):null;return{apps:document.querySelectorAll('#pctHomeGrid .sk-home-app').length,favorites:document.querySelectorAll('#pctHomeGrid .sk-favorite-button').length,columns:getComputedStyle(g).gridTemplateColumns.split(' ').filter(Boolean).length,touch:b?Math.min(b.getBoundingClientRect().width,b.getBoundingClientRect().height):0,visible:b?b.getBoundingClientRect().width-2*(parseFloat(ring.inset)||0):0,inactiveGlow:ring?.boxShadow||'',titles:t.map(x=>x.textContent.trim()),titleOverflow:t.some(x=>x.scrollWidth>x.clientWidth+2),external:document.querySelector('[data-app-id="eh-device-viewer"]')?.href,mess:!!document.querySelector('[data-app-id="messstellen-doku"]'),icons:icons.length,iconFiles:new Set(icons.map(i=>i.src.split('?')[0])).size,iconBroken:icons.some(i=>!i.complete||i.naturalWidth===0),png:icons.every(i=>i.src.split('?')[0].endsWith('.png')),versioned:icons.every(i=>i.src.includes('/v2-6-1-3-')),overlayNodes:document.querySelectorAll('.knowledge-icon-badge,[data-icon-area],[data-discipline-overlay]').length,pseudoOverlay:boxes.some(x=>forbidden.test(getComputedStyle(x,'::after').content||''))}}""")
        check(home['apps']==10,f'Startseite: {home["apps"]} statt 10 Apps');check(home['favorites']==10,f'Startseite: {home["favorites"]} statt 10 Favoritensterne');check(home['columns']==3,f'Smartphone-Startseite: {home["columns"]} statt 3 Spalten');check(home['touch']>=44,f'Favoriten-Touchziel nur {home["touch"]} px');check(21<=home['visible']<=23,f'Sichtbarer Favoritenkreis ist {home["visible"]} statt rund 22 px');check('120, 255, 50' not in home['inactiveGlow'],f'Inaktiver Favorit leuchtet grün: {home["inactiveGlow"]}');check(all(title in home['titles'] for title in ('Umrechnen','Siemens RAW','Werkstoffe','Wissen')),f'Verkürzte Titel fehlen: {home["titles"]}');check(not home['titleOverflow'],'App-Titel läuft horizontal über');check(not home['mess'],'Messstellen-Doku noch vorhanden');check(home['external']=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H-Ziel falsch');check(home['icons']==10 and home['iconFiles']==10 and home['png'] and home['versioned'] and not home['iconBroken'],f'Startseiten-PNGs fehlerhaft: {home}');check(home['overlayNodes']==0 and not home['pseudoOverlay'],f'Startseite besitzt noch ein zusätzliches Fachbereichs-Overlay: {home}')
        first_favorite=page.locator('#pctHomeGrid .sk-favorite-button').first;first_favorite.click();active=page.evaluate("""()=>{const b=document.querySelector('#pctHomeGrid .sk-favorite-button'),ring=getComputedStyle(b,'::after');return{active:b.dataset.active,shadow:ring.boxShadow,color:getComputedStyle(b).color}}""");check(active['active']=='true' and ('120, 255, 50' in active['shadow'] or '120, 255, 50' in active['color']),f'Aktiver Favorit leuchtet nicht grün: {active}')

        goto(page,'einheitendatenbank/');page.wait_for_selector('.unit-category-card')
        unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open).length,favorites:!!document.querySelector('#unitFavoritesPanel')})""")
        check(unit['open']==0,f'Einheitendatenbank: {unit["open"]} Kategorien initial geöffnet');check(unit['favorites'],'Einheiten-Favoritenbereich fehlt')
        page.fill('#unitSearch','Fahrenheit');page.wait_for_timeout(100);unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open&&!x.hidden).length,rows:[...document.querySelectorAll('#unitCategoryList .unit-row')].filter(x=>!x.hidden).length})""")
        check(unit['open']>=1 and unit['rows']>=1,'Einheitensuche öffnet Treffer nicht automatisch')

        goto(page,'werkstoffdatenbank/');page.wait_for_selector('.material-compare-table td');material=page.evaluate("""()=>({row:getComputedStyle(document.querySelector('.material-compare-table tbody tr')).display,label:document.querySelector('.material-compare-table td')?.dataset.label||''})""")
        check(material['row']=='block','Werkstoffvergleich mobil nicht gestapelt');check(bool(material['label']),'Mobile Werkstoff-Schlüssel fehlen')

        goto(page,'wissensdatenbank/');page.wait_for_selector('.knowledge-brand-logo');knowledge_icons=page.evaluate("""()=>{const icons=[...document.querySelectorAll('img.knowledge-brand-logo')],hub=[...document.querySelectorAll('.knowledge-hub img.knowledge-brand-logo')],entries=[...document.querySelectorAll('.knowledge-entry img.knowledge-brand-logo')],boxes=[...document.querySelectorAll('.knowledge-home-icon')],forbidden=/RECHNER|WISSEN|EXTERN|MATERIAL|PCT|PIPING/i;return{count:icons.length,files:new Set(icons.map(i=>i.src.split('?')[0])).size,broken:icons.some(i=>!i.complete||i.naturalWidth===0),png:icons.every(i=>i.src.split('?')[0].endsWith('.png')),hubManufacturers:hub.every(i=>i.src.includes('manufacturer-')),entryBooks:entries.length===5&&entries.every(i=>i.src.includes('app-wissensdatenbank.png')),entryFavorites:document.querySelectorAll('.knowledge-entry .sk-favorite-button').length,versioned:icons.every(i=>i.src.includes('/v2-6-1-3-')),legacyBadges:document.querySelectorAll('.knowledge-icon-badge,[data-icon-area],[data-discipline-overlay]').length,pseudoOverlay:boxes.some(x=>forbidden.test(getComputedStyle(x,'::after').content||''))}}""")
        check(knowledge_icons['count']==10 and knowledge_icons['files']==6 and knowledge_icons['png'] and knowledge_icons['hubManufacturers'] and knowledge_icons['entryBooks'] and knowledge_icons['entryFavorites']==5 and knowledge_icons['versioned'] and knowledge_icons['legacyBadges']==0 and not knowledge_icons['pseudoOverlay'] and not knowledge_icons['broken'],f'Wissens-/Hersteller-PNGs fehlerhaft: {knowledge_icons}')
        goto(page,'wissensdatenbank/endress-hauser-promass-einbaulage/');page.wait_for_selector('.kb-detail-group');knowledge=page.evaluate("""()=>({short:!!document.querySelector('.kb-short-answer'),closed:[...document.querySelectorAll('.kb-detail-group')].every(d=>!d.open),sources:document.querySelector('.kb-source-bundle')?.textContent||'',safety:[...document.querySelectorAll('.kb-callout.danger,.kb-callout.warning')].every(n=>n.offsetParent!==null)})""")
        check(knowledge['short'],'Kurzantwort fehlt');check(knowledge['closed'],'Details nicht initial geschlossen');check(EXPERIENCE_SOURCE in knowledge['sources'],'Erfahrungsberichte fehlen im Quellenbündel');check(knowledge['safety'],'Sicherheitshinweis ausgeblendet')

        goto(page,'analogsignal/');check('12' in page.text_content('#out') and 'mA' in page.text_content('#out'),'Analogsignal 50 → 12 mA fehlgeschlagen');check('50' in page.text_content('#pct'),'Analogsignal 50 % fehlgeschlagen')
        goto(page,'pf-rechner/');check('0,16' in page.text_content('#k'),'P+F K=0,16 fehlgeschlagen');check(page.text_content('#n').strip()=='4','P+F Nullpunkt=4 fehlgeschlagen')

        goto(page,'pt-rechner/');check('100' in page.text_content('#out') and 'Ω' in page.text_content('#out'),'Pt100 0 °C → 100 Ω fehlgeschlagen')
        page.fill('#x','900');check('Außerhalb IEC 60751' in page.text_content('#out'),'Pt100 Temperatur >850 °C wird nicht abgewiesen')
        page.fill('#x','-201');check('Außerhalb IEC 60751' in page.text_content('#out'),'Pt100 Temperatur <-200 °C wird nicht abgewiesen')
        page.select_option('#dir','rt');page.fill('#x','404.97');check('Außerhalb IEC 60751' in page.text_content('#out'),'Pt100 Widerstand über Messbereich wird nicht abgewiesen')
        page.fill('#x','1');check('Außerhalb IEC 60751' in page.text_content('#out'),'Pt100 Widerstand unter Messbereich wird nicht abgewiesen')
        page.select_option('#sensor','1000');page.fill('#x','1000');check('0' in page.text_content('#out'),'Pt1000 1000 Ω → 0 °C fehlgeschlagen')

        goto(page,'einheitenrechner/');check('100' in page.text_content('#out') and 'kPa' in page.text_content('#out'),'1 bar → 100 kPa fehlgeschlagen')
        goto(page,'siemens-analogwert-rechner/');check('13.824' in page.text_content('#rawResult').replace(' ',''),'Siemens 12 mA → 13.824 fehlgeschlagen');check('50' in page.text_content('#physicalResult'),'Siemens 12 mA → 50 °C fehlgeschlagen')
        siemens=page.evaluate("""()=>{const host=document.querySelector('main.sk-app-scroll'),button=document.querySelector('#physicalMinSignToggle'),style=getComputedStyle(button),box=button.getBoundingClientRect();return{client:host.clientHeight,scroll:host.scrollHeight,hostOverflow:getComputedStyle(host).overflowY,touchAction:getComputedStyle(host).touchAction,buttonWidth:box.width,buttonHeight:box.height,buttonRadius:style.borderRadius}}""")
        page.locator('main.sk-app-scroll').hover(force=True);page.mouse.wheel(0,700);page.wait_for_timeout(150)
        check(siemens['scroll']>siemens['client'] and page.eval_on_selector('main.sk-app-scroll','e=>e.scrollTop')>0,'Siemens-Rechner: Inhalt lässt sich nicht scrollen')
        check(siemens['hostOverflow']=='scroll' and siemens['touchAction']=='pan-y','Siemens-Rechner: Touch-Scrollregeln fehlen')
        check(round(siemens['buttonWidth'])==44 and round(siemens['buttonHeight'])==44 and siemens['buttonRadius'].startswith('13px'),'Siemens-Rechner: ±-Taster fehlerhaft')

        goto(page,'spannungsfall-rechner/')
        initial=page.evaluate("""()=>({hidden:document.querySelector('#result').hidden,display:getComputedStyle(document.querySelector('#result')).display,height:document.querySelector('#result').getBoundingClientRect().height})""")
        check(initial['hidden'] and initial['display']=='none' and initial['height']==0,f'Spannungsfall-Ergebnis initial sichtbar: {initial}')
        page.fill('#current','16');page.fill('#length','35');page.click('#calculate');page.wait_for_selector('#result:not([hidden])');check('6,93' in page.text_content('#dropV'),'Spannungsfall ΔU≈6,93 V fehlgeschlagen');check('1,73' in page.text_content('#dropPercent'),'Spannungsfall ≈1,73 % fehlgeschlagen');check('393,07' in page.text_content('#loadVoltage'),'Lastspannung ≈393,07 V fehlgeschlagen')
        page.click('#reset');reset=page.evaluate("""()=>({I:document.querySelector('#current').value,L:document.querySelector('#length').value,hidden:document.querySelector('#result').hidden,display:getComputedStyle(document.querySelector('#result')).display,height:document.querySelector('#result').getBoundingClientRect().height})""")
        check(reset['I']=='' and reset['L']=='' and reset['hidden'] and reset['display']=='none' and reset['height']==0,f'Spannungsfall-Reset fehlerhaft: {reset}')

        # Reale Tap-Auslösung und Vorzeichenwechsel auf Smartphone und Tablet.
        touch_cases=[('analogsignal/','#x'),('pf-rechner/','#x2'),('pt-rechner/','#x'),('einheitenrechner/','#x'),('siemens-analogwert-rechner/','#physicalMin')]
        for device,width,height in (('Smartphone-Touch',390,844),('Tablet-Touch',820,1180)):
            touch_context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=True,is_mobile=True)
            touch_page=touch_context.new_page()
            for route,field in touch_cases:
                goto(touch_page,route);touch_page.fill(field,'7')
                button=touch_page.locator(f'{field}').locator('xpath=..').locator('button.pct-control--sign')
                check(button.count()==1,f'{device} {route}: eindeutiger ±-Taster fehlt')
                if button.count()==1:
                    button.tap();touch_page.wait_for_timeout(40)
                    check(touch_page.input_value(field)=='-7',f'{device} {route}: Vorzeichenwechsel per Tap fehlgeschlagen')
                    box=button.bounding_box();style=button.evaluate("b=>({touch:getComputedStyle(b).touchAction,radius:getComputedStyle(b).borderRadius})")
                    check(box is not None and round(box['width'])==44 and round(box['height'])==44,f'{device} {route}: Touchziel nicht 44 × 44 px')
                    check(style['touch']=='manipulation' and style['radius'].startswith('13px'),f'{device} {route}: Touch-/Designstandard abweichend')
            touch_context.close()

        goto(page,'');page.evaluate("""async()=>{if('serviceWorker'in navigator)await navigator.serviceWorker.ready}""");page.wait_for_timeout(600);context.set_offline(True)
        for route in ('einheitenrechner/','wissensdatenbank/endress-hauser-promass-einbaulage/'):
            try:
                response=page.goto(urljoin(BASE,route),wait_until='domcontentloaded',timeout=15000)
                check(response is not None and response.status==200,f'Offline {route}: keine HTTP-200-Antwort');check('SK PCT Tools' in page.title(),f'Offline {route}: falsches Dokument')
            except Exception as exc: check(False,f'Offline {route}: {exc}')
        context.close()

        # Neuinstallation/Upgrade: ein vorab angelegter Alt-Cache muss beim ersten
        # Aktivieren der neuen PWA verschwinden; nur der neue Epoch darf bleiben.
        upgrade_context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1)
        upgrade_page=upgrade_context.new_page()
        upgrade_page.goto(urljoin(BASE,'assets/icon-192.png'),wait_until='domcontentloaded')
        upgrade_page.evaluate("""async()=>{const c=await caches.open('sk-pct-tools-core-v2.6.1.0-Beta');await c.put('./legacy-icon.png',new Response('old'))}""")
        goto(upgrade_page,'')
        upgrade_page.evaluate("""async()=>{if('serviceWorker'in navigator)await navigator.serviceWorker.ready}""")
        upgrade_page.wait_for_timeout(900)
        cache_state=upgrade_page.evaluate("""async()=>{const keys=await caches.keys();return{keys,old:keys.some(k=>k.includes('2.6.1.0')),current:keys.filter(k=>k.startsWith('sk-pct-tools-')).every(k=>k.includes('v2-6-1-3-icons-r1'))}}""")
        check(not cache_state['old'] and cache_state['current'] and len(cache_state['keys'])>=2,f'PWA-Cache-Neuaufbau fehlerhaft: {cache_state}')
        upgrade_context.set_offline(True)
        upgrade_page.goto(urljoin(BASE,''),wait_until='domcontentloaded',timeout=15000)
        check('SK PCT Tools' in upgrade_page.title(),'Neuinstallationskontext ist offline nicht startfähig')
        upgrade_context.close()
    finally: browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Prüfungen');[print(f'- {item}') for item in failures];sys.exit(1)
print(f'PASS · {checks} Browserprüfungen · 15 Seiten × 3 Viewports · Reflow 320 px · 6 Rechnerreferenzen · Offline')
