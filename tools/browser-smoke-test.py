#!/usr/bin/env python3
"""Browser smoke test for SK PLT Tools 2.1.0.5-Beta."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test-artifacts"
OUT.mkdir(exist_ok=True)
BASE = "http://127.0.0.1:4173"
VERSION = "2.1.0.5-Beta"
APP_ID = f"./?app=sk-plt-tools-{VERSION.lower()}"


def assert_text(page, selector, expected):
    actual = page.locator(selector).inner_text().strip()
    assert actual == expected, f"{selector}: expected {expected!r}, got {actual!r}"


def set_input(page, selector, value):
    page.locator(selector).fill(str(value))
    page.locator(selector).dispatch_event("input")


def assert_box(page, selector, width, height, tolerance=1):
    box = page.locator(selector).bounding_box()
    assert box, f"{selector}: kein sichtbares Rechteck"
    assert abs(box["width"] - width) <= tolerance, f"{selector}: Breite {box['width']} statt {width}"
    assert abs(box["height"] - height) <= tolerance, f"{selector}: Höhe {box['height']} statt {height}"


PAGES = [
    "/", "/analogsignal/", "/siemens-analogwert-rechner/", "/einheitenrechner/", "/messstellen-doku/",
    "/pf-rechner/", "/pt-rechner/", "/servicewerte/", "/spannungsfall-rechner/",
    "/plausibilitaetspruefung-vde0100-600/", "/wissensdatenbank/",
    "/wissensdatenbank/air-torque-antrieb-drehrichtung/",
    "/wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/", "/wissensdatenbank/siemens-sps-rohwert/",
    "/wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/",
    "/wissensdatenbank/werkstoff-nachschlagewerk/"
]


with sync_playwright() as p:
    executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    browser = p.chromium.launch(headless=True, executable_path=executable) if executable else p.chromium.launch(headless=True)
    console_errors = []

    desktop = browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
    desktop.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    desktop.goto(f"{BASE}/siemens-analogwert-rechner/")
    desktop.wait_for_load_state("networkidle")
    assert desktop.locator("body").get_attribute("data-sk-version") == VERSION
    assert desktop.locator("header.sk-global-header").bounding_box()["height"] <= 88
    assert_box(desktop, ".sk-favorites-trigger", 48, 48)
    assert_box(desktop, ".sk-tree-trigger", 48, 48)
    assert_text(desktop, "h1", "Siemens Rohwert")
    assert desktop.locator("#cardProfile option").count() == 5
    assert desktop.locator("#signalType option").count() == 4
    assert desktop.locator("#inputKind option").count() == 2
    assert_text(desktop, "#rawResult", "13.824")
    assert_text(desktop, "#signalResult", "12,000 mA")
    assert desktop.locator("#sliderScale span").all_inner_texts() == ["-32.768", "-4.865", "0", "27.648", "32.512", "32.767"]

    for raw, status in [("-4865", "Unterlauf"), ("-4864", "Untersteuerung"), ("0", "Nennbereich"), ("27648", "Nennbereich"), ("27649", "Übersteuerung"), ("32512", "Überlauf")]:
        set_input(desktop, "#inputValue", raw)
        assert_text(desktop, "#rangeStatus", status)

    set_input(desktop, "#inputValue", "13824")
    desktop.locator("#inputKind").select_option("signal")
    assert float(desktop.locator("#inputValue").input_value()) == 12.0
    desktop.locator("#signalType").select_option("0-20mA")
    assert float(desktop.locator("#inputValue").input_value()) == 10.0
    set_input(desktop, "#inputValue", "15")
    assert_text(desktop, "#rawResult", "20.736")

    desktop.locator("#cardProfile").select_option("et200spha_on")
    assert desktop.locator('#signalType option[value="0-20mA"]').evaluate("option => option.disabled")
    desktop.locator("#inputKind").select_option("raw")
    for raw, status in [("-691", "Unterlauf"), ("-690", "Untersteuerung"), ("-345", "Nennbereich"), ("28511", "Nennbereich"), ("28512", "Übersteuerung"), ("29376", "Überlauf")]:
        set_input(desktop, "#inputValue", raw)
        assert_text(desktop, "#rangeStatus", status)

    desktop.locator("#cardProfile").select_option("s71500_fai_scale")
    assert_text(desktop, "#rangeStatus", "Nur Umrechnung")
    assert desktop.locator("#stateStrip").is_hidden()
    card_info = desktop.locator("details.analog-card-info")
    assert not card_info.get_attribute("open")
    card_info.locator("summary").click()
    assert card_info.get_attribute("open") is not None
    assert "nicht bewertet" in desktop.locator("#statusDetail").inner_text().lower()
    desktop.screenshot(path=str(OUT / "siemens-desktop.png"), full_page=True)

    desktop.goto(f"{BASE}/wissensdatenbank/")
    desktop.wait_for_load_state("networkidle")
    knowledge = desktop.locator('a.knowledge-entry[href="siemens-sps-rohwert/"]')
    assert knowledge.count() == 1
    assert_text(desktop, 'a.knowledge-entry[href="siemens-sps-rohwert/"] h2', "Rohwert Grundlagen")

    desktop.goto(f"{BASE}/wissensdatenbank/siemens-sps-rohwert/")
    desktop.wait_for_load_state("networkidle")
    assert desktop.locator('a.cta').get_attribute('href') == '../../siemens-analogwert-rechner/'
    assert '12 mA = 13824' in desktop.locator('main').inner_text()
    assert desktop.locator('.sk-logo-version').count() == 0
    assert 'Version ' not in desktop.locator('footer.sk-footer').inner_text()
    breadcrumb_links = desktop.locator('.knowledge-breadcrumb a')
    assert breadcrumb_links.count() == 2
    assert breadcrumb_links.all_inner_texts() == ['Startseite', 'Wissensdatenbank']
    assert breadcrumb_links.evaluate_all("links => links.map(link => getComputedStyle(link).color)") == ['rgb(0, 183, 232)', 'rgb(0, 183, 232)']
    desktop.screenshot(path=str(OUT / "rohwert-grundlagen-desktop.png"), full_page=True)

    desktop.goto(f"{BASE}/")
    desktop.wait_for_load_state("networkidle")
    external = desktop.locator('a.sk-external-card')
    assert external.count() == 1
    assert external.get_attribute("href") == "https://netilion.endress.com/app/library/device_viewer"
    assert external.get_attribute("target") == "_blank"
    assert set((external.get_attribute("rel") or "").split()) >= {"external", "noopener", "noreferrer"}
    assert external.get_attribute("referrerpolicy") == "no-referrer"
    assert_text(desktop, '.hero .badge', f'Version {VERSION}')
    assert desktop.locator(f'text=Version {VERSION}').count() == 1

    # Suche und Suchübergabe in das getrennte Werkstoffmodul.
    desktop.locator('#skToolSearch').fill('316L')
    desktop.wait_for_function("document.querySelectorAll('#skKnowledgeResultList > a').length > 0")
    material_hit = desktop.locator('#skKnowledgeResultList a[href*="werkstoff-nachschlagewerk"]')
    assert material_hit.count() == 1
    assert 'q=316L' in material_hit.get_attribute('href')
    assert '1 Beitrag' in desktop.locator('#skFilterResult').inner_text()
    desktop.locator('#skFilterReset').click()
    assert desktop.locator('.tools > a.card:visible').count() == 10

    # Kategorie und Sortierung.
    desktop.locator('.sk-filter-button[data-filter="RECHNER"]').click()
    assert desktop.locator('.tools > a.card:visible').count() == 6
    desktop.locator('#skFilterReset').click()
    desktop.locator('#skToolSort').select_option('title-asc')
    sorted_titles = desktop.locator('.tools > a.card h2').all_inner_texts()
    assert sorted_titles == sorted(sorted_titles, key=lambda value: value.casefold())
    desktop.locator('#skToolSort').select_option('default')

    # Favoriten per UI hinzufügen, nach Reload wiederfinden und entfernen.
    analog_card = desktop.locator('.tools > a.card[href="analogsignal/"]')
    analog_card.locator('.sk-favorite-button').click()
    desktop.locator('.sk-favorites-trigger').click()
    assert_text(desktop, '.sk-favorites-list strong', 'Analogsignal-Rechner')
    desktop.locator('.sk-favorites-close').click()
    desktop.reload()
    desktop.wait_for_load_state('networkidle')
    desktop.locator('.sk-favorites-trigger').click()
    assert_text(desktop, '.sk-favorites-list strong', 'Analogsignal-Rechner')
    desktop.locator('.sk-favorite-remove').click()
    assert_text(desktop, '.sk-favorites-empty strong', 'Noch keine Favoriten')
    desktop.locator('.sk-favorites-close').click()

    desktop.locator('.sk-tree-trigger').click()
    desktop.wait_for_timeout(300)
    knowledge_group = desktop.locator('.sk-tree-group-toggle[data-group="knowledge"]')
    assert knowledge_group.get_attribute('aria-expanded') == 'true'
    knowledge_row = desktop.locator('.sk-tree-group-toggle[data-group="knowledge"] + .sk-tree-list > .sk-tree-item.has-children > .sk-tree-node-row')
    assert knowledge_row.count() == 1
    assert_text(desktop, '.sk-tree-group-toggle[data-group="knowledge"] + .sk-tree-list > .sk-tree-item.has-children > .sk-tree-node-row > .sk-tree-link', 'Wissensdatenbank')
    assert desktop.locator('.sk-tree-node-toggle a').count() == 0
    assert knowledge_row.evaluate("row => getComputedStyle(row).backgroundColor") == 'rgb(10, 38, 57)'
    assert knowledge_group.evaluate("button => getComputedStyle(button).backgroundColor") == 'rgb(10, 38, 57)'
    assert knowledge_row.locator('.sk-tree-chevron').inner_text() == '⌄'
    assert knowledge_row.locator('.sk-tree-node-toggle').evaluate("button => getComputedStyle(button).color") == 'rgb(137, 211, 41)'
    row_box = knowledge_row.bounding_box()
    toggle_box = knowledge_row.locator('.sk-tree-node-toggle').bounding_box()
    link_box = knowledge_row.locator('.sk-tree-link').bounding_box()
    assert row_box and toggle_box and link_box
    assert row_box['x'] <= toggle_box['x'] and toggle_box['x'] + toggle_box['width'] <= row_box['x'] + row_box['width']
    assert row_box['x'] <= link_box['x'] and link_box['x'] + link_box['width'] <= row_box['x'] + row_box['width']
    assert abs((toggle_box['y'] + toggle_box['height'] / 2) - (row_box['y'] + row_box['height'] / 2)) <= 1
    assert desktop.get_by_text('Rohwert Grundlagen', exact=True).count() == 1
    assert desktop.get_by_text('Rohwert-Rechner', exact=True).count() == 0
    desktop.screenshot(path=str(OUT / "navigation-wissen-desktop.png"), full_page=True)
    desktop.locator('.sk-tree-close').click()
    desktop.wait_for_function("document.querySelector('.sk-tree-drawer').getBoundingClientRect().left >= window.innerWidth")
    desktop.screenshot(path=str(OUT / "startseite-desktop.png"), full_page=True)

    # VDE-Prüfung: messwertzentrierte Oberfläche ohne sichtbare Mustervorlage
    # und ohne formale Bewertungselemente.
    desktop.goto(f"{BASE}/plausibilitaetspruefung-vde0100-600/")
    desktop.wait_for_load_state("networkidle")
    assert "PDF oder Smartphone-Foto" in desktop.locator("#uploadPanel").inner_text()
    assert "Ausschließlich Messwerte" in desktop.locator("#uploadPanel").inner_text()
    assert desktop.locator("#loadSample").count() == 0
    assert desktop.locator('a[href*="VDEProtokoll.pdf"]').count() == 0
    assert desktop.locator("text=Formularpassung").count() == 0
    assert desktop.locator("#notRelevant").count() == 0
    assert desktop.locator("#useForm").count() == 0
    assert desktop.locator("#manualFormReview").count() == 0
    assert desktop.locator("#replaceFile").count() == 0
    assert desktop.locator("#confirmFail").is_hidden()
    assert desktop.locator("#resultPanel").is_hidden()
    assert "Namen" in desktop.locator(".template-note").inner_text()
    assert "Unterschriften" in desktop.locator(".template-note").inner_text()
    desktop.screenshot(path=str(OUT / "vde-messwert-upload-desktop.png"), full_page=True)

    tablet = browser.new_page(viewport={"width": 820, "height": 1180}, device_scale_factor=2, is_mobile=True)
    tablet.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    for route in PAGES:
        tablet.goto(f"{BASE}{route}")
        tablet.wait_for_load_state("networkidle")
        assert tablet.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"Horizontales Überlaufen: {route}"
        assert tablet.locator("body").get_attribute("data-sk-version") == VERSION
        assert tablet.locator("header.sk-global-header").bounding_box()["height"] <= 88
        assert_box(tablet, ".sk-favorites-trigger", 48, 48)
        assert_box(tablet, ".sk-tree-trigger", 48, 48)
    tablet.goto(f"{BASE}/siemens-analogwert-rechner/")
    tablet.wait_for_load_state("networkidle")
    assert tablet.locator("details.analog-card-info").get_attribute("open") is None
    tablet.screenshot(path=str(OUT / "siemens-tablet.png"), full_page=True)

    mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    mobile.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    mobile.goto(f"{BASE}/siemens-analogwert-rechner/")
    mobile.wait_for_load_state("networkidle")
    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    assert mobile.locator("header.sk-global-header").bounding_box()["height"] <= 76
    assert_box(mobile, ".sk-favorites-trigger", 42, 42)
    assert_box(mobile, ".sk-tree-trigger", 42, 42)
    assert mobile.locator("#cardProfile").is_visible()
    assert mobile.locator("details.analog-card-info").get_attribute("open") is None
    input_box = mobile.locator(".analog-input-shell").bounding_box()
    input_field_box = mobile.locator("#inputValue").bounding_box()
    suffix_box = mobile.locator("#inputSuffix").bounding_box()
    assert input_box["height"] <= 41
    assert abs(input_field_box["y"] - suffix_box["y"]) <= 1
    assert mobile.locator(".analog-state-strip span").first.bounding_box()["height"] <= 29
    mobile.screenshot(path=str(OUT / "siemens-mobile.png"), full_page=True)
    for route in PAGES:
        mobile.goto(f"{BASE}{route}")
        mobile.wait_for_load_state("networkidle")
        assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"Mobiles Überlaufen: {route}"
        assert_box(mobile, ".sk-favorites-trigger", 42, 42)
        assert_box(mobile, ".sk-tree-trigger", 42, 42)
    mobile.goto(f"{BASE}/")
    mobile.wait_for_load_state("networkidle")
    mobile.locator('.sk-tree-trigger').click()
    mobile.wait_for_timeout(300)
    mobile_row = mobile.locator('.sk-tree-group-toggle[data-group="knowledge"] + .sk-tree-list > .sk-tree-item.has-children > .sk-tree-node-row')
    mobile_row_box = mobile_row.bounding_box()
    mobile_toggle_box = mobile_row.locator('.sk-tree-node-toggle').bounding_box()
    mobile_link_box = mobile_row.locator('.sk-tree-link').bounding_box()
    assert mobile_row_box and mobile_toggle_box and mobile_link_box
    assert mobile_row_box['x'] <= mobile_toggle_box['x'] and mobile_toggle_box['x'] + mobile_toggle_box['width'] <= mobile_row_box['x'] + mobile_row_box['width']
    assert mobile_row_box['x'] <= mobile_link_box['x'] and mobile_link_box['x'] + mobile_link_box['width'] <= mobile_row_box['x'] + mobile_row_box['width']
    assert abs((mobile_toggle_box['y'] + mobile_toggle_box['height'] / 2) - (mobile_row_box['y'] + mobile_row_box['height'] / 2)) <= 1
    mobile.screenshot(path=str(OUT / "navigation-wissen-mobile.png"))
    mobile.locator('.sk-tree-close').click()
    mobile.goto(f"{BASE}/analogsignal/")
    mobile.wait_for_load_state("networkidle")
    assert abs(mobile.locator("button.sign").first.bounding_box()["width"] - 38) <= 1

    # PWA-Metadaten, Service Worker und echter Offline-Aufruf aus dem Cache.
    pwa = browser.new_page(viewport={"width": 1280, "height": 900})
    pwa.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    pwa.goto(f"{BASE}/")
    pwa.wait_for_load_state("networkidle")
    manifest = pwa.evaluate("fetch('manifest.webmanifest').then(response => response.json())")
    assert manifest["version"] == VERSION
    assert manifest["id"] == APP_ID
    pwa.evaluate("navigator.serviceWorker.ready.then(() => true)")
    if not pwa.evaluate("Boolean(navigator.serviceWorker.controller)"):
        pwa.reload()
        pwa.wait_for_load_state("networkidle")
    assert pwa.evaluate("Boolean(navigator.serviceWorker.controller)")
    cache_keys = pwa.evaluate("caches.keys()")
    assert f"sk-plt-tools-v{VERSION}" in cache_keys
    cached_urls = pwa.evaluate(f"caches.open('sk-plt-tools-v{VERSION}').then(cache => cache.keys()).then(keys => keys.map(key => new URL(key.url).pathname))")
    for required in ('/index.html','/assets/core.css','/assets/app.js','/assets/navigation-tree.json','/assets/vde0100-600-engine.js','/assets/vde0100-600-template.json','/vendor/pdfjs/pdf.min.mjs','/vendor/pdfjs/pdf.worker.min.mjs','/siemens-analogwert-rechner/index.html','/wissensdatenbank/werkstoff-nachschlagewerk/index.html'):
        assert required in cached_urls, f"Offline-Cache fehlt: {required}"
    pwa.context.set_offline(True)
    pwa.goto(f"{BASE}/siemens-analogwert-rechner/")
    pwa.wait_for_load_state("domcontentloaded")
    assert_text(pwa, 'h1', 'Siemens Rohwert')
    assert_text(pwa, '#rawResult', '13.824')
    pwa.goto(f"{BASE}/wissensdatenbank/werkstoff-nachschlagewerk/")
    pwa.wait_for_load_state("domcontentloaded")
    assert pwa.locator('#materialSearch').is_visible()
    pwa.goto(f"{BASE}/")
    pwa.wait_for_load_state("domcontentloaded")
    pwa.locator('#skToolSearch').fill('Vacon')
    pwa.wait_for_function("document.querySelectorAll('#skKnowledgeResultList > a').length === 1")
    assert_text(pwa, '#skKnowledgeResultList h3', 'Vacon Frequenzumrichter')
    pwa.context.set_offline(False)

    browser.close()
    assert not console_errors, "Browser console errors: " + " | ".join(console_errors)
    print("OK: 16 Direktseiten, Desktop/Tablet/Mobil, Rechner, messwertzentrierte VDE-Oberfläche mit gesperrtem Endergebnis, Suche, Filter, Sortierung, Favoriten, Navigation sowie PWA- und Offline-Verhalten geprüft.")
