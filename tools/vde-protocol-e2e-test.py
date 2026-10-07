#!/usr/bin/env python3
"""End-to-end regression for the VDE protocol analyzer without shipping real protocol files."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
from PIL import Image
from playwright.sync_api import sync_playwright

BASE = os.environ.get("SK_TEST_BASE_URL", "http://127.0.0.1:4173")
REFERENCE = Path(os.environ.get("SK_VDE_REFERENCE_PDF", ""))
FILLED = Path(os.environ.get("SK_VDE_FILLED_PDF", ""))


def require_external_inputs() -> None:
    assert REFERENCE.is_file(), "SK_VDE_REFERENCE_PDF muss auf die autorisierte leere Referenz-PDF zeigen"
    assert FILLED.is_file(), "SK_VDE_FILLED_PDF muss auf die externe ausgefüllte Test-PDF zeigen"


def make_photo_variants(folder: Path) -> tuple[Path, Path]:
    prefix = folder / "reference"
    subprocess.run(
        ["pdftoppm", "-f", "1", "-singlefile", "-r", "145", "-png", str(REFERENCE), str(prefix)],
        check=True,
        capture_output=True,
    )
    png = prefix.with_suffix(".png")
    with Image.open(png) as image:
        image = image.convert("RGB")
        image = image.resize((round(image.width * 0.78), round(image.height * 0.78)), Image.Resampling.LANCZOS)
        jpeg = folder / "reference-photo.jpg"
        image.save(jpeg, quality=62, optimize=True)
    return png, jpeg


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


def main() -> int:
    require_external_inputs()
    with tempfile.TemporaryDirectory(prefix="sk-vde-e2e-") as temp_name:
        png, jpeg = make_photo_variants(Path(temp_name))
        with sync_playwright() as playwright:
            executable = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
            browser = playwright.chromium.launch(headless=True, executable_path=executable) if executable else playwright.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1440, "height": 1050})
            console_errors: list[str] = []
            page.on("console", lambda message: console_errors.append(message.text) if message.type == "error" else None)

            reference_pdf = analyze(page, REFERENCE)
            assert_blank_reference(reference_pdf, "leere PDF", exact_hash=True)
            reference_png = analyze(page, png)
            assert_blank_reference(reference_png, "PNG-Foto")
            reference_jpeg = analyze(page, jpeg)
            assert_blank_reference(reference_jpeg, "JPEG-Foto")

            foreign = analyze(page, FILLED)
            assert foreign["formStatus"] == "rejected", f"historisches Fremdformular wurde nicht abgelehnt: {foreign}"
            assert foreign["layoutScore"] < 0.84, f"historisches Fremdformular liegt nicht unter der harten Ablehnungsschwelle: {foreign['layoutScore']:.3f}"
            assert foreign["fieldCount"] == 1, f"Fremdformular erzeugte positionsgebundene Felder: {foreign['fieldCount']}"
            assert [item["id"] for item in foreign["pending"]] == ["FORM-LAYOUT"], f"Fremdformular erzeugte falsche Folgefelder: {foreign['pending']}"
            page.locator("#openIssues").click()
            assert page.locator("#notRelevant").is_hidden(), "Formularabweichung kann als nicht relevant übersprungen werden"
            assert page.locator("#applyCorrection").is_hidden(), "hart abgelehntes Formular kann manuell auf unterstützt umgestellt werden"
            assert page.locator("#confirmFail").is_visible()
            page.locator("#confirmFail").click()
            page.locator("#resultPanel").wait_for(state="visible")
            assert page.locator("#verdictIcon").inner_text() == "×"
            assert page.locator("#verdictTitle").inner_text() == "Nicht plausibel"

            browser.close()
            assert not console_errors, "Browser-Konsole: " + " | ".join(console_errors)

    result = {
        "reference_pdf_score": round(reference_pdf["layoutScore"], 4),
        "reference_png_score": round(reference_png["layoutScore"], 4),
        "reference_jpeg_score": round(reference_jpeg["layoutScore"], 4),
        "foreign_form_score": round(foreign["layoutScore"], 4),
        "blank_signatures": "missing",
        "blank_checkbox_false_positives": 0,
        "foreign_form_fields_mapped": foreign["fieldCount"] - 1,
        "result": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
