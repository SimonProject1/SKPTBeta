#!/usr/bin/env python3
"""V2.6.5.3-Beta: Raster-, Rahmen-, Favoriten-, Touch- und Accessibility-Regression."""
from __future__ import annotations
import glob, json, os, sys
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
PROFILES=[
    ('Desktop',1440,1000,False,False,5),
    ('Tablet',820,1180,True,False,4),
    ('iPhone-Portrait',390,844,True,True,3),
    ('Smartphone-Portrait',412,915,True,True,3),
    ('Smartphone-Landscape',844,390,True,True,6),
]
ROUTES=[
    ('RECHNER','Analogsignal-Rechner','Prozesswert und Analogsignal umrechnen.','analogsignal/','app-analogsignal'),
    ('RECHNER','P+F-Rechner','K-Faktor und Nullpunkt berechnen.','pf-rechner/','app-pf-rechner'),
    ('RECHNER','Pt100 / Pt1000','Pt100 und Pt1000 in beide Richtungen.','pt-rechner/','app-pt-rechner'),
    ('RECHNER','Einheitenrechner','Alle Einheitenkategorien umrechnen.','einheitenrechner/','app-einheitenrechner'),
    ('WISSEN','Einheitendatenbank','Einheiten und persönliche Favoriten.','einheitendatenbank/','app-einheitendatenbank'),
    ('WISSEN','Werkstoffdatenbank','Werkstoffe zentral nachschlagen.','werkstoffdatenbank/','app-werkstoffdatenbank'),
    ('WISSEN','Wissensdatenbank','Anleitungen und Praxistipps.','wissensdatenbank/','app-wissensdatenbank'),
    ('RECHNER','Spannungsfall-Rechner','Spannungsfall berechnen.','spannungsfall-rechner/','app-spannungsfall'),
    ('RECHNER','Siemens Rohwert','Signale und Siemens-Rohwerte.','siemens-analogwert-rechner/','app-siemens-rohwert'),
    ('AIR TORQUE','Antrieb','Drehrichtung SCO und SCC.','wissensdatenbank/air-torque-antrieb-drehrichtung/','knowledge-air-torque-antrieb-drehrichtung'),
    ('ENDRESS+HAUSER · PROMASS','Einbaulage','Optimale Einbausituation.','wissensdatenbank/endress-hauser-promass-einbaulage/','knowledge-endress-hauser-promass-einbaulage'),
    ('SIEMENS · SITRANS P320','SIL Verriegelung','SIL-Verriegelung und Schreibschutz.','wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','knowledge-siemens-sitrans-p320-sil-verriegelung'),
    ('SIEMENS · SPS','Rohwert','Skalierung und Diagnosebereiche.','wissensdatenbank/siemens-sps-rohwert/','knowledge-siemens-sps-rohwert'),
    ('VACON','Frequenzumrichter','Ist-/Sollwert-Abweichung prüfen.','wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/','knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung'),
]
checks=0;failures=[]
def check(value,message):
    global checks
    checks+=1
    if not value: failures.append(message)
def goto(page,route=''):
    response=page.goto(urljoin(BASE,route),wait_until='networkidle')
    check(response and response.ok,f'{route or "/"}: HTTP nicht OK')

def rect_equal(a,b,tol=.75):
    return all(abs(a[k]-b[k])<=tol for k in ('x','y','width','height'))

