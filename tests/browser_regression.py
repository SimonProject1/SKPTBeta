#!/usr/bin/env python3
"""Playwright-Prüfung: 15 Seiten, 3 Haupt-Viewports, 5 Reorder-Profile, Headeridentität, Touch, 6 Rechner und Offline."""
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
                state=page.evaluate("""()=>{const s=document.querySelector('.sk-app-scroll'),h=document.querySelector('.pct-home-head,.sk-header-inner'),f=document.querySelector('.sk-footer'),frame=document.querySelector('.pct-home-screen,.sk-app-frame'),plate=document.querySelector('.pct-release-module'),version=plate?.querySelector('.sk-release-number'),byline=plate?.querySelector('.sk-release-credit'),skin=plate?.querySelector('.pct-release-module-skin'),controls=[...document.querySelectorAll(document.body.dataset.skPage==='start'?'.pct-home-quick-actions>.pct-control,.pct-home-quick-actions>.pct-home-search-trigger':'.pct-header-actions>.pct-control')],r=n=>n?({top:n.getBoundingClientRect().top,right:n.getBoundingClientRect().right,bottom:n.getBoundingClientRect().bottom,left:n.getBoundingClientRect().left,width:n.getBoundingClientRect().width,height:n.getBoundingClientRect().height}):null,fs=f?getComputedStyle(f):null,ps=plate?getComputedStyle(plate):null,logo=document.querySelector('.pct-home-brand-mark img,.sk-header-logo'),headerGraphics=[...document.querySelectorAll(document.body.dataset.skPage==='start'?'.pct-home-quick-actions img.pct-nav-graphic':'.pct-header-actions img.pct-nav-graphic')];return{doc:document.documentElement.scrollWidth>innerWidth+2,scroll:s?s.scrollWidth>s.clientWidth+2:false,h:r(h),f:r(f),frame:r(frame),footerStyle:fs?{borderTop:fs.borderTopWidth,outline:fs.outlineWidth,shadow:fs.boxShadow}:null,vw:innerWidth,vh:innerHeight,h1:document.querySelectorAll('h1').length,referrer:document.querySelector('meta[name=referrer]')?.content||'',nav:{count:headerGraphics.length,png:headerGraphics.every(i=>i.src.split('?')[0].endsWith('.png')),broken:headerGraphics.some(i=>!i.complete||i.naturalWidth===0),natural:headerGraphics.map(i=>[i.naturalWidth,i.naturalHeight]),files:headerGraphics.map(i=>i.src.split('?')[0].split('/').pop())},alignment:{logo:logo?(logo.getBoundingClientRect().top+logo.getBoundingClientRect().bottom)/2:null,plate:plate?(plate.getBoundingClientRect().top+plate.getBoundingClientRect().bottom)/2:null,controls:controls.map(n=>(n.getBoundingClientRect().top+n.getBoundingClientRect().bottom)/2)},plate:plate?{box:r(plate),version:version?.textContent||'',byline:byline?.textContent||'',border:ps.borderTopWidth,borderLeft:ps.borderLeftWidth,borderRight:ps.borderRightWidth,radius:ps.borderRadius,background:ps.backgroundImage,backgroundColor:ps.backgroundColor,shadow:ps.boxShadow,before:getComputedStyle(plate,'::before').content,after:getComputedStyle(plate,'::after').content,transform:ps.transform,overflowX:plate.scrollWidth-plate.clientWidth,overflowY:plate.scrollHeight-plate.clientHeight,skin:skin?{file:skin.src.split('?')[0].split('/').pop(),natural:[skin.naturalWidth,skin.naturalHeight],broken:!skin.complete||skin.naturalWidth===0}:null}:null,controls:controls.map(n=>{const b=n.getBoundingClientRect(),cs=getComputedStyle(n);return{w:b.width,h:b.height,border:cs.borderTopWidth,radius:cs.borderRadius,background:cs.backgroundColor,backgroundImage:cs.backgroundImage,shadow:cs.boxShadow,transform:cs.transform,touch:cs.touchAction,images:n.querySelectorAll('img.pct-nav-graphic').length}})}}""")
                check(not state['doc'],f'{name} {route or "/"}: horizontaler Dokumentüberlauf')
                check(not state['scroll'],f'{name} {route or "/"}: horizontaler Inhaltsüberlauf')
                check(state['h'] and state['h']['top']>=-1 and state['h']['right']<=state['vw']+1,f'{name} {route or "/"}: Header außerhalb des Viewports')
                check(state['f'] and state['f']['bottom']<=state['vh']+1 and state['f']['left']>=-1,f'{name} {route or "/"}: Footer außerhalb des Viewports')
                check(state['footerStyle'] and state['footerStyle']['borderTop']=='0px' and state['footerStyle']['outline']=='0px' and state['footerStyle']['shadow']=='none',f'{name} {route or "/"}: Footer besitzt Kontur/Schatten')
                check(state['h1']==1,f'{name} {route or "/"}: {state["h1"]} H1 statt genau einer')
                check(state['referrer']=='no-referrer',f'{name} {route or "/"}: Referrer-Schutz fehlt')
                check(state['plate'] and state['plate']['version']=='V2.6.3.7-Beta' and state['plate']['byline']=='Tool by S.K.',f'{name} {route or "/"}: Release-Modul oder Herkunftstext fehlerhaft: {state["plate"]}')
                check(state['plate'] and state['plate']['border']=='0px' and state['plate']['borderLeft']=='0px' and state['plate']['borderRight']=='0px' and state['plate']['radius']=='0px' and state['plate']['transform']=='none' and state['plate']['background']=='none' and state['plate']['backgroundColor']=='rgba(0, 0, 0, 0)' and state['plate']['shadow']=='none' and state['plate']['before']=='none' and state['plate']['after']=='none' and state['plate']['overflowX']<=1 and state['plate']['overflowY']<=1 and state['plate']['skin']=={'file':'release-module-v2-6-3-7.png','natural':[1536,512],'broken':False},f'{name} {route or "/"}: Release-Modul besitzt einen alten Panelrahmen, eine Außenkachel oder eine fehlerhafte PNG-Haut: {state["plate"]}')
                expected_controls=2 if not route else 3
                check(len(state['controls'])==expected_controls and all(c['w']>=44 and c['h']>=44 and c['border']=='0px' and c['radius']=='0px' and c['background']=='rgba(0, 0, 0, 0)' and c['backgroundImage']=='none' and c['shadow']=='none' and c['transform']=='none' and c['touch']=='manipulation' and c['images']==1 for c in state['controls']),f'{name} {route or "/"}: Headerbuttons besitzen noch eine Außenkachel oder fehlerhafte Touchgeometrie: {state["controls"]}')
                centers=[state['alignment']['logo'],state['alignment']['plate'],*state['alignment']['controls']]
                check(all(value is not None for value in centers) and max(centers)-min(centers)<=1,f'{name} {route or "/"}: Headerobjekte liegen nicht auf einer gemeinsamen vertikalen Mittellinie: {state["alignment"]}')
                check(state['nav']['count']==expected_controls and state['nav']['png'] and not state['nav']['broken'] and all(size==[512,512] for size in state['nav']['natural']),f'{name} {route or "/"}: eigenständige Header-PNGs fehlerhaft: {state["nav"]}')
                if route:
                    check(set(state['nav']['files'])=={'v2-6-3-7-nav-favorite.png','v2-6-3-7-nav-back.png','v2-6-3-7-nav-home.png'},f'{name} {route}: Headergrafik-Bestand fehlerhaft: {state["nav"]}')
                    shared_brand=page.evaluate("""()=>{const i=document.querySelector('.sk-header-logo'),w=i?.closest('.sk-logo-version-stack'),s=w?getComputedStyle(w):null,ir=i?.getBoundingClientRect(),wr=w?.getBoundingClientRect();return i?{src:i.src,natural:[i.naturalWidth,i.naturalHeight],broken:!i.complete||i.naturalWidth===0,frame:s?{border:s.borderTopWidth,background:s.backgroundColor,shadow:s.boxShadow,overflow:s.overflow}:null,delta:ir&&wr?[ir.width-wr.width,ir.height-wr.height]:[]}:null}""")
                    check(shared_brand and shared_brand['src'].split('?')[0].endswith('/assets/logo-sk-pct-tools-header.png') and shared_brand['natural']==[512,512] and not shared_brand['broken'],f'{name} {route}: neues Headerlogo fehlt oder ist defekt: {shared_brand}')
                    check(shared_brand and shared_brand['frame']=={'border':'0px','background':'rgba(0, 0, 0, 0)','shadow':'none','overflow':'visible'} and max(abs(x) for x in shared_brand['delta'])<=.25,f'{name} {route}: Headerlogo besitzt noch eine äußere Rahmen-/Logokachel oder füllt den Host nicht: {shared_brand}')
                if route in ('','analogsignal/'):
                    selector='.pct-home-quick-actions>.pct-control,.pct-home-quick-actions>.pct-home-search-trigger' if not route else '.pct-header-actions>.pct-control'
                    controls=page.locator(selector)
                    for index in range(controls.count()):
                        control=controls.nth(index)
                        snap=lambda: control.evaluate("""n=>{const r=n.getBoundingClientRect(),s=getComputedStyle(n);return{x:r.x,y:r.y,w:r.width,h:r.height,transform:s.transform,translate:s.translate}}""")
                        base=snap();control.hover();hover=snap();control.focus();focus=snap()
                        box=control.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();pressed=snap();page.mouse.move(0,0);page.mouse.up()
                        control.evaluate("n=>n.classList.add('active')");active=snap();control.evaluate("n=>n.classList.remove('active')")
                        check(all(all(abs(state2[k]-base[k])<=.25 for k in ('x','y','w','h')) and state2['transform']=='none' and state2['translate']=='none' for state2 in (hover,focus,pressed,active)),f'{name} {route or "/"} Headerbutton {index+1}: Position ändert sich im Interaktionszustand: {base} / {hover} / {focus} / {pressed} / {active}')
                    if not route:
                        brand_link=page.locator('.pct-home-brand');release_module=page.locator('.pct-release-module')
                        release_snap=lambda: release_module.evaluate("n=>{const r=n.getBoundingClientRect(),s=getComputedStyle(n);return{x:r.x,y:r.y,w:r.width,h:r.height,transform:s.transform,translate:s.translate,filter:s.filter}}")
                        release_base=release_snap();brand_link.hover();release_hover=release_snap();brand_link.focus();release_focus=release_snap()
                        box=brand_link.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();release_pressed=release_snap();page.mouse.move(0,0);page.mouse.up()
                        check(all(all(abs(candidate[k]-release_base[k])<=.25 for k in ('x','y','w','h')) and candidate['transform']=='none' and candidate['translate']=='none' and candidate['filter']=='none' for candidate in (release_hover,release_focus,release_pressed)),f'{name} Startseite: Release-Modul verschiebt oder skaliert sich bei Hover/Fokus/Drücken: {release_base} / {release_hover} / {release_focus} / {release_pressed}')
                if not route:
                    app_icons=page.evaluate("""()=>[...document.querySelectorAll('#pctHomeGrid .sk-home-app')].map(app=>{const frame=app.querySelector('.sk-home-icon'),image=app.querySelector('img.sk-nav-graphic'),star=app.querySelector('.sk-favorite-button'),fr=frame.getBoundingClientRect(),ir=image.getBoundingClientRect(),sr=star.getBoundingClientRect(),fs=getComputedStyle(frame),ring=getComputedStyle(star,'::after'),inset=parseFloat(ring.inset)||0,visible={left:sr.left+inset,top:sr.top+inset,right:sr.right-inset,bottom:sr.bottom-inset},diameter=sr.width-2*inset,alpha={left:ir.left+ir.width*13/512,top:ir.top+ir.height*9/512,right:ir.left+ir.width*489/512,bottom:ir.top+ir.height*491/512};return{fw:fr.width,fh:fr.height,iw:ir.width,ih:ir.height,border:fs.borderTopWidth,shadow:fs.boxShadow,transform:fs.transform,imageTransform:getComputedStyle(image).transform,cardTransform:getComputedStyle(app).transform,arc:getComputedStyle(frame,'::before').backgroundImage,starX:sr.left-fr.right,starY:sr.top-fr.top,touch:Math.min(sr.width,sr.height),visible:diameter,intrusionX:fr.right-visible.left,intrusionY:visible.bottom-fr.top,outsideX:visible.right-fr.right,outsideY:fr.top-visible.top,centerOutX:(visible.left+visible.right)/2-fr.right,centerOutY:fr.top-(visible.top+visible.bottom)/2,alphaDelta:[alpha.left-fr.left,alpha.top-fr.top,alpha.right-fr.right,alpha.bottom-fr.bottom],structural:frame.classList.contains('sk-app-icon-wrapper')&&star.parentElement===frame,straddles:visible.left<fr.right&&visible.right>fr.right&&visible.top<fr.top&&visible.bottom>fr.top,natural:[image.naturalWidth,image.naturalHeight],broken:!image.complete||image.naturalWidth===0}})""")
                    check(len(app_icons)==10,f'{name} Startseite: {len(app_icons)} statt 10 Icon-Rahmen')
                    if app_icons:
                        first=app_icons[0]
                        check(all(abs(x['fw']-first['fw'])<=1 and abs(x['fh']-first['fh'])<=1 and x['border']==first['border'] and x['shadow']==first['shadow'] and x['transform']==first['transform'] for x in app_icons),f'{name} Startseite: Außenmaß, Rahmen, Perspektive oder Schatten der Icons uneinheitlich')
                        check(all(abs(x['iw']-first['iw'])<=1 and abs(x['ih']-first['ih'])<=1 and x['natural']==[512,512] and not x['broken'] for x in app_icons),f'{name} Startseite: PNG-Innenmaß oder natürliche Größe uneinheitlich')
                        check(all(abs(x['starX']-first['starX'])<=1 and abs(x['starY']-first['starY'])<=1 for x in app_icons),f'{name} Startseite: Favoritensternposition uneinheitlich')
                        check(all(x['structural'] for x in app_icons),f'{name} Startseite: Favoritenbutton ist nicht direkter Bestandteil des festen Icon-Wrappers: {app_icons}')
                        check(all(max(abs(delta) for delta in x['alphaDelta'])<=.25 for x in app_icons),f'{name} Startseite: Wrapper stimmt nicht mit den tatsächlichen sichtbaren PNG-Grenzen überein: {app_icons}')
                        check(all(x['touch']>=44 and 21<=x['visible']<=23 and x['straddles'] and .48<=x['intrusionX']/x['visible']<=.52 and .48<=x['intrusionY']/x['visible']<=.52 and .48<=x['outsideX']/x['visible']<=.52 and .48<=x['outsideY']/x['visible']<=.52 and abs(x['centerOutX'])<=.25 and abs(x['centerOutY'])<=.25 for x in app_icons),f'{name} Startseite: Mittelpunkt des sichtbaren Favoritenkreises liegt nicht exakt auf der oberen rechten Icon-Wrapperkante: {app_icons}')
                        check(all(x['transform']=='none' and x['imageTransform']=='none' and x['cardTransform']=='none' for x in app_icons),f'{name} Startseite: App-Icon besitzt im Ruhezustand eine Transformation')
                        check(all(x['arc']=='none' for x in app_icons),f'{name} Startseite: alte innere CSS-Rahmenlinie ist noch aktiv')
                    # Aktiver und inaktiver Favorit müssen dieselbe sichtbare Kreisgeometrie behalten.
                    for index in range(10):
                        favorite=page.locator('#pctHomeGrid .sk-favorite-button').nth(index)
                        geometry=lambda: favorite.evaluate("""b=>{const r=b.getBoundingClientRect(),s=getComputedStyle(b,'::after'),i=parseFloat(s.inset)||0;return{x:r.left+i,y:r.top+i,w:r.width-2*i,h:r.height-2*i,active:b.dataset.active}}""")
                        inactive=geometry();favorite.click();active_favorite=geometry();favorite.click();restored=geometry()
                        check(active_favorite['active']=='true' and restored['active']=='false',f'{name} Startseite App {index+1}: Favoritenstatus schaltet nicht korrekt')
                        check(all(abs(active_favorite[k]-inactive[k])<=.25 and abs(restored[k]-inactive[k])<=.25 for k in ('x','y','w','h')),f'{name} Startseite App {index+1}: sichtbarer Favoritenkreis verschiebt sich zwischen inaktiv/aktiv: {inactive} -> {active_favorite} -> {restored}')
                    # Jedes App-Icon muss bei Hover, Fokus, Drücken und aktivem Zustand pixelstabil bleiben.
                    for index in range(10):
                        card=page.locator('#pctHomeGrid .sk-home-app').nth(index)
                        snapshot=lambda: card.locator('.sk-home-icon').evaluate("n=>{const r=n.getBoundingClientRect(),i=n.querySelector('img').getBoundingClientRect();return{x:r.x,y:r.y,right:r.right,top:r.top,ix:i.x,iy:i.y,iright:i.right,itop:i.top,transform:getComputedStyle(n).transform,imageTransform:getComputedStyle(n.querySelector('img')).transform}}")
                        base=snapshot();card.hover();hover=snapshot()
                        check(all(abs(hover[k]-base[k])<=.25 for k in ('x','y','right','top','ix','iy','iright','itop')) and hover['transform']=='none' and hover['imageTransform']=='none',f'{name} Startseite App {index+1}: Hover verschiebt das Icon: {base} -> {hover}')
                        card.focus();focus=snapshot()
                        check(all(abs(focus[k]-base[k])<=.25 for k in ('x','y','right','top','ix','iy','iright','itop')) and focus['transform']=='none' and focus['imageTransform']=='none',f'{name} Startseite App {index+1}: Fokus verschiebt das Icon: {base} -> {focus}')
                        card.hover();box=card.bounding_box();page.mouse.down();pressed=snapshot();page.mouse.move(1,1);page.mouse.up()
                        check(all(abs(pressed[k]-base[k])<=.25 for k in ('x','y','right','top','ix','iy','iright','itop')) and pressed['transform']=='none' and pressed['imageTransform']=='none',f'{name} Startseite App {index+1}: Drücken verschiebt das Icon: {base} -> {pressed}')
                        card.evaluate("n=>{n.classList.add('active');n.dataset.active='true'}");active=snapshot();card.evaluate("n=>{n.classList.remove('active');delete n.dataset.active}")
                        check(all(abs(active[k]-base[k])<=.25 for k in ('x','y','right','top','ix','iy','iright','itop')) and active['transform']=='none' and active['imageTransform']=='none',f'{name} Startseite App {index+1}: Aktivzustand verschiebt das Icon: {base} -> {active}')
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
            knowledge_favorites=0
            for manufacturer in ('air-torque','endress-hauser','siemens','vacon'):
                goto(page,f'wissensdatenbank/?manufacturer={manufacturer}')
                cards=page.locator('.knowledge-entry:visible');knowledge_favorites+=cards.count()
                for index in range(cards.count()):
                    card=cards.nth(index)
                    geometry=lambda: card.evaluate("""card=>{const icon=card.querySelector('.knowledge-home-icon'),image=icon.querySelector('img'),button=card.querySelector('.sk-favorite-button'),ir=icon.getBoundingClientRect(),pr=image.getBoundingClientRect(),br=button.getBoundingClientRect(),style=getComputedStyle(button,'::after'),inset=parseFloat(style.inset)||0,visible={left:br.left+inset,top:br.top+inset,right:br.right-inset,bottom:br.bottom-inset},alpha={left:pr.left+pr.width*13/512,top:pr.top+pr.height*9/512,right:pr.left+pr.width*489/512,bottom:pr.top+pr.height*491/512};return{touch:Math.min(br.width,br.height),visible:br.width-2*inset,centerX:(visible.left+visible.right)/2-ir.right,centerY:(visible.top+visible.bottom)/2-ir.top,alphaDelta:[alpha.left-ir.left,alpha.top-ir.top,alpha.right-ir.right,alpha.bottom-ir.bottom],structural:icon.classList.contains('sk-app-icon-wrapper')&&button.parentElement===icon,x:visible.left,y:visible.top,w:visible.right-visible.left,h:visible.bottom-visible.top,active:button.dataset.active}}""")
                    inactive=geometry();favorite=card.locator('.sk-favorite-button');favorite.click();active_favorite=geometry();favorite.click();restored=geometry()
                    check(inactive['structural'] and max(abs(delta) for delta in inactive['alphaDelta'])<=.25 and inactive['touch']>=43.99 and 21<=inactive['visible']<=23 and abs(inactive['centerX'])<=.25 and abs(inactive['centerY'])<=.25,f'{name} Wissens-App {manufacturer}/{index+1}: Wrapper, sichtbare PNG-Grenze oder Favoritenkreis weicht von der oberen rechten Iconecke ab: {inactive}')
                    check(active_favorite['active']=='true' and restored['active']=='false' and all(abs(active_favorite[k]-inactive[k])<=.25 and abs(restored[k]-inactive[k])<=.25 for k in ('centerX','centerY','w','h')),f'{name} Wissens-App {manufacturer}/{index+1}: Favoritenkreis verschiebt sich relativ zur Iconecke zwischen inaktiv/aktiv: {inactive} -> {active_favorite} -> {restored}')
            check(knowledge_favorites==5,f'{name} Wissensdatenbank: {knowledge_favorites} statt 5 Favoritenfelder vermessen')
            context.close()

        # WCAG-Reflow-Sanity: 320 CSS px entspricht der üblichen 400-%-Reflow-Prüfbreite.
        context=browser.new_context(viewport={'width':320,'height':900},device_scale_factor=1); page=context.new_page()
        for route in REFLOW_ROUTES:
            goto(page,route)
            state=page.evaluate("""()=>{const plate=document.querySelector('.pct-release-module'),buttons=[...document.querySelectorAll('.pct-home-quick-actions>.pct-control,.pct-home-quick-actions>.pct-home-search-trigger,.pct-header-actions>.pct-control')];return{doc:document.documentElement.scrollWidth,body:document.body.scrollWidth,vw:innerWidth,controls:[...document.querySelectorAll('button,a,input,select')].filter(x=>x.offsetParent!==null&&!x.closest('.sk-favorites-drawer:not(.open)')).some(x=>x.getBoundingClientRect().right>innerWidth+2||x.getBoundingClientRect().left<-2),plate:plate?{scrollX:plate.scrollWidth-plate.clientWidth,scrollY:plate.scrollHeight-plate.clientHeight,right:plate.getBoundingClientRect().right}:null,touch:buttons.map(b=>Math.min(b.getBoundingClientRect().width,b.getBoundingClientRect().height))}}""")
            check(state['doc']<=state['vw']+2 and state['body']<=state['vw']+2,f'Reflow 320 px {route or "/"}: horizontaler Überlauf {state}')
            check(not state['controls'],f'Reflow 320 px {route or "/"}: Bedienelement außerhalb des Viewports')
            check(state['plate'] and state['plate']['scrollX']<=1 and state['plate']['scrollY']<=1 and state['plate']['right']<=state['vw']+1,f'Reflow 320 px {route or "/"}: Release-Modul läuft über oder wird abgeschnitten: {state["plate"]}')
            check(state['touch'] and all(size>=44 for size in state['touch']),f'Reflow 320 px {route or "/"}: Header-Touchfläche unter 44 px: {state["touch"]}')
            long_release=page.evaluate("""async()=>{const module=document.querySelector('.pct-release-module'),number=module?.querySelector('.sk-release-number');if(!module||!number)return null;number.textContent='V2.6.3.7-RC.12-Beta';window.dispatchEvent(new Event('resize'));await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));const mr=module.getBoundingClientRect(),nr=number.getBoundingClientRect();return{moduleScrollX:module.scrollWidth-module.clientWidth,moduleScrollY:module.scrollHeight-module.clientHeight,numberScrollX:number.scrollWidth-number.clientWidth,font:parseFloat(getComputedStyle(number).fontSize),inside:nr.left>=mr.left-1&&nr.right<=mr.right+1&&nr.top>=mr.top-1&&nr.bottom<=mr.bottom+1}}""")
            check(long_release and long_release['moduleScrollX']<=1 and long_release['moduleScrollY']<=1 and long_release['numberScrollX']<=1 and long_release['font']>=6 and long_release['inside'],f'Reflow 320 px {route or "/"}: längerer Versionsstand wird im Release-Modul abgeschnitten: {long_release}')
        context.close()

        context=browser.new_context(viewport={'width':390,'height':844}); page=context.new_page();goto(page,'')
        brand=page.evaluate("""()=>{const i=document.querySelector('.pct-home-brand img'),w=i?.closest('.pct-home-brand-mark'),s=w?getComputedStyle(w):null,ir=i?.getBoundingClientRect(),wr=w?.getBoundingClientRect(),favicon=document.querySelector('link[rel="icon"]'),apple=document.querySelector('link[rel="apple-touch-icon"]'),manifest=document.querySelector('link[rel="manifest"]');return{src:i?.src||'',natural:i?[i.naturalWidth,i.naturalHeight]:[],broken:i?!i.complete||i.naturalWidth===0:true,alt:i?.alt||'',frame:s?{border:s.borderTopWidth,background:s.backgroundColor,shadow:s.boxShadow,overflow:s.overflow}:null,delta:ir&&wr?[ir.width-wr.width,ir.height-wr.height]:[],favicon:favicon?.href||'',apple:apple?.href||'',manifest:manifest?.href||''}}""")
        check(brand['src'].split('?')[0].endswith('/assets/logo-sk-pct-tools-header.png') and brand['natural']==[512,512] and not brand['broken'],f'Startseite: neues Markenlogo fehlt oder ist defekt: {brand}')
        check(brand['frame']=={'border':'0px','background':'rgba(0, 0, 0, 0)','shadow':'none','overflow':'visible'} and max(abs(x) for x in brand['delta'])<=.25,f'Startseite: Logo besitzt noch eine äußere Rahmen-/Logokachel oder füllt den Host nicht: {brand}')
        check(brand['alt']=='SK PCT Tools' and brand['favicon'].split('?')[0].endswith('/assets/favicon.png') and brand['apple'].split('?')[0].endswith('/assets/apple-touch-icon.png') and brand['manifest'].endswith('/manifest-v2-6-3-7.webmanifest'),f'Startseite: Markenmetadaten unvollständig: {brand}')
        header_assets=page.evaluate("""()=>[...document.querySelectorAll('.pct-home-quick-actions img.pct-nav-graphic')].map(i=>({file:i.src.split('?')[0].split('/').pop(),natural:[i.naturalWidth,i.naturalHeight],broken:!i.complete||i.naturalWidth===0}))""")
        check({item['file'] for item in header_assets}=={'v2-6-3-7-nav-search.png','v2-6-3-7-nav-favorite.png'} and all(item['natural']==[512,512] and not item['broken'] for item in header_assets),f'Startseite: Suche-/Favoriten-Grafiken fehlerhaft: {header_assets}')
        manifest_data=page.evaluate("""async()=>{const r=await fetch(document.querySelector('link[rel="manifest"]').href,{cache:'no-store'});return await r.json()}""")
        check(manifest_data.get('version')=='2.6.3.7-Beta' and {(i.get('src'),i.get('purpose')) for i in manifest_data.get('icons',[])}=={('assets/icon-192.png','any'),('assets/icon-512.png','any'),('assets/icon-maskable-192.png','maskable'),('assets/icon-maskable-512.png','maskable')},f'PWA-Manifest oder Icon-Purpose fehlerhaft: {manifest_data}')
        home=page.evaluate("""()=>{const g=document.querySelector('#pctHomeGrid'),b=document.querySelector('#pctHomeGrid .sk-favorite-button'),t=[...document.querySelectorAll('.sk-home-app-title')],icons=[...document.querySelectorAll('#pctHomeGrid img.sk-nav-graphic')],boxes=[...document.querySelectorAll('#pctHomeGrid .sk-home-icon')],forbidden=/RECHNER|WISSEN|EXTERN|MATERIAL|PCT|PIPING/i,ring=b?getComputedStyle(b,'::after'):null;return{apps:document.querySelectorAll('#pctHomeGrid .sk-home-app').length,favorites:document.querySelectorAll('#pctHomeGrid .sk-favorite-button').length,columns:getComputedStyle(g).gridTemplateColumns.split(' ').filter(Boolean).length,touch:b?Math.min(b.getBoundingClientRect().width,b.getBoundingClientRect().height):0,visible:b?b.getBoundingClientRect().width-2*(parseFloat(ring.inset)||0):0,inactiveGlow:ring?.boxShadow||'',titles:t.map(x=>x.textContent.trim()),titleOverflow:t.some(x=>x.scrollWidth>x.clientWidth+2),external:document.querySelector('[data-app-id="eh-device-viewer"]')?.href,mess:!!document.querySelector('[data-app-id="messstellen-doku"]'),icons:icons.length,iconFiles:new Set(icons.map(i=>i.src.split('?')[0])).size,iconBroken:icons.some(i=>!i.complete||i.naturalWidth===0),png:icons.every(i=>i.src.split('?')[0].endsWith('.png')),versioned:icons.every(i=>i.src.includes('/v2-6-3-7-')),overlayNodes:document.querySelectorAll('.knowledge-icon-badge,[data-icon-area],[data-discipline-overlay]').length,pseudoOverlay:boxes.some(x=>forbidden.test(getComputedStyle(x,'::after').content||''))}}""")
        check(home['apps']==10,f'Startseite: {home["apps"]} statt 10 Apps');check(home['favorites']==10,f'Startseite: {home["favorites"]} statt 10 Favoritensterne');check(home['columns']==3,f'Smartphone-Startseite: {home["columns"]} statt 3 Spalten');check(home['touch']>=44,f'Favoriten-Touchziel nur {home["touch"]} px');check(21<=home['visible']<=23,f'Sichtbarer Favoritenkreis ist {home["visible"]} statt rund 22 px');check('120, 255, 50' not in home['inactiveGlow'],f'Inaktiver Favorit leuchtet grün: {home["inactiveGlow"]}');check(all(title in home['titles'] for title in ('Umrechnen','Siemens RAW','Werkstoffe','Wissen')),f'Verkürzte Titel fehlen: {home["titles"]}');check(not home['titleOverflow'],'App-Titel läuft horizontal über');check(not home['mess'],'Messstellen-Doku noch vorhanden');check(home['external']=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H-Ziel falsch');check(home['icons']==10 and home['iconFiles']==10 and home['png'] and home['versioned'] and not home['iconBroken'],f'Startseiten-PNGs fehlerhaft: {home}');check(home['overlayNodes']==0 and not home['pseudoOverlay'],f'Startseite besitzt noch ein zusätzliches Fachbereichs-Overlay: {home}')
        first_favorite=page.locator('#pctHomeGrid .sk-favorite-button').first;first_favorite.click();active=page.evaluate("""()=>{const b=document.querySelector('#pctHomeGrid .sk-favorite-button'),ring=getComputedStyle(b,'::after');return{active:b.dataset.active,shadow:ring.boxShadow,color:getComputedStyle(b).color}}""");check(active['active']=='true' and ('120, 255, 50' in active['shadow'] or '120, 255, 50' in active['color']),f'Aktiver Favorit leuchtet nicht grün: {active}')
        search_trigger=page.locator('#skFilterToggle');search_before=search_trigger.bounding_box();search_trigger.click();page.wait_for_timeout(80)
        search_state=page.evaluate("""()=>({expanded:document.querySelector('#skFilterToggle')?.getAttribute('aria-expanded'),hidden:document.querySelector('#skFilterContent')?.hidden,open:document.body.classList.contains('pct-home-search-open')})""")
        search_after=search_trigger.bounding_box();check(search_state=={'expanded':'true','hidden':False,'open':True},f'Startseitensuche öffnet nicht korrekt: {search_state}');check(all(abs(search_after[k]-search_before[k])<=.25 for k in ('x','y','width','height')),f'Suchbutton verschiebt sich beim Öffnen: {search_before} -> {search_after}')
        search_trigger.click();page.wait_for_timeout(80);check(page.get_attribute('#skFilterToggle','aria-expanded')=='false','Startseitensuche schließt nicht korrekt')
        favorites_trigger=page.locator('.pct-home-quick-actions>.sk-favorites-trigger');favorites_trigger.click();page.wait_for_timeout(320)
        drawer=page.evaluate("""()=>{const d=document.querySelector('.sk-favorites-drawer'),r=d.getBoundingClientRect();return{open:d.classList.contains('open'),aria:d.getAttribute('aria-hidden'),left:r.left,right:r.right,width:r.width,close:!!d.querySelector('.sk-favorites-close'),rows:d.querySelectorAll('.sk-favorite-row').length}}""")
        check(drawer['open'] and drawer['aria']=='false' and drawer['left']>=-1 and drawer['right']<=390+1 and drawer['width']>=300 and drawer['close'] and drawer['rows']==1,f'Favoritenübersicht fehlerhaft: {drawer}')
        page.click('.sk-favorites-close');page.wait_for_timeout(320);check(page.get_attribute('.sk-favorites-drawer','aria-hidden')=='true','Favoritenübersicht schließt nicht korrekt')

        goto(page,'einheitendatenbank/');page.wait_for_selector('.unit-category-card')
        unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open).length,favorites:!!document.querySelector('#unitFavoritesPanel')})""")
        check(unit['open']==0,f'Einheitendatenbank: {unit["open"]} Kategorien initial geöffnet');check(unit['favorites'],'Einheiten-Favoritenbereich fehlt')
        page.fill('#unitSearch','Fahrenheit');page.wait_for_timeout(100);unit=page.evaluate("""()=>({open:[...document.querySelectorAll('.unit-category-card')].filter(x=>x.open&&!x.hidden).length,rows:[...document.querySelectorAll('#unitCategoryList .unit-row')].filter(x=>!x.hidden).length})""")
        check(unit['open']>=1 and unit['rows']>=1,'Einheitensuche öffnet Treffer nicht automatisch')

        goto(page,'werkstoffdatenbank/');page.wait_for_selector('.material-compare-table td');material=page.evaluate("""()=>({row:getComputedStyle(document.querySelector('.material-compare-table tbody tr')).display,label:document.querySelector('.material-compare-table td')?.dataset.label||''})""")
        check(material['row']=='block','Werkstoffvergleich mobil nicht gestapelt');check(bool(material['label']),'Mobile Werkstoff-Schlüssel fehlen')

        goto(page,'wissensdatenbank/');page.wait_for_selector('.knowledge-brand-logo');knowledge_icons=page.evaluate("""()=>{const icons=[...document.querySelectorAll('img.knowledge-brand-logo')],hub=[...document.querySelectorAll('.knowledge-hub img.knowledge-brand-logo')],entries=[...document.querySelectorAll('.knowledge-entry img.knowledge-brand-logo')],boxes=[...document.querySelectorAll('.knowledge-home-icon')],forbidden=/RECHNER|WISSEN|EXTERN|MATERIAL|PCT|PIPING/i;return{count:icons.length,files:new Set(icons.map(i=>i.src.split('?')[0])).size,broken:icons.some(i=>!i.complete||i.naturalWidth===0),png:icons.every(i=>i.src.split('?')[0].endsWith('.png')),hubManufacturers:hub.every(i=>i.src.includes('manufacturer-')),entryKnowledge:entries.length===5&&entries.every(i=>i.src.includes('knowledge-')),entryFavorites:document.querySelectorAll('.knowledge-entry .sk-favorite-button').length,versioned:icons.every(i=>i.src.includes('/v2-6-3-7-')),legacyBadges:document.querySelectorAll('.knowledge-icon-badge,[data-icon-area],[data-discipline-overlay]').length,pseudoOverlay:boxes.some(x=>forbidden.test(getComputedStyle(x,'::after').content||''))}}""")
        check(knowledge_icons['count']==10 and knowledge_icons['files']==10 and knowledge_icons['png'] and knowledge_icons['hubManufacturers'] and knowledge_icons['entryKnowledge'] and knowledge_icons['entryFavorites']==5 and knowledge_icons['versioned'] and knowledge_icons['legacyBadges']==0 and not knowledge_icons['pseudoOverlay'] and not knowledge_icons['broken'],f'Wissens-/Hersteller-PNGs fehlerhaft: {knowledge_icons}')
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

        # Neue Reorder-Zustandsmaschine: klare Trennung zwischen Navigation und Sortierung.
        # Geprüft werden iPhone-/iOS-PWA-nahe Pointerfolgen, Tablet-Touch und Desktop.
        for device,width,height,has_touch,is_mobile in (
            ('Kleines-Smartphone-Reorder',320,700,True,True),
            ('iPhone-PWA-Emulation',390,844,True,True),
            ('iPhone-Landscape-Reorder',844,390,True,True),
            ('Tablet-Touch-Reorder',820,1180,True,True),
            ('Desktop-Pointer-Reorder',1440,1000,False,False),
        ):
            reorder_context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=has_touch,is_mobile=is_mobile)
            reorder_page=reorder_context.new_page();goto(reorder_page,'')
            def install_tap_probes():
                reorder_page.evaluate("""()=>{window.__tapCounts={};window.__tapHandlers=[];document.querySelectorAll('#pctHomeGrid .sk-home-app').forEach(card=>{const handler=event=>{event.preventDefault();window.__tapCounts[card.dataset.appId]=(window.__tapCounts[card.dataset.appId]||0)+1};card.addEventListener('click',handler);window.__tapHandlers.push([card,handler])})}""")
            install_tap_probes()
            pointer_type='touch' if has_touch else 'mouse'
            def dispatch(selector,event_type,pointer_id,x,y,buttons):
                reorder_page.locator(selector).dispatch_event(event_type,{'pointerId':pointer_id,'pointerType':pointer_type,'isPrimary':True,'button':0,'buttons':buttons,'clientX':x,'clientY':y,'bubbles':True,'cancelable':True})
            def dispatch_body(event_type,pointer_id,x,y,buttons):
                reorder_page.locator('body').dispatch_event(event_type,{'pointerId':pointer_id,'pointerType':pointer_type,'isPrimary':True,'button':0,'buttons':buttons,'clientX':x,'clientY':y,'bubbles':True,'cancelable':True})
            def card_box(app_id): return reorder_page.locator(f'#pctHomeGrid [data-app-id="{app_id}"]').bounding_box()
            def tap_probe(app_id,pointer_id):
                box=card_box(app_id);x=box['x']+box['width']/2;y=box['y']+box['height']/2;selector=f'#pctHomeGrid [data-app-id="{app_id}"]'
                dispatch(selector,'pointerdown',pointer_id,x,y,1);dispatch(selector,'pointerup',pointer_id,x,y,0);reorder_page.locator(selector).dispatch_event('click')
            def long_press(app_id,pointer_id,wait=500):
                box=card_box(app_id);x=box['x']+box['width']/2;y=box['y']+box['height']/2;selector=f'#pctHomeGrid [data-app-id="{app_id}"]'
                dispatch(selector,'pointerdown',pointer_id,x,y,1);reorder_page.wait_for_timeout(wait);return x,y
            def mode_state():
                return reorder_page.evaluate("""()=>({mode:document.querySelector('#pctHomeGrid').dataset.mode,engine:document.querySelector('#pctHomeGrid').dataset.reorderEngine,editing:document.body.classList.contains('pct-home-editing'),overlays:document.querySelectorAll('.pct-home-drag-overlay').length,layers:document.querySelectorAll('body>.pct-home-drag-layer').length,placeholders:document.querySelectorAll('#pctHomeGrid>.pct-home-drop-placeholder').length,gridApps:document.querySelectorAll('#pctHomeGrid>.sk-home-app').length})""")
            def header_state():
                return reorder_page.evaluate("""()=>{const head=document.querySelector('.pct-home-head'),selectors={head:'.pct-home-head',brand:'.pct-home-brand',mark:'.pct-home-brand-mark',logo:'.pct-home-brand-mark img',plate:'.pct-home-release-module',version:'.sk-release-number',byline:'.sk-release-credit',utility:'.pct-home-utility',quick:'.pct-home-quick-actions',search:'#skFilterToggle',favorite:'.pct-home-quick-actions>.sk-favorites-trigger',count:'.pct-home-quick-actions .sk-favorites-count'},props=['display','position','inset','top','right','bottom','left','width','height','minWidth','maxWidth','margin','padding','gap','alignItems','justifyContent','background','backgroundImage','border','borderRadius','boxShadow','overflow','transform','translate','opacity','visibility','zIndex'];const snap={};for(const [key,selector] of Object.entries(selectors)){const n=document.querySelector(selector),r=n.getBoundingClientRect(),s=getComputedStyle(n);snap[key]={html:n.outerHTML,rect:[r.x,r.y,r.width,r.height,r.right,r.bottom],style:Object.fromEntries(props.map(prop=>[prop,s[prop]]))}}return{html:head.innerHTML,snap}}""")

            # Normalmodus: kurzer Tap öffnet; eine Scrollbewegung vor Ablauf des Long-Press
            # bleibt Scrollgeste und darf den Sortiermodus nicht starten.
            initial=mode_state();check(initial['mode']=='navigate' and initial['engine']=='pointer-overlay-v3' and not initial['editing'] and initial['overlays']==0 and initial['placeholders']==0 and initial['gridApps']==10,f'{device}: falscher Ausgangsmodus: {initial}')
            tap_probe('analogsignal',301)
            check(reorder_page.evaluate("()=>window.__tapCounts.analogsignal||0")==1,f'{device}: kurzer Ausgangs-Tap wird unterdrückt')
            scroll_id=302;box=card_box('pf-rechner');sx=box['x']+box['width']/2;sy=box['y']+box['height']/2
            dispatch('#pctHomeGrid [data-app-id="pf-rechner"]','pointerdown',scroll_id,sx,sy,1);dispatch_body('pointermove',scroll_id,sx,sy+34,1);reorder_page.wait_for_timeout(470);dispatch_body('pointerup',scroll_id,sx,sy+34,0)
            scrolled=mode_state();check(scrolled['mode']=='navigate' and scrolled['overlays']==0 and scrolled['placeholders']==0 and scrolled['gridApps']==10,f'{device}: Scrollgeste startet Sortierung oder hinterlässt Zustand: {scrolled}')

            # Long-Press startet sichtbar den Sortiermodus samt Wackeln. Der normale
            # Header muss dabei strukturell, geometrisch, stilistisch und pixelgenau
            # identisch bleiben; das getrennte Dock darf weder Header noch Apps treffen.
            stable_before=reorder_page.locator('#pctHomeGrid [data-app-id="pf-rechner"]').evaluate("""n=>{const w=n.querySelector('.sk-app-icon-wrapper'),t=n.querySelector('.sk-home-app-title'),f=n.querySelector('.sk-favorite-button'),r=e=>{const b=e.getBoundingClientRect();return[b.x,b.y,b.width,b.height]};return{card:r(n),wrapper:r(w),title:r(t),favorite:r(f)}}""")
            header_before=header_state();header_png_before=reorder_page.locator('.pct-home-head').screenshot()
            first='analogsignal';target='eh-device-viewer';ax,ay=long_press(first,303);b=card_box(target);bx=b['x']+b['width']*.8;by=b['y']+b['height']*.8
            active=mode_state();header_during=header_state();header_png_during=reorder_page.locator('.pct-home-head').screenshot()
            active_visual=reorder_page.evaluate("""()=>{const head=document.querySelector('.pct-home-head'),bar=document.querySelector('.pct-home-edit-actions'),grid=document.querySelector('#pctHomeGrid'),card=grid.querySelector('[data-app-id="pf-rechner"]'),w=card.querySelector('.sk-app-icon-wrapper'),img=w.querySelector('.sk-nav-graphic'),t=card.querySelector('.sk-home-app-title'),f=card.querySelector('.sk-favorite-button'),overlay=document.querySelector('.pct-home-drag-overlay'),r=e=>{const b=e.getBoundingClientRect();return{x:b.x,y:b.y,right:b.right,bottom:b.bottom,width:b.width,height:b.height}},hit=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top,br=bar.getBoundingClientRect(),hr=head.getBoundingClientRect(),nodes=[...grid.querySelectorAll(':scope>.sk-home-app,:scope>.pct-home-drop-placeholder')],firstTop=Math.min(...nodes.map(n=>n.getBoundingClientRect().top)),firstRow=nodes.filter(n=>Math.abs(n.getBoundingClientRect().top-firstTop)<1),titles=[...grid.querySelectorAll(':scope>.sk-home-app .sk-home-app-title')];return{head:r(head),bar:r(bar),grid:r(grid),firstTop,brand:getComputedStyle(document.querySelector('.pct-home-brand')).display,quick:getComputedStyle(document.querySelector('.pct-home-quick-actions')).display,search:getComputedStyle(document.querySelector('#skFilterToggle')).display,headerFavorite:getComputedStyle(document.querySelector('.pct-home-quick-actions>.sk-favorites-trigger')).display,barPosition:getComputedStyle(bar).position,barOutsideHeader:!head.contains(bar),barHidden:bar.hidden,barAria:bar.getAttribute('aria-hidden'),barHeaderOverlap:hit(br,hr),barFirstRowOverlap:firstRow.some(n=>hit(br,n.getBoundingClientRect())),barTitleOverlap:titles.some(n=>hit(br,n.getBoundingClientRect())),card:r(card),wrapper:r(w),title:r(t),favorite:r(f),cardAnimation:getComputedStyle(card).animationName,wrapperAnimation:getComputedStyle(w).animationName,titleAnimation:getComputedStyle(t).animationName,imageAnimation:getComputedStyle(img).animationName,favoriteAnimation:getComputedStyle(f).animationName,favoriteOpacity:getComputedStyle(f).opacity,touch:getComputedStyle(card).touchAction,cardTransform:getComputedStyle(card).transform,wrapperTransform:getComputedStyle(w).transform,overlay:r(overlay),overlayParent:overlay?.parentElement?.parentElement===document.body,overlayDockOverlap:hit(overlay.getBoundingClientRect(),br),undo:!!document.querySelector('#pctHomeUndo'),redo:!!document.querySelector('#pctHomeRedo')}}""")
            check(active['mode']=='sort' and active['editing'] and active['overlays']==1 and active['layers']==1 and active['placeholders']==1 and active['gridApps']==9,f'{device}: Long-Press startet keinen eindeutigen Overlay-/Platzhaltermodus: {active}')
            check(header_during==header_before and header_png_during==header_png_before,f'{device}: normaler Header ändert sich im Sortiermodus: {header_before} -> {header_during}')
            check(active_visual['brand']!='none' and active_visual['quick']!='none' and active_visual['search']!='none' and active_visual['headerFavorite']!='none' and active_visual['undo'] and active_visual['redo'],f'{device}: normale Headerbestandteile bleiben im Sortiermodus nicht vollständig sichtbar: {active_visual}')
            check(active_visual['barPosition']=='fixed' and active_visual['barOutsideHeader'] and not active_visual['barHidden'] and active_visual['barAria']=='false' and not active_visual['barHeaderOverlap'] and not active_visual['barFirstRowOverlap'] and not active_visual['barTitleOverlap'] and active_visual['firstTop']>=active_visual['head']['bottom']-1,f'{device}: separates Sortier-Dock überdeckt Header, erste App-Reihe oder Beschriftung: {active_visual}')
            check(active_visual['imageAnimation']=='pct-home-icon-wiggle' and active_visual['cardAnimation']=='none' and active_visual['wrapperAnimation']=='none' and active_visual['titleAnimation']=='none' and active_visual['favoriteAnimation']=='none' and active_visual['favoriteOpacity']=='0' and active_visual['touch']=='none' and active_visual['cardTransform']=='none' and active_visual['wrapperTransform']=='none',f'{device}: Wackeln wirkt nicht ausschließlich auf den sichtbaren Iconkörper: {active_visual}')
            stable_after={key:[active_visual[key]['x'],active_visual[key]['y'],active_visual[key]['width'],active_visual[key]['height']] for key in ('card','wrapper','title','favorite')}
            check(all(all(abs(a-b)<=.5 for a,b in zip(stable_before[key],stable_after[key])) for key in stable_before),f'{device}: Sortiermodus verschiebt Kachel/Wrapper/Text/Favorit: {stable_before} -> {stable_after}')
            check(active_visual['overlayParent'] and active_visual['overlay']['y']>=active_visual['head']['bottom']-1 and not active_visual['overlayDockOverlap'],f'{device}: Drag-Ebene bleibt nicht zwischen unverändertem Header und Sortier-Dock: {active_visual}')
            overlay_before=active_visual['overlay'];dispatch_body('pointermove',303,bx,by,1);moved_overlay=reorder_page.evaluate("""()=>{const o=document.querySelector('.pct-home-drag-overlay').getBoundingClientRect(),d=document.querySelector('.pct-home-edit-actions').getBoundingClientRect(),p=document.querySelector('.pct-home-drop-placeholder'),g=document.querySelector('#pctHomeGrid'),hit=(a,b)=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top;return{x:o.x,y:o.y,index:[...g.children].indexOf(p),target:p.dataset.target||'',right:o.right,bottom:o.bottom,dockOverlap:hit(o,d)}}""")
            check(abs(moved_overlay['x']-overlay_before['x'])>20 or abs(moved_overlay['y']-overlay_before['y'])>20,f'{device}: freie Drag-Ebene bewegt sich nicht über mehrere Rasterpositionen: {overlay_before} -> {moved_overlay}')
            check(moved_overlay['index']>=7 and moved_overlay['right']<=width+1 and moved_overlay['bottom']<=height+1 and not moved_overlay['dockOverlap'],f'{device}: Zielplatzhalter/Randbegrenzung oder Dock-Sicherheitskante fehlerhaft: {moved_overlay}')
            dispatch_body('pointerup',303,bx,by,0)
            after_drop=mode_state();order_after_first=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)')
            header_after=header_state();header_png_after=reorder_page.locator('.pct-home-head').screenshot()
            restored_visual=reorder_page.evaluate("""()=>({brand:getComputedStyle(document.querySelector('.pct-home-brand')).display,bar:getComputedStyle(document.querySelector('.pct-home-edit-actions')).display,barHidden:document.querySelector('.pct-home-edit-actions').hidden,barAria:document.querySelector('.pct-home-edit-actions').getAttribute('aria-hidden'),favorites:[...document.querySelectorAll('#pctHomeGrid .sk-favorite-button')].every(b=>getComputedStyle(b).opacity==='1'),animations:[...document.querySelectorAll('#pctHomeGrid .sk-home-app')].every(n=>getComputedStyle(n).animationName==='none')})""")
            check(order_after_first.index(first)>=7 and after_drop['mode']=='navigate' and not after_drop['editing'] and after_drop['overlays']==0 and after_drop['placeholders']==0 and after_drop['gridApps']==10 and restored_visual['brand']!='none' and restored_visual['bar']=='none' and restored_visual['barHidden'] and restored_visual['barAria']=='true' and restored_visual['favorites'] and restored_visual['animations'] and header_after==header_before and header_png_after==header_png_before,f'{device}: Drop/Reihenfolge/Normaldesign oder Headeridentität fehlerhaft: order={order_after_first}, state={after_drop}, visual={restored_visual}')
            reorder_page.locator(f'#pctHomeGrid [data-app-id="{first}"]').dispatch_event('click')
            check(reorder_page.evaluate("()=>window.__tapCounts.analogsignal||0")==1,f'{device}: Drag-Abschlussklick öffnet versehentlich die App')
            tap_probe(first,304)
            check(reorder_page.evaluate("()=>window.__tapCounts.analogsignal||0")==2,f'{device}: erster echter Tap nach Drop bleibt gesperrt')

            # Mehrfachsortierung: ein zweiter Long-Press/Drop funktioniert ohne Reload.
            second='pf-rechner';second_target='pt-rechner';ax,ay=long_press(second,305);b=card_box(second_target);bx=b['x']+b['width']*.8;by=b['y']+b['height']*.8
            check(mode_state()['mode']=='sort',f'{device}: zweiter Sortiermodus startet nicht')
            dispatch_body('pointermove',305,bx,by,1);dispatch_body('pointerup',305,bx,by,0)
            reorder_page.locator(f'#pctHomeGrid [data-app-id="{second}"]').dispatch_event('click')
            check(reorder_page.evaluate("()=>window.__tapCounts['pf-rechner']||0")==0,f'{device}: zweiter Drag löst versehentlich Öffnen aus')
            tap_probe(second,306)
            check(reorder_page.evaluate("()=>window.__tapCounts['pf-rechner']||0")==1,f'{device}: Tap nach zweitem Drop bleibt gesperrt')

            # pointercancel muss die laufende Sortierung zurückrollen, alle Zustände lösen
            # und den nächsten echten Tap sofort wieder freigeben.
            cancelled='pt-rechner';before_cancel=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)');ax,ay=long_press(cancelled,307)
            b=card_box('einheitenrechner');dispatch_body('pointermove',307,b['x']+b['width']*.8,b['y']+b['height']*.8,1);dispatch_body('pointercancel',307,ax,ay,0)
            cancelled_state=mode_state();after_cancel=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)')
            check(after_cancel==before_cancel and cancelled_state['mode']=='navigate' and cancelled_state['overlays']==0 and cancelled_state['placeholders']==0 and cancelled_state['gridApps']==10,f'{device}: pointercancel räumt nicht auf oder rollt nicht zurück: {cancelled_state}')
            reorder_page.locator(f'#pctHomeGrid [data-app-id="{cancelled}"]').dispatch_event('click')
            check(reorder_page.evaluate("()=>window.__tapCounts['pt-rechner']||0")==0,f'{device}: Cancel-Abschlussklick öffnet versehentlich')
            tap_probe(cancelled,308)
            check(reorder_page.evaluate("()=>window.__tapCounts['pt-rechner']||0")==1,f'{device}: Tap nach pointercancel bleibt gesperrt')

            # Hintergrundwechsel/pagehide bricht sauber ab. Der getrennte, per Tastatur
            # gestartete Sortiermodus blockiert Navigation bis "Fertig" und gibt sie dann frei.
            interrupted='einheitenrechner';before_interrupt=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)');long_press(interrupted,309)
            reorder_page.evaluate("()=>window.dispatchEvent(new PageTransitionEvent('pagehide'))")
            interrupted_state=mode_state();after_interrupt=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)')
            check(after_interrupt==before_interrupt and interrupted_state['mode']=='navigate' and interrupted_state['overlays']==0 and interrupted_state['placeholders']==0 and interrupted_state['gridApps']==10,f'{device}: pagehide räumt Drag nicht auf: {interrupted_state}')
            tap_probe(interrupted,310)
            check(reorder_page.evaluate("()=>window.__tapCounts['einheitenrechner']||0")==1,f'{device}: Tap nach Hintergrundabbruch bleibt gesperrt')
            keyboard_card=reorder_page.locator('#pctHomeGrid [data-app-id="werkstoffdatenbank"]');keyboard_card.focus();keyboard_card.dispatch_event('keydown',{'key':' ','code':'Space','bubbles':True,'cancelable':True})
            separated=mode_state();keyboard_card.dispatch_event('click')
            check(separated['mode']=='sort' and separated['editing'] and reorder_page.evaluate("()=>window.__tapCounts.werkstoffdatenbank||0")==0,f'{device}: Sortier- und Navigationsmodus sind nicht getrennt: {separated}')
            keyboard_before=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)');keyboard_card.dispatch_event('keydown',{'key':'ArrowRight','code':'ArrowRight','bubbles':True,'cancelable':True});keyboard_moved=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)')
            history_buttons=reorder_page.evaluate("""()=>({undo:document.querySelector('#pctHomeUndo').disabled,redo:document.querySelector('#pctHomeRedo').disabled})""")
            check(keyboard_moved!=keyboard_before and not history_buttons['undo'],f'{device}: Tastaturverschiebung oder Rückgängig-Aktivierung fehlt: {keyboard_before} -> {keyboard_moved}, {history_buttons}')
            reorder_page.locator('#pctHomeUndo').click();keyboard_undone=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)');check(keyboard_undone==keyboard_before and not reorder_page.locator('#pctHomeRedo').is_disabled(),f'{device}: Rückgängig/Wiederholen-Historie fehlerhaft: {keyboard_undone}')
            reorder_page.locator('#pctHomeRedo').click();keyboard_redone=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)');check(keyboard_redone==keyboard_moved,f'{device}: Wiederholen stellt Verschiebung nicht her: {keyboard_redone}')
            reorder_page.locator('#pctHomeDone').dispatch_event('click');tap_probe('werkstoffdatenbank',311)
            check(mode_state()['mode']=='navigate' and reorder_page.evaluate("()=>window.__tapCounts.werkstoffdatenbank||0")==1,f'{device}: Navigation nach Fertig nicht sofort aktiv')

            # DOM und localStorage müssen identisch sein und nach Reload wiederhergestellt werden.
            saved=reorder_page.evaluate("""()=>({dom:[...document.querySelectorAll('#pctHomeGrid .sk-home-app')].map(n=>n.dataset.appId),stored:JSON.parse(localStorage.getItem('skPctHomeOrderV1')||'[]'),overlays:document.querySelectorAll('.pct-home-drag-overlay').length,placeholders:document.querySelectorAll('.pct-home-drop-placeholder').length})""")
            check(saved['dom']==saved['stored'] and saved['overlays']==0 and saved['placeholders']==0,f'{device}: Reihenfolge/Speicherung/Aufräumen fehlerhaft: {saved}')
            expected_order=saved['dom'];reorder_page.reload(wait_until='domcontentloaded');reorder_page.wait_for_function("document.querySelector('#pctHomeGrid')?.dataset.reorderEngine==='pointer-overlay-v3'")
            restored=reorder_page.eval_on_selector_all('#pctHomeGrid .sk-home-app','nodes=>nodes.map(n=>n.dataset.appId)')
            check(restored==expected_order,f'{device}: gespeicherte Reihenfolge nach Neustart nicht wiederhergestellt: {restored}')
            install_tap_probes()
            default_order=['analogsignal','pf-rechner','pt-rechner','einheitenrechner','einheitendatenbank','werkstoffdatenbank','wissensdatenbank','spannungsfall-rechner','siemens-rohwert','eh-device-viewer']
            reset_card=reorder_page.locator('#pctHomeGrid [data-app-id="analogsignal"]');reset_card.focus();reset_card.dispatch_event('keydown',{'key':' ','code':'Space','bubbles':True,'cancelable':True});reorder_page.locator('#pctHomeReset').dispatch_event('click')
            reset_state=reorder_page.evaluate("""()=>({mode:document.querySelector('#pctHomeGrid').dataset.mode,dom:[...document.querySelectorAll('#pctHomeGrid .sk-home-app')].map(n=>n.dataset.appId),stored:JSON.parse(localStorage.getItem('skPctHomeOrderV1')||'[]')})""")
            check(reset_state['mode']=='navigate' and reset_state['dom']==default_order and reset_state['stored']==default_order,f'{device}: Zurücksetzen stellt Standardreihenfolge oder Navigation nicht wieder her: {reset_state}')

            # Favorit bleibt fest an seinem Icon und bedienbar; echte Navigation funktioniert
            # nach mehreren Sortierungen und einem Reload ohne PWA-Neustart.
            favorite=reorder_page.locator('#pctHomeGrid [data-app-id="analogsignal"] .sk-favorite-button');favorite_host=favorite.evaluate("b=>b.parentElement.classList.contains('sk-app-icon-wrapper')");before=favorite.get_attribute('data-active');favorite.click();after=favorite.get_attribute('data-active')
            check(favorite_host and before!=after,f'{device}: Favoritenbutton nach Sortieren nicht icongebunden oder nicht bedienbar')
            reorder_page.evaluate("""()=>{window.__tapHandlers.forEach(([card,handler])=>card.removeEventListener('click',handler));window.__tapHandlers=[]}""")
            if has_touch: reorder_page.locator('#pctHomeGrid [data-app-id="analogsignal"]').tap()
            else: reorder_page.locator('#pctHomeGrid [data-app-id="analogsignal"]').click()
            reorder_page.wait_for_url('**/analogsignal/',timeout=5000)
            check(reorder_page.url.endswith('/analogsignal/'),f'{device}: echte Navigation nach mehrfacher Sortierung fehlgeschlagen: {reorder_page.url}')
            reorder_context.close()

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
        cache_state=upgrade_page.evaluate("""async()=>{const keys=await caches.keys();return{keys,old:keys.some(k=>k.includes('2.6.1.0')),current:keys.filter(k=>k.startsWith('sk-pct-tools-')).every(k=>k.includes('v2-6-3-7-core-r1'))}}""")
        check(not cache_state['old'] and cache_state['current'] and len(cache_state['keys'])==1,f'PWA-Cache-Neuaufbau fehlerhaft: {cache_state}')
        upgrade_context.set_offline(True)
        upgrade_page.goto(urljoin(BASE,''),wait_until='domcontentloaded',timeout=15000)
        check('SK PCT Tools' in upgrade_page.title(),'Neuinstallationskontext ist offline nicht startfähig')
        upgrade_context.close()
    finally: browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Prüfungen');[print(f'- {item}') for item in failures];sys.exit(1)
print(f'PASS · {checks} Browserprüfungen · 15 Seiten × 3 Haupt-Viewports · 5 Reorder-Profile · pixelidentische Headerzustände · Drag/Touch/Pointer · Reflow 320 px · 6 Rechnerreferenzen · Offline')
