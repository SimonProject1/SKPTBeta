#!/usr/bin/env python3
"""Struktur-, Inhalt- und Integritätsprüfung für SK PCT Tools 2.5.2.1-Beta."""
from __future__ import annotations
import hashlib, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.5.2.1-Beta'
FOOTER=f'SK PCT Tools · Entwickelt von Simon Kiesler · V{VERSION}'
APPS={'analogsignal','pf-rechner','pt-rechner','messstellen-doku','einheitenrechner','einheitendatenbank','werkstoffdatenbank','wissensdatenbank','spannungsfall-rechner','siemens-rohwert','eh-device-viewer'}
CALCULATORS={'analogsignal','pf-rechner','pt-rechner','einheitenrechner','spannungsfall-rechner','siemens-analogwert-rechner'}
KNOWLEDGE_ARTICLES={'air-torque-antrieb-drehrichtung','endress-hauser-promass-einbaulage','siemens-sitrans-p320-sil-verriegelung','siemens-sps-rohwert','vacon-frequenzumrichter-ist-sollwert-abweichung'}

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.refs=[]; self.apps=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); classes=set(a.get('class','').split())
        if tag=='a' and 'sk-home-app' in classes:self.apps.append(a)
        if tag in {'a','img','script','link'}:
            value=a.get('href' if tag in {'a','link'} else 'src')
            if value and not urlsplit(value).scheme and not value.startswith(('#','mailto:','tel:')):self.refs.append(value)

def target_exists(source:Path,ref:str)->bool:
    target=(source.parent/urlsplit(ref).path).resolve()
    try: target.relative_to(ROOT)
    except ValueError:return False
    return target.is_file() or (target.is_dir() and (target/'index.html').is_file())

def check(condition:bool,message:str,errors:list[str]):
    if not condition:errors.append(message)

