#!/usr/bin/env python3
"""Struktur-, Referenz-, Design- und Integritätsprüfung für SK PCT Tools 2.6.1.4-Beta."""
from __future__ import annotations
import hashlib, json, re, struct, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.6.1.4-Beta'
VERSION_SLUG='v2-6-1-4'
MANIFEST=f'manifest-{VERSION_SLUG}.webmanifest'
SEARCH_INDEX=f'assets/search-index-{VERSION_SLUG}.json'
SHARED_CSS=f'assets/app-{VERSION_SLUG}.css'
SHARED_JS=f'assets/app-{VERSION_SLUG}.js'
APPS={'analogsignal','pf-rechner','pt-rechner','einheitenrechner','einheitendatenbank','werkstoffdatenbank','wissensdatenbank','spannungsfall-rechner','siemens-rohwert','eh-device-viewer'}
KNOWLEDGE_ARTICLES={'air-torque-antrieb-drehrichtung','endress-hauser-promass-einbaulage','siemens-sitrans-p320-sil-verriegelung','siemens-sps-rohwert','vacon-frequenzumrichter-ist-sollwert-abweichung'}
NAV_ICONS={
 f'{VERSION_SLUG}-app-calculator.png',f'{VERSION_SLUG}-app-database.png',f'{VERSION_SLUG}-app-eh-viewer.png',
 f'{VERSION_SLUG}-manufacturer-air-torque.png',f'{VERSION_SLUG}-manufacturer-endress-hauser.png',
 f'{VERSION_SLUG}-manufacturer-siemens.png',f'{VERSION_SLUG}-manufacturer-sonstiges.png',f'{VERSION_SLUG}-manufacturer-vacon.png',
 f'{VERSION_SLUG}-nav-back.png',f'{VERSION_SLUG}-nav-home.png'
}
BACKGROUND_PERIMETER_SHA256='63f387a45785714c19b416ffbabe702908b9b873e4918f4cd846a3bd638aad10'
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
    check(not list(ROOT.glob('manifest-v2-6-1-[0-3].webmanifest')),'Altes Manifest vorhanden.',errors)
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
    check(start.count(f'{VERSION_SLUG}-app-calculator.png')==6,'Sechs Rechner verwenden nicht den gemeinsamen Rechner-Master.',errors)
    check(start.count(f'{VERSION_SLUG}-app-database.png')==3,'Drei Datenbanken verwenden nicht den gemeinsamen Buch-Master.',errors)
    external=[a for a in p.apps if a.get('data-app-id')=='eh-device-viewer']
    check(len(external)==1 and external[0].get('href')=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H-Viewer-Ziel fehlerhaft.',errors)

    operational='\n'.join(p.read_text(encoding='utf-8') for suffix in ('*.html','*.css','*.js','*.json','*.webmanifest') for p in ROOT.rglob(suffix))
    check(not re.search(r'2\.6\.1\.[0-3](?:-Beta)?|v2-6-1-[0-3]',operational),'Operative Altversionsverweise vorhanden.',errors)
    for removed in ('core.css','responsive.css','design-system.css','pct-frame.css','pct-controls-v2-6-1-4.css','pct-home-v2-6-1-4.css','app-v2-6-1-4.js.js'):
        check(not (ROOT/'assets'/removed).exists(),f'Ersetzte Datei noch vorhanden: {removed}',errors)
    check(len(list((ROOT/'assets').glob('*.css')))==1,'Mehr als ein CSS-Bestand vorhanden.',errors)
    check((ROOT/SHARED_CSS).is_file() and (ROOT/SHARED_JS).is_file(),'Zentrale CSS-/JS-Datei fehlt.',errors)

    css=(ROOT/SHARED_CSS).read_text();js=(ROOT/SHARED_JS).read_text()
    check(css.count('!important')<=5,f'Zu viele !important: {css.count("!important")}',errors)
    for token in ('--sk-touch-min:44px','--sk-header-size:76px','--sk-footer-size:38px','viewport','Finale Kaskaden-Normalisierung'):
        check(token in css,f'Zentrale CSS-Regel fehlt: {token}',errors)
    for token in ('SK_PCT_SHARED','buildSharedLayout','data-sk-shared-header','data-sk-shared-footer','skPctToolsFavoritesV2','search-index-v2-6-1-4.json','v2-6-1-4-nav-home.png'):
        check(token in js,f'Zentrale Laufzeit unvollständig: {token}',errors)
    check('Object.keys(localStorage).find' not in js,'Veraltete Favoriten-Key-Migration noch vorhanden.',errors)

    nav_dir=ROOT/'assets/navigation-icons';icons=sorted(nav_dir.glob('*.png'))
    check({p.name for p in icons}==NAV_ICONS,f'Navigationsicon-Bestand abweichend: {[p.name for p in icons]}',errors)
    for icon in icons:
        raw=icon.read_bytes();check(raw[:8]==b'\x89PNG\r\n\x1a\n',f'PNG-Signatur fehlt: {icon.name}',errors)
        if len(raw)>=26:
            width,height=struct.unpack('>II',raw[16:24]);check((width,height)==(512,512),f'Icon-Größe falsch: {icon.name}',errors)
        with Image.open(icon) as image:
            rgba=image.convert('RGBA');pixels=list(rgba.get_flattened_data());check(rgba.getchannel('A').getextrema()==(0,255),f'Transparenz fehlerhaft: {icon.name}',errors)
            colored=sum(1 for r,g,b,a in pixels if a and not (r==g==b));black=sum(1 for r,g,b,a in pixels if a>240 and r<18 and g<18 and b<18);white=sum(1 for r,g,b,a in pixels if a>240 and r>245 and g>245 and b>245)
            check(colored>60000 and black>12000 and 20000<=white<=55000,f'Verlauf/Kontur/Symbolmasse fehlerhaft: {icon.name}',errors)
            perimeter=bytearray()
            for i,pixel in enumerate(pixels):
                x=i%512;y=i//512
                if x<80 or x>=432 or y<72 or y>=420:perimeter.extend(pixel)
            check(hashlib.sha256(perimeter).hexdigest()==BACKGROUND_PERIMETER_SHA256,f'Hintergrundmaster verändert: {icon.name}',errors)
            check(rgba.getpixel((60,256))[1]>rgba.getpixel((60,256))[2],f'Grünseite fehlt: {icon.name}',errors)
            check(rgba.getpixel((400,90))[2]>rgba.getpixel((400,90))[1],f'Blauseite fehlt: {icon.name}',errors)

    knowledge=(ROOT/'wissensdatenbank/index.html').read_text()
    check(knowledge.count(f'{VERSION_SLUG}-app-database.png')==5,'Wissensbeiträge verwenden nicht den gemeinsamen Buch-Master.',errors)
    for slug in KNOWLEDGE_ARTICLES:
        article=(ROOT/'wissensdatenbank'/slug/'index.html').read_text()
        check('knowledge-compact.js' in article and EXPERIENCE_SOURCE in article,f'Wissensbeitrag unvollständig: {slug}',errors)

    worker=(ROOT/'service-worker.js').read_text()
    check("CACHE_EPOCH='v2-6-1-4-core-r1'" in worker,'Cache-Epoch falsch.',errors)
    check('DOCUMENT_CACHE' not in worker and 'OPTIONAL_DOCUMENTS' not in worker,'Nicht benötigter Dokumentcache noch vorhanden.',errors)
    cached=re.findall(r"'\./([^']+)'",worker)
    for ref in cached:check(target_exists(ROOT/'index.html',ref),f'Offline-Ziel fehlt: {ref}',errors)
    for icon in NAV_ICONS:check(f"'./assets/navigation-icons/{icon}'" in worker,f'Icon fehlt im Offline-Cache: {icon}',errors)
    for stale in ('core.css','design-system.css','pct-frame.css','knowledge-cartoon.css','ICON-DESIGNRICHTLINIE.txt'):
        check(stale not in worker,f'Unnötiger Cache-Eintrag: {stale}',errors)

    generator=(ROOT/'tools/generate_png_icons.py').read_text()
    for token in ('PREFIX = "v2-6-1-4-"','save("app-calculator", calculator())','save("app-database", book())','save("app-eh-viewer", globe())'):
        check(token in generator,f'Icon-Generator unvollständig: {token}',errors)
    for required in ('README.txt','RELEASE-NOTES.txt','ICON-DESIGNRICHTLINIE.txt','WISSENSBEITRAGS-STANDARD.md','TESTPLAN.md','TEST-RESULTS.txt','SECURITY-DEPLOYMENT.md','UEBERGABE-V2.6.1.4-Beta.txt'):
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
    print(f'PASS · {files} Dateien · 10 Apps · 6 Rechner · 14 interne Unterseiten · 10 Navigationsicons · {css.count("!important")} !important · Version {VERSION}')
    return 0

if __name__=='__main__':sys.exit(main())
