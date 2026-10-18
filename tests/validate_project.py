#!/usr/bin/env python3
"""Vollständige Struktur-, Referenz-, Inhalts- und Assetprüfung für 2.6.6.0-Beta."""
from __future__ import annotations
import hashlib,json,re,sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
VERSION='2.6.6.0-Beta'; SLUG='v2-6-6-0'
MANIFEST=f'manifest-{SLUG}.webmanifest'; CSS=f'assets/app-{SLUG}.css'; JS=f'assets/app-{SLUG}.js'; SEARCH=f'assets/search-index-{SLUG}.json'
ARTICLES={
'air-torque-antrieb-drehrichtung':('Air Torque','Pneumatischer Antrieb','Drehrichtung SCO/SCC',['SCO','SCC']),
'endress-hauser-promass-einbaulage':('Endress+Hauser','Promass','Einbaulage und Einbausituation',['Steigleitung','Promass','Gasblasen','Feststoffe']),
'siemens-sitrans-p320-sil-verriegelung':('Siemens','SITRANS P320','SIL-Verriegelung',['2457','SIMATIC PDM','Schreibschutz']),
'siemens-sps-rohwert':('Siemens','SPS / Analogkarte','Rohwert und Skalierung',['27648','5530','Rohwert','Skalierung']),
'vacon-frequenzumrichter-ist-sollwert-abweichung':('Vacon','Frequenzumrichter','Ist-/Sollwert-Abweichung im PLS',['2.2.3.7','maximale Frequenz','PLS'])}
MANUFACTURERS=['air-torque','endress-hauser','siemens','vacon','sonstiges']
DEVICES=['device-air-torque-pneumatic-actuator','device-endress-hauser-promass','device-siemens-sitrans-p320','device-siemens-sps-analogkarte','device-vacon-frequenzumrichter']
PROTECTED={
'logo-sk-pct-tools.png':'232bfe68bd3985f793c6f0c62eb4393686a2fbbd5fd90790b979b91f6da34c2e','favicon.png':'7e2eb34f36ac8764e78549663b8c8387b609c4ad52c79b01848d40326a161d99','apple-touch-icon.png':'b9e8f9ca3ad5f661439a19d58ff2499ed0a5c5015832d40f98599868e1c6fc32','icon-192.png':'7a7bc6cc6641fd0bc34372ae954f5f2383a206bb52d8e1b4ceb2d4b9d1e70c60','icon-512.png':'232bfe68bd3985f793c6f0c62eb4393686a2fbbd5fd90790b979b91f6da34c2e','icon-maskable-192.png':'d886b66da8024688d80385c5fa71e60826fa07808fa109d861126ff568a9e93b','icon-maskable-512.png':'b6e7fd947838c2be5852f9ec909aa41895710fa753dffa4c3846e11ffdb7af4f','header-logo-simple.png':'6d5f179fb992998d5f9aee70a7c327f03796d06733ea27bc6562cefd5cb6fbd7'}
MANUFACTURER_HASHES={'air-torque':'0f4ef826b1a26001da33e58a1f0ed4368df42246e7868609d0134a5f6d1dc155','endress-hauser':'34f4087f005202174fcdc324d07032b5f159e17b6163586ad90d64345170d29f','siemens':'c3d516f1a74a647b902c972d9958324f17794c47c4b69c3d5a52354b32daaf66','sonstiges':'fc556b32927f7ad15741308f2b3cc663356c77852c03b213fab6ed80e8671b95','vacon':'851a27f15e4638d4423706d18825a703f245a0b2bb73521fb529398135b2f9e0'}
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.h1=0;self.headers=0;self.footers=0;self.css=[];self.js=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if tag=='header' and 'data-sk-shared-header' in a:self.headers+=1
  if tag=='footer' and 'data-sk-shared-footer' in a:self.footers+=1
  if tag=='link' and a.get('rel')=='stylesheet':self.css.append(a.get('href','').split('?')[0])
  if tag=='script' and a.get('src'):self.js.append(a['src'].split('?')[0])
  if tag in {'a','img','script','link'}:
   ref=a.get('href' if tag in {'a','link'} else 'src')
   if ref and not urlsplit(ref).scheme and not ref.startswith(('#','mailto:','tel:')):self.refs.append(ref)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(c,m,e):
 if not c:e.append(m)
