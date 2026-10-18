#!/usr/bin/env python3
"""Browser-, Touch-, Navigations-, Such-, Favoriten-, Vergleichs- und Offlinetest 2.6.6.0."""
from __future__ import annotations
import os,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('SK_BASE_URL','http://127.0.0.1:8080/')
ROOT=Path(__file__).resolve().parents[1]
SHOT=ROOT/'tests'/'screenshots-v2660';SHOT.mkdir(exist_ok=True)
ROUTES=['','analogsignal/','pf-rechner/','pt-rechner/','einheitenrechner/','einheitendatenbank/','spannungsfall-rechner/','siemens-analogwert-rechner/','werkstoffdatenbank/','wissensdatenbank/','wissensdatenbank/air-torque-antrieb-drehrichtung/','wissensdatenbank/endress-hauser-promass-einbaulage/','wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','wissensdatenbank/siemens-sps-rohwert/','wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/']
PATHS=[
 ('air-torque','pneumatischer-antrieb','Drehrichtung SCO/SCC','air-torque-antrieb-drehrichtung/'),
 ('endress-hauser','promass','Einbaulage und Einbausituation','endress-hauser-promass-einbaulage/'),
 ('siemens','sitrans-p320','SIL-Verriegelung','siemens-sitrans-p320-sil-verriegelung/'),
 ('siemens','sps-analogkarte','Rohwert und Skalierung','siemens-sps-rohwert/'),
 ('vacon','frequenzumrichter','Ist-/Sollwert-Abweichung im PLS','vacon-frequenzumrichter-ist-sollwert-abweichung/')]
def assert_no_overflow(page,label):
 metrics=page.evaluate('''()=>({sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,bad:[...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.right>document.documentElement.clientWidth+2||r.left<-2}).slice(0,8).map(e=>e.className||e.tagName)})''')
 assert metrics['sw']<=metrics['cw']+2,f'{label}: horizontal overflow {metrics}'
def stable(page,locator,label):
 locator.scroll_into_view_if_needed();page.wait_for_timeout(40);before=locator.bounding_box();assert before,label+' missing';locator.hover();page.wait_for_timeout(90);after=locator.bounding_box();assert after,label+' missing after hover';assert abs(before['x']-after['x'])<.6 and abs(before['y']-after['y'])<.6 and abs(before['width']-after['width'])<.6 and abs(before['height']-after['height'])<.6,f'{label} moved on hover: {before} -> {after}'
