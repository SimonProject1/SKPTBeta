#!/usr/bin/env python3
"""Browser smoke test for SK PLT Tools Beta 2.0.3.5-Beta.1."""
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


with sync_playwright() as p:
    executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
    browser = p.chromium.launch(headless=True, executable_path=executable) if executable else p.chromium.launch(headless=True)
    console_errors = []

    desktop = browser.new_page(viewport={"width": 1440, "height": 1050}, device_scale_factor=1)
    desktop.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    desktop.goto(f"{BASE}/siemens-analogwert-rechner/")
    desktop.wait_for_load_state("networkidle")
    assert desktop.locator("body").get_attribute("data-sk-version") == "2.0.3.5-Beta.1"
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

    mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    mobile.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    mobile.goto(f"{BASE}/siemens-analogwert-rechner/")
    mobile.wait_for_load_state("networkidle")
    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    assert mobile.locator("#cardProfile").is_visible()
    mobile.screenshot(path=str(OUT / "siemens-mobile.png"), full_page=True)

    browser.close()
    assert not console_errors, "Browser console errors: " + " | ".join(console_errors)
    print("OK: Desktop/Mobil, bestätigte Siemens-Kartenprofile, NE43-Grenzen, Synchronisierung und Wissenskachel geprüft.")
