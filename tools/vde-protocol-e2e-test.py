#!/usr/bin/env python3
"""End-to-end regression for the VDE protocol analyzer with external test inputs only."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image, ImageEnhance
from playwright.sync_api import sync_playwright

BASE = os.environ.get("SK_TEST_BASE_URL", "http://127.0.0.1:4173")
REFERENCE = Path(os.environ.get("SK_VDE_REFERENCE_PDF", ""))
FILLED = Path(os.environ.get("SK_VDE_FILLED_PDF", ""))
ARTIFACT_DIR = Path(os.environ.get("SK_TEST_ARTIFACT_DIR", tempfile.gettempdir()))


def require_external_inputs() -> None:
    assert REFERENCE.is_file(), "SK_VDE_REFERENCE_PDF muss auf die autorisierte leere Referenz-PDF zeigen"
    assert FILLED.is_file(), "SK_VDE_FILLED_PDF muss auf die externe ausgefüllte Test-PDF zeigen"


def render_first_page(pdf: Path, output_prefix: Path, dpi: int = 145) -> Path:
    subprocess.run(
        ["pdftoppm", "-f", "1", "-singlefile", "-r", str(dpi), "-png", str(pdf), str(output_prefix)],
        check=True,
        capture_output=True,
    )
    return output_prefix.with_suffix(".png")


def make_photo_variants(folder: Path) -> tuple[Path, Path, Path]:
    reference_png = render_first_page(REFERENCE, folder / "reference")
    with Image.open(reference_png) as image:
        reference = image.convert("RGB")
        reference = reference.resize((round(reference.width * 0.78), round(reference.height * 0.78)), Image.Resampling.LANCZOS)
        reference_jpeg = folder / "reference-photo.jpg"
        reference.save(reference_jpeg, quality=62, optimize=True)

    filled_png = render_first_page(FILLED, folder / "filled", dpi=160)
    with Image.open(filled_png) as image:
        photo = image.convert("RGB")
        photo = ImageEnhance.Contrast(photo).enhance(0.93)
        photo = photo.resize((1170, round(photo.height * 1170 / photo.width)), Image.Resampling.LANCZOS)
        # Deterministic JPEG path representative of an iPhone document photo.
        filled_phone = folder / "filled-iphone-photo.jpg"
        photo.save(filled_phone, quality=68, optimize=True, progressive=True, dpi=(72, 72))
    return reference_png, reference_jpeg, filled_phone


def analyze(page, file_path: Path) -> dict:
    page.goto(f"{BASE}/plausibilitaetspruefung-vde0100-600/")
    page.wait_for_load_state("networkidle")
    page.locator("#documentInput").set_input_files(str(file_path))
    page.locator("#startAnalysis").click()
    page.locator("#reviewPanel").wait_for(state="visible", timeout=45_000)
    return page.evaluate("window.SK_VDE_CHECKER.summary()")


def assert_blank_reference(summary: dict, label: str, exact_hash: bool = False) -> None:
    assert summary["formStatus"] == "accepted", f"{label}: Referenzformular nicht akzeptiert: {summary}"
    assert summary["layoutScore"] >= 0.90, f"{label}: instabile Formularpassung {summary['layoutScore']:.3f}"
    if exact_hash:
        assert summary["mode"] == "reference-hash", f"{label}: Referenz-Hash nicht genutzt"
    data = summary["data"]
    assert data.get("signatureState") == "missing", f"{label}: leere Prüferunterschrift falsch positiv"
    assert data.get("commissioningSignature") == "missing", f"{label}: leere Inbetriebnehmer-Unterschrift falsch positiv"
    false_statuses = [
        key for key, value in data.items()
        if (key.startswith("inspection") or key.startswith("test") or key.endswith("Status"))
        and value in {"io", "nio", "nrel"}
    ]
    assert not false_statuses, f"{label}: falsche Checkboxwerte {false_statuses}"
    sign_issue = next(item for item in summary["pending"] if item["id"] == "SIGN-MISSING")
    assert not sign_issue["allowNotRelevant"], f"{label}: Pflichtunterschrift wäre überspringbar"


def assert_uncertain_form_is_nonblocking(page, summary: dict, label: str) -> None:
    assert summary["formStatus"] in {"ambiguous", "uncertain"}, f"{label}: unerwarteter Formularstatus {summary}"
    assert summary["layoutScore"] < 0.90, f"{label}: Test erwartet abweichende Formularidentität"
    identity = next((item for item in summary["pending"] if item["id"] == "FORM-IDENTITY"), None)
    assert identity and identity["status"] == "open", f"{label}: technischer Formularhinweis fehlt"
    assert not any(item["id"] == "FORM-LAYOUT" for item in summary["pending"]), f"{label}: alte automatische Ablehnung aktiv"
    assert page.locator("#resultPanel").is_hidden(), f"{label}: Endergebnis trotz offener Punkte sichtbar"
    page.locator("#openIssues").click()
    for selector, text in (
        ("#useForm", "Formular trotzdem verwenden"),
        ("#manualFormReview", "Zuordnung manuell prüfen"),
        ("#replaceFile", "Andere Datei hochladen"),
    ):
        assert page.locator(selector).is_visible(), f"{label}: Option fehlt: {selector}"
        assert page.locator(selector).inner_text() == text, f"{label}: falsche Beschriftung: {selector}"
    assert page.locator("#normalIssueActions").is_hidden(), f"{label}: n.i.O.-Aktion darf bei Formularidentität nicht erscheinen"
    assert page.locator("#verdictIcon").is_hidden() or page.locator("#resultPanel").is_hidden(), f"{label}: rotes X vor Klärung"


def main() -> int:
    require_external_inputs()
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="sk-vde-e2e-") as temp_name:
        reference_png, reference_jpeg, filled_phone = make_photo_variants(Path(temp_name))
        with sync_playwright() as playwright:
            executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            browser = playwright.chromium.launch(headless=True, executable_path=executable) if executable else playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1050})
            console_errors: list[str] = []
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)

            reference_pdf = analyze(page, REFERENCE)
            assert_blank_reference(reference_pdf, "leere PDF", exact_hash=True)
            reference_png_summary = analyze(page, reference_png)
            assert_blank_reference(reference_png_summary, "PNG-Foto")
            reference_jpeg_summary = analyze(page, reference_jpeg)
            assert_blank_reference(reference_jpeg_summary, "JPEG-Foto")

            filled = analyze(page, FILLED)
            assert_uncertain_form_is_nonblocking(page, filled, "ausgefüllte Test-PDF")
            page.locator("#useForm").click()
            continued = page.evaluate("window.SK_VDE_CHECKER.summary()")
            assert continued["formIdentityDecision"] == "use"
            assert not any(item["id"] == "FORM-IDENTITY" for item in continued["pending"])
            assert continued["pending"], "Fachliche offene Punkte müssen nach Formularfreigabe erhalten bleiben"
            assert page.locator("#resultPanel").is_hidden(), "Kein Endergebnis vor Klärung aller Pflichtpunkte"

            phone = analyze(page, filled_phone)
            assert_uncertain_form_is_nonblocking(page, phone, "Smartphone-Foto")
            page.set_viewport_size({"width": 390, "height": 844})
            page.screenshot(path=str(ARTIFACT_DIR / "vde-formularhinweis-smartphone.png"), full_page=True)
            page.locator("#manualFormReview").click()
            manual = page.evaluate("window.SK_VDE_CHECKER.summary()")
            assert manual["formIdentityDecision"] == "manual"
            assert not any(item["id"] == "FORM-IDENTITY" for item in manual["pending"])
            assert manual["pending"], "Manuelle Zuordnung muss offene fachliche Punkte erzeugen"
            assert page.locator("#resultPanel").is_hidden(), "Kein Endergebnis während manueller Zuordnung"

            page.set_viewport_size({"width": 1440, "height": 1050})
            analyze(page, FILLED)
            page.locator("#openIssues").click()
            page.locator("#replaceFile").click()
            assert page.locator("#uploadPanel").is_visible(), "Andere Datei hochladen führt nicht zurück zum Upload"
            assert page.locator("#fileList .file-row").count() == 0, "Dateiauswahl wurde beim Ersetzen nicht geleert"

            browser.close()
            assert not console_errors, "Browser-Konsole: " + " | ".join(console_errors)

    result = {
        "reference_pdf_score": round(reference_pdf["layoutScore"], 4),
        "reference_png_score": round(reference_png_summary["layoutScore"], 4),
        "reference_jpeg_score": round(reference_jpeg_summary["layoutScore"], 4),
        "filled_test_pdf_score": round(filled["layoutScore"], 4),
        "smartphone_photo_score": round(phone["layoutScore"], 4),
        "filled_form_identity": filled["formStatus"],
        "smartphone_form_identity": phone["formStatus"],
        "automatic_form_failure": False,
        "result_before_open_points_resolved": False,
        "blank_signatures": "missing",
        "blank_checkbox_false_positives": 0,
        "result": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