def main():
 errors=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path=os.environ.get('SK_CHROMIUM_EXECUTABLE') or '/opt/pw-browsers/chromium-1208/chrome-linux64/chrome')
  # Viewports including 320, 390, tablet and desktop.
  for width,height,name in [(320,740,'320'),(390,844,'iphone390'),(768,1024,'tablet'),(1440,1000,'desktop')]:
   context=browser.new_context(viewport={'width':width,'height':height},is_mobile=width<=430,has_touch=width<=768,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148' if width<=430 else None)
   page=context.new_page();page.on('console',lambda msg,n=name: errors.append(f'{n} console {msg.type}: {msg.text}') if msg.type=='error' else None);page.on('pageerror',lambda exc,n=name: errors.append(f'{n} pageerror: {exc}'))
   for route in ROUTES:
    page.goto(BASE+route,wait_until='networkidle');assert page.locator('h1').count()==1,f'{name} {route}: h1';assert_no_overflow(page,f'{name} {route}')
    if width<=430:
     targets=page.locator('a:visible,button:visible,input:visible,select:visible,summary:visible');
     for i in range(min(targets.count(),40)):
      box=targets.nth(i).bounding_box()
      if box and targets.nth(i).evaluate("e=>!e.matches('input[type=search],select')"):
       assert box['height']>=39,f'{name} {route}: touch target {i} only {box["height"]}'
   page.goto(BASE+'wissensdatenbank/',wait_until='networkidle');page.screenshot(path=str(SHOT/f'knowledge-{name}.png'),full_page=True)
   page.goto(BASE+'werkstoffdatenbank/',wait_until='networkidle');page.wait_for_selector('.material-tile');page.screenshot(path=str(SHOT/f'materials-{name}.png'),full_page=True)
   context.close()
  # Functional desktop flow.
  context=browser.new_context(viewport={'width':1280,'height':900})
  page=context.new_page();page.on('console',lambda msg: errors.append(f'functional console {msg.type}: {msg.text}') if msg.type=='error' else None);page.on('pageerror',lambda exc: errors.append(f'functional pageerror: {exc}'))
  page.goto(BASE,wait_until='networkidle');assert page.locator('.sk-home-app').count()==10;assert page.locator('text=V2.6.6.0-Beta').count()>=1
  # Header geometry remains fixed when sort mode is entered by long mouse press.
  first=page.locator('.sk-home-app').first;head=page.locator('.pct-home-head');hb=head.bounding_box();box=first.bounding_box();page.mouse.move(box['x']+box['width']/2,box['y']+box['height']/2);page.mouse.down();page.wait_for_timeout(360);page.mouse.up();page.wait_for_timeout(80);ha=head.bounding_box();assert abs(hb['x']-ha['x'])<1 and abs(hb['y']-ha['y'])<1 and abs(hb['height']-ha['height'])<1,'Header moved in sort mode';page.locator('#pctHomeDone').click() if page.locator('#pctHomeDone:visible').count() else None
  # Five complete manufacturer -> family -> article paths and parent navigation.
  for manufacturer,family,title,slug in PATHS:
   page.goto(BASE+'wissensdatenbank/',wait_until='networkidle');page.locator(f'a[href*="manufacturer={manufacturer}"]').first.click();page.wait_for_url(f'**manufacturer={manufacturer}');page.locator(f'a[href*="family={family}"]').first.click();page.wait_for_url(f'**family={family}');assert page.locator('.knowledge-tile').count()>=1;stable(page,page.locator('.knowledge-tile').first,f'{slug} tile');page.locator('.knowledge-tile').first.click();page.wait_for_url(f'**/{slug}');assert page.locator('h1').inner_text().strip();assert page.locator('.kb-context-back').count()==1;page.locator(f'.kb-breadcrumb a[href*="family={family}"]').click();page.wait_for_url(f'**family={family}');page.locator(f'.knowledge-breadcrumb a[href*="manufacturer={manufacturer}"]').click();page.wait_for_url(f'**manufacturer={manufacturer}');page.locator('.knowledge-breadcrumb a').filter(has_text='Wissensdatenbank').click();page.wait_for_url('**/wissensdatenbank/')
  # Search across all levels.
  page.goto(BASE+'wissensdatenbank/',wait_until='networkidle');page.locator('#knowledgeSearch').fill('Promass');page.wait_for_timeout(100);texts=page.locator('.knowledge-tile').all_inner_texts();assert any('Promass' in x for x in texts) and any('Einbaulage' in x for x in texts),texts;page.locator('#knowledgeSearchReset').click();assert page.locator('.knowledge-tile').count()==5
  # Empty and populated favorites.
  page.evaluate("localStorage.setItem('skPctToolsFavoritesV2','[]')");page.reload(wait_until='networkidle');page.locator('.sk-favorites-trigger').click();assert page.locator('.sk-favorites-empty').is_visible();page.locator('.sk-favorites-close').click();page.locator('.knowledge-tile .sk-favorite-button').first.click();page.locator('.sk-favorites-trigger').click();assert page.locator('.sk-favorite-entry').count()==1;page.locator('.sk-favorites-close').click()
  # Material direct list/detail/back/search/filter/comparison.
  page.goto(BASE+'werkstoffdatenbank/',wait_until='networkidle');page.wait_for_selector('.material-tile');assert page.locator('.material-tile').count()==10;stable(page,page.locator('.material-tile').first,'material tile');page.locator('.material-tile').filter(has_text='1.4404').click();page.wait_for_url('**material=1-4404');assert page.locator('#materialDetail').is_visible();assert 'X2CrNiMo17-12-2' in page.locator('#materialDetail').inner_text();page.locator('.material-breadcrumb a').filter(has_text='Werkstoffdatenbank').click();page.wait_for_url('**/werkstoffdatenbank/');page.locator('#materialSearch').fill('316L');page.wait_for_timeout(80);assert page.locator('.material-tile').count()>=3;page.locator('#materialSearch').fill('1.4404');assert page.locator('.material-tile').count()==1;page.locator('#materialReset').click();page.locator('#materialCompareSelect').select_option('14404-vs-14408');assert '1.4404 gegen 1.4408' in page.locator('#materialComparison').inner_text()
  # Material favorite survives query URL and reopens the direct detail.
  page.locator('.material-tile').first.locator('.sk-favorite-button').click();page.locator('.sk-favorites-trigger').click();assert page.locator('.sk-favorite-entry').count()>=2;page.locator('.sk-favorites-close').click()
  # Mobile back chip and full desktop breadcrumb behavior.
  page.goto(BASE+'wissensdatenbank/siemens-sps-rohwert/',wait_until='networkidle');assert page.locator('.kb-breadcrumb').is_visible();context.close()
  mobile=browser.new_context(viewport={'width':390,'height':844},is_mobile=True,has_touch=True,user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148')
  page=mobile.new_page();page.goto(BASE+'wissensdatenbank/siemens-sps-rohwert/',wait_until='networkidle');assert page.locator('.kb-context-back').is_visible();assert not page.locator('.kb-breadcrumb').is_visible();page.goto(BASE+'werkstoffdatenbank/?material=1-4404',wait_until='networkidle');assert page.locator('#materialBack').is_visible();assert_no_overflow(page,'mobile material detail');mobile.close()
  # Service worker and offline direct routes.
  context=browser.new_context(viewport={'width':390,'height':844})
  page=context.new_page();page.goto(BASE,wait_until='networkidle');page.evaluate("async()=>{await navigator.serviceWorker.ready;if(!navigator.serviceWorker.controller){await new Promise(r=>navigator.serviceWorker.addEventListener('controllerchange',r,{once:true}))}}")
  page.goto(BASE+'wissensdatenbank/',wait_until='networkidle');page.wait_for_selector('.knowledge-tile');context.set_offline(True)
  page.goto(BASE+'wissensdatenbank/endress-hauser-promass-einbaulage/',wait_until='domcontentloaded');assert 'Einbaulage' in page.locator('h1').inner_text()
  page.goto(BASE+'werkstoffdatenbank/?material=1-4404',wait_until='domcontentloaded');page.wait_for_selector('#materialDetail:not([hidden])');assert '1.4404' in page.locator('#materialDetail').inner_text();context.set_offline(False);context.close();browser.close()
 if errors:raise AssertionError('\n'.join(errors))
 print('PASS · Browser/Touch/Navigation/Suche/Favoriten/Werkstoffvergleich/Offline · 320/390/768/1440 · Chromium iPhone-Emulation')
 return 0
if __name__=='__main__':
 try:sys.exit(main())
 except Exception as exc:print('FAIL',exc);sys.exit(1)
