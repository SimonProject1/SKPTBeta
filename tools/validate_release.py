#!/usr/bin/env python3
"""Static release validation for SK PLT Tools 2.1.0.5-Beta."""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.1.0.5-Beta'
EXPECTED_PAGES={
 'index.html','analogsignal/index.html','siemens-analogwert-rechner/index.html','einheitenrechner/index.html','messstellen-doku/index.html',
 'pf-rechner/index.html','pt-rechner/index.html','servicewerte/index.html',
 'spannungsfall-rechner/index.html','plausibilitaetspruefung-vde0100-600/index.html',
 'wissensdatenbank/index.html','wissensdatenbank/air-torque-antrieb-drehrichtung/index.html',
 'wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/index.html','wissensdatenbank/siemens-sps-rohwert/index.html',
 'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html',
 'wissensdatenbank/werkstoff-nachschlagewerk/index.html'
}
EXPECTED_MATERIAL_IDS={'1-4301','1-4401','1-4404','1-4408','1-4409','1-4435','1-4539','1-4571','2-4602','2-4605'}
TEMPLATE_HASHES={
 'wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf':'6fb4b02aa6033a628f426c7bb9e6bf7f21f132ca191a77c1eb012d9999cb04db',
 'wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.docx':'95d130036ad3e2c9e5aa799ff696114bd8dadd0b9e326d66263f742d93079e98'
}
errors=[]
pages={p.relative_to(ROOT).as_posix():p for p in ROOT.rglob('index.html')}

OBSOLETE_FILES={
 'assets/styles.css','assets/design.css','assets/favorites.css','assets/favorites.js','assets/start-filter.css','assets/start-filter.js',
 'assets/sort-tools.css','assets/sort-tools.js','assets/navigation-tree.css','assets/navigation-tree.js','assets/card-cleanup.css',
 'assets/card-cleanup.js','assets/disable-support.js','assets/header-alignment-fix.css','assets/header-alignment-fix.js',
 'assets/header-version-footer-fix.css','assets/header-version-footer-fix.js','assets/knowledge-template-pdf.js',
 'assets/search-service-cleanup.js','assets/siemens-sitrans-integration.js','assets/sk-shell.css','assets/sk-shell.js',
 'assets/start-vde-integration.js','assets/start-voltage-drop-integration.js',
 'plausibilitaetspruefung-vde0100-600/logo-fallback.js','wissensdatenbank/vorlagen/Wissensdatenbank_Beitragsvorlage.pdf.pdf'
}
for rel in sorted(OBSOLETE_FILES):
    if (ROOT/rel).exists(): errors.append(f'Nachweislich ersetzte Altdatei noch vorhanden: {rel}')
for path in (ROOT/'assets').glob('version-*.js'):
    errors.append(f'Nachweislich ersetzte Versions-Patchdatei noch vorhanden: {path.relative_to(ROOT)}')
