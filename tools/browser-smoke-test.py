#!/usr/bin/env python3
"""Browser-, Responsive-, PWA- und Rechner-Volltest für SK PLT Tools 2.1.7.3-Beta."""
from pathlib import Path
import json,os
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'test-artifacts'; OUT.mkdir(exist_ok=True)
BASE='http://127.0.0.1:4173'; VERSION='2.1.7.3-Beta'
LAYOUT_MEASUREMENTS=[]
PAGES=['/','/analogsignal/','/siemens-analogwert-rechner/','/einheitenrechner/','/einheitendatenbank/','/messstellen-doku/','/pf-rechner/','/pt-rechner/','/servicewerte/','/spannungsfall-rechner/','/wissensdatenbank/','/wissensdatenbank/air-torque-antrieb-drehrichtung/','/wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/','/wissensdatenbank/siemens-sps-rohwert/','/wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/','/wissensdatenbank/werkstoff-nachschlagewerk/']
CALCULATORS=[('analogsignal','/analogsignal/'),('siemens','/siemens-analogwert-rechner/'),('einheiten','/einheitenrechner/'),('pf','/pf-rechner/'),('pt','/pt-rechner/'),('spannungsfall','/spannungsfall-rechner/')]

def text(page,selector,expected):
    actual=page.locator(selector).inner_text().strip(); assert actual==expected,f'{selector}: {actual!r} statt {expected!r}'
def set_input(page,selector,value):
    page.locator(selector).fill(str(value)); page.locator(selector).dispatch_event('input')
def common(page,route,mobile=False):
    page.goto(BASE+route); page.wait_for_load_state('networkidle')
    assert page.locator('body').get_attribute('data-sk-version')==VERSION
    assert page.evaluate('document.documentElement.scrollWidth<=window.innerWidth'),f'Überlauf: {route}'
    assert page.locator('header.sk-global-header').count()==1
    assert page.locator('.sk-header-home').count()==1
    assert page.locator('.sk-favorites-trigger').is_visible() and page.locator('.sk-tree-trigger').is_visible()
    if mobile:
        header=page.locator('header.sk-global-header').bounding_box(); viewport=page.viewport_size
        assert abs(header['x'])<=1 and abs(header['width']-viewport['width'])<=1
        assert page.locator('html').evaluate('el=>getComputedStyle(el).backgroundColor')=='rgb(4, 19, 31)'
        assert page.locator('header.sk-global-header').evaluate('el=>getComputedStyle(el).borderBottomStyle')!='none'
def numeric_keypads(page,route):
    fields=page.locator('input[type="number"]'); assert fields.count()>0
    for index in range(fields.count()):
        assert fields.nth(index).get_attribute('inputmode') in ('decimal','numeric'),f'inputmode fehlt: {route} #{fields.nth(index).get_attribute("id")}'
def unit_database_cta(page,route):
    cta=page.locator('.sk-unit-database-cta'); button=page.locator('.sk-unit-database-button')
    calculator=page.locator('.calc-panel,.analog-panel').first
    assert cta.count()==1 and cta.is_visible(),f'Einheitendatenbank-Bereich fehlt: {route}'
    assert button.count()==1 and button.is_visible(),f'Einheitendatenbank-Button fehlt: {route}'
    assert calculator.count()==1 and calculator.is_visible(),f'Rechner-Hauptbereich fehlt: {route}'
    assert button.get_attribute('href')=='../einheitendatenbank/',f'Einheitendatenbank-Ziel falsch: {route}'
    box=cta.bounding_box(); calc=calculator.bounding_box(); viewport=page.viewport_size; assert box and calc
    assert cta.evaluate('el=>getComputedStyle(el).boxSizing')=='border-box',f'Einheitenfavoriten ohne border-box: {route}'
    assert abs(box['x']-calc['x'])<=1,f'Linke Kante abweichend: {route} ({box["x"]}/{calc["x"]})'
    assert abs((box['x']+box['width'])-(calc['x']+calc['width']))<=1,f'Rechte Kante abweichend: {route}'
    assert abs(box['width']-calc['width'])<=1,f'Breite weicht vom Rechner-Hauptbereich ab: {route} ({box["width"]}/{calc["width"]})'
    assert box['x']>=0 and box['x']+box['width']<=viewport['width']+1,f'Einheitenfavoriten außerhalb des Viewports: {route}'
    LAYOUT_MEASUREMENTS.append({'route':route,'viewport':viewport,'calculator':{key:round(calc[key],2) for key in ('x','width')},'unitFavorites':{key:round(box[key],2) for key in ('x','width')},'edgeDelta':{'left':round(box['x']-calc['x'],2),'right':round((box['x']+box['width'])-(calc['x']+calc['width']),2)}})
    if viewport['width']<=760:
        assert button.bounding_box()['width']<=box['width'],f'Einheitendatenbank-Button mobil zu breit: {route}'
