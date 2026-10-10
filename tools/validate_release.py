#!/usr/bin/env python3
"""Statische Vollständigkeits- und Integritätsprüfung für SK PLT Tools 2.1.7.2-Beta."""
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path
from urllib.parse import urlparse

ROOT=Path(__file__).resolve().parents[1]
CONFIG=json.loads((ROOT/'release-config.json').read_text(encoding='utf-8'))
VERSION=CONFIG['version']
errors=[]
def check(condition,message):
    if not condition: errors.append(message)
def load(path): return (ROOT/path).read_text(encoding='utf-8')
def data(path): return json.loads(load(path))

def html_pages(): return sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob('index.html'))
def local_target(page,value):
    if not value or '${' in value or value.startswith(('#','data:','mailto:','tel:','javascript:')): return None
    parsed=urlparse(value)
    if parsed.scheme or parsed.netloc: return None
    clean=value.split('?',1)[0].split('#',1)[0]
    if not clean: return None
    target=(page.parent/clean).resolve()
    try: target.relative_to(ROOT.resolve())
    except ValueError: return target
    if clean.endswith('/') or target.is_dir(): target=target/'index.html'
    return target

pages=html_pages(); registry=data('shared/pages.json')
check(pages==sorted(registry),f'HTML-Seiten und shared/pages.json abweichend: {pages}')
check(len(pages)==16,f'16 HTML-Seiten erwartet, gefunden {len(pages)}')
for rel in pages:
    page=ROOT/rel; text=page.read_text(encoding='utf-8')
    check(f'data-sk-version="{VERSION}"' in text,f'{rel}: Version fehlt')
    check('sk-global-header' in text and 'sk-footer' in text and 'sk-header-home' in text,f'{rel}: gemeinsame App-Schale unvollständig')
    check('apple-mobile-web-app-status-bar-style' in text and 'black-translucent' in text,f'{rel}: iPhone-Statusleiste fehlt')
    for value in re.findall(r'\b(?:src|href)="([^"]+)"',text):
        target=local_target(page,value)
        check(target is None or target.exists(),f'{rel}: lokales Ziel fehlt: {value}')

for rel in ['analogsignal/index.html','einheitenrechner/index.html','pf-rechner/index.html','pt-rechner/index.html','siemens-analogwert-rechner/index.html','spannungsfall-rechner/index.html']:
    text=load(rel); fields=re.findall(r'<input\b[^>]*\btype="number"[^>]*>',text)
    check(fields and all(re.search(r'\binputmode="(?:decimal|numeric)"',field) for field in fields),f'{rel}: mobile Zahlentastatur unvollständig')
    check('unit-system.js' in text,f'{rel}: zentrale Einheitendatenbank nicht eingebunden')
    check(text.count('class="sk-unit-database-cta"')==1,f'{rel}: genau ein Datenbank-Sprung erwartet')
    check('class="sk-unit-database-button" href="../einheitendatenbank/"' in text,f'{rel}: Datenbank-Sprung fehlt oder hat falsches Ziel')
    check(text.rfind('sk-unit-database-cta') < text.rfind('</main>'),f'{rel}: Datenbank-Sprung muss am Ende des Hauptinhalts liegen')

units=data('assets/units.json')
check(units.get('release')==VERSION,'assets/units.json: Release inkonsistent')
check(len(units.get('categories',[]))==19,'Einheitendatenbank: 19 Kategorien erwartet')
check(sum(len(entry.get('units',[])) for entry in units.get('categories',[]))==115,'Einheitendatenbank: 115 Einheiten erwartet')
category_ids=set(); unit_keys=set()
for category in units.get('categories',[]):
    check(category['id'] not in category_ids,f'Doppelte Kategorie: {category["id"]}'); category_ids.add(category['id'])
    ids={item['id'] for item in category['units']}; check(category['defaultUnit'] in ids,f'{category["id"]}: Standardeinheit fehlt')
    for unit in category['units']:
        key=(category['id'],unit['id']); check(key not in unit_keys,f'Doppelte Einheit: {key}'); unit_keys.add(key)
        factor=unit.get('toBase',{}).get('factor'); offset=unit.get('toBase',{}).get('offset',0)
        check(isinstance(factor,(int,float)) and factor!=0 and isinstance(offset,(int,float)),f'Ungültige Formel: {key}')
required={'pressure':'bar','temperature':'celsius','volumeFlow':'cubic_metre_hour','length':'metre','voltage':'volt','current':'ampere','resistance':'ohm'}
actual={entry['id']:entry['defaultUnit'] for entry in units['categories']}
for key,value in required.items(): check(actual.get(key)==value,f'{key}: Grundeinheit {value} fehlt')

runtime=load('assets/unit-system.js')
for needle in ["skPltUnitFavoritesV1",'localStorage.setItem(STORAGE_KEY,',"standard.label='Standardeinheit'","favoriteGroup.label='Favoriten'","new CustomEvent('sk:unit-change'"]: check(needle in runtime,f'unit-system.js: Funktion fehlt: {needle}')
database=load('einheitendatenbank/index.html')
for needle in ['id="unitSearch"','id="unitCategoryFilter"','unit-database-page.js']: check(needle in database,f'Einheitendatenbank: {needle} fehlt')