def main()->int:
    errors=[]
    check((ROOT/'VERSION').read_text().strip()==VERSION,'VERSION stimmt nicht.',errors)
    manifest=json.loads((ROOT/'manifest.webmanifest').read_text())
    check(manifest.get('version')==VERSION,'Manifest-Version stimmt nicht.',errors)
    check(VERSION in manifest.get('description',''),'Manifest-Beschreibung enthält die Version nicht.',errors)

    html_pages=sorted(ROOT.rglob('*.html'))
    check(len(html_pages)==17,f'Unerwartete HTML-Anzahl: {len(html_pages)} statt 17.',errors)
    for page in html_pages:
        rel=page.relative_to(ROOT); text=page.read_text(encoding='utf-8'); parser=Parser(); parser.feed(text)
        check('viewport-fit=cover' in text,f'viewport-fit fehlt: {rel}',errors)
        check('design-system.css' in text,f'Zentrales Design-System fehlt: {rel}',errors)
        check(VERSION in text,f'Version fehlt: {rel}',errors)
        for ref in parser.refs:
            check(target_exists(page,ref),f'Lokales Ziel fehlt in {rel}: {ref}',errors)

    start=(ROOT/'index.html').read_text(); p=Parser(); p.feed(start)
    ids=[app.get('data-app-id') for app in p.apps]
    check(len(ids)==11 and set(ids)==APPS and len(ids)==len(set(ids)),f'App-Inventar fehlerhaft: {ids}',errors)
    e=[app for app in p.apps if app.get('data-app-id')=='eh-device-viewer']
    check(len(e)==1,'E+H Viewer fehlt oder ist doppelt.',errors)
    if e:
        app=e[0]
        check(app.get('href')=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H Device-Viewer-Ziel ist falsch.',errors)
        check(app.get('target')=='_blank' and {'external','noopener','noreferrer'}<=set(app.get('rel','').split()),'Externe E+H-Kennzeichnung/Absicherung fehlt.',errors)
        check(app.get('data-external')=='true','E+H Dienst ist nicht als extern markiert.',errors)
    check('Externer Onlinedienst ↗' in start,'Sichtbare externe Kennzeichnung fehlt.',errors)
    check(FOOTER in start,'Startseitenfooter ist nicht vereinheitlicht.',errors)
    check('class="pct-home-version"' in start,'Startseite nutzt nicht den gemeinsamen Versionskopf.',errors)

    framed=[]
    for page in html_pages:
        text=page.read_text(encoding='utf-8')
        if 'data-sk-layout="framed"' in text and 'data-sk-page="redirect"' not in text:framed.append(page)
    check(len(framed)==15,f'Gerahmte Unterseiten: {len(framed)} statt 15.',errors)
    for page in framed:
        rel=page.relative_to(ROOT); text=page.read_text(encoding='utf-8')
        for token in ('sk-global-header','sk-header-inner','sk-logo-version-stack','sk-header-home','sk-app-scroll','sk-footer'):
            check(text.count(token)>=1,f'Gemeinsame Komponente {token} fehlt: {rel}',errors)
        check(text.count('sk-header-version')==1,f'Gemeinsame Versionsanzeige fehlt oder ist doppelt: {rel}',errors)
        check('class="brand"' not in text,f'Alter abweichender Headertext noch vorhanden: {rel}',errors)
        check(text.count('sk-global-header')==1,f'Header nicht eindeutig: {rel}',errors)
        check(text.count('sk-footer')==1,f'Footer nicht eindeutig: {rel}',errors)
        check(FOOTER in text,f'Footertext nicht einheitlich: {rel}',errors)

    design=(ROOT/'assets/design-system.css').read_text()
    for token in ('--sk-touch-min:44px','--sk-header-size:76px','--sk-footer-size:38px','--sk-content-max:1060px','@media(max-width:430px)','grid-template-columns:repeat(3','unit-favorites-panel','unit-row-details','material-compare-table td::before','kb-short-answer','kb-source-bundle'):
        check(token in design,f'Design-System-Regel fehlt: {token}',errors)
    for token in ('verbindlicher Header-/Footer-Standard','border:0!important;','box-shadow:none!important;','body.sk-documentation-page #note','--sk-shared-content-width:1060px'):
        check(token in design,f'Layout-Korrektur fehlt: {token}',errors)
    important=sum(path.read_text().count('!important') for path in (ROOT/'assets').glob('*.css'))
    check(important<=900,f'Zu viele !important-Deklarationen nach Layout-Konsolidierung: {important}',errors)

    units=(ROOT/'assets/unit-database-page.js').read_text(); unit_system=(ROOT/'assets/unit-system.js').read_text(); unit_html=(ROOT/'einheitendatenbank/index.html').read_text()
    for token in ('unitFavoritesPanel','unitFavoritesList','unitFavoriteCount'):check(token in unit_html,f'Favoritenbereich fehlt: {token}',errors)
    for token in ("document.createElement('details')",'card.open=categoryUnits>0','renderFavorites','unit-row-details'):check(token in units,f'Kompakte Einheitendatenbank unvollständig: {token}',errors)
    check('node.textContent=item.symbol' in unit_system,'Einheitenauswahl zeigt nicht nur das Kurzsymbol.',errors)
    check('syncSelectMeta' in unit_system,'Vollständige Einheitenbezeichnung für Label/ARIA fehlt.',errors)

    materials_js=(ROOT/'assets/materials.js').read_text()
    check('leftCell.dataset.label' in materials_js and 'rightCell.dataset.label' in materials_js,'Mobile Werkstoff-Schlüssel fehlen.',errors)

    for slug in KNOWLEDGE_ARTICLES:
        page=ROOT/'wissensdatenbank'/slug/'index.html'; text=page.read_text()
        check('knowledge-compact.js' in text,f'Wissensverdichtung fehlt: {slug}',errors)
        check('kb-source' in text,f'Quellen-/Gültigkeitshinweis fehlt: {slug}',errors)
    compact=(ROOT/'assets/knowledge-compact.js').read_text()
    for token in ('kb-short-answer','kb-detail-group','kb-visible-safety','kb-source-bundle'):
        check(token in compact,f'Wissensverdichtung unvollständig: {token}',errors)

    for slug in CALCULATORS:
        page=ROOT/slug/'index.html'; text=page.read_text()
        check('sk-calculator-page' in text,f'Rechnerklasse fehlt: {slug}',errors)
        check('design-system.css' in text,f'Rechner nutzt Design-System nicht: {slug}',errors)
    check('minimumFractionDigits:0' in (ROOT/'assets/app.js').read_text(),'Einheitliches praxisgerechtes Zahlenformat fehlt.',errors)

    worker=(ROOT/'service-worker.js').read_text()
    for token in ("'./assets/design-system.css'","'./assets/knowledge-compact.js'","'./einheitendatenbank/'","'./werkstoffdatenbank/'","'./wissensdatenbank/endress-hauser-promass-einbaulage/'"):
        check(token in worker,f'Offline-Kerncache unvollständig: {token}',errors)
    cached=re.findall(r"'\./([^']+)'",worker)
    for ref in cached:check(target_exists(ROOT/'index.html',ref),f'Offline-Ziel fehlt: {ref}',errors)

    # SHA256SUMS is checked after it has been regenerated for the final package.
    sums=ROOT/'SHA256SUMS.txt'
    if sums.exists() and VERSION in (ROOT/'README.txt').read_text():
        for line in sums.read_text().splitlines():
            m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            check(bool(m),f'Ungültige Prüfsummenzeile: {line}',errors)
            if not m:continue
            expected,rel=m.groups(); path=ROOT/rel.removeprefix('./')
            check(path.is_file(),f'Prüfsummendatei fehlt: {rel}',errors)
            if path.is_file():check(hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Prüfsumme falsch: {rel}',errors)

    if errors:
        print('FAIL'); [print(f'- {e}') for e in errors]; return 1
    print(f'PASS · 11 Apps · 6 Rechner · 15 interne Unterseiten · 5 Wissensbeiträge · {important} !important · Version {VERSION}')
    return 0
if __name__=='__main__':sys.exit(main())