for required in ('release-config.json','shared/header.html','shared/footer.html','shared/controls.html','shared/pages.json','tools/sync_shared.py','tools/release.py','assets/vde0100-600-engine.js','assets/vde0100-600-template.json','vendor/pdfjs/pdf.min.mjs','vendor/pdfjs/pdf.worker.min.mjs','vendor/pdfjs/LICENSE','tools/vde-protocol-e2e-test.py','VDE0100-600-AUTOMATIK.md'):
    if not (ROOT/required).is_file(): errors.append(f'Zentrale Build-/Shell-Datei fehlt: {required}')
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
    if soup.select('.sk-logo-version'): errors.append(f'{rel}: sichtbare Header-Version muss entfernt sein')
    if 'Version ' in soup.select_one('footer.sk-footer').get_text(' ',strip=True): errors.append(f'{rel}: sichtbare Footer-Version muss entfernt sein')
    if soup.select_one('footer.sk-footer').get_text(' ',strip=True)!='SK PLT Tools · Entwickelt von Simon Kiesler': errors.append(f'{rel}: Footer-Standard falsch')
    if 'SK PLT Tools' not in soup.get_text(' ',strip=True): errors.append(f'{rel}: Produktkennzeichnung fehlt')
    styles=[tag.get('href','') for tag in soup.find_all('link',rel=lambda value:value and 'stylesheet' in value)]
    core_styles=[value for value in styles if 'assets/core.css' in value]
    if len(core_styles)!=1: errors.append(f'{rel}: genau eine zentrale core.css erwartet')
    scripts=[tag.get('src','') for tag in soup.find_all('script',src=True)]
    if sum('assets/app.js' in value for value in scripts)!=1: errors.append(f'{rel}: genau eine zentrale app.js erwartet')
    for forbidden in ('favorites.js','start-filter.js','sort-tools.js','navigation-tree.js','sk-shell.js','header-alignment-fix.js','header-version-footer-fix.js','card-cleanup.js','start-vde-integration.js','start-voltage-drop-integration.js','version-1.9.8.5.js'):
        if any(forbidden in value for value in scripts): errors.append(f'{rel}: alte Patchdatei noch eingebunden: {forbidden}')
    if len(soup.select('.sk-favorites-trigger'))!=1 or len(soup.select('.sk-tree-trigger'))!=1: errors.append(f'{rel}: statische Seitentrigger fehlen')
    for marker in ('header','footer','controls'):
        if text.count(f'<!-- sk:{marker}:start -->')!=1 or text.count(f'<!-- sk:{marker}:end -->')!=1: errors.append(f'{rel}: zentraler {marker}-Marker fehlt oder ist doppelt')
    for tag in soup.find_all(src=True)+soup.find_all(href=True):
        ref=tag.get('src') or tag.get('href')
        target=resolve_local(page,ref)
        if target is not None and not target.exists(): errors.append(f'{rel}: fehlende lokale Referenz {ref}')

start=BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'),'html.parser')
if len(start.select('.tools > a.card'))!=10: errors.append('Startseite: genau 10 sichtbare Werkzeugkacheln erwartet')
if len(start.select('.badge'))!=1 or start.select_one('.badge').get_text(strip=True)!=f'Version {VERSION}': errors.append('Startseite: Hero-Version fehlt oder ist nicht eindeutig')
for rel,page in pages.items():
    if rel!='index.html' and BeautifulSoup(page.read_text(encoding='utf-8'),'html.parser').select('.badge'): errors.append(f'{rel}: Unterseite darf keine sichtbare Versionsbadge enthalten')
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
    'siemens-sps-rohwert/'
}
actual_knowledge_hrefs={tile.get('href') for tile in knowledge_tiles}
if actual_knowledge_hrefs!=expected_knowledge_hrefs: errors.append(f'Wissensdatenbank: Wissenskacheln abweichend: {sorted(actual_knowledge_hrefs)}')
for tile in knowledge_tiles:
    if 'tool-card' not in tile.get('class',[]): errors.append(f'Wissensdatenbank: Kachel nicht in Favoriten integriert: {tile.get("href","?")}')
if '.knowledge-entry[hidden]{display:none}' not in (ROOT/'wissensdatenbank/index.html').read_text(encoding='utf-8'): errors.append('Wissensdatenbank: hidden-Kacheln werden durch das Karten-CSS nicht zuverlässig ausgeblendet')
favorites=(ROOT/'assets/app.js').read_text(encoding='utf-8')
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
if not any(item.get('manufacturer')=='Siemens' and item.get('device')=='SPS' and item.get('topic')=='Rohwert' and item.get('url')=='siemens-analogwert-rechner/' for item in search_index): errors.append('Suche: Siemens-Rohwert-Rechner fehlt')
if not any(item.get('manufacturer')=='Siemens' and item.get('device')=='SPS' and item.get('topic')=='Rohwert Grundlagen' and item.get('url')=='wissensdatenbank/siemens-sps-rohwert/' for item in search_index): errors.append('Suche: Rohwert-Grundlagenartikel fehlt')
if 'assets/materials.json' not in (ROOT/'assets/app.js').read_text(encoding='utf-8'): errors.append('Startseitensuche: zentrale Werkstoffdatei wird nicht geladen')
nav=json.loads((ROOT/'assets/navigation-tree.json').read_text(encoding='utf-8'))
if nav.get('version')!=VERSION: errors.append('Navigationsbaum: Version inkonsistent')
def walk_nav(items):
    for item in items:
        yield item
        yield from walk_nav(item.get('children',[]))
