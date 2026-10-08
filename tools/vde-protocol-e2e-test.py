#!/usr/bin/env python3
"""End-to-end tests for the manual VDE measurement checker.

The historical filename is retained for project-structure compatibility. No protocol,
PDF, photograph or OCR input is used.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from playwright.sync_api import sync_playwright

BASE = os.environ.get("SK_TEST_BASE_URL", "http://127.0.0.1:4173")
ARTIFACT_DIR = Path(os.environ.get("SK_TEST_ARTIFACT_DIR", tempfile.gettempdir()))


def choose(page, measurement: str) -> None:
    page.locator(f'[data-measurement="{measurement}"]').click()


def fill(page, values: dict[str, str]) -> None:
    for field, value in values.items():
        control = page.locator(f"#{field}")
        if control.evaluate("el => el.tagName") == "SELECT":
            control.select_option(value)
        else:
            control.fill(value)


def evaluate(page) -> None:
    page.locator("#evaluateMeasurement").click()


def main() -> int:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
        browser = playwright.chromium.launch(headless=True, executable_path=executable) if executable else playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 1050})
        console_errors: list[str] = []
        page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
        page.goto(f"{BASE}/plausibilitaetspruefung-vde0100-600/")
        page.wait_for_load_state("networkidle")

        summary = page.evaluate("window.SK_VDE_CHECKER.summary()")
        assert summary["version"] == "2.1.1.0-Beta"
        assert summary["mode"] == "manual-only"
        assert summary["automaticDocumentAnalysis"] is False
        assert page.locator('input[type="file"]').count() == 0
        assert page.locator("#measurementNav .measurement-button").count() == 6

        # Missing values must be queried specifically and must not expose a verdict.
        fill(page, {"voltageDropMode": "percent", "approvedMaxDropPercent": "3"})
        evaluate(page)
        assert page.locator("#inputAlert").is_visible()
        assert "Gemessener Spannungsfall fehlt" in page.locator("#inputAlertList").inner_text()
        assert page.locator("#resultPanel").is_hidden()
        assert page.evaluate("window.SK_VDE_CHECKER.summary().resultVisible") is False

        # Exact boundary is i. O.; limit, formula and calculation are visible.
        page.locator("#measuredDropPercent").fill("3")
        evaluate(page)
        assert page.locator("#resultPanel").is_visible()
        assert page.locator("#resultTitle").inner_text().lower() == "i. o."
        assert "≤ 3 %" in page.locator("#resultLimit").inner_text()
        assert "ΔU%gemessen" in page.locator("#resultFormula").inner_text()
        assert "3 % ≤ 3 %" in page.locator("#resultCalculation").inner_text()

        # Insulation failure from a complete, explicit basis.
        choose(page, "insulation")
        fill(page, {"measuredInsulation": "0,99", "approvedMinInsulation": "1"})
        evaluate(page)
        assert page.locator("#resultTitle").inner_text().lower() == "nicht i. o."
        assert "0,99 MΩ < 1 MΩ" in page.locator("#resultCalculation").inner_text()

        # Zs formula route: no result without Ia, then transparent calculated limit.
        choose(page, "disconnection")
        fill(page, {"disconnectionMode": "loop-formula", "measuredLoopImpedance": "2,875", "phaseVoltage": "230"})
        evaluate(page)
        assert page.locator("#resultPanel").is_hidden()
        assert "Erforderlicher Auslösestrom Ia" in page.locator("#inputAlertList").inner_text()
        page.locator("#requiredTripCurrent").fill("80")
        evaluate(page)
        assert page.locator("#resultTitle").inner_text().lower() == "i. o."
        assert "2,875 Ω" in page.locator("#resultLimit").inner_text()
        assert "U0 / Ia" in page.locator("#resultFormula").inner_text()

        # Combined RCD evaluation exposes both calculations and an overall failure.
        choose(page, "rcd")
        fill(page, {
            "rcdMode": "both",
            "measuredRcdTime": "299",
            "approvedMaxRcdTime": "300",
            "measuredRcdCurrent": "31",
            "approvedMinRcdCurrent": "15",
            "approvedMaxRcdCurrent": "30",
        })
        evaluate(page)
        assert page.locator("#resultTitle").inner_text().lower() == "nicht i. o."
        assert page.locator("#resultChecks .check-row").count() == 2
        assert page.locator("#resultChecks .check-row.fail").count() == 1
        assert page.locator("#sessionCount").inner_text() == "4"
        page.screenshot(path=str(ARTIFACT_DIR / "vde-messwertpruefer-desktop.png"), full_page=True)

        # Mobile interaction and overflow.
        mobile = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
        mobile.goto(f"{BASE}/plausibilitaetspruefung-vde0100-600/")
        mobile.wait_for_load_state("networkidle")
        choose(mobile, "continuity")
        fill(mobile, {"measuredContinuity": "0,5", "approvedMaxContinuity": "0,5"})
        evaluate(mobile)
        assert mobile.locator("#resultTitle").inner_text().lower() == "i. o."
        assert mobile.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
        mobile.screenshot(path=str(ARTIFACT_DIR / "vde-messwertpruefer-mobile.png"), full_page=True)
        mobile.close()

        browser.close()
        assert not console_errors, "Browser-Konsole: " + " | ".join(console_errors)

    result = {
        "version": "2.1.1.0-Beta",
        "mode": "manual-only",
        "automatic_document_analysis": False,
        "missing_input_blocks_result": "PASS",
        "inclusive_boundary": "PASS",
        "transparent_limit_formula_calculation": "PASS",
        "confirmed_failure": "PASS",
        "responsive_mobile": "PASS",
        "result": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
