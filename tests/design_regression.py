#!/usr/bin/env python3
"""V2.6.5.0-Beta: Clean-Design-, Zustands-, Touch- und Favoritendialog-Prüfung."""
from __future__ import annotations
import glob, os, sys
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
PROFILES=[
    ('iPhone-PWA',390,844,True,True),
    ('Tablet-Touch',820,1180,True,True),
    ('Desktop',1440,1000,False,False),
]
MANUFACTURERS=('air-torque','endress-hauser','siemens','vacon','sonstiges')
failures=[];checks=0

def check(condition,message):
    global checks
    checks+=1
    if not condition:failures.append(message)

def goto(page,route):
    return page.goto(urljoin(BASE,route),wait_until='networkidle')

def rect_equal(a,b,tolerance=.35):
    keys=('x','y','width','height','right','bottom')
    return all(abs(a[k]-b[k])<=tolerance for k in keys)

def tile_state(card):
    return card.evaluate("""card=>{const icon=card.querySelector('.knowledge-home-icon'),image=icon?.querySelector('img.knowledge-brand-logo'),title=card.querySelector('h2'),r=node=>{const b=node.getBoundingClientRect();return{x:b.x,y:b.y,width:b.width,height:b.height,right:b.right,bottom:b.bottom}},s=node=>{const c=getComputedStyle(node);return{border:c.borderTopWidth,background:c.backgroundColor,backgroundImage:c.backgroundImage,shadow:c.boxShadow,filter:c.filter,transform:c.transform,translate:c.translate,scale:c.scale,transition:c.transitionProperty}},before=icon?getComputedStyle(icon,'::before'):null,after=icon?getComputedStyle(icon,'::after'):null;return{card:r(card),icon:r(icon),image:r(image),title:r(title),cardStyle:s(card),iconStyle:s(icon),imageStyle:s(image),before:before?.content,after:after?.content}}""")

def verify_stable_states(page,card,label):
    base=tile_state(card)
    card.hover(force=True);hover=tile_state(card)
    card.focus();focus=tile_state(card)
    box=card.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();pressed=tile_state(card);page.mouse.move(0,0);page.mouse.up()
    card.evaluate("n=>{n.classList.add('active');n.dataset.active='true';n.setAttribute('aria-selected','true')}");active=tile_state(card);card.evaluate("n=>{n.classList.remove('active');delete n.dataset.active;n.removeAttribute('aria-selected')}")
    for state_name,state in (('Hover',hover),('Fokus',focus),('Drücken',pressed),('Aktiv',active)):
        check(all(rect_equal(base[key],state[key]) for key in ('card','icon','image','title')),f'{label} {state_name}: Kachel/Icon/Text verschoben: {base} -> {state}')
        check(all(state[key]['transform']=='none' and state[key]['translate']=='none' and state[key]['scale']=='none' for key in ('cardStyle','iconStyle','imageStyle')),f'{label} {state_name}: Transform/Translate/Scale aktiv: {state}')
    check(base['iconStyle']['border']=='0px' and base['iconStyle']['background']=='rgba(0, 0, 0, 0)' and base['iconStyle']['backgroundImage']=='none' and base['iconStyle']['shadow']=='none' and base['iconStyle']['filter']=='none' and base['before']=='none' and base['after']=='none',f'{label}: alter Wrapper/Rahmen/Schatten aktiv: {base}')
    check(base['imageStyle']['filter']=='none' and base['imageStyle']['transform']=='none',f'{label}: PNG wird zusätzlich gefiltert oder transformiert: {base}')