def mobile_controls(page):
    viewport=page.viewport_size; left=page.locator('.sk-favorites-trigger').bounding_box(); right=page.locator('.sk-tree-trigger').bounding_box()
    assert left and right and abs(left['x']-10)<=1 and abs(viewport['width']-right['x']-right['width']-10)<=1
    left_bottom=viewport['height']-left['y']-left['height']; right_bottom=viewport['height']-right['y']-right['height']
    assert 8<=left_bottom<=10 and 8<=right_bottom<=10
    assert page.locator('.sk-favorites-trigger').evaluate('el=>getComputedStyle(el).position')=='fixed'

def calculator_tests(page):
    page.goto(BASE+'/einheitenrechner/'); page.wait_for_load_state('networkidle'); text(page,'#out','1.000,000 mbar')
    page.locator('#cat').select_option('temperature'); page.locator('#from').select_option('fahrenheit'); set_input(page,'#x',32); text(page,'#out','273,150 K')
    page.locator('#to').select_option('celsius'); text(page,'#out','0,000 °C')

    page.goto(BASE+'/analogsignal/'); page.wait_for_load_state('networkidle'); text(page,'#out','12,000 mA'); text(page,'#pct','50,0 %')
    page.locator('#processUnit').select_option('psi'); assert abs(float(page.locator('#x').input_value())-725.18868865)<1e-8; text(page,'#out','12,000 mA')
    page.locator('#signalUnit').select_option('ampere'); assert abs(float(page.locator('#s1').input_value())-.02)<1e-12; text(page,'#out','0,012 A')

    page.goto(BASE+'/pf-rechner/'); page.wait_for_load_state('networkidle'); text(page,'#k','0,160000'); text(page,'#n','4,000000')
    page.locator('#xUnit').select_option('psi'); assert abs(float(page.locator('#x2').input_value())-1450.3773773)<1e-8
    page.locator('#yUnit').select_option('ampere'); assert abs(float(page.locator('#y2').input_value())-.02)<1e-12

    page.goto(BASE+'/pt-rechner/'); page.wait_for_load_state('networkidle'); text(page,'#out','100,000 Ω')
    page.locator('#inputUnit').select_option('fahrenheit'); assert page.locator('#x').input_value()=='32'; text(page,'#out','100,000 Ω')
    page.locator('#dir').select_option('rt'); assert page.locator('#x').input_value()=='100'; text(page,'#out','0,00 °C')
    page.locator('#outputUnit').select_option('fahrenheit'); text(page,'#out','32,00 °F')

    page.goto(BASE+'/siemens-analogwert-rechner/'); page.wait_for_load_state('networkidle'); text(page,'#rawResult','13.824'); text(page,'#physicalResult','50,000 °C')
    page.locator('#physicalUnitSelect').select_option('fahrenheit'); assert page.locator('#physicalMin').input_value()=='-58' and page.locator('#physicalMax').input_value()=='302'; text(page,'#physicalResult','122,000 °F')
    page.locator('#inputSignToggle').click(); assert float(page.locator('#inputValue').input_value())==-12; page.locator('#inputSignToggle').click()

    page.goto(BASE+'/spannungsfall-rechner/'); page.wait_for_load_state('networkidle'); set_input(page,'#current',16); set_input(page,'#length',35); page.locator('#calculate').click(); text(page,'#dropV','6,93 V'); text(page,'#dropPercent','1,73 %')
    page.locator('#currentUnit').select_option('milliampere'); assert page.locator('#current').input_value()=='16000'; text(page,'#dropV','6,93 V')
    page.locator('#lengthUnit').select_option('foot'); assert abs(float(page.locator('#length').input_value())-114.829396325)<1e-8; text(page,'#dropV','6,93 V')
    page.locator('#voltageUnit').select_option('millivolt'); text(page,'#dropV','6.928,20 mV')