nav_items=[item for group in nav.get('groups',[]) for item in walk_nav(group.get('items',[]))]
for item in nav_items:
    url=item.get('url','')
    if not url or url.startswith(('http://','https://')): continue
    target=ROOT/url
    if url.endswith('/'): target=target/'index.html'
    if not target.exists(): errors.append(f'Navigationsbaum: lokales Ziel fehlt: {url}')
if len([item for item in nav_items if item.get('url')])!=len({item.get('url') for item in nav_items if item.get('url')}): errors.append('Navigationsbaum: doppelte Ziel-URL')
if 'wissensdatenbank/werkstoff-nachschlagewerk/' not in json.dumps(nav): errors.append('Navigationsbaum: Werkstoffbereich fehlt')
if 'siemens-analogwert-rechner/' not in json.dumps(nav): errors.append('Navigationsbaum: Siemens-SPS-Analogwert-Rechner fehlt')
sps_nodes=[sps for group in nav.get('groups',[]) for item in group.get('items',[]) for child in item.get('children',[]) for sps in child.get('children',[]) if item.get('title')=='Wissensdatenbank' and child.get('title')=='Siemens' and sps.get('title')=='SPS']
expected_sps_children=[{'title':'Rohwert Grundlagen','url':'wissensdatenbank/siemens-sps-rohwert/'}]
if len(sps_nodes)!=1: errors.append(f'Navigationsbaum: genau ein Pfad Wissen > Siemens > SPS erwartet, gefunden {len(sps_nodes)}')
elif sps_nodes[0].get('children')!=expected_sps_children: errors.append(f'Navigationsbaum: unter Wissen > Siemens > SPS darf nur Rohwert Grundlagen stehen: {sps_nodes[0].get("children")}')
if not any(group.get('id')=='external-services' and any(item.get('url')=='https://netilion.endress.com/app/library/device_viewer' and item.get('type')=='external' for item in group.get('items',[])) for group in nav.get('groups',[])): errors.append('Navigationsbaum: E+H Device Viewer fehlt oder ist nicht extern gekennzeichnet')
if 'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/' not in json.dumps(nav): errors.append('Navigationsbaum: Vacon-Wissensbeitrag fehlt')
if not any(item.get('url')=='wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/' and item.get('manufacturer')=='Vacon' and '2.2.3.7' in ' '.join(item.get('keywords',[])) for item in search_index): errors.append('Startseitensuche: Vacon-Wissensbeitrag oder Parameter 2.2.3.7 fehlt')

vde_path=ROOT/'plausibilitaetspruefung-vde0100-600/index.html'
vde_html=vde_path.read_text(encoding='utf-8')
vde_page=BeautifulSoup(vde_html,'html.parser')
for selector in ('#documentInput','#analysisPanel','#reviewPanel','#previewFrame','#statGroups','#statFields','#statRules','#statOpen','#recognitionDetail','#issuePanel','#issueCard','#issueSource','#resolutionPolicy','#confirmFail','#applyCorrection','#resultPanel','#verdictIcon','#verdictTitle'):
    if not vde_page.select_one(selector): errors.append(f'VDE-Messwertprüfung: Element fehlt: {selector}')
