#!/usr/bin/env python3
"""Struktur- und Integritätsprüfung für SK PCT Tools 2.5.0.3-Beta."""
from __future__ import annotations
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.5.0.3-Beta"
EXPECTED_APPS = {
    "analogsignal", "pf-rechner", "pt-rechner", "messstellen-doku",
    "einheitenrechner", "einheitendatenbank", "werkstoffdatenbank",
    "wissensdatenbank", "spannungsfall-rechner", "siemens-rohwert",
    "eh-device-viewer",
}

class StartParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.apps: list[dict[str, str]] = []
        self.local_refs: list[str] = []
        self.icon_uses: list[str] = []
    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        classes = set(values.get("class", "").split())
        if tag == "a" and "sk-home-app" in classes:
            self.apps.append(values)
        if tag in {"script", "link", "img", "a"}:
            attr = "href" if tag in {"link", "a"} else "src"
            value = values.get(attr)
            if value and not urlsplit(value).scheme and not value.startswith(("#", "mailto:", "tel:")):
                self.local_refs.append(value)
        if tag == "use" and values.get("href"):
            self.icon_uses.append(values["href"])

def fail(message: str, errors: list[str]) -> None:
    errors.append(message)

def target_exists(ref: str, source: Path = ROOT / "index.html") -> bool:
    path = urlsplit(ref).path
    target = (source.parent / path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return False
    return target.is_file() or (target.is_dir() and (target / "index.html").is_file())

def main() -> int:
    errors: list[str] = []
    if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != VERSION:
        fail("VERSION stimmt nicht.", errors)
    manifest = json.loads((ROOT / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest.get("version") != VERSION:
        fail("Manifest-Version stimmt nicht.", errors)
    parser = StartParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    ids = [app.get("data-app-id", "") for app in parser.apps]
    if len(ids) != 11 or set(ids) != EXPECTED_APPS or len(ids) != len(set(ids)):
        fail(f"App-Inventar unvollständig oder nicht eindeutig: {ids}", errors)
    for app in parser.apps:
        if not app.get("aria-label") or not app.get("href"):
            fail(f"App ohne zugänglichen Namen oder Ziel: {app}", errors)
        if not urlsplit(app.get("href", "")).scheme and not target_exists(app["href"]):
            fail(f"App-Ziel fehlt: {app['href']}", errors)
    if len(parser.icon_uses) != 11 or len(set(parser.icon_uses)) != 11:
        fail("Jede App muss genau ein eigenes Symbol verwenden.", errors)
    for ref in parser.icon_uses:
        sprite, _, symbol = ref.partition("#")
        if not target_exists(sprite) or not symbol:
            fail(f"Ungültige Symbolreferenz: {ref}", errors)
    for ref in parser.local_refs:
        if not target_exists(ref):
            fail(f"Lokale Startseitenreferenz fehlt: {ref}", errors)
    worker = (ROOT / "service-worker.js").read_text(encoding="utf-8")
    for required in (
        "./assets/pct-home.css", "./assets/pct-home.js", "./assets/pct-home-icons.svg",
        "./assets/knowledge-overview.css", "./assets/knowledge-overview.js",
        "./assets/knowledge-manufacturer-logos.svg",
    ):
        if required not in worker:
            fail(f"Offline-Kerncache enthält {required} nicht.", errors)

    cached_refs = re.findall(r"'\./([^']+)'", worker)
    for ref in cached_refs:
        if not target_exists(ref):
            fail(f"Offline-Cache-Ziel fehlt: {ref}", errors)
    if "icon-" + "tree" in (ROOT / "assets/pct-controls.svg").read_text(encoding="utf-8"):
        fail("Entferntes Hierarchie-Symbol noch vorhanden.", errors)

    runtime_files = [ROOT / "index.html", ROOT / "assets/app.js", ROOT / "assets/pct-home.js", ROOT / "service-worker.js"]
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        if VERSION not in text:
            fail(f"Versionskennung fehlt in {path.relative_to(ROOT)}.", errors)
        if "2.4.2.1" in text:
            fail(f"Alte Laufzeitversion in {path.relative_to(ROOT)} gefunden.", errors)

    start_html = (ROOT / "index.html").read_text(encoding="utf-8")
    if "viewport-fit=cover" not in start_html:
        fail("Startseite aktiviert viewport-fit=cover nicht.", errors)
    forbidden_home = ("pctHomeClock", "pctHomeDate", "pct-home-heading", "pctHomeEdit", "skCompactCardsToggle")
    for token in forbidden_home:
        if token in start_html:
            fail(f"Entferntes Startseitenelement noch vorhanden: {token}", errors)
    for required_home in ("pctHomeGrid", "skFilterToggle", "pctHomeDone", "pctHomeReset", "pct-home-brand-mark"):
        if required_home not in start_html:
            fail(f"Erforderliches Startseitenelement fehlt: {required_home}", errors)
    if start_html.index("pct-home-brand-mark") < start_html.index("pct-home-screen"):
        fail("Das Startseitenlogo liegt nicht innerhalb des PCT Home-Screens.", errors)
    knowledge_html = (ROOT / "wissensdatenbank" / "index.html").read_text(encoding="utf-8")
    if "viewport-fit=cover" not in knowledge_html:
        fail("Wissensdatenbank aktiviert viewport-fit=cover nicht.", errors)
    if knowledge_html.index("sk:header:start") < knowledge_html.index("knowledge-home-screen"):
        fail("Der Wissensdatenbank-Kopf liegt nicht im abgerundeten App-Paket.", errors)
    if knowledge_html.count('class="knowledge-entry tool-card"') != 5:
        fail("Die Wissensdatenbank muss genau fünf vorhandene Fachbeiträge enthalten.", errors)
    for logo in ("logo-air-torque", "logo-endress-hauser", "logo-siemens", "logo-vacon"):
        if f"knowledge-manufacturer-logos.svg#{logo}" not in knowledge_html:
            fail(f"Herstellerkennzeichnung fehlt: {logo}", errors)
    home_css = (ROOT / "assets" / "pct-home.css").read_text(encoding="utf-8")
    knowledge_css = (ROOT / "assets" / "knowledge-overview.css").read_text(encoding="utf-8")
    for label, css in (("Startseite", home_css), ("Wissensdatenbank", knowledge_css)):
        for inset in ("safe-area-inset-top", "safe-area-inset-left", "safe-area-inset-right"):
            if inset not in css:
                fail(f"{label} berücksichtigt {inset} nicht.", errors)
    if 'data-manufacturer="' in knowledge_css:
        fail("Herstellerspezifische farbige Icon-Gründe sind noch vorhanden.", errors)
    manufacturer_svg = (ROOT / "assets" / "knowledge-manufacturer-logos.svg").read_text(encoding="utf-8")
    for logo in ("logo-air-torque", "logo-endress-hauser", "logo-siemens", "logo-vacon"):
        match = re.search(rf'<symbol id="{re.escape(logo)}".*?</symbol>', manufacturer_svg, re.S)
        if not match:
            fail(f"SVG-Wortmarke fehlt: {logo}", errors)
            continue
        symbol = match.group(0)
        if "currentColor" not in symbol or re.search(r'#[0-9a-fA-F]{3,8}', symbol) or "<rect" in symbol:
            fail(f"Herstellerkennzeichnung ist nicht als reduzierte weiße/monochrome Marke umgesetzt: {logo}", errors)
    if ">E+H<" not in manufacturer_svg:
        fail("E+H-Kurzmarke fehlt.", errors)
    for required_knowledge in ("knowledgeSearch", "knowledgeCompactToggle", "knowledgeGrid", "Wissensdatenbank_Beitragsvorlage.pdf"):
        if required_knowledge not in knowledge_html:
            fail(f"Erforderliche Wissensdatenbank-Funktion fehlt: {required_knowledge}", errors)
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
    if (ROOT / "assets/navigation-tree.json").exists():
        fail("Navigationsdaten wurden nicht entfernt.", errors)

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
        for error in errors: print(f"- {error}")
        return 1
    print(f"PASS · {len(ids)} Apps · {len(parser.icon_uses)} eindeutige Symbole · Version {VERSION}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