with sync_playwright() as p:
    executable=os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
    if not executable:
        candidates=[Path('/opt/pw-browsers/chromium-1208/chrome-linux64/chrome'),Path('/opt/pw-browsers/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell')]
        executable=str(next((item for item in candidates if item.exists()),'')) or None
    browser=p.chromium.launch(headless=True,executable_path=executable)
    context=browser.new_context(viewport={'width':1440,'height':1050},device_scale_factor=1)
    desktop=context.new_page(); console_errors=[]
    desktop.on('console',lambda msg: console_errors.append(msg.text) if msg.type=='error' else None)
    for route in PAGES: common(desktop,route)
    desktop.goto(BASE+'/'); desktop.wait_for_load_state('networkidle'); assert desktop.locator('.tools>a.card').count()==10; text(desktop,'.hero .badge',f'Version {VERSION}')
    external=desktop.locator('.sk-external-card'); assert external.get_attribute('href')=='https://www.de.endress.com/de/onlinetools?store_locale=de'; assert external.get_attribute('target')=='_blank'; assert external.get_attribute('rel')=='noopener noreferrer'
    desktop.locator('#skToolSearch').fill('psi'); desktop.wait_for_function("document.querySelectorAll('#skKnowledgeResultList>a').length===1"); text(desktop,'#skKnowledgeResultList h3','Einheitendatenbank'); desktop.locator('#skFilterReset').click()
    unit_card=desktop.locator('.tools>a.card[href="einheitendatenbank/"]'); unit_card.locator('.sk-favorite-button').click(); desktop.locator('.sk-favorites-trigger').click(); assert desktop.locator('.sk-favorites-list').get_by_text('Einheitendatenbank',exact=True).count()==1; desktop.locator('.sk-favorites-close').click()

    desktop.goto(BASE+'/einheitendatenbank/'); desktop.wait_for_load_state('networkidle'); assert desktop.locator('.unit-category-card').count()==19; assert desktop.locator('.unit-row').count()==115; text(desktop,'#unitResult','115 Einheiten in 19 Kategorien')
    desktop.locator('#unitSearch').fill('Fahrenheit'); assert desktop.locator('.unit-row:visible').count()==1; desktop.locator('#unitReset').click(); desktop.locator('#unitCategoryFilter').select_option('viscosity'); assert desktop.locator('.unit-category-card:visible').count()==1; desktop.locator('#unitReset').click()
    fahrenheit=desktop.locator('.unit-row').filter(has_text='Grad Fahrenheit').locator('.unit-favorite-button'); fahrenheit.click(); assert fahrenheit.get_attribute('data-active')=='true'; desktop.reload(); desktop.wait_for_load_state('networkidle'); assert desktop.locator('.unit-row').filter(has_text='Grad Fahrenheit').locator('.unit-favorite-button').get_attribute('data-active')=='true'
    desktop.goto(BASE+'/einheitenrechner/'); desktop.wait_for_load_state('networkidle'); desktop.locator('#cat').select_option('temperature'); assert desktop.locator('#from optgroup[label="Favoriten"] option[value="fahrenheit"]').count()==1
    calculator_tests(desktop)
    for slug,route in CALCULATORS:
        common(desktop,route); numeric_keypads(desktop,route); unit_database_cta(desktop,route); assert desktop.locator('select optgroup[label="Standardeinheit"]').count()>=1; desktop.screenshot(path=str(OUT/f'rechner-{slug}-desktop.png'),full_page=True)
    common(desktop,'/einheitendatenbank/'); desktop.screenshot(path=str(OUT/'einheitendatenbank-desktop.png'),full_page=True)

    # PWA installieren lassen und die neue Datenbank aus dem Cache offline öffnen.
    desktop.goto(BASE+'/'); desktop.wait_for_load_state('networkidle'); desktop.evaluate("navigator.serviceWorker.ready.then(()=>true)"); desktop.wait_for_function("caches.keys().then(keys=>keys.includes('sk-plt-tools-v2.1.7.3-Beta'))")
    desktop.reload(); desktop.wait_for_load_state('networkidle'); context.set_offline(True); desktop.goto(BASE+'/einheitendatenbank/'); desktop.wait_for_load_state('domcontentloaded'); text(desktop,'h1','Einheitendatenbank'); assert desktop.locator('.unit-row').count()==115; context.set_offline(False)

    tablet_context=browser.new_context(viewport={'width':820,'height':1180},device_scale_factor=2,is_mobile=True)
    tablet=tablet_context.new_page(); tablet_errors=[]; tablet.on('console',lambda msg: tablet_errors.append(msg.text) if msg.type=='error' else None)
    for route in PAGES: common(tablet,route)
    for slug,route in CALCULATORS: common(tablet,route); numeric_keypads(tablet,route); unit_database_cta(tablet,route); tablet.screenshot(path=str(OUT/f'rechner-{slug}-tablet.png'),full_page=True)
    common(tablet,'/einheitendatenbank/'); tablet.screenshot(path=str(OUT/'einheitendatenbank-tablet.png'),full_page=True)

    mobile_context=browser.new_context(viewport={'width':390,'height':844},device_scale_factor=2,is_mobile=True,has_touch=True)
    mobile=mobile_context.new_page(); mobile_errors=[]; mobile.on('console',lambda msg: mobile_errors.append(msg.text) if msg.type=='error' else None)
    for route in PAGES: common(mobile,route,True); mobile_controls(mobile)
    for slug,route in CALCULATORS: common(mobile,route,True); numeric_keypads(mobile,route); unit_database_cta(mobile,route); mobile.screenshot(path=str(OUT/f'rechner-{slug}-mobile.png'),full_page=True)
    common(mobile,'/einheitendatenbank/',True); mobile.locator('#unitSearch').fill('bar'); assert mobile.locator('.unit-row:visible').count()>=1; mobile.screenshot(path=str(OUT/'einheitendatenbank-mobile.png'),full_page=True)
    landscape_context=browser.new_context(viewport={'width':844,'height':390},device_scale_factor=2,is_mobile=True,has_touch=True)
    landscape=landscape_context.new_page(); common(landscape,'/',True); mobile_controls(landscape); landscape.screenshot(path=str(OUT/'startseite-mobile-landscape.png'),full_page=True)

    assert not console_errors,f'Desktop-Konsole: {console_errors}'; assert not tablet_errors,f'Tablet-Konsole: {tablet_errors}'; assert not mobile_errors,f'Mobil-Konsole: {mobile_errors}'
    (OUT/'einheitenfavoriten-layout.json').write_text(json.dumps({'version':VERSION,'tolerancePx':1,'measurements':LAYOUT_MEASUREMENTS},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('OK: Desktop, Tablet, iPhone-Touchprofil, Querformat, alle Rechner, Einheitenfavoriten, automatische Umrechnungen und Offline-PWA geprüft.')
    browser.close()
