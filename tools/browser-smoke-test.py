#!/usr/bin/env python3
"""Browser smoke test for SK PLT Tools Beta 2.0.3.4-Beta.1."""
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
    assert desktop.locator("body").get_attribute("data-sk-version") == "2.0.3.4-Beta.1"
    assert_text(desktop, "h1", "Siemens Rohwert")
    assert desktop.locator("#signalType option").count() == 4
    assert desktop.locator("#inputKind option").count() == 2
    assert desktop.locator("#valueSlider").count() == 1
    assert "physikalisch" not in desktop.locator("body").inner_text().lower()
    assert_text(desktop, "#rawResult", "13.824")
    assert_text(desktop, "#signalResult", "12,000 mA")
    assert desktop.locator("#valueSlider").get_attribute("min") == "-32768"
    assert desktop.locator("#valueSlider").get_attribute("max") == "32767"
    assert desktop.locator("#sliderScale span").all_inner_texts() == ["−32.768", "−4.864", "0", "27.648", "32.511", "32.767"]

    cases = [
        ("-4865", "Unterlauf"),
        ("-4864", "Unterbereich"),
        ("0", "Nennbereich"),
        ("27648", "Nennbereich"),
        ("27649", "Überbereich"),
        ("32512", "Überlauf"),
    ]
    for raw, status in cases:
        desktop.locator(f'button[data-raw="{raw}"]').click()
        assert_text(desktop, "#rangeStatus", status)

    desktop.locator("#signalType").select_option("0-10V")
    desktop.locator("#inputKind").select_option("signal")
    assert desktop.locator("#valueSlider").get_attribute("min") == "0"
    assert desktop.locator("#valueSlider").get_attribute("max") == "10"
    assert desktop.locator("#sliderScale span").all_inner_texts() == ["0 V", "2,5 V", "5 V", "7,5 V", "10 V"]
    set_input(desktop, "#inputValue", "2.5")
    assert_text(desktop, "#rawResult", "6.912")
    assert_text(desktop, "#signalResult", "2,500 V")
    assert_text(desktop, "#rangeStatus", "Nennbereich")
    signal_scales = {
        "4-20mA": ["4 mA", "8 mA", "12 mA", "16 mA", "20 mA"],
        "0-20mA": ["0 mA", "5 mA", "10 mA", "15 mA", "20 mA"],
        "0-10V": ["0 V", "2,5 V", "5 V", "7,5 V", "10 V"],
        "2-10V": ["2 V", "4 V", "6 V", "8 V", "10 V"],
    }
    for signal_type, expected_scale in signal_scales.items():
        desktop.locator("#signalType").select_option(signal_type)
        assert desktop.locator("#sliderScale span").all_inner_texts() == expected_scale
    desktop.locator("#inputKind").select_option("raw")
    assert desktop.locator("#sliderScale span").all_inner_texts() == ["−32.768", "−4.864", "0", "27.648", "32.511", "32.767"]
    desktop.screenshot(path=str(OUT / "siemens-desktop.png"), full_page=True)

    desktop.goto(f"{BASE}/")
    desktop.wait_for_load_state("networkidle")
    external = desktop.locator('a.sk-external-card')
    assert external.count() == 1
    assert external.get_attribute("href") == "https://netilion.endress.com/app/library/device_viewer"
    assert external.get_attribute("target") == "_blank"
    assert set((external.get_attribute("rel") or "").split()) >= {"external", "noopener", "noreferrer"}
    assert external.get_attribute("referrerpolicy") == "no-referrer"
    assert "nicht in SK PLT Tools gespeichert" in external.inner_text()
    assert external.locator("input, textarea, form").count() == 0
    desktop.screenshot(path=str(OUT / "startseite-desktop.png"), full_page=True)
    desktop.locator('[data-filter="EXTERN"]').click()
    assert external.is_visible()
    assert desktop.locator('.tools > a.card:visible').count() == 1
    desktop.locator('[data-filter="ALLE"]').click()
    set_input(desktop, "#skToolSearch", "Rohwert")
    card = desktop.locator('a[href="siemens-analogwert-rechner/"]')
    assert_text(desktop, 'a[href="siemens-analogwert-rechner/"] h2', 'Siemens Rohwert')
    assert card.is_visible(), "Siemens-Rechner wird in der Startseitensuche nicht gefunden"
    card.locator(".sk-favorite-button").click()
    assert card.locator(".sk-favorite-button").get_attribute("data-active") == "true"
    desktop.locator(".sk-tree-trigger").click()
    assert desktop.get_by_text("Siemens-SPS-Analogwert-Rechner", exact=True).count() >= 1

    mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
    mobile.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
    mobile.goto(f"{BASE}/")
    mobile.wait_for_load_state("networkidle")
    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    assert mobile.locator("a.sk-external-card").is_visible()
    assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    mobile.screenshot(path=str(OUT / "startseite-mobile.png"), full_page=True)

    browser.close()
    assert not console_errors, "Browser console errors: " + " | ".join(console_errors)
    print("OK: Desktop, Mobilansicht, E+H-Externlink, Slider-Zustände, Rückrechnung, Suche, Favorit und Navigation geprüft.")