for forbidden_selector in ('#loadSample','#notRelevant','#useForm','#manualFormReview','#replaceFile','#formIdentityActions','#layoutScore'):
    if vde_page.select_one(forbidden_selector): errors.append(f'VDE-Messwertprüfung: formales/überholtes Steuerelement vorhanden: {forbidden_selector}')
if 'Muster laden' in vde_html or 'VDEProtokoll.pdf' in vde_html: errors.append('VDE-Messwertprüfung: Mustervorlage darf nicht genannt, geladen oder verlinkt sein')
for phrase in ('Ausschließlich Messwerte','Formularidentität','Unterschriften','Namen','Datum','Orte','Kreuze'):
    if phrase not in vde_html: errors.append(f'VDE-Messwertprüfung: Ausschluss-/Umfangshinweis fehlt: {phrase}')
for asset in ('assets/vde0100-600-engine.js','assets/vde0100-600-template.json','assets/vde0100-600-rules.json','vendor/pdfjs/pdf.min.mjs','vendor/pdfjs/pdf.worker.min.mjs'):
    if not (ROOT/asset).is_file(): errors.append(f'VDE-Messwertprüfung: Laufzeitdatei fehlt: {asset}')
if any(path.name.lower()=='vdeprotokoll.pdf' for path in ROOT.rglob('*') if path.is_file()): errors.append('VDE-Messwertprüfung: Mustervorlage darf nicht Bestandteil des Webprojekts sein')
try:
    vde_schema=json.loads((ROOT/'assets/vde0100-600-template.json').read_text(encoding='utf-8'))
    reference=vde_schema.get('referenceForm',{})
    if vde_schema.get('moduleVersion')!=VERSION: errors.append('VDE-Schema: Modulversion inkonsistent')
    if reference.get('embedded') is not False or reference.get('downloadable') is not False: errors.append('VDE-Schema: Mustervorlage muss nicht eingebettet und nicht downloadbar sein')
    if 'interne Lokalisierung' not in reference.get('purpose',''): errors.append('VDE-Schema: Referenzzweck ist nicht auf interne Messfeldlokalisierung begrenzt')
    descriptor=vde_schema.get('referenceDescriptor',{})
    if descriptor.get('version')!='structure-v2' or len(descriptor.get('grid',[]))!=432 or len(descriptor.get('x',[]))!=64 or len(descriptor.get('y',[]))!=96: errors.append('VDE-Schema: interner Orientierungsfingerabdruck unvollständig')
    field_map=vde_schema.get('fieldMap',{})
    if len(field_map)!=18: errors.append(f'VDE-Schema: erwartet werden 18 Mess-/Bezugsfeldzonen, gefunden {len(field_map)}')
    forbidden_form_fields={'protocolType','testReason','building','testerName','testDate','signatureState','commissioningSignature','inspection31','test71'}
    if forbidden_form_fields & set(field_map): errors.append(f'VDE-Schema: formale Felder im Lokalisierungsprofil: {sorted(forbidden_form_fields & set(field_map))}')
    for field in ('insulationValues','loopImpedance','shortCircuitCurrent','loadCurrent','voltageDrop','voltageDropPercent','rcdTripCurrent','rcdTripTime'):
        if field not in field_map: errors.append(f'VDE-Schema: Messwertfeld fehlt: {field}')
    rule_ids={item.get('id') for item in vde_schema.get('plausibilityRules',[])}
    for rule in ('MEAS-INS','MEAS-ZS','MEAS-IK-CONSISTENCY','CIRCUIT-IB-IN','MEAS-DU','RCD-I','RCD-T'):
        if rule not in rule_ids: errors.append(f'VDE-Schema: Rechenregel fehlt: {rule}')
except Exception as exc:
    errors.append(f'VDE-Schema ungültig: {exc}')
