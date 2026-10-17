#!/usr/bin/env python3
"""V2.6.5.0-Beta: Audit-Abnahme für Layout, Touch, Suche, Favoriten, Chevron und Offline."""
from __future__ import annotations
import glob, os, sys
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
VERSION='2.6.5.0-Beta'
ROUTES=['','analogsignal/','einheitendatenbank/','einheitenrechner/','pf-rechner/','pt-rechner/','siemens-analogwert-rechner/','spannungsfall-rechner/','werkstoffdatenbank/','wissensdatenbank/','wissensdatenbank/air-torque-antrieb-drehrichtung/','wissensdatenbank/endress-hauser-promass-einbaulage/','wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','wissensdatenbank/siemens-sps-rohwert/','wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/','wissensdatenbank/werkstoff-nachschlagewerk/']
ARTICLE='wissensdatenbank/endress-hauser-promass-einbaulage/'
checks=0;failures=[]
def check(value,message):
 global checks
 checks+=1
 if not value: failures.append(message)
def goto(page,route,wait='networkidle'):
 return page.goto(urljoin(BASE,route),wait_until=wait)

def audit_route(page,route,profile):
 errors=[]
 page.on('pageerror',lambda error: errors.append(str(error)))
 response=goto(page,route)
 check(response and response.ok,f'{profile} {route or "/"}: HTTP nicht OK')
 check(not errors,f'{profile} {route or "/"}: JavaScript-Fehler {errors}')
 state=page.evaluate("""()=>({version:document.body.dataset.skVersion,h1:document.querySelectorAll('h1').length,overflow:document.documentElement.scrollWidth-innerWidth,footer:document.querySelector('[data-sk-shared-footer]')?.textContent||'',identity:document.querySelectorAll('.sk-page-identity img').length,broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)})""")
 check(state['version']==VERSION,f'{profile} {route or "/"}: Version {state["version"]}')
 check(state['h1']==1,f'{profile} {route or "/"}: H1-Anzahl {state["h1"]}')
 check(state['overflow']<=1,f'{profile} {route or "/"}: horizontaler Überlauf {state["overflow"]} px')
 check('V2.6.5' not in state['footer'] and state['footer']=='SK PCT Tools · Simon Kiesler · Offline verfügbar',f'{profile} {route or "/"}: Footer {state["footer"]!r}')
 check(not state['broken'],f'{profile} {route or "/"}: defekte Bilder {state["broken"]}')
 if route and route!='wissensdatenbank/werkstoff-nachschlagewerk/':check(state['identity']==1,f'{profile} {route}: Seitenidentität {state["identity"]}')