def seed(page,count):
    items=[]
    for idx,(category,title,description,route,stem) in enumerate(ROUTES[:count]):
        # Der erste Datensatz simuliert einen aus V2.6.5.0 übernommenen Favoriten.
        version='v2-6-5-0' if idx==0 else 'v2-6-5-3'
        items.append({'url':urljoin(BASE,route),'title':title,'description':description,'category':category,'external':False,'icon':urljoin(BASE,f'assets/navigation-icons/{version}-{stem}.png')})
    page.evaluate("items=>localStorage.setItem('skPctToolsFavoritesV2',JSON.stringify(items))",items)
    page.reload(wait_until='networkidle')

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for name,width,height,has_touch,is_mobile,expected_columns in PROFILES:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=has_touch,is_mobile=is_mobile)
            page=context.new_page();errors=[];page.on('pageerror',lambda error:errors.append(str(error)))

            # Hersteller-Hub muss dieselbe Raster- und Icongeometrie wie Home verwenden.
            goto(page,'')
            home=page.evaluate("""()=>{const grid=document.querySelector('#pctHomeGrid'),card=grid.querySelector('.sk-home-app'),icon=card.querySelector('.sk-app-icon-wrapper'),title=card.querySelector('h2'),r=icon.getBoundingClientRect();return{columns:getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length,icon:{width:r.width,height:r.height},title:{font:parseFloat(getComputedStyle(title).fontSize),line:parseFloat(getComputedStyle(title).lineHeight)},frame:document.querySelector('.pct-home-screen').getBoundingClientRect().toJSON()}}""")
            check(home['columns']==expected_columns,f'{name}: Home-Raster {home["columns"]} statt {expected_columns}')
            goto(page,'wissensdatenbank/')
            hub=page.evaluate("""()=>{const grid=document.querySelector('.knowledge-hub'),cards=[...grid.querySelectorAll('.knowledge-hub-card:not([hidden])')],icon=cards[0].querySelector('.knowledge-home-icon'),title=cards[0].querySelector('h2'),r=icon.getBoundingClientRect(),search=document.querySelector('.knowledge-search-wrap').getBoundingClientRect(),first=cards[0].getBoundingClientRect(),last=cards.at(-1).getBoundingClientRect(),footer=document.querySelector('.sk-footer').getBoundingClientRect();return{cards:cards.length,columns:getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length,icon:{width:r.width,height:r.height},title:{font:parseFloat(getComputedStyle(title).fontSize),line:parseFloat(getComputedStyle(title).lineHeight)},searchGap:first.top-search.bottom,footerGap:footer.top-last.bottom,overflow:document.documentElement.scrollWidth-innerWidth}}""")
            check(hub['cards']==5 and hub['columns']==expected_columns,f'{name}: Hersteller-Hub {hub["cards"]} Karten / {hub["columns"]} Spalten statt 5 / {expected_columns}')
            check(abs(hub['icon']['width']-home['icon']['width'])<=1 and abs(hub['icon']['height']-home['icon']['height'])<=1,f'{name}: Herstellericon {hub["icon"]} weicht von Home {home["icon"]} ab')
            check(abs(hub['title']['font']-home['title']['font'])<=2 and abs(hub['title']['line']-home['title']['line'])<=3,f'{name}: Beschriftungsmaß Hub {hub["title"]} / Home {home["title"]}')
            check(hub['searchGap']>=-2 and hub['footerGap']>=-2 and abs(hub['searchGap']-hub['footerGap'])<=25,f'{name}: Inhaltsraum nicht ausgewogen zwischen Suche, Kacheln und Footer {hub}')
            check(hub['overflow']<=1,f'{name}: horizontaler Überlauf im Hersteller-Hub {hub}')

            # Suche, Filterung und vollständige Tap-/Tastaturnavigation bleiben erhalten.
            page.fill('#knowledgeSearch','Siemens');page.wait_for_timeout(80)
            filtered=page.evaluate("""()=>({visible:document.querySelectorAll('.knowledge-hub-card:not([hidden])').length,count:document.querySelector('#knowledgeResultCount').textContent})""")
            check(filtered['visible']==1 and filtered['count'].startswith('1 '),f'{name}: Wissenssuche fehlerhaft {filtered}')
            page.fill('#knowledgeSearch','');card=page.locator('.knowledge-hub-card').first
            base=card.bounding_box();card.hover();hover=card.bounding_box();card.focus();focus=card.bounding_box()
            box=card.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();pressed=card.bounding_box();page.mouse.up()
            check(rect_equal(base,hover) and rect_equal(base,focus) and rect_equal(base,pressed),f'{name}: Herstellerkachel bewegt sich bei Interaktion')
            card.focus();page.keyboard.press('Enter');page.wait_for_url('**/wissensdatenbank/?manufacturer=air-torque')
            check(page.locator('.knowledge-entry:visible').count()==1,f'{name}: Herstelleransicht öffnet nicht')

            # Kurze Favoritenliste innerhalb desselben App-Rahmens.
            seed(page,1)
            frame_before=page.locator('.sk-app-frame').bounding_box();trigger=page.locator('.pct-header-actions>.sk-favorites-trigger');trigger.click();page.wait_for_timeout(60)
            fav=page.evaluate("""()=>{const frame=document.querySelector('.sk-app-frame'),drawer=document.querySelector('#skFavoritesDrawer'),header=frame.querySelector('.sk-global-header'),footer=frame.querySelector('.sk-footer'),list=drawer.querySelector('.sk-favorites-list'),icon=drawer.querySelector('.sk-favorite-icon-host img'),fr=frame.getBoundingClientRect(),dr=drawer.getBoundingClientRect(),hr=header.getBoundingClientRect(),rr=footer.getBoundingClientRect(),s=getComputedStyle(drawer);return{parent:drawer.parentElement===frame,frame:{x:fr.x,y:fr.y,right:fr.right,bottom:fr.bottom},drawer:{x:dr.x,y:dr.y,right:dr.right,bottom:dr.bottom},headerVisible:header.offsetParent!==null,footerVisible:footer.offsetParent!==null,between:dr.top>=hr.bottom-1&&dr.bottom<=rr.top+1,position:s.position,background:s.backgroundColor,border:s.borderTopWidth,shadow:s.boxShadow,rows:drawer.querySelectorAll('.sk-favorite-row').length,shortScroll:list.scrollHeight-list.clientHeight,iconFile:icon?.src.split('?')[0].split('/').pop(),expanded:document.querySelector('.sk-favorites-trigger').getAttribute('aria-expanded'),backdrop:!!document.querySelector('.sk-favorites-backdrop')}}""")
            frame_after=page.locator('.sk-app-frame').bounding_box()
            check(fav['parent'] and fav['between'] and fav['drawer']['x']>=fav['frame']['x']-1 and fav['drawer']['right']<=fav['frame']['right']+1 and fav['drawer']['bottom']<=fav['frame']['bottom']+1,f'{name}: Favoriten verlassen den App-Rahmen {fav}')
            check(rect_equal(frame_before,frame_after) and fav['headerVisible'] and fav['footerVisible'],f'{name}: äußerer App-Rahmen/Header/Footer verändert')
            check(fav['position']=='relative' and fav['background']=='rgba(0, 0, 0, 0)' and fav['border']=='0px' and fav['shadow']=='none' and not fav['backdrop'],f'{name}: konkurrierende Favoriten-Hauptfläche {fav}')
            check(fav['rows']==1 and fav['shortScroll']<=1 and fav['expanded']=='true' and fav['iconFile'].startswith('v2-6-5-3-'),f'{name}: kurze Favoritenliste/Migration fehlerhaft {fav}')
            page.keyboard.press('Escape');check(trigger.get_attribute('aria-expanded')=='false' and trigger.evaluate('n=>document.activeElement===n'),f'{name}: Escape/Fokusrückgabe fehlerhaft')

            # Lange Liste scrollt ausschließlich im inneren Favoritenbereich.
            seed(page,len(ROUTES));trigger=page.locator('.pct-header-actions>.sk-favorites-trigger');frame_before=page.locator('.sk-app-frame').bounding_box();trigger.click();page.wait_for_timeout(60)
            long_state=page.evaluate("""()=>{const frame=document.querySelector('.sk-app-frame'),list=document.querySelector('.sk-favorites-list'),drawer=document.querySelector('#skFavoritesDrawer'),fr=frame.getBoundingClientRect(),lr=list.getBoundingClientRect(),dr=drawer.getBoundingClientRect();list.scrollTop=list.scrollHeight;return{rows:drawer.querySelectorAll('.sk-favorite-row').length,scrollable:list.scrollHeight>list.clientHeight+1,scrollTop:list.scrollTop,listInside:lr.left>=fr.left-1&&lr.right<=fr.right+1&&lr.top>=fr.top-1&&lr.bottom<=fr.bottom+1,drawerInside:dr.left>=fr.left-1&&dr.right<=fr.right+1&&dr.top>=fr.top-1&&dr.bottom<=fr.bottom+1}}""")
            frame_after=page.locator('.sk-app-frame').bounding_box()
            check(long_state['rows']==len(ROUTES) and long_state['scrollable'] and long_state['scrollTop']>0 and long_state['listInside'] and long_state['drawerInside'] and rect_equal(frame_before,frame_after),f'{name}: lange Favoritenliste/Scroll fehlerhaft {long_state}')
            before_count=page.locator('.sk-favorite-row').count();page.locator('.sk-favorite-remove').last.click();after_count=page.locator('.sk-favorite-row').count()
            check(after_count==before_count-1 and page.locator('#skFavoritesDrawer').evaluate('d=>d.contains(document.activeElement)'),f'{name}: Einzellöschen/Fokusführung fehlerhaft')
            page.locator('.sk-favorites-clear').click()
            empty=page.evaluate("""()=>({rows:document.querySelectorAll('.sk-favorite-row').length,empty:!!document.querySelector('.sk-favorites-empty'),disabled:document.querySelector('.sk-favorites-clear').disabled,countHidden:document.querySelector('.sk-favorites-count').hidden})""")
            check(empty=={'rows':0,'empty':True,'disabled':True,'countHidden':True},f'{name}: Alle leeren/leerer Zustand fehlerhaft {empty}')
            check(not errors,f'{name}: JavaScript-Fehler {errors}')
            context.close()

        # Zielöffnung und Persistenz einmal separat mit echtem Reload prüfen.
        context=browser.new_context(viewport={'width':1440,'height':1000})
        page=context.new_page();goto(page,'wissensdatenbank/');seed(page,1)
        page.locator('.pct-header-actions>.sk-favorites-trigger').click();page.locator('.sk-favorite-entry').click();page.wait_for_url('**/analogsignal/')
        check(page.locator('h1').inner_text().strip()=='Analogsignal-Rechner','Favoritenziel wurde nicht geöffnet')
        page.go_back(wait_until='networkidle');page.locator('.pct-header-actions>.sk-favorites-trigger').click()
        check(page.locator('.sk-favorite-row').count()==1,'Gespeicherter Favorit ging nach Navigation/Reload verloren')
        context.close()
    finally:
        browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Designprüfungen')
    for failure in failures:print('-',failure)
    sys.exit(1)
print(f'PASS · {checks} Designprüfungen · 5 Profile · Rastergleichheit · Hoch/Querformat · Rahmen-Favoriten · Kurz/Lang/Leer · Scroll · Fokus · Touch')