vde_rules=json.loads((ROOT/'assets/vde0100-600-rules.json').read_text(encoding='utf-8'))
if vde_rules.get('moduleVersion')!=VERSION: errors.append('VDE-Regeln: Modulversion inkonsistent')
if not vde_rules.get('resolutionGovernance',{}).get('queryEachMissingOrUncertainValue'): errors.append('VDE-Regeln: Einzelabfrage fehlender/unsicherer Werte fehlt')
if vde_rules.get('resolutionGovernance',{}).get('missingOrUncertainValuesCauseFailure') is not False: errors.append('VDE-Regeln: fehlender/unsicherer Wert darf nicht rot werden')
if vde_rules.get('resolutionGovernance',{}).get('finalResultWhileValuesMissing') is not False: errors.append('VDE-Regeln: Endergebnis bei fehlenden Werten nicht gesperrt')
vde_engine=(ROOT/'assets/vde0100-600-engine.js').read_text(encoding='utf-8')
for required in ('MEASUREMENT_GROUPS','detectedMeasurementGroups','requiredFieldsForGroup','buildIssues','finalState','MEAS-IK-CONSISTENCY','SCOPE-CONFIRM','missing-measurement','missing-reference'):
    if required not in vde_engine: errors.append(f'VDE-Engine: Merkmal fehlt: {required}')
for forbidden in ('signatureState','testerName','testDate','FORM-IDENTITY','STATUS-inspection','CHOICE-MULTIPLE'):
    if forbidden in vde_engine: errors.append(f'VDE-Engine: formale Bewertungslogik noch vorhanden: {forbidden}')
checker=(ROOT/'plausibilitaetspruefung-vde0100-600/checker.js').read_text(encoding='utf-8')
for required in ('_measurementScope','_scopeConfirmed','scopeControl','data-scope','internalLocatorUsed','renderIssueContext','confirmedFailIds','TextDetector'):
    if required not in checker: errors.append(f'VDE-Erkennung: Merkmal fehlt: {required}')
for forbidden in ('resolveFormIdentity','formIdentityActions','signatureState','checkboxMarked','_choiceMarks'):
    if forbidden in checker: errors.append(f'VDE-Erkennung: formale Bewertungslogik noch vorhanden: {forbidden}')
if 'loadSample' in checker: errors.append('VDE-Erkennung: alte Musterladefunktion noch vorhanden')

nav_js=(ROOT/'assets/app.js').read_text(encoding='utf-8')
nav_css=(ROOT/'assets/core.css').read_text(encoding='utf-8')
for required in ('sk-tree-node-row','aria-controls','aria-label="${label} einklappen"'):
    if required not in nav_js: errors.append(f'Navigationsbaum: valide Knotenstruktur unvollständig: {required}')
if '<button class="sk-tree-node-toggle" type="button" data-node="${id}" aria-expanded="true"><span class="sk-tree-chevron">⌄</span>${row}</button>' in nav_js:
    errors.append('Navigationsbaum: interaktiver Link ist weiterhin unzulässig in eine Schaltfläche verschachtelt')
for required in ('.sk-tree-node-row{display:flex;align-items:stretch', 'background:#0a2639', '.sk-tree-node-toggle{display:grid;place-items:center', 'color:#89d329'):
    if required not in nav_css: errors.append(f'Navigationsbaum: Kachel-/Pfeilausrichtung unvollständig: {required}')

article_html=(ROOT/'wissensdatenbank/siemens-sps-rohwert/index.html').read_text(encoding='utf-8')
for required in ('4 mA  =     0','12 mA = 13824','4 mA  =  5530','12 mA = 16589','Rohwert = 13824','../../siemens-analogwert-rechner/'):
    if required not in article_html: errors.append(f'Rohwert-Grundlagenartikel: Inhalt/Verknüpfung fehlt: {required}')
