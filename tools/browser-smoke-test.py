#!/usr/bin/env python3
"""Browser smoke test for SK PLT Tools Beta 2.0.3.5-Beta.2."""
from pathlib import Path
import os
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "test-artifacts"
OUT.mkdir(exist_ok=True)
BASE = "http://127.0.0.1:4173"


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
    "/wissensdatenbank/siemens-sitrans-p320-sil-verriegelung/",
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
    assert desktop.locator("body").get_attribute("data-sk-version") == "2.0.3.5-Beta.2"
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
    knowledge = desktop.locator('a.knowledge-entry[href="../siemens-analogwert-rechner/"]')
    assert knowledge.count() == 1
    assert_text(desktop, 'a.knowledge-entry[href="../siemens-analogwert-rechner/"] h2', "Rohwert")

    desktop.goto(f"{BASE}/")
    desktop.wait_for_load_state("networkidle")
    external = desktop.locator('a.sk-external-card')
    assert external.count() == 1
    assert external.get_attribute("href") == "https://netilion.endress.com/app/library/device_viewer"
    assert external.get_attribute("target") == "_blank"
    assert set((external.get_attribute("rel") or "").split()) >= {"external", "noopener", "noreferrer"}
    assert external.get_attribute("referrerpolicy") == "no-referrer"
    desktop.screenshot(path=str(OUT / "startseite-desktop.png"), full_page=True)

    tablet = browser.new_page(viewport={"width": 820, "height": 1180}, device_scale_factor=2, is_mobile=True)
    tablet.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    for route in PAGES:
        tablet.goto(f"{BASE}{route}")
        tablet.wait_for_load_state("networkidle")
        assert tablet.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"Horizontales Überlaufen: {route}"
        assert tablet.locator("body").get_attribute("data-sk-version") == "2.0.3.5-Beta.2"
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
    mobile.goto(f"{BASE}/analogsignal/")
    mobile.wait_for_load_state("networkidle")
    assert abs(mobile.locator("button.sign").first.bounding_box()["width"] - 38) <= 1

    browser.close()
    assert not console_errors, "Browser console errors: " + " | ".join(console_errors)
    print("OK: 15 Seiten auf iPad-Breite, Desktop/Mobil, kompakte Bedienelemente, einklappbare Karteninformationen, Siemens-Kartenprofile, NE43-Grenzen, Synchronisierung und Wissenskachel geprüft.")
