#!/usr/bin/env python3
"""Struktur-, Referenz-, Design- und Integritätsprüfung für SK PCT Tools 2.6.2.0-Beta."""
from __future__ import annotations
import hashlib, json, re, struct, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.6.2.0-Beta'
VERSION_SLUG='v2-6-2-0'
MANIFEST=f'manifest-{VERSION_SLUG}.webmanifest'
SEARCH_INDEX=f'assets/search-index-{VERSION_SLUG}.json'
SHARED_CSS=f'assets/app-{VERSION_SLUG}.css'
SHARED_JS=f'assets/app-{VERSION_SLUG}.js'
BRAND_ASSETS={
 'logo-sk-pct-tools.png':(512,512,True),'favicon.png':(64,64,True),
 'apple-touch-icon.png':(180,180,False),'icon-192.png':(192,192,True),
 'icon-512.png':(512,512,True),'icon-maskable-192.png':(192,192,False),
 'icon-maskable-512.png':(512,512,False)
}
APPS={'analogsignal','pf-rechner','pt-rechner','einheitenrechner','einheitendatenbank','werkstoffdatenbank','wissensdatenbank','spannungsfall-rechner','siemens-rohwert','eh-device-viewer'}
KNOWLEDGE_ARTICLES={'air-torque-antrieb-drehrichtung','endress-hauser-promass-einbaulage','siemens-sitrans-p320-sil-verriegelung','siemens-sps-rohwert','vacon-frequenzumrichter-ist-sollwert-abweichung'}
APP_ICON_MAP={
 'analogsignal':'app-analogsignal','pf-rechner':'app-pf-rechner','pt-rechner':'app-pt-rechner',
 'einheitenrechner':'app-einheitenrechner','einheitendatenbank':'app-einheitendatenbank',
 'werkstoffdatenbank':'app-werkstoffdatenbank','wissensdatenbank':'app-wissensdatenbank',
 'spannungsfall-rechner':'app-spannungsfall','siemens-rohwert':'app-siemens-rohwert','eh-device-viewer':'app-eh-viewer'
}
KNOWLEDGE_ICON_MAP={slug:f'knowledge-{slug}' for slug in KNOWLEDGE_ARTICLES}
ICON_STEMS=set(APP_ICON_MAP.values())|set(KNOWLEDGE_ICON_MAP.values())|{
 'manufacturer-air-torque','manufacturer-endress-hauser','manufacturer-siemens',
 'manufacturer-sonstiges','manufacturer-vacon','nav-back','nav-home'
}
NAV_ICONS={f'{VERSION_SLUG}-{stem}.png' for stem in ICON_STEMS}
BACKGROUND_PERIMETER_SHA256='58a873d04834f9ecbc7c831803d9183dcb5c21c0cb034955642c6dc829a28773'
ICON_SHA256={
 'app-analogsignal':'5a6ea80d40ccabcc6b417db51f63aa6834addddde3b39ae9957bf51368564249',
 'app-eh-viewer':'ec504e0b5c2199b5816567748de345d575947d20cc9838fc04cdf53728d8a826',
 'app-einheitendatenbank':'2b96afe18b52af0e54b20e30c74d2e3041eea5fd788f21ab8b5fd47d363d2f77',
 'app-einheitenrechner':'2164c0d976091519d4d891327aa3baddbc052ddcebc5194cee5a1e94c846e3e5',
 'app-pf-rechner':'0ffa0ab10cbd1110407575aa6bd91909d98d54c9a9fe4a14d4091a533e62e974',
 'app-pt-rechner':'7f00c1da75882e66c9f40e322c9810b910bd742a42db4e3d350a4c92d4e0541f',
 'app-siemens-rohwert':'6146e852cc3ba1bf0e574034ad07b0e94a782d658b897a68f21ba31d1cf44468',
 'app-spannungsfall':'7a3d68d616a2099905e936f75e33c06bcc2c52fd005fd4c0a69a41dd8fa24903',
 'app-werkstoffdatenbank':'2d68661d47e20851b2775d6c2a5bdea9d9cfe1957ffe765cc872cbb8f2459912',
 'app-wissensdatenbank':'c1c0fa25f0c6fa8a4f7d313d3cfcdd1250b93b5f937be037f25f715cab8507b1',
 'knowledge-air-torque-antrieb-drehrichtung':'5c24a392ff6590e34a5c0f851bb68475b7a5de6fd86dbd7712173e6664e0ca19',
 'knowledge-endress-hauser-promass-einbaulage':'0f49e64d698277659577bc65ffff4cbf4265a26fa2d8ab8fe6022af0769ac1d0',
 'knowledge-siemens-sitrans-p320-sil-verriegelung':'bd342d7698a289cad81417a52cf35372ae73b2e810b44c353d9c4d8740dc30a5',
 'knowledge-siemens-sps-rohwert':'1a98040b230de0356af8c8c9c174830f086599eb4efc454d428d90eff771adc0',
 'knowledge-vacon-frequenzumrichter-ist-sollwert-abweichung':'aa54b1154d1685c75bab47159b333f0f02744392291e95caf45401f4f68b9bfa',
 'manufacturer-air-torque':'0f4ef826b1a26001da33e58a1f0ed4368df42246e7868609d0134a5f6d1dc155',
 'manufacturer-endress-hauser':'34f4087f005202174fcdc324d07032b5f159e17b6163586ad90d64345170d29f',
 'manufacturer-siemens':'c3d516f1a74a647b902c972d9958324f17794c47c4b69c3d5a52354b32daaf66',
 'manufacturer-sonstiges':'fc556b32927f7ad15741308f2b3cc663356c77852c03b213fab6ed80e8671b95',
 'manufacturer-vacon':'851a27f15e4638d4423706d18825a703f245a0b2bb73521fb529398135b2f9e0',
 'nav-back':'15d767d5f452365c6b81af1d7b674ebabb3eed1c344182a6bef08e06914f829f',
 'nav-home':'d3434a58f707423cc5c93192db5deed0edc63654bddf4cdb8cb0f2d074580d04'
}
EXPERIENCE_SOURCE='Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.refs=[];self.apps=[];self.h1=0;self.styles=[];self.scripts=[];self.shared_header=0;self.shared_footer=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);classes=set(a.get('class','').split())
        if tag=='h1':self.h1+=1
        if tag=='a' and 'sk-home-app' in classes:self.apps.append(a)
        if tag=='header' and 'data-sk-shared-header' in a:self.shared_header+=1
        if tag=='footer' and 'data-sk-shared-footer' in a:self.shared_footer+=1
        if tag=='link' and a.get('rel')=='stylesheet':self.styles.append(a.get('href','').split('?')[0])
        if tag=='script' and a.get('src'):self.scripts.append(a['src'].split('?')[0])
        if tag in {'a','img','script','link'}:
            ref=a.get('href' if tag in {'a','link'} else 'src')
            if ref and not urlsplit(ref).scheme and not ref.startswith(('#','mailto:','tel:')):self.refs.append(ref)