if article_html.count(f'Version {VERSION}')>0: errors.append('Rohwert-Grundlagenartikel: sichtbare Versionsnummer außerhalb Startseiten-Hero')
article_page=BeautifulSoup(article_html,'html.parser')
article_breadcrumb=article_page.select_one('nav.knowledge-breadcrumb[aria-label="Brotkrümelnavigation"]')
if article_breadcrumb is None: errors.append('Rohwert-Grundlagenartikel: Breadcrumb fehlt')
else:
    breadcrumb_links=[(link.get_text(' ',strip=True),link.get('href')) for link in article_breadcrumb.find_all('a')]
    if breadcrumb_links!=[('Startseite','../../'),('Wissensdatenbank','../')]: errors.append(f'Rohwert-Grundlagenartikel: Breadcrumb-Links falsch: {breadcrumb_links}')
if not re.search(r'\.knowledge-breadcrumb\s+a\s*\{[^}]*color\s*:\s*#00b7e8',article_html,re.S): errors.append('Rohwert-Grundlagenartikel: einheitliche cyanfarbene Breadcrumb-Links fehlen')

vacon_page=(ROOT/'wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html').read_text(encoding='utf-8')
for required in ('Vacon','Frequenzumrichter','Ist-/Sollwert-Abweichung im PLS','2.2.3.7','maximale Frequenz','vacon-wissen.css'):
    if required not in vacon_page: errors.append(f'Vacon-Wissensbeitrag: Inhalt/Integration fehlt: {required}')

sw=(ROOT/'service-worker.js').read_text(encoding='utf-8')
for forbidden in ('enhanceHtml','enhanceJs','.replace(\'</head>\'','.replace(\'</body>\''):
    if forbidden in sw: errors.append(f'Service Worker enthält verbotene Laufzeit-Patchlogik: {forbidden}')
if f"const RELEASE='{VERSION}'" not in sw: errors.append('Service Worker verwendet falsche Version')
if "const CACHE_PREFIX='sk-plt-tools-'" not in sw or 'const CACHE=`${CACHE_PREFIX}v${RELEASE}`' not in sw: errors.append('Service Worker verwendet nicht den Release-Cache')
if 'key.startsWith(CACHE_PREFIX)&&key!==CACHE' not in sw: errors.append('Service Worker bereinigt ältere SK-PLT-Tools-Caches nicht')
for required in ('./assets/core.css','./assets/app.js','./assets/navigation-tree.json','./assets/siemens-analogwert-rechner.css','./assets/siemens-analogwert-rechner.js','./siemens-analogwert-rechner/index.html','./assets/materials.json','./assets/materials.js','./assets/materials.css','./wissensdatenbank/werkstoff-nachschlagewerk/index.html','./assets/vacon-wissen.css','./wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html','./assets/vde0100-600-engine.js','./assets/vde0100-600-template.json','./vendor/pdfjs/pdf.min.mjs','./vendor/pdfjs/pdf.worker.min.mjs'):
    if required not in sw: errors.append(f'Service Worker: Precache-Eintrag fehlt: {required}')
for forbidden in ('_'.join(('228','SR4','K06','E07.1.pdf')),'744f24436071c5c9f36d91fc82fa2a6'+'a16f20ec8662bd81f68e3f53321792772'):
    if forbidden in sw: errors.append('Service Worker enthält eine personenbezogene Testreferenz')


manifest=json.loads((ROOT/'manifest.webmanifest').read_text(encoding='utf-8'))
if manifest.get('name')!='SK PLT Tools' or manifest.get('short_name')!='SK PLT Tools': errors.append('Manifest: offizieller App-Name fehlt')
expected_app_id=f'./?app=sk-plt-tools-{VERSION.lower()}'
if manifest.get('id')!=expected_app_id or manifest.get('start_url')!=expected_app_id or manifest.get('version')!=VERSION: errors.append('Manifest: Release-ID/start_url/version nicht eindeutig')
if manifest.get('description')!=f'Praktische Werkzeuge und Wissensdatenbank für die Prozessleittechnik · Version {VERSION}': errors.append('Manifest: Release-Beschreibung inkonsistent')
release_config=json.loads((ROOT/'release-config.json').read_text(encoding='utf-8'))
if release_config.get('version')!=VERSION or release_config.get('stableBaseline')!='2.1.0.0' or release_config.get('archiveName')!=f'SK-PLT-Tools-V{VERSION}.zip': errors.append('Release-Konfiguration: Beta-Version, stabile Basis oder Archivname inkonsistent')
siemens_html=(ROOT/'siemens-analogwert-rechner/index.html').read_text(encoding='utf-8')
siemens_page=BeautifulSoup(siemens_html,'html.parser')
for selector in ('#cardProfile','#signalType','#inputKind','#inputValue','#inputValueLabel','#inputSuffix','#valueSlider','#sliderLabel','#sliderScale','#rawResult','#signalResult','#percentResult','#rangeStatus','#statusDetail','#calculationError'):
    if not siemens_page.select_one(selector): errors.append(f'Siemens-Rechner: Element fehlt: {selector}')
