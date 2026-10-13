#!/usr/bin/env python3
"""Struktur- und Integritätsprüfung für SK PCT Tools 2.5.0.6-Beta."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.5.0.6-Beta"
EXPECTED_APPS = {
    "analogsignal", "pf-rechner", "pt-rechner", "messstellen-doku",
    "einheitenrechner", "einheitendatenbank", "werkstoffdatenbank",
    "wissensdatenbank", "spannungsfall-rechner", "siemens-rohwert",
    "eh-device-viewer",
}
EXPECTED_MANUFACTURERS = {
    "air-torque": 1,
    "endress-hauser": 1,
    "siemens": 2,
    "vacon": 1,
    "sonstiges": 0,
}

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.apps: list[dict[str, str]] = []
        self.hub_cards: list[dict[str, str]] = []
        self.entries: list[dict[str, str]] = []
        self.views: list[dict[str, str]] = []
        self.local_refs: list[str] = []
        self.icon_uses: list[str] = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = set(values.get("class", "").split())
        if tag == "a" and "sk-home-app" in classes:
            self.apps.append(values)
        if tag == "a" and "knowledge-hub-card" in classes:
            self.hub_cards.append(values)
        if tag == "a" and "knowledge-entry" in classes:
            self.entries.append(values)
        if tag == "section" and "knowledge-manufacturer-view" in classes:
            self.views.append(values)
        if tag in {"script", "link", "img", "a"}:
            attr = "href" if tag in {"link", "a"} else "src"
            value = values.get(attr)
            if value and not urlsplit(value).scheme and not value.startswith(("#", "mailto:", "tel:")):
                self.local_refs.append(value)
        if tag == "use" and values.get("href"):
            self.icon_uses.append(values["href"])

def fail(message: str, errors: list[str]) -> None:
    errors.append(message)

def target_exists(ref: str, source: Path) -> bool:
    path = urlsplit(ref).path
    target = (source.parent / path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return False
    return target.is_file() or (target.is_dir() and (target / "index.html").is_file())

def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser

def main() -> int:
    errors: list[str] = []
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        fail("VERSION stimmt nicht.", errors)
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        fail("Manifest-Version stimmt nicht.", errors)

    start_path = ROOT / "index.html"
    start_html = start_path.read_text(encoding="utf-8")
    start = parse_page(start_path)
    ids = [app.get("data-app-id", "") for app in start.apps]
    if len(ids) != 11 or set(ids) != EXPECTED_APPS or len(ids) != len(set(ids)):
        fail(f"App-Inventar unvollständig oder nicht eindeutig: {ids}", errors)
    for app in start.apps:
        if not app.get("aria-label") or not app.get("href"):
            fail(f"App ohne zugänglichen Namen oder Ziel: {app}", errors)
        elif not urlsplit(app["href"]).scheme and not target_exists(app["href"], start_path):
            fail(f"App-Ziel fehlt: {app['href']}", errors)
    if len(start.icon_uses) != 11 or len(set(start.icon_uses)) != 11:
        fail("Jede App muss genau ein eigenes Symbol verwenden.", errors)
    for ref in start.local_refs:
        if not target_exists(ref, start_path):
            fail(f"Lokale Startseitenreferenz fehlt: {ref}", errors)
    if "viewport-fit=cover" not in start_html:
        fail("Startseite aktiviert viewport-fit=cover nicht.", errors)
    if "pct-home-brand-copy" in start_html or "<strong>SK PCT Tools</strong>" in start_html:
        fail("Der sichtbare weiße Produkttext wurde nicht aus dem Startseitenkopf entfernt.", errors)
    for required in ("pctHomeGrid", "skFilterToggle", "pctHomeDone", "pctHomeReset", "pct-home-brand-mark", "pct-home-version", "pct-home-quick-actions", "sk-favorites-trigger"):
        if required not in start_html:
            fail(f"Erforderliches Startseitenelement fehlt: {required}", errors)
    if start_html.count('class="sk-favorites-trigger"') != 1:
        fail("Die Startseite muss genau einen Favoriten-Schnellzugriff enthalten.", errors)
    if not re.search(r'<section[^>]*class="pct-home-screen".*?<footer[^>]*class="[^"]*pct-home-footer[^"]*".*?</footer>.*?</section>', start_html, re.S):
        fail("Der Startseitenfooter liegt nicht vollständig im abgerundeten Home-Rechteck.", errors)

    knowledge_path = ROOT / "wissensdatenbank" / "index.html"
    knowledge_html = knowledge_path.read_text(encoding="utf-8")
    knowledge = parse_page(knowledge_path)
    if "viewport-fit=cover" not in knowledge_html:
        fail("Wissensdatenbank aktiviert viewport-fit=cover nicht.", errors)
    hub_slugs = [card.get("data-manufacturer-slug", "") for card in knowledge.hub_cards]
    if len(hub_slugs) != 5 or set(hub_slugs) != set(EXPECTED_MANUFACTURERS) or len(hub_slugs) != len(set(hub_slugs)):
        fail(f"Hersteller-Hub unvollständig oder nicht eindeutig: {hub_slugs}", errors)
    if len(knowledge.entries) != 5:
        fail(f"Es müssen genau fünf vorhandene Fachbeiträge erhalten bleiben, gefunden: {len(knowledge.entries)}", errors)
    view_slugs = [view.get("data-manufacturer-slug", "") for view in knowledge.views]
    if len(view_slugs) != 5 or set(view_slugs) != set(EXPECTED_MANUFACTURERS):
        fail(f"Herstelleransichten unvollständig: {view_slugs}", errors)
    for slug, expected_count in EXPECTED_MANUFACTURERS.items():
        pattern = rf'<section class="knowledge-manufacturer-view"[^>]*data-manufacturer-slug="{re.escape(slug)}".*?</section>'
        match = re.search(pattern, knowledge_html, re.S)
        if not match:
            fail(f"Herstelleransicht fehlt: {slug}", errors)
        else:
            count = match.group(0).count('class="knowledge-entry tool-card"')
            if count != expected_count:
                fail(f"Falsche Beitragszahl für {slug}: {count} statt {expected_count}", errors)
    for slug in EXPECTED_MANUFACTURERS:
        if f'href="?manufacturer={slug}"' not in knowledge_html:
            fail(f"Herstellerlink fehlt: {slug}", errors)
    for required in ("knowledgeSearch", "knowledgeCompactToggle", "knowledgeHub", "knowledgeViews", "Wissensdatenbank_Beitragsvorlage.pdf"):
        if required not in knowledge_html:
            fail(f"Erforderliche Wissensdatenbank-Funktion fehlt: {required}", errors)
    for logo in ("logo-air-torque", "logo-endress-hauser", "logo-siemens", "logo-vacon", "logo-sonstiges"):
        if f"knowledge-manufacturer-logos.svg#{logo}" not in knowledge_html:
            fail(f"Herstellerkennzeichnung fehlt: {logo}", errors)
    for ref in knowledge.local_refs:
        if not target_exists(ref, knowledge_path):
            fail(f"Lokale Wissensdatenbank-Referenz fehlt: {ref}", errors)

    home_css = (ROOT / "assets" / "pct-home.css").read_text(encoding="utf-8")
    knowledge_css = (ROOT / "assets" / "knowledge-overview.css").read_text(encoding="utf-8")
    for label, css in (("Startseite", home_css), ("Wissensdatenbank", knowledge_css)):
        required_insets = ("safe-area-inset-top", "safe-area-inset-left", "safe-area-inset-right")
        if label == "Startseite":
            required_insets += ("safe-area-inset-bottom",)
        for inset in required_insets:
            if inset not in css:
                fail(f"{label} berücksichtigt {inset} nicht.", errors)
    for token in ("--pct-home-action-size:46px", "--pct-home-action-size:42px", "--pct-home-logo-size:calc((var(--pct-home-action-size) * 2) + var(--pct-home-action-gap))", ".pct-home-screen>.pct-home-footer", ".pct-home-search-trigger{display:grid;place-items:center", "grid-template-columns:repeat(6", "grid-template-columns:repeat(4", "grid-template-columns:repeat(3"):
        if token not in home_css:
            fail(f"Startseiten-Designregel fehlt: {token}", errors)
    for token in (".knowledge-hub", ".knowledge-manufacturer-view", ".knowledge-grid", ".knowledge-view-back"):
        if token not in knowledge_css:
            fail(f"Hersteller-Hub-Designregel fehlt: {token}", errors)

    overview_js = (ROOT / "assets" / "knowledge-overview.js").read_text(encoding="utf-8")
    for token in ("popstate", "history.pushState", "knowledge-hub-card", "knowledge-entry"):
        if token not in overview_js:
            fail(f"Herstelleransichts-Logik fehlt: {token}", errors)
    # URLSearchParams is expressed through URL(...).searchParams in the implementation.
    if "URLSearchParams" not in overview_js and ".searchParams.get('manufacturer')" not in overview_js:
        fail("Herstellerparameter wird nicht ausgewertet.", errors)

    manufacturer_svg = (ROOT / "assets" / "knowledge-manufacturer-logos.svg").read_text(encoding="utf-8")
    for logo in ("logo-air-torque", "logo-endress-hauser", "logo-siemens", "logo-vacon", "logo-sonstiges"):
        if not re.search(rf'<symbol id="{re.escape(logo)}".*?</symbol>', manufacturer_svg, re.S):
            fail(f"SVG-Symbol fehlt: {logo}", errors)
    if ">E+H<" not in manufacturer_svg:
        fail("E+H-Kurzmarke fehlt.", errors)

    worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    for required in ("./assets/pct-home.css", "./assets/pct-home.js", "./assets/pct-home-icons.svg", "./assets/knowledge-overview.css", "./assets/knowledge-overview.js", "./assets/knowledge-manufacturer-logos.svg", "./wissensdatenbank/"):
        if required not in worker:
            fail(f"Offline-Kerncache enthält {required} nicht.", errors)
    cached_refs = re.findall(r"'\./([^']+)'", worker)
    for ref in cached_refs:
        if not target_exists(ref, ROOT / "index.html"):
            fail(f"Offline-Cache-Ziel fehlt: {ref}", errors)

    runtime_files = [ROOT / "index.html", ROOT / "assets/app.js", ROOT / "assets/pct-home.js", ROOT / "assets/knowledge-overview.js", ROOT / "service-worker.js"]
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        if VERSION not in text:
            fail(f"Versionskennung fehlt in {path.relative_to(ROOT)}.", errors)
        if "2.5.0.5-Beta" in text:
            fail(f"Alte Laufzeitversion in {path.relative_to(ROOT)} gefunden.", errors)

    forbidden_tree = ("sk" + "-tree", "navigation" + "-tree", "Navigations" + "baum", "Seitennavi" + "gation")
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.name == "SHA256SUMS.txt" or path.resolve() == Path(__file__).resolve():
            continue
        if path.suffix.lower() not in {".html", ".js", ".css", ".json", ".md", ".txt", ".webmanifest"}:
            continue
        content = path.read_text(encoding="utf-8")
        for token in forbidden_tree:
            if token in content:
                fail(f"Rest der entfernten Hierarchienavigation in {path.relative_to(ROOT)}: {token}", errors)

    sums = ROOT / "SHA256SUMS.txt"
    if sums.is_file():
        for line in sums.read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                fail(f"Ungültige Prüfsummenzeile: {line}", errors); continue
            expected, rel = match.groups(); path = ROOT / rel.removeprefix("./")
            if not path.is_file():
                fail(f"Prüfsummendatei fehlt: {rel}", errors); continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != expected:
                fail(f"Prüfsumme falsch: {rel}", errors)
    else:
        fail("SHA256SUMS.txt fehlt.", errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS · {len(ids)} Apps · {len(knowledge.hub_cards)} Hersteller-Bereiche · {len(knowledge.entries)} Wissensbeiträge · Version {VERSION}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