def exists(source,ref):
 target=(source.parent/urlsplit(ref).path).resolve()
 try:target.relative_to(ROOT)
 except ValueError:return False
 return target.is_file() or (target.is_dir() and (target/'index.html').is_file())
def main():
 e=[]
 check((ROOT/'VERSION').read_text().strip()==VERSION,'VERSION falsch',e)
 manifest=json.loads((ROOT/MANIFEST).read_text());check(manifest.get('version')==VERSION,'Manifest-Version falsch',e)
 html=sorted(ROOT.rglob('*.html'));check(len(html)==16,f'HTML-Seiten {len(html)} statt 16',e)
 for page in html:
  text=page.read_text();p=Parser();p.feed(text);rel=page.relative_to(ROOT);redirect='data-sk-page="redirect"' in text
  check(VERSION in text,f'Version fehlt: {rel}',e);check(p.h1==1,f'H1-Anzahl {p.h1}: {rel}',e);check('viewport-fit=cover' in text,f'Viewport-fit fehlt: {rel}',e);check(MANIFEST in text,f'Manifest fehlt: {rel}',e);check(any(x.endswith(CSS) for x in p.css),f'Zentral-CSS fehlt: {rel}',e)
  if not redirect:check(any(x.endswith(JS) for x in p.js),f'Zentral-JS fehlt: {rel}',e)
  if 'data-sk-layout="framed"' in text and not redirect:check(p.headers==1 and p.footers==1,f'Shared Shell fehlt: {rel}',e)
  for ref in p.refs:check(exists(page,ref),f'Referenz fehlt in {rel}: {ref}',e)
 # Hierarchie und Beiträge
 khtml=(ROOT/'wissensdatenbank/index.html').read_text();kjs=(ROOT/'assets/knowledge-overview.js').read_text()
 for token in ['HERSTELLER','GERÄT · FAMILIE · THEMENBEREICH','WISSENSBEITRÄGE','knowledge-tile-grid','knowledge-context-back']:check(token in khtml+kjs,f'Wissensnavigation fehlt: {token}',e)
 check("name:'Sonstiges'" in kjs and "families:[]" in kjs,'Sonstiges muss fachlich leer bleiben',e)
 for slug,(manufacturer,family,article,tokens) in ARTICLES.items():
  text=(ROOT/'wissensdatenbank'/slug/'index.html').read_text();check('knowledge-flat' in text and 'knowledge-cartoon' not in text,f'Flachdesign fehlt: {slug}',e);check('kb-context-back' in text,f'Mobiler Eltern-Link fehlt: {slug}',e)
  for token in [manufacturer,family,article,*tokens,'knowledge-compact.js','Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)']:check(token in text,f'Inhalt {token} fehlt: {slug}',e)
 # Werkstoffe
 materials=json.loads((ROOT/'assets/materials.json').read_text());check(len(materials['materials'])==10,'Werkstoffanzahl nicht 10',e)
 mjs=(ROOT/'assets/materials.js').read_text();mhtml=(ROOT/'werkstoffdatenbank/index.html').read_text()
 for token in ['material-tile tool-card','materialDetail','materialCompareSelect','materialSearch','detailUrl','material-context-back']:check(token in mjs+mhtml,f'Werkstoff-Direktnavigation fehlt: {token}',e)
 check('Werkstoffgruppenebene' not in mhtml,'Unzulässige Werkstoffgruppenebene',e)
 # Suchindex
 index=json.loads((ROOT/SEARCH).read_text());check(len(index)==19,f'Suchindex {len(index)} statt 19 Einträge',e);check(all(x.get('release')==VERSION for x in index),'Suchindex-Version fehlerhaft',e)
 check(sum(x.get('type')=='Hersteller' for x in index)==5,'Hersteller nicht vollständig im Suchindex',e);check(sum(x.get('type')=='Gerät / Familie / Themenbereich' for x in index)==5,'Zwischenebenen nicht vollständig im Suchindex',e)
 # Icons
 icons=sorted((ROOT/'assets/navigation-icons').glob('*.png'));check(len(icons)==39,f'Iconanzahl {len(icons)} statt 39',e);check(len({sha(x) for x in icons})==39,'Icons nicht eigenständig',e)
 for icon in icons:
  with Image.open(icon) as im:check(im.size==(512,512),f'Icongröße falsch: {icon.name}',e);check(im.convert('RGBA').getchannel('A').getextrema()==(0,255),f'Transparenz fehlt: {icon.name}',e)
 for slug,h in MANUFACTURER_HASHES.items():check(sha(ROOT/f'assets/navigation-icons/{SLUG}-manufacturer-{slug}.png')==h,f'Freigegebenes Herstellericon verändert: {slug}',e)
 for item in materials['materials']:check((ROOT/f"assets/navigation-icons/{SLUG}-material-{item['id']}.png").is_file(),f"Werkstofficon fehlt: {item['id']}",e)
 for name,h in PROTECTED.items():check(sha(ROOT/'assets'/name)==h,f'Geschütztes Markenasset verändert: {name}',e)
 # Offline und Gestaltung
 worker=(ROOT/'service-worker.js').read_text();check("CACHE_EPOCH='v2-6-6-0-core-r1'" in worker,'Cache-Epoch falsch',e)
 for stem in DEVICES+[f"material-{x['id']}" for x in materials['materials']]:check(f"'{stem}'" in worker,f'Offline-Icon fehlt: {stem}',e)
 css=(ROOT/CSS).read_text();check('V2.6.6.0-Beta: verbindliche App-Kachel-Navigation' in css,'Finaler Designblock fehlt',e);check('knowledge-cartoon' not in '\n'.join((ROOT/'wissensdatenbank'/x/'index.html').read_text() for x in ARTICLES),'Knowledge-Cartoon operativ',e)
 for token in ['transform:none!important','translate:none!important','scale:none!important','@media(max-width:350px)','--sk-tile-icon-size','material-detail-card']:check(token in css,f'CSS-Abnahmeregel fehlt: {token}',e)
 # Doku
 for name in ['README.txt','RELEASE-NOTES.txt','WISSENSBEITRAGS-STANDARD.md','ICON-DESIGNRICHTLINIE.txt','TESTPLAN.md','TEST-RESULTS.txt','SECURITY-DEPLOYMENT.md','UEBERGABE-V2.6.6.0-Beta.txt']:check((ROOT/name).is_file(),f'Dokument fehlt: {name}',e)
 # Prüfsummen, sobald vorhanden
 sums=ROOT/'SHA256SUMS.txt'
 if sums.exists() and sums.read_text().strip():
  listed=[]
  for line in sums.read_text().splitlines():
   m=re.fullmatch(r'([0-9a-f]{64})  (.+)',line);check(bool(m),f'Ungültige Prüfsumme: {line}',e)
   if m:
    expected,rel=m.groups();p=ROOT/rel.removeprefix('./');listed.append(p.resolve());check(p.is_file() and sha(p)==expected,f'Prüfsumme falsch: {rel}',e)
  expected={p.resolve() for p in ROOT.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts};check(set(listed)==expected,'Prüfsummenbestand unvollständig',e)
 if e:print('FAIL');[print('-',x) for x in e];return 1
 print(f'PASS · {len(html)} HTML-Seiten · 5 Beiträge · 10 Werkstoffe · 39 Icons · 19 Suchindexeinträge · {VERSION}');return 0
if __name__=='__main__':sys.exit(main())
