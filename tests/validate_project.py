#!/usr/bin/env python3
"""Struktur-, Inhalt- und Integritätsprüfung für SK PCT Tools 2.6.0.2-Beta."""
from __future__ import annotations
import hashlib, json, re, struct, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.6.0.2-Beta'
FOOTER=f'SK PCT Tools · Entwickelt von Simon Kiesler · V{VERSION}'
APPS={'analogsignal','pf-rechner','pt-rechner','einheitenrechner','einheitendatenbank','werkstoffdatenbank','wissensdatenbank','spannungsfall-rechner','siemens-rohwert','eh-device-viewer'}
CALCULATORS={'analogsignal','pf-rechner','pt-rechner','einheitenrechner','spannungsfall-rechner','siemens-analogwert-rechner'}
CALCULATOR_ICON_FILES={
    'app-analogsignal.png','app-pf-rechner.png','app-pt-rechner.png',
    'app-einheitenrechner.png','app-spannungsfall.png','app-siemens-rohwert.png'
}
LEGACY_OVERSIZED_CALCULATOR_SHA256='9e019b856ce2bad92c027830efdb10a23483cae0b91f782090e5d9c4649720df'
KNOWLEDGE_ARTICLES={'air-torque-antrieb-drehrichtung','endress-hauser-promass-einbaulage','siemens-sitrans-p320-sil-verriegelung','siemens-sps-rohwert','vacon-frequenzumrichter-ist-sollwert-abweichung'}
EXPERIENCE_SOURCE='Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)'

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.apps=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs); classes=set(a.get('class','').split())
        if tag=='h1': self.h1+=1
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
    check(len(html_pages)==16,f'Unerwartete HTML-Anzahl: {len(html_pages)} statt 16.',errors)
    for page in html_pages:
        rel=page.relative_to(ROOT); text=page.read_text(encoding='utf-8'); parser=Parser(); parser.feed(text)
        check('viewport-fit=cover' in text,f'viewport-fit fehlt: {rel}',errors)
        check('design-system.css' in text,f'Zentrales Design-System fehlt: {rel}',errors)
        check(VERSION in text,f'Version fehlt: {rel}',errors)
        check(parser.h1==1,f'Genau eine H1 erwartet, gefunden {parser.h1}: {rel}',errors)
        check('name="referrer"' in text and 'content="no-referrer"' in text,f'Referrer-Schutz fehlt: {rel}',errors)
        for ref in parser.refs: check(target_exists(page,ref),f'Lokales Ziel fehlt in {rel}: {ref}',errors)

    start=(ROOT/'index.html').read_text(); p=Parser(); p.feed(start)
    ids=[app.get('data-app-id') for app in p.apps]
    check(len(ids)==10 and set(ids)==APPS and len(ids)==len(set(ids)),f'App-Inventar fehlerhaft: {ids}',errors)
    check('messstellen-doku' not in start.lower(),'Messstellen-App ist noch auf der Startseite.',errors)
    check('10 Apps angezeigt' in start,'Startseiten-Zähler ist nicht auf 10 Apps aktualisiert.',errors)
    e=[app for app in p.apps if app.get('data-app-id')=='eh-device-viewer']
    check(len(e)==1,'E+H Viewer fehlt oder ist doppelt.',errors)
    if e:
        app=e[0]
        check(app.get('href')=='https://www.de.endress.com/de/onlinetools/device-viewer','E+H Device-Viewer-Ziel ist falsch.',errors)
        check(app.get('target')=='_blank' and {'external','noopener','noreferrer'}<=set(app.get('rel','').split()),'Externe E+H-Kennzeichnung/Absicherung fehlt.',errors)
        check(app.get('data-external')=='true','E+H Dienst ist nicht als extern markiert.',errors)
    check(FOOTER in start,'Startseitenfooter ist nicht vereinheitlicht.',errors)
    nav_dir=ROOT/'assets/navigation-icons'; nav_icons=sorted(nav_dir.glob('*.png'))
    check(len(nav_icons)==17,f'PNG-Navigationsgrafiken: {len(nav_icons)} statt 17.',errors)
    check(not list(nav_dir.glob('*.svg')),'SVG-Navigationsgrafiken sind noch vorhanden.',errors)
    check(start.count('class="sk-nav-graphic"')==10,'Startseite verwendet nicht für alle 10 Ziele eigenständige Grafiken.',errors)
    check('pct-home-icons.svg' not in start and not (ROOT/'assets/pct-home-icons.svg').exists(),'Altes Startseiten-Icon-Sprite ist noch aktiv.',errors)
    for icon in nav_icons:
        raw=icon.read_bytes()
        check(raw[:8]==b'\x89PNG\r\n\x1a\n',f'PNG-Signatur fehlt: {icon.name}',errors)
        if len(raw)>=26 and raw[:8]==b'\x89PNG\r\n\x1a\n':
            width,height=struct.unpack('>II',raw[16:24]); color_type=raw[25]
            check((width,height)==(512,512),f'PNG-Mastergröße falsch: {icon.name} = {width}x{height}',errors)
            check(color_type in {4,6},f'PNG besitzt keinen Alphakanal: {icon.name}',errors)
    calculator_icons=[nav_dir/name for name in sorted(CALCULATOR_ICON_FILES)]
    check(all(path.is_file() for path in calculator_icons),'Rechner-PNG-Bestand ist unvollständig.',errors)
    calculator_hashes={hashlib.sha256(path.read_bytes()).hexdigest() for path in calculator_icons if path.is_file()}
    check(len(calculator_hashes)==1,'Rechner-PNGs sind nicht einheitlich erzeugt.',errors)
    check(LEGACY_OVERSIZED_CALCULATOR_SHA256 not in calculator_hashes,'Veraltetes übergroßes Taschenrechner-PNG ist noch aktiv.',errors)
    for icon in calculator_icons:
        if not icon.is_file():continue
        with Image.open(icon) as image:
            alpha=image.convert('RGBA').getchannel('A')
            bbox=alpha.getbbox()
            check(bbox is not None,f'Rechner-PNG ist vollständig transparent: {icon.name}',errors)
            if bbox:
                left,top,right,bottom=bbox
                check(left>=96 and top>=48 and right<=416 and bottom<=458,
                      f'Rechner-Innenmotiv verlässt die definierte Safe-Zone: {icon.name} = {bbox}',errors)
    guideline=(ROOT/'ICON-DESIGNRICHTLINIE.txt')
    check(guideline.is_file(),'ICON-DESIGNRICHTLINIE.txt fehlt.',errors)
    if guideline.is_file():
        guide=guideline.read_text(encoding='utf-8')
        for token in ('DATEIFORMAT UND TECHNISCHE MASTERGRÖSSE','VERBINDLICHE MOTIVKLASSEN','BEREICHSFELD','GEMEINSAMER APP-RAHMEN UND RECHNER-SAFE-ZONE','FORM UND LESBARKEIT','SCHWARZE COMIC-KONTUREN','FARBPALETTE','LICHTWIRKUNG','BENENNUNG UND ABLAGE','EINBINDUNG','ZUSTÄNDE UND BEDIENUNG','ABNAHME VOR EINBAU','CSA','EQP','PIPING'):
            check(token in guide,f'Icon-Richtlinie unvollständig: {token}',errors)

    framed=[]
    for page in html_pages:
        text=page.read_text(encoding='utf-8')
        if 'data-sk-layout="framed"' in text and 'data-sk-page="redirect"' not in text:framed.append(page)
    check(len(framed)==14,f'Gerahmte Unterseiten: {len(framed)} statt 14.',errors)
    for page in framed:
        rel=page.relative_to(ROOT); text=page.read_text(encoding='utf-8')
        for token in ('sk-global-header','sk-header-inner','sk-logo-version-stack','sk-header-home','sk-app-scroll','sk-footer'):
            check(text.count(token)>=1,f'Gemeinsame Komponente {token} fehlt: {rel}',errors)
        check(text.count('sk-header-version')==1,f'Versionsanzeige fehlt oder ist doppelt: {rel}',errors)
        check(text.count('sk-global-header')==1,f'Header nicht eindeutig: {rel}',errors)
        check(text.count('sk-footer')==1,f'Footer nicht eindeutig: {rel}',errors)
        check(FOOTER in text,f'Footertext nicht einheitlich: {rel}',errors)

    check(not (ROOT/'messstellen-doku').exists(),'Ordner messstellen-doku ist noch vorhanden.',errors)
    check(not list(ROOT.rglob('*.pdf')),'PDF-Dateien sind noch im Projekt vorhanden.',errors)
    knowledge_home=(ROOT/'wissensdatenbank/index.html').read_text()
    check('Beitrag vorschlagen' not in knowledge_home and 'Beitragsvorlage.pdf' not in knowledge_home,'PDF-Vorlagenaktion ist noch vorhanden.',errors)
    check(knowledge_home.count('class="knowledge-brand-logo"')==10,'Wissensnavigation besitzt nicht 10 PNG-Grafiken.',errors)
    check(knowledge_home.count('manufacturer-')>=5,'Hersteller-Hub verwendet die weißen Kurzmarken nicht vollständig.',errors)
    check(knowledge_home.count('app-wissensdatenbank.png')==5,'Wissensbeiträge verwenden nicht vollständig Buch/PCT.',errors)
    check('knowledge-icon-badge' not in knowledge_home,'Alte Geräte-/Beitragsfelder überlagern das Bereichsfeld.',errors)
    check('knowledge-manufacturer-logos.svg' not in knowledge_home and not (ROOT/'assets/knowledge-manufacturer-logos.svg').exists(),'Altes Hersteller-Icon-Sprite ist noch aktiv.',errors)

    overlay_sources='\n'.join(path.read_text(encoding='utf-8') for suffix in ('*.html','*.css','*.js') for path in ROOT.rglob(suffix))
    for token in ('.sk-home-icon::after','.knowledge-home-icon::after','.knowledge-icon-badge','data-icon-area','data-discipline-overlay'):
        check(token not in overlay_sources,f'Doppeltes Fachbereichs-Overlay noch vorhanden: {token}',errors)
    check(not re.search(r'content\s*:\s*[\"\'](?:PCT|PIPING|CSA|EQP)(?:\s*↗)?[\"\']', (ROOT/'assets/pct-home.css').read_text(), re.I),'CSS erzeugt noch ein Fachbereichsfeld auf Startseiten-/WWW-Icons.',errors)

    design=(ROOT/'assets/design-system.css').read_text(); core=(ROOT/'assets/core.css').read_text(); controls=(ROOT/'assets/pct-controls.css').read_text(); siemens_css=(ROOT/'assets/siemens-analogwert-rechner.css').read_text()
    for token in ('--sk-touch-min:44px','--sk-header-size:76px','--sk-footer-size:38px','--sk-content-max:1060px','@media(max-width:430px)','grid-template-columns:repeat(3','unit-favorites-panel','unit-row-details','material-compare-table td::before','kb-short-answer','kb-source-bundle'):
        check(token in design,f'Design-System-Regel fehlt: {token}',errors)
    check('[hidden]{display:none!important}' in core,'Zentrale hidden-Regel fehlt.',errors)
    check('sk-documentation-page' not in design,'Veraltete Messstellen-CSS-Regeln sind noch vorhanden.',errors)
    for token in ('verbindlicher Plus/Minus-Standard','width:44px!important','height:44px!important','touch-action:manipulation!important',':is(.number,.analog-input-shell,.analog-range-input-shell)'):
        check(token in controls,f'Zentraler Vorzeichenstandard unvollständig: {token}',errors)
    check('ruhiger Vorzeichen-Taster' not in siemens_css,'Siemens besitzt noch einen lokalen statt zentralen Vorzeichenstandard.',errors)
    important=sum(path.read_text().count('!important') for path in (ROOT/'assets').glob('*.css'))
    check(important<=900,f'Zu viele !important-Deklarationen: {important} statt höchstens 900.',errors)

    units=(ROOT/'assets/unit-database-page.js').read_text(); unit_system=(ROOT/'assets/unit-system.js').read_text(); unit_html=(ROOT/'einheitendatenbank/index.html').read_text()
    for token in ('unitFavoritesPanel','unitFavoritesList','unitFavoriteCount'):check(token in unit_html,f'Favoritenbereich fehlt: {token}',errors)
    for token in ("document.createElement('details')",'card.open=categoryUnits>0','renderFavorites','unit-row-details'):check(token in units,f'Kompakte Einheitendatenbank unvollständig: {token}',errors)
    check('node.textContent=item.symbol' in unit_system,'Einheitenauswahl zeigt nicht nur das Kurzsymbol.',errors)

    for slug in KNOWLEDGE_ARTICLES:
        page=ROOT/'wissensdatenbank'/slug/'index.html'; text=page.read_text()
        check('knowledge-compact.js' in text,f'Wissensverdichtung fehlt: {slug}',errors)
        check('kb-source' in text,f'Quellen-/Gültigkeitshinweis fehlt: {slug}',errors)
        check(EXPERIENCE_SOURCE in text,f'Erfahrungsberichte als Quellenart fehlen: {slug}',errors)
    standard=(ROOT/'WISSENSBEITRAGS-STANDARD.md').read_text()
    check(EXPERIENCE_SOURCE in standard,'Quellenart fehlt im Wissensbeitragsstandard.',errors)
    check('separate PDF-Beitragsvorlage ist nicht Bestandteil' in standard,'Chat-Beitragsweg ist nicht dokumentiert.',errors)

    pt=(ROOT/'assets/pt-rechner.js').read_text()
    for token in ('MIN_C=-200','MAX_C=850','minOhm','maxOhm','outOfRange'):
        check(token in pt,f'Pt-Bereichsprüfung unvollständig: {token}',errors)

    for slug in CALCULATORS:
        page=ROOT/slug/'index.html'; text=page.read_text()
        check('sk-calculator-page' in text,f'Rechnerklasse fehlt: {slug}',errors)
        check('design-system.css' in text,f'Rechner nutzt Design-System nicht: {slug}',errors)

    worker=(ROOT/'service-worker.js').read_text()
    for token in ("'./assets/design-system.css'","'./assets/knowledge-compact.js'","'./assets/navigation-icons/app-analogsignal.png'","'./assets/navigation-icons/nav-home.png'","'./einheitendatenbank/'","'./werkstoffdatenbank/'","'./wissensdatenbank/endress-hauser-promass-einbaulage/'","'./ICON-DESIGNRICHTLINIE.txt'"):
        check(token in worker,f'Offline-Kerncache unvollständig: {token}',errors)
    for icon in nav_icons:
        check(f"'./assets/navigation-icons/{icon.name}'" in worker,f'Navigationsgrafik fehlt im Offline-Cache: {icon.name}',errors)
    check('messstellen-doku' not in worker and 'Beitragsvorlage.pdf' not in worker and 'pct-home-icons.svg' not in worker and 'knowledge-manufacturer-logos.svg' not in worker,'Entfernte Inhalte/Sprites sind noch im Service Worker.',errors)
    check(".svg'" not in '\n'.join(line for line in worker.splitlines() if 'navigation-icons/' in line),'Service Worker referenziert noch SVG-Navigationsgrafiken.',errors)
    remaining_svg={str(x.relative_to(ROOT)) for x in ROOT.rglob('*.svg')}
    check(remaining_svg=={'assets/pct-controls.svg'},f'Unerwartete SVG-Dateien vorhanden: {sorted(remaining_svg)}',errors)
    check((ROOT/'tools/generate_png_icons.py').is_file(),'PNG-Icon-Generator fehlt.',errors)
    for shortcut in manifest.get('shortcuts',[]):
        for item in shortcut.get('icons',[]):
            check(item.get('type')=='image/png' and item.get('sizes')=='512x512' and item.get('src','').endswith('.png'),f'Manifest-Shortcut nicht auf PNG umgestellt: {item}',errors)
    cached=re.findall(r"'\./([^']+)'",worker)
    for ref in cached:check(target_exists(ROOT/'index.html',ref),f'Offline-Ziel fehlt: {ref}',errors)
    check((ROOT/'SECURITY-DEPLOYMENT.md').is_file(),'Deployment-Sicherheitsdokument fehlt.',errors)

    sums=ROOT/'SHA256SUMS.txt'
    if sums.exists():
        listed=[]
        for line in sums.read_text().splitlines():
            m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line)
            check(bool(m),f'Ungültige Prüfsummenzeile: {line}',errors)
            if not m:continue
            expected,rel=m.groups(); path=ROOT/rel.removeprefix('./'); listed.append(path.resolve())
            check(path.is_file(),f'Prüfsummendatei fehlt: {rel}',errors)
            if path.is_file():check(hashlib.sha256(path.read_bytes()).hexdigest()==expected,f'Prüfsumme falsch: {rel}',errors)
        expected_files={p.resolve() for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts}
        check(set(listed)==expected_files,'SHA256SUMS-Dateibestand ist unvollständig oder enthält Zusatzdateien.',errors)

    if errors:
        print('FAIL'); [print(f'- {e}') for e in errors]; return 1
    print(f'PASS · 10 Apps · 6 Rechner · 14 interne Unterseiten · 5 Wissensbeiträge · {important} !important · Version {VERSION}')
    return 0
if __name__=='__main__':sys.exit(main())