card_info=siemens_page.select_one('details.analog-card-info > summary')
if card_info is None or card_info.get_text(' ',strip=True)!='Karteninformationen': errors.append('Siemens-Rechner: einklappbare Karteninformationen fehlen')
if siemens_page.select_one('h1') is None or siemens_page.select_one('h1').get_text(strip=True)!='Siemens Rohwert': errors.append('Siemens-Rechner: große Seitenüberschrift heißt nicht exakt Siemens Rohwert')
for state in ('underflow','underrange','nominal','overrange','overflow'):
    if not siemens_page.select_one(f'[data-state-key="{state}"]'): errors.append(f'Siemens-Rechner: Statusanzeige fehlt: {state}')
for forbidden in ('physicalMin','physicalMax','physicalUnit','physicalResult','Physikalischer Wert','physikalischen Wert'):
    if forbidden in siemens_html: errors.append(f'Siemens-Rechner: entfernte physikalische Konfiguration noch vorhanden: {forbidden}')
siemens_css=(ROOT/'assets/siemens-analogwert-rechner.css').read_text(encoding='utf-8')
for required in ('linear-gradient(90deg,#d74c57 0 var(--b1)', '#f5b942 var(--b1) var(--b2)', '#69c93d var(--b2) var(--b3)', '--thumb-color'):
    if required not in siemens_css: errors.append(f'Siemens-Rechner: feste Bereichsfarbgebung fehlt: {required}')
if '.analog-workbench::after' in siemens_css or "content:'INT'" in siemens_css or "content:'TNT'" in siemens_css: errors.append('Siemens-Rechner: transparentes Hintergrundelement im Konfigurationsbereich nicht vollständig entfernt')
for required in ('.analog-input-shell{display:grid!important','padding:5px 7px','.analog-card-info summary'):
    if required not in siemens_css: errors.append(f'Siemens-Rechner: Kompaktierungsmerkmal fehlt: {required}')
siemens_js=(ROOT/'assets/siemens-analogwert-rechner.js').read_text(encoding='utf-8')
for required in ("'4-20mA'","'0-20mA'","'0-10V'","'2-10V'",'et200sp_st:Object.freeze','et200spha_off:Object.freeze','et200spha_on:Object.freeze','s71500_fai_scale:Object.freeze','generic_scale:Object.freeze','statusForRaw','signalScaleForType','profileScale','boundaries',"$('cardProfile')","$('valueSlider')","$('sliderScale')"):
    if required not in siemens_js: errors.append(f'Siemens-Rechner: Berechnungs-/Profilmerkmal fehlt: {required}')
for forbidden in ('physicalMin','physicalMax','physicalUnit','physicalResult',"inputKind==='percent'","inputKind==='physical'"):
    if forbidden in siemens_js: errors.append(f'Siemens-Rechner: entfernte Berechnungsart noch vorhanden: {forbidden}')
for required in ("elements.inputValue.inputMode=mode==='raw'?'numeric':'decimal'","event.currentTarget.select()"):
    if required not in siemens_js: errors.append(f'Siemens-Rechner: optimierte Rohwert-Eingabe fehlt: {required}')