with sync_playwright() as p:
    candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
    browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
    try:
        for name,width,height,has_touch,is_mobile in PROFILES:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,has_touch=has_touch,is_mobile=is_mobile)
            page=context.new_page();goto(page,'wissensdatenbank/')
            hubs=page.locator('.knowledge-hub-card:visible')
            check(hubs.count()==5,f'{name}: {hubs.count()} statt 5 Herstellerkacheln')
            for index in range(hubs.count()):verify_stable_states(page,hubs.nth(index),f'{name} Hersteller {index+1}')
            hub_files=page.eval_on_selector_all('.knowledge-hub-card img.knowledge-brand-logo',"nodes=>nodes.map(n=>({file:n.src.split('?')[0].split('/').pop(),natural:[n.naturalWidth,n.naturalHeight],broken:!n.complete||n.naturalWidth===0}))")
            check(len(hub_files)==5 and all(item['file'].startswith('v2-6-5-0-manufacturer-') and item['natural']==[512,512] and not item['broken'] for item in hub_files),f'{name}: Hersteller-PNGs fehlerhaft: {hub_files}')

            total_entries=0
            for manufacturer in MANUFACTURERS:
                goto(page,f'wissensdatenbank/?manufacturer={manufacturer}')
                entries=page.locator('.knowledge-entry:visible');total_entries+=entries.count()
                for index in range(entries.count()):verify_stable_states(page,entries.nth(index),f'{name} Beitrag {manufacturer}/{index+1}')
            check(total_entries==5,f'{name}: {total_entries} statt 5 Wissensbeiträge über alle Hersteller')

            # Dialog mit realem Favoritenbestand öffnen und Design/Funktionen prüfen.
            goto(page,'wissensdatenbank/?manufacturer=siemens')
            first=page.locator('.knowledge-entry:visible').first
            first_title=first.locator('h2').inner_text().strip();first.locator('.sk-favorite-button').click()
            trigger=page.locator('.pct-header-actions>.sk-favorites-trigger')
            if has_touch:trigger.tap()
            else:trigger.click()
            page.wait_for_timeout(180)
            dialog=page.locator('#skFavoritesDrawer')
            state=dialog.evaluate("""d=>{const r=d.getBoundingClientRect(),s=getComputedStyle(d),row=d.querySelector('.sk-favorite-row'),rs=row?getComputedStyle(row):null,close=d.querySelector('.sk-favorites-close'),remove=d.querySelector('.sk-favorite-remove'),clear=d.querySelector('.sk-favorites-clear'),button=b=>{const x=b.getBoundingClientRect(),c=getComputedStyle(b);return{rect:{x:x.x,y:x.y,width:x.width,height:x.height,right:x.right,bottom:x.bottom},transform:c.transform,translate:c.translate,scale:c.scale,shadow:c.boxShadow}};return{open:d.classList.contains('open'),aria:d.getAttribute('aria-hidden'),role:d.getAttribute('role'),modal:d.getAttribute('aria-modal'),rect:{x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom},transform:s.transform,translate:s.translate,scale:s.scale,shadow:s.boxShadow,borderRight:s.borderRightWidth,row:row?{border:rs.borderTopWidth,shadow:rs.boxShadow,transform:rs.transform}:null,rows:d.querySelectorAll('.sk-favorite-row').length,summary:d.querySelector('.sk-favorites-summary')?.textContent,clearDisabled:clear.disabled,close:button(close),remove:button(remove),clear:button(clear)}}""")
            check(state['open'] and state['aria']=='false' and state['role']=='dialog' and state['modal']=='true',f'{name}: Favoritendialog semantisch/visuell nicht geöffnet: {state}')
            check(state['rect']['x']>=-1 and state['rect']['right']<=width+1 and state['rect']['bottom']<=height+1 and state['rect']['width']>=min(320,width-12),f'{name}: Favoritendialog außerhalb Viewport/Safe-Area: {state}')
            check(state['transform']=='none' and state['translate']=='none' and state['scale']=='none' and state['shadow']=='none' and state['borderRight']=='1px',f'{name}: Favoritendialog besitzt alten Außenkasten/Schatten/Bewegung: {state}')
            check(state['rows']==1 and state['row']=={'border':'1px','shadow':'none','transform':'none'} and state['summary']=='1 gespeicherter Favorit' and not state['clearDisabled'],f'{name}: Favoritenzeile/Zähler/Leeren fehlerhaft: {state}')
            check(all(min(state[key]['rect']['width'],state[key]['rect']['height'])>=44 and state[key]['transform']=='none' and state[key]['translate']=='none' and state[key]['scale']=='none' and state[key]['shadow']=='none' for key in ('close','remove','clear')),f'{name}: Dialogbedienelement unter 44 px oder bewegt/verschattet: {state}')

            # Hover/Fokus/Drücken der Dialogaktionen dürfen die Geometrie nicht ändern.
            for selector in ('.sk-favorites-close','.sk-favorite-remove','.sk-favorites-clear'):
                button=dialog.locator(selector).first
                snap=lambda:button.evaluate("b=>{const r=b.getBoundingClientRect(),s=getComputedStyle(b);return{x:r.x,y:r.y,width:r.width,height:r.height,right:r.right,bottom:r.bottom,transform:s.transform,translate:s.translate,scale:s.scale}}")
                base=snap();button.hover(force=True);hover=snap();button.focus();focus=snap();box=button.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();pressed=snap();page.mouse.move(0,0);page.mouse.up()
                check(all(rect_equal(base,value) and value['transform']=='none' and value['translate']=='none' and value['scale']=='none' for value in (hover,focus,pressed)),f'{name} {selector}: Bedienelement bewegt sich: {base}/{hover}/{focus}/{pressed}')

            # Speicherung über Reload, Einzellöschen, Leeren und leerer Zustand.
            page.keyboard.press('Escape');page.wait_for_timeout(40)
            check(dialog.get_attribute('aria-hidden')=='true' and trigger.evaluate('n=>document.activeElement===n'),f'{name}: Escape schließt nicht oder Fokus kehrt nicht zurück')
            page.reload(wait_until='networkidle');trigger=page.locator('.pct-header-actions>.sk-favorites-trigger');trigger.click();page.wait_for_timeout(120)
            check(page.locator('#skFavoritesDrawer .sk-favorite-row').count()==1 and first_title in page.locator('#skFavoritesDrawer').inner_text(),f'{name}: Favorit bleibt nach Reload nicht erhalten')
            page.locator('#skFavoritesDrawer .sk-favorite-remove').click();check(page.locator('#skFavoritesDrawer .sk-favorite-row').count()==0 and page.locator('#skFavoritesDrawer .sk-favorites-empty').count()==1 and page.locator('#skFavoritesDrawer .sk-favorites-clear').is_disabled(),f'{name}: Einzellöschen/leerer Zustand fehlerhaft')
            page.locator('.sk-favorites-close').click();goto(page,'wissensdatenbank/?manufacturer=siemens');page.locator('.knowledge-entry:visible').first.locator('.sk-favorite-button').click();page.locator('.pct-header-actions>.sk-favorites-trigger').click();page.locator('#skFavoritesDrawer .sk-favorites-clear').click()
            check(page.locator('#skFavoritesDrawer .sk-favorite-row').count()==0 and page.locator('#skFavoritesDrawer .sk-favorites-empty').count()==1 and page.locator('.sk-favorites-count').is_hidden(),f'{name}: Alle leeren oder Favoritenzähler fehlerhaft')
            context.close()
    finally:browser.close()

if failures:
    print(f'FAIL · {len(failures)}/{checks} Designprüfungen')
    for failure in failures:print(f'- {failure}')
    sys.exit(1)
print(f'PASS · {checks} Designprüfungen · 3 Viewports · 5 Hersteller · 5 Wissensbeiträge · ortsfeste Zustände · Favoritendialog · Touch · Tastatur')