def check(condition,message,errors):
    if not condition:errors.append(message)

def target_exists(source:Path,ref:str)->bool:
    target=(source.parent/urlsplit(ref).path).resolve()
    try:target.relative_to(ROOT)
    except ValueError:return False
    return target.is_file() or (target.is_dir() and (target/'index.html').is_file())

def text_files():
    for p in ROOT.rglob('*'):
        if p.is_file() and p.suffix.lower() not in {'.png','.jpg','.jpeg','.gif','.ico','.zip'}:
            try:yield p,p.read_text(encoding='utf-8')
            except UnicodeDecodeError:pass

def main()->int:
    errors=[]
    check((ROOT/'VERSION').read_text().strip()==VERSION,'VERSION stimmt nicht.',errors)
    manifest=json.loads((ROOT/MANIFEST).read_text())
    check(manifest.get('version')==VERSION,'Manifest-Version stimmt nicht.',errors)
    check(VERSION in manifest.get('description',''),'Manifest-Beschreibung enthält die Version nicht.',errors)
    manifest_icons={(item.get('src'),item.get('sizes'),item.get('purpose')) for item in manifest.get('icons',[])}
    check(manifest_icons=={
        ('assets/icon-192.png','192x192','any'),('assets/icon-512.png','512x512','any'),
        ('assets/icon-maskable-192.png','192x192','maskable'),('assets/icon-maskable-512.png','512x512','maskable')
    },f'Manifest-Iconbestand oder Purpose falsch: {manifest_icons}',errors)
    check(not list(ROOT.glob('manifest-v2-6-1-*.webmanifest')),'Altes Manifest vorhanden.',errors)
    index=json.loads((ROOT/SEARCH_INDEX).read_text())
    check(index and all(item.get('release')==VERSION for item in index),'Suchindex besitzt falsche Release-Markierungen.',errors)

    html_pages=sorted(ROOT.rglob('*.html'))
    check(len(html_pages)==16,f'HTML-Anzahl {len(html_pages)} statt 16.',errors)
    framed=[]
    for page in html_pages:
        rel=page.relative_to(ROOT);text=page.read_text();parser=Parser();parser.feed(text)
        redirect='data-sk-page="redirect"' in text
        check('viewport-fit=cover' in text,f'viewport-fit fehlt: {rel}',errors)
        check(VERSION in text,f'Version fehlt: {rel}',errors)
        check(parser.h1==1,f'H1-Anzahl in {rel}: {parser.h1}',errors)
        check('name="referrer"' in text and 'content="no-referrer"' in text,f'Referrer-Schutz fehlt: {rel}',errors)
        check(MANIFEST in text,f'Manifest-Verweis fehlt: {rel}',errors)
        check('favicon.png' in text and 'apple-touch-icon.png' in text,f'Browser-/Apple-Icon-Verweis fehlt: {rel}',errors)
        check(len(parser.styles)==1 and parser.styles[0].endswith(SHARED_CSS),f'Nicht genau ein Zentral-CSS in {rel}: {parser.styles}',errors)
        if not redirect:
            check(sum(x.endswith(SHARED_JS) for x in parser.scripts)==1,f'Zentrale Laufzeit fehlt oder ist doppelt: {rel}',errors)
        for ref in parser.refs:check(target_exists(page,ref),f'Lokales Ziel fehlt in {rel}: {ref}',errors)
        if 'data-sk-layout="framed"' in text and not redirect:
            framed.append(page)
            check(parser.shared_header==1,f'Zentraler Header-Platzhalter fehlt: {rel}',errors)
            check(parser.shared_footer==1,f'Zentraler Footer-Platzhalter fehlt: {rel}',errors)
    check(len(framed)==14,f'Gerahmte Seiten: {len(framed)} statt 14.',errors)

    start=(ROOT/'index.html').read_text();p=Parser();p.feed(start)
    ids=[a.get('data-app-id') for a in p.apps]
    check(len(ids)==10 and set(ids)==APPS and len(ids)==len(set(ids)),f'App-Inventar fehlerhaft: {ids}',errors)
    for app_id,stem in APP_ICON_MAP.items():
        check(start.count(f'{VERSION_SLUG}-{stem}.png')==1,f'Eindeutiges App-Icon fehlt oder ist doppelt: {app_id}',errors)
    external=[a for a in p.apps if a.get('data-app-id')=='eh-device-viewer']
    check(len(external)==1 and external[0].get('href')=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H-Viewer-Ziel fehlerhaft.',errors)

    operational='\n'.join(p.read_text(encoding='utf-8') for suffix in ('*.html','*.css','*.js','*.json','*.webmanifest') for p in ROOT.rglob(suffix))
    check(not re.search(r'2\.6\.1\.[0-9](?:-Beta)?|v2-6-1-[0-9]',operational),'Operative Altversionsverweise vorhanden.',errors)
    for removed in ('core.css','responsive.css','design-system.css','pct-frame.css','pct-controls-v2-6-1-5.css','pct-home-v2-6-1-5.css','app-v2-6-1-5.css','app-v2-6-1-5.js','app-v2-6-1-6.css','app-v2-6-1-6.js','app-v2-6-1-7.css','app-v2-6-1-7.js','app-v2-6-1-8.css','app-v2-6-1-8.js'):
        check(not (ROOT/'assets'/removed).exists(),f'Ersetzte Datei noch vorhanden: {removed}',errors)
    check(len(list((ROOT/'assets').glob('*.css')))==1,'Mehr als ein CSS-Bestand vorhanden.',errors)
    check((ROOT/SHARED_CSS).is_file() and (ROOT/SHARED_JS).is_file(),'Zentrale CSS-/JS-Datei fehlt.',errors)

    css=(ROOT/SHARED_CSS).read_text();js=(ROOT/SHARED_JS).read_text()
    check(css.count('!important')<=5,f'Zu viele !important: {css.count("!important")}',errors)
    for token in ('--sk-touch-min:44px','--sk-header-size:76px','--sk-footer-size:38px','viewport','strukturell icongebundene Favoriten','sk-app-icon-wrapper','tatsächlichen sichtbaren','--sk-favorite-touch-size:44px','--sk-favorite-visible-size:22px','--sk-favorite-ring-inset:11px','inset-block-start:-22px','inset-inline-end:-22px','translate:none'):
        check(token in css,f'Zentrale CSS-Regel fehlt: {token}',errors)
    check('sk-home-app.card:hover{transform:translateY' not in css,'Startseiten-Hover verschiebt App-Icons noch.',errors)
    check('--sk-favorite-circle-outset' not in css,'Alte 25/75-Favoritenposition ist noch aktiv.',errors)
    final_css=css.split('/* === V2.6.2.0-Beta: strukturell icongebundene Favoriten',1)[-1]
    check(final_css.count('>.sk-app-icon-wrapper>.sk-favorite-button.pct-control')>=10,'Direkte Wrapper-Verankerung des Favoritenbuttons fehlt.',errors)
    check('calc(50%' not in final_css and '--sk-home-icon-top' not in final_css and '--sk-knowledge-icon-top' not in final_css,'Finale Favoritenposition hängt noch von Kachelmitte oder Geräteabständen ab.',errors)
    for token in ('SK_PCT_SHARED','buildSharedLayout','data-sk-shared-header','data-sk-shared-footer','skPctToolsFavoritesV2','search-index-v2-6-2-0.json','logo-sk-pct-tools.png','v2-6-2-0-nav-home.png','const iconWrapper=card.querySelector',"iconWrapper.classList.add('sk-app-icon-wrapper')",'const host=iconWrapper||card','host.append(button)',"setAttribute('aria-pressed'"):
        check(token in js,f'Zentrale Laufzeit unvollständig: {token}',errors)
    check('Object.keys(localStorage).find' not in js,'Veraltete Favoriten-Key-Migration noch vorhanden.',errors)

    nav_dir=ROOT/'assets/navigation-icons';icons=sorted(nav_dir.glob('*.png'))
    check({p.name for p in icons}==NAV_ICONS,f'Navigationsicon-Bestand abweichend: {[p.name for p in icons]}',errors)
    for icon in icons:
        raw=icon.read_bytes();stem=icon.stem.removeprefix(f'{VERSION_SLUG}-')
        check(hashlib.sha256(raw).hexdigest()==ICON_SHA256.get(stem),f'Bestätigtes Icon-Design wurde verändert: {icon.name}',errors)
        check(raw[:8]==b'\x89PNG\r\n\x1a\n',f'PNG-Signatur fehlt: {icon.name}',errors)
        if len(raw)>=26:
            width,height=struct.unpack('>II',raw[16:24]);check((width,height)==(512,512),f'Icon-Größe falsch: {icon.name}',errors)
        with Image.open(icon) as image:
            rgba=image.convert('RGBA');pixels=list(rgba.get_flattened_data());check(rgba.getchannel('A').getextrema()==(0,255),f'Transparenz fehlerhaft: {icon.name}',errors)
            check(rgba.getchannel('A').getbbox()==(13,9,489,491),f'Sichtbare Icon-Grenze verändert: {icon.name}',errors)
            colored=sum(1 for r,g,b,a in pixels if a and not (r==g==b));black=sum(1 for r,g,b,a in pixels if a>240 and r<18 and g<18 and b<18);white=sum(1 for r,g,b,a in pixels if a>240 and r>245 and g>245 and b>245)
            check(colored>80000 and black>35000 and 10000<=white<=60000,f'Verlauf/Kontur/Symbolmasse fehlerhaft: {icon.name}',errors)
            perimeter=bytearray()
            for i,pixel in enumerate(pixels):
                x=i%512;y=i//512
                if x<80 or x>=432 or y<72 or y>=420:perimeter.extend(pixel)
            check(hashlib.sha256(perimeter).hexdigest()==BACKGROUND_PERIMETER_SHA256,f'Hintergrundmaster verändert: {icon.name}',errors)
            check(rgba.getpixel((60,256))[1]>rgba.getpixel((60,256))[2],f'Grünseite fehlt: {icon.name}',errors)
            check(rgba.getpixel((400,90))[2]>rgba.getpixel((400,90))[1],f'Blauseite fehlt: {icon.name}',errors)

    # Neue Markenfamilie: Standardvarianten transparent, Maskable/iOS vollflächig
    # und die kontrastreiche Wort-/Motivmasse innerhalb der zentralen Safe-Zone.
    for name,(width,height,transparent) in BRAND_ASSETS.items():
        path=ROOT/'assets'/name
        check(path.is_file(),f'Marken-/PWA-Datei fehlt: {name}',errors)
        if not path.is_file():continue
        with Image.open(path) as image:
            rgba=image.convert('RGBA');alpha=rgba.getchannel('A')
            check(rgba.size==(width,height),f'Marken-/PWA-Größe falsch: {name} {rgba.size}',errors)
            if transparent:check(alpha.getextrema()==(0,255),f'Transparente Markenvariante fehlerhaft: {name}',errors)
            else:check(alpha.getextrema()==(255,255),f'Vollflächige Maskable-/iOS-Variante nicht opak: {name}',errors)
            pixels=list(rgba.get_flattened_data())
            black=sum(1 for r,g,b,a in pixels if a>240 and r<18 and g<18 and b<18)
            white=sum(1 for r,g,b,a in pixels if a>240 and r>245 and g>245 and b>245)
            cyan=sum(1 for r,g,b,a in pixels if a>240 and b>170 and g>130 and r<80)
            green=sum(1 for r,g,b,a in pixels if a>240 and g>170 and r<140 and b<150)
            white_min=.01 if width<=64 else .02
            check(black>width*height*.04 and white>width*height*white_min and cyan>width*height*.003 and green>width*height*.003,f'Markenpalette/Konturmasse fehlerhaft: {name}',errors)
    maskable=Image.open(ROOT/'assets/icon-maskable-512.png').convert('RGBA')
    safe_white=unsafe_white=0
    for y in range(512):
        for x in range(512):
            r,g,b,a=maskable.getpixel((x,y))
            if r>245 and g>245 and b>245:
                if ((x-255.5)**2+(y-255.5)**2)**.5<=205:safe_white+=1
                else:unsafe_white+=1
    check(safe_white>10000 and unsafe_white<500,f'Maskable-Safe-Zone fehlerhaft: innen={safe_white}, außen={unsafe_white}',errors)
    check('logo-sk-pct-tools.png' in start and "alt=\"SK PCT Tools · Tool's by S.K.\"" in start,'Neues sichtbares Startseitenlogo fehlt.',errors)

    knowledge=(ROOT/'wissensdatenbank/index.html').read_text()
    for slug,stem in KNOWLEDGE_ICON_MAP.items():
        check(knowledge.count(f'{VERSION_SLUG}-{stem}.png')==1,f'Eindeutiges Wissensicon fehlt oder ist doppelt: {slug}',errors)
    for slug in KNOWLEDGE_ARTICLES:
        article=(ROOT/'wissensdatenbank'/slug/'index.html').read_text()
        check('knowledge-compact.js' in article and EXPERIENCE_SOURCE in article,f'Wissensbeitrag unvollständig: {slug}',errors)

    worker=(ROOT/'service-worker.js').read_text()
    check("CACHE_EPOCH='v2-6-2-0-core-r1'" in worker,'Cache-Epoch falsch.',errors)
    check('DOCUMENT_CACHE' not in worker and 'OPTIONAL_DOCUMENTS' not in worker,'Nicht benötigter Dokumentcache noch vorhanden.',errors)
    cached=re.findall(r"'\./([^']+)'",worker)
    for ref in cached:check(target_exists(ROOT/'index.html',ref),f'Offline-Ziel fehlt: {ref}',errors)
    for icon in NAV_ICONS:check(f"'./assets/navigation-icons/{icon}'" in worker,f'Icon fehlt im Offline-Cache: {icon}',errors)
    for brand in BRAND_ASSETS:check(f"'./assets/{brand}'" in worker,f'Marken-/PWA-Datei fehlt im Offline-Cache: {brand}',errors)
    for stale in ('core.css','design-system.css','pct-frame.css','knowledge-cartoon.css','ICON-DESIGNRICHTLINIE.txt'):
        check(stale not in worker,f'Unnötiger Cache-Eintrag: {stale}',errors)

    generator=(ROOT/'tools/generate_png_icons.py').read_text()
    for token in ('PREFIX = "v2-6-2-0-"','"app-analogsignal": app_analogsignal','"app-wissensdatenbank": app_knowledge_database','"knowledge-siemens-sps-rohwert": knowledge_sps_raw'):
        check(token in generator,f'Icon-Generator unvollständig: {token}',errors)
    brand_generator=(ROOT/'tools/generate_brand_assets.py').read_text()
    for token in ('def standard_master()','def maskable_master()','TOOL\'S BY S.K.','result.putalpha(255)'):
        check(token in brand_generator,f'Markenlogo-Generator unvollständig: {token}',errors)
    check(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in icons})==22,'Icons sind nicht vollständig eigenständig.',errors)
    sprite=(ROOT/'assets/pct-controls.svg').read_text()
    for symbol in ('search','star','close','reset','chevron','copy','check','warning','info','print','trash','download','calculate','done'):
        check(f'id="icon-{symbol}"' in sprite,f'Control-Sprite unvollständig: icon-{symbol}',errors)
    for required in ('README.txt','RELEASE-NOTES.txt','ICON-DESIGNRICHTLINIE.txt','WISSENSBEITRAGS-STANDARD.md','TESTPLAN.md','TEST-RESULTS.txt','SECURITY-DEPLOYMENT.md','UEBERGABE-V2.6.2.0-Beta.txt'):
        check((ROOT/required).is_file(),f'Dokument fehlt: {required}',errors)

    sums=ROOT/'SHA256SUMS.txt'
    if sums.exists():
        listed=[]
        for line in sums.read_text().splitlines():
            m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);check(bool(m),f'Ungültige Prüfsummenzeile: {line}',errors)
            if not m:continue
            expected,rel=m.groups();path=ROOT/rel.removeprefix('./');listed.append(path.resolve());check(path.is_file(),f'Prüfsummendatei fehlt: {rel}',errors)
            if path.is_file():check(hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Prüfsumme falsch: {rel}',errors)
        expected={p.resolve() for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts}
        check(set(listed)==expected,'SHA256SUMS-Dateibestand unvollständig oder zusätzlich.',errors)

    if errors:
        print('FAIL');[print(f'- {e}') for e in errors];return 1
    files=sum(1 for p in ROOT.rglob('*') if p.is_file())
    print(f'PASS · {files} Dateien · 10 Apps · 6 Rechner · 14 interne Unterseiten · 22 Navigationsicons · {css.count("!important")} !important · Version {VERSION}')
    return 0

if __name__=='__main__':sys.exit(main())
