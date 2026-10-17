#!/usr/bin/env python3
"""Struktur-, Referenz-, Design- und Integritätsprüfung für SK PCT Tools 2.6.5.1-Beta."""
from __future__ import annotations
import hashlib, json, re, struct, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
VERSION='2.6.5.1-Beta'
VERSION_SLUG='v2-6-5-1'
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
BRAND_SHA256={
 'logo-sk-pct-tools.png':'232bfe68bd3985f793c6f0c62eb4393686a2fbbd5fd90790b979b91f6da34c2e',
 'favicon.png':'7e2eb34f36ac8764e78549663b8c8387b609c4ad52c79b01848d40326a161d99',
 'apple-touch-icon.png':'b9e8f9ca3ad5f661439a19d58ff2499ed0a5c5015832d40f98599868e1c6fc32',
 'icon-192.png':'7a7bc6cc6641fd0bc34372ae954f5f2383a206bb52d8e1b4ceb2d4b9d1e70c60',
 'icon-512.png':'232bfe68bd3985f793c6f0c62eb4393686a2fbbd5fd90790b979b91f6da34c2e',
 'icon-maskable-192.png':'d886b66da8024688d80385c5fa71e60826fa07808fa109d861126ff568a9e93b',
 'icon-maskable-512.png':'b6e7fd947838c2be5852f9ec909aa41895710fa753dffa4c3846e11ffdb7af4f',
}
HEADER_LOGO='header-logo-simple.png'
HEADER_LOGO_SHA256='6d5f179fb992998d5f9aee70a7c327f03796d06733ea27bc6562cefd5cb6fbd7'
LEGACY_HEADER_LOGO='logo-sk-pct-tools-header.png'
LEGACY_HEADER_LOGO_SHA256='5128cff1bf2864d8821ac25f363c14a7ff52bd5a130cf2db023a80f9b0cf1aed'
RELEASE_MODULE='release-module-v2-6-5-1.png'
RELEASE_MODULE_SHA256='4d7fd9a089525219f0488045f2b8c98f4ac6f7b3921479ab0bb99718cc5c5289'
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
 'manufacturer-sonstiges','manufacturer-vacon','nav-back','nav-home','nav-search','nav-favorite'
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
 'nav-back':'782ee6e39d7d434d8e02347cd7732856b2acada454357cc564aca6a16bb237a2',
 'nav-home':'180193252a11350c0d1ad2f5e4f4595f2c9d754ff7a71b14db4cf4af97bb81fa',
 'nav-search':'3a4da7a8c0966e4ab2af33594dd4fd29a3367cabf88baba3225d6e7d9ac5d42f',
 'nav-favorite':'577de46932cb937bca6e085c70cc8d2d2a3eea21f3015a4747dbe7300c654179'
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
    check(not list(ROOT.glob('manifest-v2-6-[12]-*.webmanifest')),'Altes Manifest vorhanden.',errors)
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
    check(not re.search(r'2\.6\.[12]\.[0-9](?:-Beta)?|v2-6-[12]-[0-9]|2\.6\.3\.[1278]|v2-6-3-[1278]',operational),'Operative Altversionsverweise vorhanden.',errors)
    for removed in ('core.css','responsive.css','design-system.css','pct-frame.css','pct-controls-v2-6-1-5.css','pct-home-v2-6-1-5.css','app-v2-6-1-5.css','app-v2-6-1-5.js','app-v2-6-1-6.css','app-v2-6-1-6.js','app-v2-6-1-7.css','app-v2-6-1-7.js','app-v2-6-1-8.css','app-v2-6-1-8.js'):
        check(not (ROOT/'assets'/removed).exists(),f'Ersetzte Datei noch vorhanden: {removed}',errors)
    check(len(list((ROOT/'assets').glob('*.css')))==1,'Mehr als ein CSS-Bestand vorhanden.',errors)
    check((ROOT/SHARED_CSS).is_file() and (ROOT/SHARED_JS).is_file(),'Zentrale CSS-/JS-Datei fehlt.',errors)

    css=(ROOT/SHARED_CSS).read_text();js=(ROOT/SHARED_JS).read_text()
    check(css.count('!important')<=5,f'Zu viele !important: {css.count("!important")}',errors)
    for token in ('--sk-touch-min:44px','--sk-header-size:76px','--sk-footer-size:38px','viewport','strukturell icongebundene Favoriten','sk-app-icon-wrapper','tatsächlichen sichtbaren','--sk-favorite-touch-size:44px','--sk-favorite-visible-size:22px','--sk-favorite-ring-inset:11px','inset-block-start:-22px','inset-inline-end:-22px','translate:none','konsolidierte Header-, Logo- und Navigationsfamilie','--sk-industrial-cyan:#00e6f1','--sk-industrial-blue:#008cff','--sk-industrial-green:#78ff32','--sk-industrial-control-size:52px','eigenständiges Release-Modul der Icon-Familie','.sk-header-release-module.pct-release-module','.pct-home-release-module.pct-release-module','.pct-release-module>.pct-release-module-skin','.pct-release-module-copy','.sk-release-number','.sk-release-credit','container-type:inline-size','background:transparent;','box-shadow:none;','object-fit:fill','gemeinsamer Clean-Designblock Wissenskacheln + Favoriten','--sk-knowledge-icon-nominal','scale:none','Favoritendialog ohne historische Zierleisten'):
        check(token in css,f'Zentrale CSS-Regel fehlt: {token}',errors)
    check(css.count('transform:none')>=15 and css.count('translate:none')>=15,'Bewegungsfreie Interaktionszustände sind nicht ausreichend abgesichert.',errors)
    check('sk-home-app.card:hover{transform:translateY' not in css,'Startseiten-Hover verschiebt App-Icons noch.',errors)
    clean_css=css.split('/* === V2.6.5.1-Beta: gemeinsamer Clean-Designblock Wissenskacheln + Favoriten ===',1)[-1]
    check('translateY(' not in clean_css and 'scale(' not in clean_css,'Clean-Designblock enthält bewegende Kachel-/Control-Zustände.',errors)
    for token in ('>.knowledge-home-icon{','content:none;','background:transparent;','box-shadow:none;','transform:none;','translate:none;','scale:none;','.sk-favorites-clear.pct-control','safe-area-inset-top','overscroll-behavior:contain'):
        check(token in clean_css,f'Clean-Design-/Favoritenregel fehlt: {token}',errors)
    check('--sk-favorite-circle-outset' not in css,'Alte 25/75-Favoritenposition ist noch aktiv.',errors)
    check('body[data-sk-home="ios"].pct-home-editing .pct-home-grid .sk-home-app.card{' in css and 'touch-action:none' in css,'Aktiver Sortiermodus besitzt keinen eindeutigen Touch-/Drag-Zustand.',errors)
    check('animation:pct-home-icon-wiggle' in css and '@keyframes pct-home-icon-wiggle' in css,'Dezentes Wackeln ausschließlich auf dem sichtbaren Iconkörper fehlt.',errors)
    check('animation:none!important' in css and '.sk-home-app:not(.is-dragging){animation:pct-home-wiggle' in css,'Historische Kachel-Wackelregel wird nicht sicher neutralisiert.',errors)
    for token in ('headerneutraler, layoutstabiler Sortiermodus','pct-home-edit-actions','pct-home-history-button','pct-home-drop-placeholder','pct-home-placeholder-icon','pct-home-drag-layer','pct-home-drag-overlay','position:fixed','z-index:110','z-index:90','contain:none','safe-area-inset-bottom','scroll-padding-block-end'):
        check(token in css,f'Neue Sortiermodus-CSS-Struktur fehlt: {token}',errors)
    sort_css=css.split('/* === V2.6.5.1-Beta: headerneutraler, layoutstabiler Sortiermodus',1)[-1]
    for forbidden in ('.pct-home-editing .pct-home-head','.pct-home-editing .pct-home-brand','.pct-home-editing .pct-home-quick-actions','.pct-home-editing .pct-home-utility','.pct-home-editing .pct-home-search-panel'):
        check(forbidden not in sort_css,f'Sortiermodus verändert weiterhin den normalen Header: {forbidden}',errors)
    check('class="pct-home-edit-actions"' in start and 'role="toolbar"' in start and 'id="pctHomeDone"' in start,'Separates Sortier-Dock fehlt.',errors)
    final_css=css.split('/* === V2.6.5.1-Beta: strukturell icongebundene Favoriten',1)[-1]
    check(final_css.count('>.sk-app-icon-wrapper>.sk-favorite-button.pct-control')>=10,'Direkte Wrapper-Verankerung des Favoritenbuttons fehlt.',errors)
    check('calc(50%' not in final_css and '--sk-home-icon-top' not in final_css and '--sk-knowledge-icon-top' not in final_css,'Finale Favoritenposition hängt noch von Kachelmitte oder Geräteabständen ab.',errors)
    for token in ('SK_PCT_SHARED','buildSharedLayout','data-sk-shared-header','data-sk-shared-footer','skPctToolsFavoritesV2','search-index-v2-6-5-1.json','header-logo-simple.png','release-module-v2-6-5-1.png','v2-6-5-1-nav-home.png','v2-6-5-1-nav-search.png','v2-6-5-1-nav-favorite.png','const iconWrapper=card.querySelector',"iconWrapper.classList.add('sk-app-icon-wrapper')",'const host=iconWrapper||card','host.append(button)',"setAttribute('aria-pressed'",'pct-release-module','sk-release-number','sk-release-credit','fitReleaseModules','Tool by S.K.','sk-favorites-clear','sk-favorites-summary',"setAttribute('aria-modal','false')",'focusable=','removeFavorite','Alle leeren','frameHost=','suspendFrame','restoreFrame','sk-favorites-page-open'):
        check(token in js,f'Zentrale Laufzeit unvollständig: {token}',errors)
    for token in (
        "mode:'navigate'","phase:'idle'","grid.dataset.reorderEngine='pointer-overlay-v3'",
        'LONG_PRESS_TOUCH=420','MOVE_TOLERANCE_TOUCH=12','enterSort','exitSort',
        'beginDrag','commitDrag','cancelDrag','swallowClickCard','stopAutoScroll',
        'editActions.hidden=!sorting','dragSafeBounds','makePlaceholder','makeOverlay','moveOverlay','targetCardAt','document.elementsFromPoint',
        'pct-home-drop-placeholder','pct-home-drag-layer','pct-home-drag-overlay',
        'pushHistory','historyStep','pctHomeUndo','pctHomeRedo','sameOrder',
        'updateAutoScroll','pointercancel','lostpointercapture','visibilitychange','pagehide',
        "window.addEventListener('blur'","window.addEventListener('storage'",
        'stopImmediatePropagation',"state.mode==='sort'"
    ):
        check(token in js,f'Neue Reorder-Zustandsmaschine unvollständig: {token}',errors)
    for obsolete in ('suppressedClick','until:now()+700','clearClickSuppression','editing?360:480','suppressClick=false'):
        check(obsolete not in js,f'Alte Sortier-/Klicklogik noch vorhanden: {obsolete}',errors)
    check(start.count('Tool by S.K.')==2 and 'class="pct-home-release-module pct-release-module"' in start,'Startseiten-Release-Modul oder exakter Herkunftstext fehlt.',errors)
    check(not any(token in start+js for token in ('pct-version-plate','pct-home-version','sk-header-version','sk-version-value','sk-version-byline')),'Alte Versionsfeld-/Textpanel-Implementierung ist noch operativ.',errors)
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
            expected_alpha=(25,25,487,487) if stem.startswith('nav-') else (13,9,489,491)
            check(rgba.getchannel('A').getbbox()==expected_alpha,f'Sichtbare Icon-Grenze verändert: {icon.name}',errors)
            colored=sum(1 for r,g,b,a in pixels if a and not (r==g==b));black=sum(1 for r,g,b,a in pixels if a>240 and r<18 and g<18 and b<18);white=sum(1 for r,g,b,a in pixels if a>240 and r>245 and g>245 and b>245)
            check(colored>80000 and black>12000 and 10000<=white<=90000,f'Verlauf/Kontur/Symbolmasse fehlerhaft: {icon.name}',errors)
            if stem.startswith('nav-'):
                check(rgba.getpixel((52,256))[3]>240 and rgba.getpixel((52,256))[0]<80,f'Einzelner Cyan-/Blau-/Grün-Grundkörper fehlt: {icon.name}',errors)
                continue
            perimeter=bytearray()
            for i,pixel in enumerate(pixels):
                x=i%512;y=i//512
                if x<80 or x>=432 or y<72 or y>=420:perimeter.extend(pixel)
            check(hashlib.sha256(perimeter).hexdigest()==BACKGROUND_PERIMETER_SHA256,f'Hintergrundmaster verändert: {icon.name}',errors)
            check(rgba.getpixel((60,256))[1]>rgba.getpixel((60,256))[2],f'Grünseite fehlt: {icon.name}',errors)
            check(rgba.getpixel((400,90))[2]>rgba.getpixel((400,90))[1],f'Blauseite fehlt: {icon.name}',errors)

    search_icon=Image.open(nav_dir/f'{VERSION_SLUG}-nav-search.png').convert('RGBA')
    search_center=search_icon.getpixel((256,256))
    check(max(search_center[:3])>100 and not all(value<45 for value in search_center[:3]),f'Suche besitzt wieder eine schwarze Innenfläche: {search_center}',errors)
    favorite_center=Image.open(nav_dir/f'{VERSION_SLUG}-nav-favorite.png').convert('RGBA').getpixel((256,256))
    check(all(value>245 for value in favorite_center[:3]),f'Favoritensymbol ist nicht klar weiß: {favorite_center}',errors)

    # Neue Markenfamilie: Standardvarianten transparent, Maskable/iOS vollflächig
    # und die kontrastreiche Wort-/Motivmasse innerhalb der zentralen Safe-Zone.
    for name,(width,height,transparent) in BRAND_ASSETS.items():
        path=ROOT/'assets'/name
        check(path.is_file(),f'Marken-/PWA-Datei fehlt: {name}',errors)
        if not path.is_file():continue
        check(hashlib.sha256(path.read_bytes()).hexdigest()==BRAND_SHA256[name],f'Freigegebenes Logo-/PWA-Bild wurde verändert: {name}',errors)
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
    check(safe_white>6000 and unsafe_white<500,f'Maskable-Safe-Zone fehlerhaft: innen={safe_white}, außen={unsafe_white}',errors)
    header_logo=ROOT/'assets'/HEADER_LOGO
    legacy_header_logo=ROOT/'assets'/LEGACY_HEADER_LOGO
    check(header_logo.is_file() and hashlib.sha256(header_logo.read_bytes()).hexdigest()==HEADER_LOGO_SHA256,'Separate sichtbare Simple-Header-Logo-Datei fehlt oder wurde verändert.',errors)
    check(legacy_header_logo.is_file() and hashlib.sha256(legacy_header_logo.read_bytes()).hexdigest()==LEGACY_HEADER_LOGO_SHA256,'Bestehende Headerlogo-Datei wurde verändert oder entfernt.',errors)
    if header_logo.is_file():
        with Image.open(header_logo) as image:
            rgba=image.convert('RGBA');alpha=rgba.getchannel('A');pixels=list(rgba.get_flattened_data())
            check(rgba.size==(512,512) and alpha.getbbox()==(25,25,487,487) and alpha.getextrema()==(0,255),'Simple-Header-Logo-Geometrie fehlerhaft.',errors)
            black=sum(1 for r,g,b,a in pixels if a>240 and r<18 and g<18 and b<18)
            inner=[rgba.getpixel((x,y)) for y in range(512) for x in range(512) if (x-256)**2+(y-256)**2<=105**2]
            inner_dark=sum(1 for r,g,b,a in inner if a>240 and max(r,g,b)<45)
            inner_luminance=sum(.2126*r+.7152*g+.0722*b for r,g,b,a in inner)/len(inner)
            check(black>30000,'PCT-Zahnrad besitzt zu wenig klare Kontur-/Schriftmasse.',errors)
            check(9000<=inner_dark<=15000 and inner_luminance>=130,f'PCT-Zentrum ist nicht deutlich heller und ruhiger: dunkel={inner_dark}, Helligkeit={inner_luminance:.1f}.',errors)
            check(min(rgba.getpixel((256,190))[:3])>180,'Helle Cyan-Stahl-Innenfläche des PCT-Zahnrads fehlt.',errors)
    check('header-logo-simple.png' in start and 'alt="SK PCT Tools"' in start and "Tool's by S.K." not in start,'Separate textfreie Startseiten-Simple-Logo-Variante fehlt.',errors)
    check(LEGACY_HEADER_LOGO not in start+js+(ROOT/'service-worker.js').read_text(),'Alte Headerlogo-Datei ist weiterhin operativ referenziert.',errors)
    release_module=ROOT/'assets'/RELEASE_MODULE
    check(release_module.is_file() and hashlib.sha256(release_module.read_bytes()).hexdigest()==RELEASE_MODULE_SHA256,'Release-Modul-Haut fehlt oder wurde verändert.',errors)
    if release_module.is_file():
        with Image.open(release_module) as image:
            rgba=image.convert('RGBA')
            check(rgba.size==(1536,512) and rgba.getchannel('A').getbbox()==(25,25,1511,487),'Release-Modul-Geometrie fehlerhaft.',errors)
            left,center,right=rgba.getpixel((52,256)),rgba.getpixel((768,256)),rgba.getpixel((1484,256))
            check(left[1]>left[2] and center[1]>100 and center[2]>100 and right[2]>right[1],'Cyan-/Blau-/Grün-Materialität des Release-Moduls fehlt.',errors)
    for token in ('border:0;','background:transparent;','box-shadow:none;','overflow:visible;','width:var(--sk-header-logo-size);','height:var(--sk-header-logo-size);'):
        check(token in css,f'Rahmenloser Header-/Startseitenlogo-Standard fehlt: {token}',errors)

    knowledge=(ROOT/'wissensdatenbank/index.html').read_text()
    for slug,stem in KNOWLEDGE_ICON_MAP.items():
        check(knowledge.count(f'{VERSION_SLUG}-{stem}.png')==1,f'Eindeutiges Wissensicon fehlt oder ist doppelt: {slug}',errors)
    for slug in KNOWLEDGE_ARTICLES:
        article=(ROOT/'wissensdatenbank'/slug/'index.html').read_text()
        check('knowledge-compact.js' in article and EXPERIENCE_SOURCE in article,f'Wissensbeitrag unvollständig: {slug}',errors)

    worker=(ROOT/'service-worker.js').read_text()
    check("CACHE_EPOCH='v2-6-5-1-core-r1'" in worker,'Cache-Epoch falsch.',errors)
    check('DOCUMENT_CACHE' not in worker and 'OPTIONAL_DOCUMENTS' not in worker,'Nicht benötigter Dokumentcache noch vorhanden.',errors)
    cached=re.findall(r"'\./([^']+)'",worker)
    for ref in cached:check(target_exists(ROOT/'index.html',ref),f'Offline-Ziel fehlt: {ref}',errors)
    for icon in NAV_ICONS:check(f"'./assets/navigation-icons/{icon}'" in worker,f'Icon fehlt im Offline-Cache: {icon}',errors)
    for brand in BRAND_ASSETS:check(f"'./assets/{brand}'" in worker,f'Marken-/PWA-Datei fehlt im Offline-Cache: {brand}',errors)
    check(f"'./assets/{HEADER_LOGO}'" in worker,'Separate Headerlogo-Variante fehlt im Offline-Cache.',errors)
    check(f"'./assets/{RELEASE_MODULE}'" in worker,'Release-Modul-Haut fehlt im Offline-Cache.',errors)
    for stale in ('core.css','design-system.css','pct-frame.css','knowledge-cartoon.css','ICON-DESIGNRICHTLINIE.txt'):
        check(stale not in worker,f'Unnötiger Cache-Eintrag: {stale}',errors)

    generator=(ROOT/'tools/generate_png_icons.py').read_text()
    for token in ('PREFIX = "v2-6-5-1-"','RELEASE_MODULE_OUT','def navigation_frame()','def release_module_skin()','"app-analogsignal": app_analogsignal','"app-wissensdatenbank": app_knowledge_database','"knowledge-siemens-sps-rohwert": knowledge_sps_raw','"nav-search": nav_search','"nav-favorite": nav_favorite'):
        check(token in generator,f'Icon-Generator unvollständig: {token}',errors)
    brand_generator=(ROOT/'tools/generate_brand_assets.py').read_text()
    for token in ('def standard_master()','def header_master()','def maskable_master()','gear_points(256, 256)','root_radius: float = 145','tooth_radius: float = 176','root_radius=112','tooth_radius=138','"PCT", 108','result.putalpha(255)'):
        check(token in brand_generator,f'Markenlogo-Generator unvollständig: {token}',errors)
    check("TOOL'S BY S.K." not in brand_generator and 'Tool by SK' not in brand_generator,'Entfernter Herkunftstext ist noch im Markenlogo-Generator vorhanden.',errors)
    simple_generator=(ROOT/'tools/generate_header_logo_simple.py').read_text()
    for token in ('OUT = ROOT / "assets" / "header-logo-simple.png"','nav.navigation_frame()','teeth: int = 10','(209, 231, 235, 255)','"PCT", 76','Generated {OUT.relative_to(ROOT)} only'):
        check(token in simple_generator,f'Standalone-Simple-Headerlogo-Generator unvollständig: {token}',errors)
    for protected in BRAND_ASSETS:
        check(protected not in simple_generator,f'Simple-Headerlogo-Generator darf geschützte Datei nicht benennen: {protected}',errors)
    check(len({hashlib.sha256(p.read_bytes()).hexdigest() for p in icons})==24,'Icons sind nicht vollständig eigenständig.',errors)
    sprite=(ROOT/'assets/pct-controls.svg').read_text()
    for symbol in ('search','star','close','reset','chevron','copy','check','warning','info','print','trash','download','calculate','done'):
        check(f'id="icon-{symbol}"' in sprite,f'Control-Sprite unvollständig: icon-{symbol}',errors)
    for required in ('README.txt','RELEASE-NOTES.txt','ICON-DESIGNRICHTLINIE.txt','WISSENSBEITRAGS-STANDARD.md','TESTPLAN.md','TEST-RESULTS.txt','SECURITY-DEPLOYMENT.md','UEBERGABE-V2.6.5.1-Beta.txt','tests/design_regression.py','tests/design_audit_v2651.py'):
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
    print(f'PASS · {files} Dateien · 10 Apps · 6 Rechner · 14 interne Unterseiten · 24 Navigationsicons · 3 Browser-Testprogramme · {css.count("!important")} !important · Version {VERSION}')
    return 0

if __name__=='__main__':sys.exit(main())