nav=data('assets/navigation-tree.json'); check(nav.get('version')==VERSION,'Navigation: Version inkonsistent')
check(any(item.get('url')=='einheitendatenbank/' for group in nav['groups'] for item in group.get('items',[])),'Navigation: Einheitendatenbank fehlt')
search=data('assets/search-index.json'); check(any(item.get('url')=='einheitendatenbank/' for item in search),'Suchindex: Einheitendatenbank fehlt')
start=load('index.html'); check(len(re.findall(r'<a\b[^>]*class="[^"]*\bcard\b[^"]*"',start))==10,'Startseite: 10 Werkzeugkacheln erwartet'); check('href="einheitendatenbank/"' in start,'Startseite: Einheitendatenbank fehlt'); check('href="https://www.de.endress.com/de/onlinetools?store_locale=de" rel="noopener noreferrer" target="_blank"' in start,'Startseite: Endress+Hauser-Link oder Sicherheitsattribute falsch')

manifest=data('manifest.webmanifest')
check(manifest.get('version')==VERSION,'Manifest-Version inkonsistent'); check(manifest.get('id')==f'./?app=sk-plt-tools-{VERSION.lower()}','Manifest-ID inkonsistent'); check(any(item.get('url')=='./einheitendatenbank/' for item in manifest.get('shortcuts',[])),'Manifest-Shortcut Einheitendatenbank fehlt')
sw=load('service-worker.js'); check(f"const RELEASE='{VERSION}';" in sw,'Service Worker Release inkonsistent')
precache=set(re.findall(r'^\s+"(\./[^"]*)",?$',sw,re.M))
required_cache={'./','./assets/units.json','./assets/unit-system.js','./assets/unit-database.css','./assets/unit-database-page.js','./einheitendatenbank/','./einheitendatenbank/index.html'}
check(required_cache<=precache,f'PWA-Precache unvollständig: {sorted(required_cache-precache)}')
for entry in precache:
    if entry=='./': continue
    target=ROOT/entry[2:]
    if entry.endswith('/'): target=target/'index.html'
    check(target.exists(),f'Precache-Ziel fehlt: {entry}')

core=load('assets/core.css'); responsive=load('assets/responsive.css'); app=load('assets/app.js')
check('safe-area-inset-top' in responsive and 'safe-area-inset-bottom' in responsive,'iPhone Safe Areas fehlen')
check('.sk-favorites-trigger' in core and '.sk-tree-trigger' in core,'Mobile untere Bedienzone fehlt')
check('.sk-unit-database-cta' in core and '.sk-unit-database-button' in core,'Stil für Einheitendatenbank-Sprung fehlt')
check('width:fit-content' in core and 'max-width:min(100%,720px)' in core,'Einheitendatenbank-Sprung ist auf Desktop nicht kompakt begrenzt')
check('@media(min-width:761px) and (max-width:1024px)' in core and 'max-width:min(100%,640px)' in core,'Einheitendatenbank-Sprung ist auf Tablet nicht kompakt begrenzt')
check('max-width:560px' in core and 'white-space:normal' in core,'Einheitendatenbank-Sprung ist mobil nicht responsiv')
check('.sk-header-home' in core or '.sk-header-home' in responsive,'Startseiten-Button-Stil fehlt')
check('border-bottom' in core,'Headerlinie fehlt')
check("button.textContent='±'" in app,'Generischer ±-Vorzeichenwechsel fehlt')
check('toggleSignValue' in load('assets/siemens-analogwert-rechner.js'),'Siemens ±-Vorzeichenwechsel fehlt')

version_files=['VERSION','README.md','RELEASE-NOTES.txt','TESTBERICHT-UND-ABNAHME.md','PROJEKTUEBERGABE_V2.1.7.2-Beta.txt','ARCHITEKTUR-CLEAN-DESIGN.md','DEPLOYMENT.md']
for rel in version_files: check((ROOT/rel).exists(),f'Dokument fehlt: {rel}'); check(VERSION in load(rel),f'{rel}: Version fehlt')
checksum_path=ROOT/'SHA256SUMS.txt'
if checksum_path.exists():
    listed={}
    for line in checksum_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        digest,name=line.split('  ',1); listed[name.removeprefix('./')]=digest
    actual_files=sorted(path.relative_to(ROOT).as_posix() for path in ROOT.rglob('*') if path.is_file() and path!=checksum_path and '__pycache__' not in path.parts and path.name!='.DS_Store')
    check(sorted(listed)==actual_files,'Prüfsummen-Dateiliste abweichend')
    for rel,digest in listed.items():
        path=ROOT/rel
        if path.exists(): check(hashlib.sha256(path.read_bytes()).hexdigest()==digest,f'Prüfsumme falsch: {rel}')

if errors:
    print('FEHLER'); print('\n'.join(f'- {item}' for item in errors)); sys.exit(1)
print(f'OK: {VERSION}, {len(pages)} Seiten, 19 Kategorien, 115 Einheiten, Rechner-, Favoriten-, PWA- und Integritätsprüfung bestanden.')