core_css=(ROOT/'assets/core.css').read_text(encoding='utf-8')
design_css=favorites_css=tree_css=styles_css=core_css
for required in ('min-height:86px','min-height:74px'):
    if required not in design_css: errors.append(f'Kompakter Header: Merkmal fehlt: {required}')
for label,content in (('Favoriten',favorites_css),('Navigation',tree_css)):
    for required in ('width:48px;height:48px','width:42px;height:42px'):
        if required not in content: errors.append(f'{label}: kompakte Schaltflächengröße fehlt: {required}')
for required in ('grid-template-columns:1fr 38px','.sign{font-size:16px;min-width:38px}'):
    if required not in styles_css: errors.append(f'Vorzeichen-Schaltfläche: Kompaktierungsmerkmal fehlt: {required}')

# Datenschutz-Gate: Das reale ausgefüllte Testprotokoll darf weder als Datei noch als Inhalt/Hash ausgeliefert werden.
PII_FIXTURE_NAME='_'.join(('228','SR4','K06','E07.1.pdf'))
PII_FIXTURE_HASH='744f24436071c5c9f36d91fc82fa2a6'+'a16f20ec8662bd81f68e3f53321792772'
for path in ROOT.rglob('*'):
    if not path.is_file(): continue
    if path.name==PII_FIXTURE_NAME: errors.append(f'Datenschutz: personenbezogene Testdatei im Release: {path.relative_to(ROOT)}')
    if hashlib.sha256(path.read_bytes()).hexdigest()==PII_FIXTURE_HASH: errors.append(f'Datenschutz: personenbezogener Testinhalt im Release: {path.relative_to(ROOT)}')
    if path.suffix.lower() in {'.js','.json','.html','.md','.txt','.py'}:
        text=path.read_text(encoding='utf-8',errors='ignore')
        if PII_FIXTURE_HASH in text: errors.append(f'Datenschutz: Hash der personenbezogenen Testdatei eingebettet: {path.relative_to(ROOT)}')

for rel,expected in TEMPLATE_HASHES.items():
    path=ROOT/rel
    actual=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else ''
    if actual!=expected: errors.append(f'Vorlage verändert oder fehlt: {rel}')

sums_path=ROOT/'SHA256SUMS.txt'
try:
    listed={}
    for line in sums_path.read_text(encoding='utf-8').splitlines():
        if not line.strip(): continue
        digest,rel=line.split(None,1)
        listed[rel.removeprefix('./')]=digest
    actual_files={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=sums_path and '__pycache__' not in p.parts and p.name!='.DS_Store'}
    if set(listed)!=actual_files:
        errors.append(f'Prüfsummen-Dateiliste abweichend: fehlend={sorted(actual_files-set(listed))}, zusätzlich={sorted(set(listed)-actual_files)}')
    for rel,digest in listed.items():
        path=ROOT/rel
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()!=digest: errors.append(f'Prüfsumme falsch: {rel}')
except Exception as exc:
    errors.append(f'SHA256SUMS.txt ungültig: {exc}')

for script in ROOT.rglob('*.js'):
    result=subprocess.run(['node','--check',str(script)],capture_output=True,text=True)
    if result.returncode: errors.append(f'{script.relative_to(ROOT)}: JS-Syntaxfehler: {result.stderr.strip()}')

if errors:
    print('FEHLER')
    for error in errors: print('-',error)
    sys.exit(1)
print(f'OK: {len(pages)} Seiten, messwertzentrierte VDE-Engine, internes Messfeldprofil und PDF.js, geführte Einzelklärung, formale Ausschlüsse, eindeutige sichtbare Hero-Version, vereinheitlichte Footer, Navigation, 10 Startseitenkacheln, Release-Cache-Isolation, Rechner, 5 Wissenskacheln, 10 Werkstoffe, vollständige SHA-256-Prüfsummen, lokale Referenzen und JavaScript geprüft.')