with sync_playwright() as p:
 candidates=sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux64/chrome'),reverse=True)
 executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE') or (candidates[0] if candidates else p.chromium.executable_path)
 browser=p.chromium.launch(headless=True,executable_path=executable,args=['--no-sandbox'])
 try:
  # Vollständige Seitenerreichbarkeit und Integrität auf Desktop.
  context=browser.new_context(viewport={'width':1440,'height':1000})
  page=context.new_page()
  for route in ROUTES:audit_route(page,route,'Desktop')
  goto(page,'')
  home=page.evaluate("""()=>{const grid=document.querySelector('#pctHomeGrid'),cards=[...grid.querySelectorAll('.sk-home-app')],host=cards[0].querySelector('.sk-home-icon'),hs=getComputedStyle(host),before=getComputedStyle(host,'::before'),img=host.querySelector('img'),is=getComputedStyle(img);return{apps:cards.length,columns:getComputedStyle(grid).gridTemplateColumns.split(' ').filter(Boolean).length,minTitle:Math.min(...cards.map(c=>parseFloat(getComputedStyle(c.querySelector('h2')).fontSize))),host:{border:hs.borderTopWidth,bg:hs.backgroundColor,shadow:hs.boxShadow,before:before.content,filter:hs.filter},image:{filter:is.filter,transform:is.transform}}}""")
  check(home['apps']==10 and home['columns']==5,f'Desktop Home: {home["apps"]} Apps / {home["columns"]} Spalten')
  check(home['minTitle']>=12,f'Desktop Home: Kartenbezeichnung nur {home["minTitle"]} px')
  check(home['host']=={'border':'0px','bg':'rgba(0, 0, 0, 0)','shadow':'none','before':'none','filter':'none'},f'Desktop Home: sichtbarer Iconhost {home["host"]}')
  check(home['image']['filter']=='none' and home['image']['transform']=='none',f'Desktop Home: PNG Zusatzgestaltung {home["image"]}')

  # Suche/Filter: Popover, Treffer unmittelbar im Panel, keine Logikverluste.
  page.click('#skFilterToggle');page.fill('#skToolSearch','Siemens');page.wait_for_timeout(150)
  search=page.evaluate("""()=>({expanded:document.querySelector('#skFilterToggle').getAttribute('aria-expanded'),apps:document.querySelectorAll('#pctHomeGrid .sk-home-app:not([hidden])').length,results:document.querySelectorAll('#skKnowledgeResultList .sk-search-result-card').length,inPanel:document.querySelector('#skFilterContent').contains(document.querySelector('#skKnowledgeResults')),panelHeight:document.querySelector('#skFilterContent').getBoundingClientRect().height})""")
  check(search['expanded']=='true' and search['apps']==1 and search['results']>=3 and search['inPanel'],f'Desktop Suche: {search}')
  check(search['panelHeight']<650,f'Desktop Suche: Panel zu hoch {search["panelHeight"]}')

  # Favoriten: linkes Fachicon, Text, Entfernen rechts; Speicherung bleibt erhalten.
  page.click('#skFilterReset');page.click('#skFilterToggle');page.locator('.sk-home-app').first.locator('.sk-favorite-button').click();page.locator('.sk-favorites-trigger').click();page.wait_for_timeout(120)
  fav=page.evaluate("""()=>{const row=document.querySelector('.sk-favorite-row'),icon=row?.querySelector('.sk-favorite-icon-host img'),link=row?.querySelector('.sk-favorite-entry'),remove=row?.querySelector('.sk-favorite-remove'),rr=row?.getBoundingClientRect(),ir=icon?.getBoundingClientRect(),lr=link?.getBoundingClientRect(),xr=remove?.getBoundingClientRect();return{rows:document.querySelectorAll('.sk-favorite-row').length,icon:!!icon&&icon.complete&&icon.naturalWidth===512,order:ir&&lr&&xr&&ir.left<lr.left&&lr.left<xr.left,inside:rr&&ir.left>=rr.left&&xr.right<=rr.right+1,text:link?.querySelector('strong')?.textContent}}""")
  check(fav['rows']==1 and fav['icon'] and fav['order'] and fav['inside'],f'Favoritenübersicht: {fav}')
  page.keyboard.press('Escape');page.reload(wait_until='networkidle');page.locator('.sk-favorites-trigger').click();check(page.locator('.sk-favorite-row').count()==1,'Favorit wurde nach Reload nicht gespeichert')
  page.locator('.sk-favorite-remove').click();check(page.locator('.sk-favorite-row').count()==0,'Favorit konnte nicht entfernt werden')

  # Sortiermodus: Header bleibt ortsfest; Dock/Bedienziele sind normgerecht.
  page.keyboard.press('Escape');goto(page,'');header_before=page.locator('.pct-home-head').bounding_box();first=page.locator('.sk-home-app').first;first.focus();page.keyboard.press('Space');page.wait_for_timeout(100);header_after=page.locator('.pct-home-head').bounding_box()
  check(all(abs(header_before[k]-header_after[k])<.5 for k in ('x','y','width','height')),f'Sortiermodus verändert Header: {header_before}/{header_after}')
  dock=page.locator('.pct-home-edit-actions');check(dock.is_visible(),'Sortierdock nicht sichtbar')
  dims=dock.locator('button').evaluate_all("bs=>bs.map(b=>{const r=b.getBoundingClientRect();return[Math.round(r.width),Math.round(r.height),!!b.querySelector('.pct-icon')]})")
  check(all(w>=44 and h>=44 and icon for w,h,icon in dims),f'Sortierdock-Touchziele/Icons: {dims}')
  page.click('#pctHomeDone');check('pct-home-editing' not in (page.locator('body').get_attribute('class') or ''),'Sortiermodus endet nicht sofort')
  context.close()

  # Smartphone / iOS-PWA-nahe Geometrie.
  context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=1,has_touch=True,is_mobile=True)
  page=context.new_page();goto(page,'')
  mobile=page.evaluate("""()=>({columns:getComputedStyle(document.querySelector('#pctHomeGrid')).gridTemplateColumns.split(' ').filter(Boolean).length,labels:[...document.querySelectorAll('.sk-home-app-title')].map(n=>parseFloat(getComputedStyle(n).fontSize)),touch:[...document.querySelectorAll('.sk-favorite-button')].map(n=>{const r=n.getBoundingClientRect();return Math.min(r.width,r.height)})})""")
  check(mobile['columns'] in (2,3),f'Mobil Home: {mobile["columns"]} Spalten')
  check(min(mobile['labels'])>=12,f'Mobil Home: Kartenlabel {min(mobile["labels"])} px')
  check(min(mobile['touch'])>=44,f'Mobil Home: Favoritentouch {min(mobile["touch"])} px')
  page.click('#skFilterToggle');page.fill('#skToolSearch','Siemens');page.wait_for_timeout(150)
  search_mobile=page.evaluate("""()=>{const input=document.querySelector('#skToolSearch'),icon=input.parentElement.querySelector('.pct-icon'),r=input.getBoundingClientRect(),i=icon.getBoundingClientRect(),s=getComputedStyle(input);return{paddingLeft:parseFloat(s.paddingLeft),iconRight:i.right-input.getBoundingClientRect().left,results:document.querySelectorAll('#skKnowledgeResultList .sk-search-result-card').length,overflow:document.documentElement.scrollWidth-innerWidth}}""")
  check(search_mobile['paddingLeft']>=42 and search_mobile['iconRight']<search_mobile['paddingLeft'],f'Mobile Suche: Icon/Text überlagert {search_mobile}')
  check(search_mobile['results']>=3 and search_mobile['overflow']<=1,f'Mobile Suche: Ergebnisse/Überlauf {search_mobile}')

  goto(page,'siemens-analogwert-rechner/')
  copy_dims=page.locator('.pct-copy-button:visible').evaluate_all("bs=>bs.map(b=>{const r=b.getBoundingClientRect();return[Math.round(r.width),Math.round(r.height)]})")
  check(copy_dims and all(w>=44 and h>=44 for w,h in copy_dims),f'Mobil Rechner: Kopierziele {copy_dims}')
  controls=page.locator('button:visible,select:visible,a.sk-unit-database-button:visible').evaluate_all("ns=>ns.map(n=>{const r=n.getBoundingClientRect();return{label:n.getAttribute('aria-label')||n.textContent.trim(),w:r.width,h:r.height}})")
  check(all(item['h']>=43.5 and item['w']>=43.5 for item in controls),f'Mobil Rechner: zu kleine Controls {[x for x in controls if x["h"]<43.5 or x["w"]<43.5]}')

  goto(page,ARTICLE)
  crumbs=page.locator('.kb-breadcrumb>*').evaluate_all("ns=>ns.filter(n=>getComputedStyle(n).display!=='none').map(n=>n.textContent.trim())")
  check(crumbs==['Wissensdatenbank'],f'Mobile Breadcrumbs: {crumbs}')

  goto(page,'einheitendatenbank/');summary=page.locator('.unit-category-head').first
  check(summary.evaluate("n=>getComputedStyle(n,'::after').content")=='none','Einheitendatenbank verwendet noch Plus/Minus-Pseudoicon')
  summary.click();page.wait_for_timeout(220)
  check(summary.locator('.pct-chevron-slot').evaluate("n=>Math.abs(parseFloat(getComputedStyle(n).rotate)-180)<2"),'Einheitendatenbank-Chevron zeigt geöffnet nicht nach oben')

  goto(page,'werkstoffdatenbank/');toggle=page.locator('.material-card-toggle').first
  check(toggle.locator('.material-toggle-icon').evaluate("n=>getComputedStyle(n,'::after').content")=='none','Werkstoffdatenbank verwendet noch Plus/Minus-Pseudoicon')
  toggle.click();page.wait_for_timeout(220)
  check(toggle.locator('.pct-chevron-slot').evaluate("n=>Math.abs(parseFloat(getComputedStyle(n).rotate)-180)<2"),'Werkstoffdatenbank-Chevron zeigt geöffnet nicht nach oben')
  context.close()

  # Tablet-Sicht und Offline-Navigation aus dem Precache.
  context=browser.new_context(viewport={'width':820,'height':1180},device_scale_factor=1,has_touch=True,is_mobile=False)
  page=context.new_page();audit_route(page,'wissensdatenbank/','Tablet')
  check(page.locator('.knowledge-hub-card').count()==5,'Tablet Wissens-Hub: nicht fünf Hersteller')
  context.close()

  context=browser.new_context(viewport={'width':390,'height':844},has_touch=True,is_mobile=True,service_workers='allow')
  page=context.new_page();goto(page,'');page.evaluate("()=>navigator.serviceWorker.ready.then(()=>true)");page.wait_for_timeout(500);context.set_offline(True)
  response=page.goto(urljoin(BASE,'einheitendatenbank/'),wait_until='domcontentloaded');check(response and response.ok,'Offline: Einheitendatenbank nicht erreichbar')
  check(page.locator('h1').inner_text().strip()=='Einheitendatenbank','Offline: falsches Fallbackziel')
  context.set_offline(False);context.close()
 finally:
  browser.close()

if failures:
 print(f'FAIL · {len(failures)}/{checks} Auditprüfungen')
 for failure in failures:print('-',failure)
 sys.exit(1)
print(f'PASS · {checks} Auditprüfungen · 16 Seiten · Desktop · Smartphone/iOS-PWA · Tablet · Suche · Favoriten · Sortierung · Touch · Offline')
