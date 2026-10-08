#!/usr/bin/env python3
"""End-to-end tests for the measurement-only VDE 0100-600 workflow."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from playwright.sync_api import sync_playwright
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

BASE = os.environ.get("SK_TEST_BASE_URL", "http://127.0.0.1:4173")
ARTIFACT_DIR = Path(os.environ.get("SK_TEST_ARTIFACT_DIR", tempfile.gettempdir()))
POSITIVE_TEXT = (
    "Messwerte VDE 0100-600 | Niederohmmessung 0,20 Ohm | Isolation >300 MOhm; >300 MOhm; >300 MOhm | "
    "Schleifenimpedanz Zs 0,50 Ohm | Kennlinie B 16 A | U0 230 V | Kurzschlussstrom Ik 460 A | "
    "Verbraucherstrom Ib 10 A | Nennstrom In 16 A | Spannungsfall DeltaU 4 V | Nennspannung Un 400 V | Spannungsfall 1,0 % | "
    "RCD Bemessungsdifferenzstrom IΔn 30 mA | Auslösestrom IΔ 18 mA | Auslösezeit tA 17 ms"
)


def make_pdf(path: Path, text: str) -> None:
    doc = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    doc.setFont("Helvetica-Bold", 18)
    doc.drawString(48, height - 52, "MESSWERTPROTOKOLL")
    doc.setFont("Helvetica", 11)
    y = height - 90
    parts = [part.strip() for part in text.split("|")]
    for part in parts:
        doc.drawString(52, y, part.replace("Δ", "Delta"))
        y -= 28
    doc.rect(42, y - 20, width - 84, height - y - 40)
    doc.save()


def make_phone_photo(path: Path, text: str) -> None:
    image = Image.new("RGB", (1170, 1650), "#f3f0e8")
    draw = ImageDraw.Draw(image)
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 46)
        body_font = ImageFont.truetype("DejaVuSans.ttf", 27)
    except OSError:
        title_font = body_font = ImageFont.load_default()
    draw.rounded_rectangle((70, 70, 1100, 1510), radius=18, fill="white", outline="#28333a", width=3)
    draw.text((110, 110), "MESSWERTPROTOKOLL", fill="#071820", font=title_font)
    y = 205
    for part in [part.strip() for part in text.split("|")]:
        draw.text((115, y), part, fill="#15252d", font=body_font)
        y += 82
    image = ImageEnhance.Contrast(image).enhance(0.94)
    image = image.rotate(1.4, resample=Image.Resampling.BICUBIC, expand=False, fillcolor="#d7d4cd")
    image.save(path, quality=68, optimize=True, progressive=True, dpi=(72, 72))


def analyze(page, file_path: Path) -> dict:
    page.goto(f"{BASE}/plausibilitaetspruefung-vde0100-600/")
    page.wait_for_load_state("networkidle")
    page.locator("#documentInput").set_input_files(str(file_path))
    page.locator("#startAnalysis").click()
    page.locator("#reviewPanel").wait_for(state="visible", timeout=45_000)
    return page.evaluate("window.SK_VDE_CHECKER.summary()")


def confirm_scope(page) -> None:
    page.locator("#openIssues").click()
    page.locator("#issuePanel").wait_for(state="visible")
    assert page.locator("[data-scope]:checked").count() > 0, "Automatisch vorgeschlagener Messumfang fehlt"
    assert page.locator("#resultPanel").is_hidden(), "Endergebnis vor Bestätigung des Messumfangs"
    page.locator("#applyCorrection").click()


def resolve_uncertain_values(page) -> None:
    for _ in range(40):
        if page.locator("#resultPanel").is_visible():
            return
        summary = page.evaluate("window.SK_VDE_CHECKER.summary()")
        assert summary["pending"], "Weder Ergebnis noch offener Wert vorhanden"
        current = summary["pending"][0]
        assert current["status"] == "open", f"Unerwartete Rechenabweichung im Positivfall: {current}"
        assert page.locator("#issueInput").is_visible(), f"Eingabefeld fehlt für {current}"
        assert page.locator("#issueInput").input_value().strip(), f"Erkannter Wert fehlt für {current}"
        page.locator("#applyCorrection").click()
    raise AssertionError("Klärungsfolge endet nicht")


def main() -> int:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sk-vde-measurements-") as temp_name:
        temp = Path(temp_name)
        positive_pdf = temp / "measurement-positive.pdf"
        missing_pdf = temp / "measurement-missing-reference.pdf"
        negative_pdf = temp / "measurement-negative.pdf"
        phone_photo = temp / "measurement-smartphone.jpg"
        make_pdf(positive_pdf, POSITIVE_TEXT)
        make_pdf(missing_pdf, POSITIVE_TEXT.replace("U0 230 V | ", ""))
        make_pdf(negative_pdf, POSITIVE_TEXT.replace("Zs 0,50 Ohm", "Zs 4,00 Ohm").replace("Ik 460 A", "Ik 57,5 A"))
        make_phone_photo(phone_photo, POSITIVE_TEXT)

        with sync_playwright() as playwright:
            executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            browser = playwright.chromium.launch(headless=True, executable_path=executable) if executable else playwright.chromium.launch(headless=True)
            console_errors: list[str] = []

            page = browser.new_page(viewport={"width": 1440, "height": 1050})
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)

            positive = analyze(page, positive_pdf)
            assert positive["version"] == "2.1.0.5-Beta"
            assert positive["pending"][0]["id"] == "SCOPE-CONFIRM"
            assert not positive["scopeConfirmed"]
            assert {"loop", "shortCircuit", "loadCurrent", "voltageDrop", "rcdCurrent", "rcdTime", "insulation", "continuity"} <= set(positive["suggestedScope"])
            assert page.locator("#resultPanel").is_hidden()
            assert page.locator("text=Formularpassung").count() == 0
            confirm_scope(page)
            page.locator("#resultPanel").wait_for(state="visible")
            assert page.locator("#verdictIcon").inner_text() == "✓"
            assert "plausibel" in page.locator("#verdictTitle").inner_text().lower()
            page.screenshot(path=str(ARTIFACT_DIR / "vde-messwerte-pdf-gruen.png"), full_page=True)

            missing = analyze(page, missing_pdf)
            confirm_scope(page)
            missing_after_scope = page.evaluate("window.SK_VDE_CHECKER.summary()")
            assert any(item["id"] == "REQ-phaseVoltage" and item["status"] == "open" for item in missing_after_scope["pending"])
            assert page.locator("#resultPanel").is_hidden(), "Fehlende Bezugsgröße darf kein Endergebnis liefern"
            assert page.locator("#confirmFail").is_hidden(), "Fehlende Bezugsgröße darf nicht als rotes X bestätigt werden"
            assert page.locator("#issueInput").get_attribute("data-field") == "phaseVoltage"
            page.locator("#issueInput").fill("230")
            page.locator("#applyCorrection").click()
            page.locator("#resultPanel").wait_for(state="visible")
            assert page.locator("#verdictIcon").inner_text() == "✓"

            negative = analyze(page, negative_pdf)
            confirm_scope(page)
            negative_after_scope = page.evaluate("window.SK_VDE_CHECKER.summary()")
            assert any(item["id"] == "MEAS-ZS" and item["status"] == "fail" for item in negative_after_scope["pending"])
            assert page.locator("#resultPanel").is_hidden(), "Unbestätigte Rechenabweichung darf kein Endergebnis liefern"
            assert page.locator("#confirmFail").is_visible()
            page.locator("#confirmFail").click()
            page.locator("#resultPanel").wait_for(state="visible")
            assert page.locator("#verdictIcon").inner_text() == "×"
            assert "nicht plausibel" in page.locator("#verdictTitle").inner_text().lower()

            phone_context = browser.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True)
            # Chromium exposes the browser-local TextDetector API only on selected platforms.
            # The deterministic adapter exercises the exact same browser interface and
            # supplies the text visibly present in the generated smartphone photograph.
            phone_context.add_init_script(
                """
                window.TextDetector = class {
                  async detect(canvas) {
                    return [{rawValue: %s, boundingBox: {x:0,y:0,width:canvas.width,height:canvas.height}}];
                  }
                };
                """ % json.dumps(POSITIVE_TEXT)
            )
            phone_page = phone_context.new_page()
            phone_page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)
            phone = analyze(phone_page, phone_photo)
            assert phone["mode"] == "local-image-text"
            assert phone["pending"][0]["id"] == "SCOPE-CONFIRM"
            assert phone["internalLocatorUsed"] is True
            confirm_scope(phone_page)
            assert phone_page.locator("#resultPanel").is_hidden(), "Unsichere Fotoerkennung darf kein Endergebnis liefern"
            assert phone_page.locator("#confirmFail").is_hidden(), "Unsichere Fotoerkennung darf kein rotes X auslösen"
            resolve_uncertain_values(phone_page)
            assert phone_page.locator("#verdictIcon").inner_text() == "✓"
            assert phone_page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            phone_page.screenshot(path=str(ARTIFACT_DIR / "vde-messwerte-smartphone-gruen.png"), full_page=True)
            phone_context.close()

            browser.close()
            assert not console_errors, "Browser-Konsole: " + " | ".join(console_errors)

    result = {
        "version": "2.1.0.5-Beta",
        "positive_pdf": "PASS · grüner Haken",
        "missing_reference": "PASS · kein Endergebnis, kein rotes X, Einzelabfrage",
        "confirmed_negative_measurement": "PASS · rotes X",
        "smartphone_photo": "PASS · lokalisieren, unsichere Werte einzeln bestätigen, grüner Haken",
        "formal_document_features_used_for_verdict": False,
        "template_used_as_verdict_criterion": False,
        "result": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
