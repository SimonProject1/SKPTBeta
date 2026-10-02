#!/usr/bin/env python3
"""Static release validation for SK PLT Tools Beta 2.0.3.5-Beta.1."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.0.3.5-Beta.1'
EXPECTED_PAGES={
 'index.html','analogsignal/index.html','siemens-analogwert-rechner/index.html','einheitenrechner/index.html','messstellen-doku/index.html',
 'pf-rechner/index.html','pt-rechner/index.html','servicewerte/index.html',
 'spannungsfall-rechner/index.html','plausibilitaetspruefung-vde0100-600/index.html',
 'wissensdatenbank/index.html','wissensdatenbank/air-torque-antrieb-drehrichtung/index.html',
 'wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/index.html',
 'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html',
 'wissensdatenbank/werkstoff-nachschlagewerk/index.html'
}
EXPECTED_MATERIAL_IDS={'1-4301','1-4401','1-4404','1-4408','1-4409','1-4435','1-4539','1-4571','2-4602','2-4605'}
TEMPLATE_HASHES={
 'wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf':'6fb4b02aa6033a628f426c7bb9e6bf7f21f132ca191a77c1eb012d9999cb04db',
 'wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf.pdf':'65e3897a145099645fc7001aa328b81b1e86365b5613d18f559b04df43e1778d',
 'wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.docx':'95d130036ad3e2c9e5aa799ff696114bd8dadd0b9e326d66263f742d93079e98'
}
errors=[]
pages={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('index.html')}
if set(pages)!=EXPECTED_PAGES:
    errors.append(f'HTML-Seiten abweichend: erwartet {sorted(EXPECTED_PAGES)}, gefunden {sorted(pages)}')

def resolve_local(page,ref):
    clean=ref.split('#',1)[0].split('?',1)[0]
    if not clean or clean.startswith(('http://','https://','mailto:','data:','javascript:','#')): return None
    path=(page.parent/clean).resolve()
    try: path.relative_to(ROOT.resolve())
    except ValueError:
        errors.append(f'{page.relative_to(ROOT)}: Referenz verlässt Paket: {ref}');return None
    if clean.endswith('/'): path=path/'index.html'
    return path

for rel,page in pages.items():
    text=page.read_text(encoding='utf-8')
    soup=BeautifulSoup(text,'html.parser')
    if soup.body is None or soup.head is None: errors.append(f'{rel}: head/body fehlt');continue
    if soup.body.get('data-sk-version')!=VERSION: errors.append(f'{rel}: data-sk-version fehlt/falsch')
    if len(soup.select('header.sk-header-normalized'))!=1: errors.append(f'{rel}: genau ein statischer Header erwartet')
    if len(soup.select('footer.sk-footer'))!=1: errors.append(f'{rel}: genau ein statischer Footer erwartet')
    if len(soup.select('.sk-logo-version'))!=1 or soup.select_one('.sk-logo-version').get_text(strip=True)!=f'Version {VERSION}': errors.append(f'{rel}: Header-Version falsch')
    if f'Version {VERSION}' not in soup.select_one('footer.sk-footer').get_text(' ',strip=True): errors.append(f'{rel}: Footer-Version falsch')
    if 'SK PLT Tools Beta' not in soup.get_text(' ',strip=True) or len(soup.select('.sk-beta-label'))!=1: errors.append(f'{rel}: sichtbare Beta-Kennzeichnung fehlt')
    styles=[tag.get('href','') for tag in soup.find_all('link',rel=lambda value:value and 'stylesheet' in value)]
    if not any('assets/styles.css' in value for value in styles): errors.append(f'{rel}: styles.css fehlt')
    if not any('assets/design.css' in value for value in styles): errors.append(f'{rel}: design.css fehlt')
    scripts=[tag.get('src','') for tag in soup.find_all('script',src=True)]
    for required in ('app.js','favorites.js','start-filter.js','sort-tools.js','navigation-tree.js'):
        if not any(required in value for value in scripts): errors.append(f'{rel}: direkt eingebundenes Modul fehlt: {required}')
    for forbidden in ('sk-shell.js','header-alignment-fix.js','header-version-footer-fix.js','card-cleanup.js','start-vde-integration.js','start-voltage-drop-integration.js','version-1.9.8.5.js'):
        if any(forbidden in value for value in scripts): errors.append(f'{rel}: alte Patchdatei noch eingebunden: {forbidden}')
    if len(soup.select('.sk-favorites-trigger'))!=1 or len(soup.select('.sk-tree-trigger'))!=1: errors.append(f'{rel}: statische Seitentrigger fehlen')
    for tag in soup.find_all(src=True)+soup.find_all(href=True):
        ref=tag.get('src') or tag.get('href')
        target=resolve_local(page,ref)
        if target is not None and not target.exists(): errors.append(f'{rel}: fehlende lokale Referenz {ref}')

start=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
if len(start.select('.tools > a.card'))!=10: errors.append('Startseite: genau 10 sichtbare Werkzeugkacheln erwartet')
siemens_tile=start.select_one('a[href="siemens-analogwert-rechner/"]')
if not siemens_tile: errors.append('Startseite: Siemens-Rechner fehlt')
elif siemens_tile.select_one('h2') is None or siemens_tile.select_one('h2').get_text(strip=True)!='Siemens Rohwert': errors.append('Startseite: Siemens-Kachel heißt nicht exakt Siemens Rohwert')
if start.select('a[href*="servicewerte"]'): errors.append('Startseite: entfernte Service-Kachel ist noch verlinkt')
external=start.select_one('a.sk-external-card[href="https://netilion.endress.com/app/library/device_viewer"]')
if external is None: errors.append('Startseite: E+H Device Viewer fehlt oder URL ist falsch')
else:
    if external.get('target')!='_blank': errors.append('E+H Device Viewer: öffnet nicht in neuem Tab')
    rel=set(external.get('rel') or [])
    if not {'external','noopener','noreferrer'}<=rel: errors.append('E+H Device Viewer: Linkschutz/Kennzeichnung unvollständig')
    if external.get('referrerpolicy')!='no-referrer': errors.append('E+H Device Viewer: Referrer-Schutz fehlt')
    if external.select_one('form,input,textarea'): errors.append('E+H Device Viewer: SK PLT Tools darf keine Seriennummerneingabe enthalten')
    if 'nicht in SK PLT Tools gespeichert' not in external.get_text(' ',strip=True): errors.append('E+H Device Viewer: Datenschutzhinweis fehlt')
if not start.select_one('[data-filter="EXTERN"]'): errors.append('Startseite: Filter für externe Dienste fehlt')
if not start.select_one('#skToolFilter #skToolSort'): errors.append('Startseite: Filter/Sortierung nicht statisch vorhanden')

knowledge=BeautifulSoup((ROOT/'wissensdatenbank/index.html').read_text(encoding='utf-8'),'html.parser')
knowledge_tiles=knowledge.select('#knowledgeGrid > a.knowledge-entry')
expected_knowledge_hrefs={
    'werkstoff-nachschlagewerk/',
    'air-torque-antrieb-drehrichtung/',
    'siemens-sitrans-p320-sil-verriegelung/',
    'vacon-frequenzumrichter-ist-sollwert-abweichung/',
    '../siemens-analogwert-rechner/'
}
actual_knowledge_hrefs={tile.get('href') for tile in knowledge_tiles}
if actual_knowledge_hrefs!=expected_knowledge_hrefs: errors.append(f'Wissensdatenbank: Wissenskacheln abweichend: {sorted(actual_knowledge_hrefs)}')
for tile in knowledge_tiles:
    if 'tool-card' not in tile.get('class',[]): errors.append(f'Wissensdatenbank: Kachel nicht in Favoriten integriert: {tile.get("href","?")}')
if '.knowledge-entry[hidden]{display:none}' not in (ROOT/'wissensdatenbank/index.html').read_text(encoding='utf-8'): errors.append('Wissensdatenbank: hidden-Kacheln werden durch das Karten-CSS nicht zuverlässig ausgeblendet')
favorites=(ROOT/'assets/favorites.js').read_text(encoding='utf-8')
for required in ("const KEY='skPltToolsFavoritesV2'",'localStorage.getItem(KEY)','localStorage.setItem(KEY','event.preventDefault()','event.stopPropagation()','render()'):
    if required not in favorites: errors.append(f'Favoritensystem: erforderliche Persistenz-/Klicklogik fehlt: {required}')

material_page=BeautifulSoup((ROOT/'wissensdatenbank/werkstoff-nachschlagewerk/index.html').read_text(encoding='utf-8'),'html.parser')
breadcrumb=material_page.select_one('nav.knowledge-breadcrumb[aria-label="Brotkrümelnavigation"]')
if breadcrumb is None:
    errors.append('Werkstoffseite: Brotkrümelnavigation fehlt')
else:
    labels=[part.get_text(' ',strip=True) for part in breadcrumb.find_all(['a','span'])]
    if labels!=['Startseite','›','Wissensdatenbank','›','Werkstoff-Nachschlagewerk']:
        errors.append(f'Werkstoffseite: Breadcrumb-Beschriftung falsch: {labels}')
    links=[link.get('href') for link in breadcrumb.find_all('a')]
    if links!=['../../','../']:
        errors.append(f'Werkstoffseite: Breadcrumb-Linkziele falsch: {links}')
for selector in ('#materialSearch','#materialGroupFilters','#materialResults','#materialCompareSelect','#materialComparison'):
    if not material_page.select_one(selector): errors.append(f'Werkstoffseite: Element fehlt: {selector}')
for asset in ('materials.css','materials.js'):
    if asset not in (ROOT/'wissensdatenbank/werkstoff-nachschlagewerk/index.html').read_text(encoding='utf-8'): errors.append(f'Werkstoffseite: {asset} fehlt')

try:
    materials=json.loads((ROOT/'assets/materials.json').read_text(encoding='utf-8'))
except Exception as exc:
    errors.append(f'materials.json ungültig: {exc}');materials={}
items=materials.get('materials',[])
ids={item.get('id') for item in items}
if ids!=EXPECTED_MATERIAL_IDS: errors.append(f'Werkstoff-IDs abweichend: {sorted(ids)}')
if len(items)!=10: errors.append(f'Genau 10 Werkstoffdatensätze erwartet, gefunden {len(items)}')
groups={group.get('id') for group in materials.get('groups',[])}
required_fields=('materialNumber','shortName','group','productForm','explanation','searchTerms','related','doNotConfuseWith','sources')
for item in items:
    for field in required_fields:
        if not item.get(field): errors.append(f'{item.get("id","?")}: Pflichtfeld fehlt/leer: {field}')
    if item.get('group') not in groups: errors.append(f'{item.get("id","?")}: unbekannte Werkstoffgruppe')
    if not all(source.get('url','').startswith('https://') for source in item.get('sources',[])): errors.append(f'{item.get("id","?")}: Quelle ohne HTTPS')
notice=materials.get('safetyNotice','')
for phrase in ('keine automatische Werkstofffreigabe','keine pauschale Medienbeständigkeitsbewertung'):
    if phrase.lower() not in notice.lower(): errors.append(f'Sicherheitshinweis unvollständig: {phrase}')

def norm(value):
    import unicodedata
    value=unicodedata.normalize('NFD',str(value or '').lower()).replace('ß','ss')
    return re.sub(r'[^a-z0-9]+','', ''.join(ch for ch in value if unicodedata.category(ch)!='Mn'))
def matches(item,query):
    hay=' '.join(norm(value) for value in [item.get('materialNumber'),item.get('shortName'),item.get('uns'),*item.get('internationalDesignations',[]),*item.get('searchTerms',[])])
    return all(norm(term) in hay for term in str(query).split() if norm(term))
if {item['id'] for item in items if matches(item,'316L')}!={'1-4404','1-4409','1-4435'}: errors.append('Werkstoffsuche: 316L liefert nicht die drei erwarteten Zuordnungen')
if {item['id'] for item in items if matches(item,'14404')}!={'1-4404'}: errors.append('Werkstoffsuche: 14404 ist nicht eindeutig 1.4404')
if {item['id'] for item in items if item.get('group')=='cast-stainless' and matches(item,'316L')}!={'1-4409'}: errors.append('Werkstoffsuche: 316L mit Stahlgussfilter ist nicht 1.4409')
comparison_ids={item.get('id') for item in materials.get('comparisons',[])}
if not {'316-vs-316l','14404-vs-14408'}<=comparison_ids: errors.append('Pflichtvergleiche fehlen')

search_index=json.loads((ROOT/'assets/search-index.json').read_text(encoding='utf-8'))
if not any(item.get('url')=='wissensdatenbank/werkstoff-nachschlagewerk/' and item.get('passthroughQuery') and item.get('catalog')=='materials' for item in search_index): errors.append('Startseitensuche: zentral angebundener Werkstoffbereich mit Suchübergabe fehlt')
if not any(item.get('manufacturer')=='Siemens' and item.get('device')=='SPS' and item.get('topic')=='Rohwert' and item.get('url')=='siemens-analogwert-rechner/' for item in search_index): errors.append('Suche: Wissenseintrag Siemens / SPS / Rohwert fehlt')
if 'assets/materials.json' not in (ROOT/'assets/start-filter.js').read_text(encoding='utf-8'): errors.append('Startseitensuche: zentrale Werkstoffdatei wird nicht geladen')
nav=json.loads((ROOT/'assets/navigation-tree.json').read_text(encoding='utf-8'))
if 'wissensdatenbank/werkstoff-nachschlagewerk/' not in json.dumps(nav): errors.append('Navigationsbaum: Werkstoffbereich fehlt')
if 'siemens-analogwert-rechner/' not in json.dumps(nav): errors.append('Navigationsbaum: Siemens-SPS-Analogwert-Rechner fehlt')
if not any(grandchild.get('title')=='SPS – Rohwert' and grandchild.get('url')=='siemens-analogwert-rechner/' for group in nav.get('groups',[]) for item in group.get('items',[]) for child in item.get('children',[]) for grandchild in child.get('children',[]) if item.get('title')=='Wissensdatenbank' and child.get('title')=='Siemens'): errors.append('Navigationsbaum: Wissenseintrag Siemens / SPS / Rohwert fehlt')
if not any(group.get('id')=='external-services' and any(item.get('url')=='https://netilion.endress.com/app/library/device_viewer' and item.get('type')=='external' for item in group.get('items',[])) for group in nav.get('groups',[])): errors.append('Navigationsbaum: E+H Device Viewer fehlt oder ist nicht extern gekennzeichnet')
if 'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/' not in json.dumps(nav): errors.append('Navigationsbaum: Vacon-Wissensbeitrag fehlt')
if not any(item.get('url')=='wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/' and item.get('manufacturer')=='Vacon' and '2.2.3.7' in ' '.join(item.get('keywords',[])) for item in search_index): errors.append('Startseitensuche: Vacon-Wissensbeitrag oder Parameter 2.2.3.7 fehlt')
vacon_page=(ROOT/'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html').read_text(encoding='utf-8')
for required in ('Vacon','Frequenzumrichter','Ist-/Sollwert-Abweichung im PLS','2.2.3.7','maximale Frequenz','vacon-wissen.css'):
    if required not in vacon_page: errors.append(f'Vacon-Wissensbeitrag: Inhalt/Integration fehlt: {required}')

sw=(ROOT/'service-worker.js').read_text(encoding='utf-8')
for forbidden in ('enhanceHtml','enhanceJs','.replace(\'</head>\'','.replace(\'</body>\''):
    if forbidden in sw: errors.append(f'Service Worker enthält verbotene Laufzeit-Patchlogik: {forbidden}')
if f"const RELEASE='{VERSION}'" not in sw: errors.append('Service Worker verwendet falsche Version')
if "const CACHE_PREFIX='sk-plt-tools-beta-'" not in sw or 'const CACHE=`${CACHE_PREFIX}v${RELEASE}`' not in sw: errors.append('Service Worker verwendet nicht den getrennten Beta-Cache')
if 'key.startsWith(CACHE_PREFIX)&&key!==CACHE' not in sw: errors.append('Service Worker bereinigt Caches nicht beta-isoliert')
for required in ('./assets/siemens-analogwert-rechner.css','./assets/siemens-analogwert-rechner.js','./siemens-analogwert-rechner/index.html','./assets/materials.json','./assets/materials.js','./assets/materials.css','./wissensdatenbank/werkstoff-nachschlagewerk/index.html','./assets/vacon-wissen.css','./wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html'):
    if required not in sw: errors.append(f'Service Worker: Precache-Eintrag fehlt: {required}')


manifest=json.loads((ROOT/'manifest.webmanifest').read_text(encoding='utf-8'))
if manifest.get('name')!='SK PLT Tools Beta' or manifest.get('short_name')!='SK PLT Beta': errors.append('Manifest: eigener Beta-App-Name fehlt')
if manifest.get('id')!='./?app=sk-plt-tools-beta-2.0.3.5-beta.1' or manifest.get('start_url')!='./?app=sk-plt-tools-beta-2.0.3.5-beta.1': errors.append('Manifest: Beta-ID/start_url nicht eindeutig')
siemens_html=(ROOT/'siemens-analogwert-rechner/index.html').read_text(encoding='utf-8')
siemens_page=BeautifulSoup(siemens_html,'html.parser')
for selector in ('#cardProfile','#signalType','#inputKind','#inputValue','#inputValueLabel','#inputSuffix','#valueSlider','#sliderLabel','#sliderScale','#rawResult','#signalResult','#percentResult','#rangeStatus','#statusDetail','#calculationError'):
    if not siemens_page.select_one(selector): errors.append(f'Siemens-Rechner: Element fehlt: {selector}')
if siemens_page.select_one('h1') is None or siemens_page.select_one('h1').get_text(strip=True)!='Siemens Rohwert': errors.append('Siemens-Rechner: große Seitenüberschrift heißt nicht exakt Siemens Rohwert')
for state in ('underflow','underrange','nominal','overrange','overflow'):
    if not siemens_page.select_one(f'[data-state-key="{state}"]'): errors.append(f'Siemens-Rechner: Statusanzeige fehlt: {state}')
for forbidden in ('physicalMin','physicalMax','physicalUnit','physicalResult','Physikalischer Wert','physikalischen Wert'):
    if forbidden in siemens_html: errors.append(f'Siemens-Rechner: entfernte physikalische Konfiguration noch vorhanden: {forbidden}')
siemens_css=(ROOT/'assets/siemens-analogwert-rechner.css').read_text(encoding='utf-8')
for required in ('linear-gradient(90deg,#d74c57 0 var(--b1)', '#f5b942 var(--b1) var(--b2)', '#69c93d var(--b2) var(--b3)', '--thumb-color'):
    if required not in siemens_css: errors.append(f'Siemens-Rechner: feste Bereichsfarbgebung fehlt: {required}')
if '.analog-workbench::after' in siemens_css or "content:'INT'" in siemens_css or "content:'TNT'" in siemens_css: errors.append('Siemens-Rechner: transparentes Hintergrundelement im Konfigurationsbereich nicht vollständig entfernt')
siemens_js=(ROOT/'assets/siemens-analogwert-rechner.js').read_text(encoding='utf-8')
for required in ("'4-20mA'","'0-20mA'","'0-10V'","'2-10V'",'et200sp_st:Object.freeze','et200spha_off:Object.freeze','et200spha_on:Object.freeze','s71500_fai_scale:Object.freeze','generic_scale:Object.freeze','statusForRaw','signalScaleForType','profileScale','boundaries',"$('cardProfile')","$('valueSlider')","$('sliderScale')"):
    if required not in siemens_js: errors.append(f'Siemens-Rechner: Berechnungs-/Profilmerkmal fehlt: {required}')
for forbidden in ('physicalMin','physicalMax','physicalUnit','physicalResult',"inputKind==='percent'","inputKind==='physical'"):
    if forbidden in siemens_js: errors.append(f'Siemens-Rechner: entfernte Berechnungsart noch vorhanden: {forbidden}')

for rel,expected in TEMPLATE_HASHES.items():
    path=ROOT/rel
    actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ''
    if actual!=expected: errors.append(f'Vorlage verändert oder fehlt: {rel}')

for script in ROOT.rglob('*.js'):
    result=subprocess.run(['node','--check',str(script)],capture_output=True,text=True)
    if result.returncode: errors.append(f'{script.relative_to(ROOT)}: JS-Syntaxfehler: {result.stderr.strip()}')

if errors:
    print('FEHLER')
    for error in errors: print('-',error)
    sys.exit(1)
print(f'OK: {len(pages)} Seiten, Werkstoff-Breadcrumb, 10 Startseitenkacheln einschließlich sicherem E+H-Externlink, Beta-Isolation, Siemens-Kartenprofile und Rohwert-Wissenseintrag, 5 favoritenfähige Wissenskacheln, 10 Werkstoffe, Integrationen, Vorlagen-Hashes, lokale Referenzen und JavaScript geprüft.')
