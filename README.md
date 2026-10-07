# SK PLT Tools 2.1.0.3-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.0.3-Beta** basiert auf dem vollständigen Bestand von **2.1.0.2-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Schwerpunkt dieser Beta

Die Plausibilitätsprüfung für VDE-0100-600-Protokolle verwendet eine mehrstufige, vollständig lokale Erkennung:

- hochwertige PDF-Rasterung und Bildnormalisierung mit Kontrastanpassung, Vierfach-Orientierung und Feinausrichtung,
- verbindlicher Abgleich gegen die aus `VDEProtokoll.pdf` abgeleiteten Strukturmerkmale,
- korrekter Referenz-SHA-256 `019b2918bbfa0b7bef71c6b95f1a48136305053995473b625693217383af05f2`,
- Ensemble aus Zellraster, horizontaler/vertikaler Projektion, Linienankern und Seitenverhältnis,
- 93 formulargebundene Feldzonen mit referenzbereinigten Baselines,
- robuste Checkbox-, Handschrift-/Tinten- und Unterschriftsevidenz statt einfacher Dunkeldichte,
- typabhängige Konfidenzschwellen und nachvollziehbare Erkennungsgründe,
- sequentielle manuelle Klärung mit markiertem Originalausschnitt,
- Mehrfeld-Dialog für den technischen Platz ohne Ortsangaben-Deadlock,
- „Nicht relevant“ nur bei im Feldschema fachlich zugelassenen Punkten,
- unvermeidbare Pflichtfelder und Sicherheitsabweichungen,
- grüner Haken für plausibel und rotes X für nicht plausibel.

Die Erkennung ist bewusst **KI-ähnlich heuristisch**, aber nicht selbstlernend: Sie kombiniert mehrere unabhängige Merkmale und Konfidenzen. Es findet kein Upload und kein Aufruf eines externen KI-/OCR-Dienstes statt.

## Datenschutz und Referenzen

- Die leere `VDEProtokoll.pdf` ist die autorisierte Referenzquelle für Hash, Geometrie, Struktur-Fingerabdruck und Blank-Baselines.
- Die Referenz-PDF selbst ist nicht in die Webanwendung eingebettet und nicht downloadbar.
- Ein reales ausgefülltes Prüfprotokoll wird ausschließlich als externe Testeingabe verwendet.
- Das Release enthält weder diese ausgefüllte PDF noch ihren Inhalt, einen Precache-Eintrag oder eine abgeleitete Vorschau.
- `tools/release.py` und `tools/validate_release.py` enthalten ein Datenschutz-Gate gegen die bekannte reale Testdatei.

## Projektstruktur

- `index.html` und 15 Direktseiten
- `assets/`: zentrale Laufzeitdateien, Datenkataloge, VDE-Engine, Regeln und Referenzprofil
- `plausibilitaetspruefung-vde0100-600/`: Upload-, Analyse-, Klärungs- und Ergebnisoberfläche
- `vendor/pdfjs/`: lokale PDF.js-Laufzeit
- `shared/`: zentrale Header-/Footer-/Bedienelement-Fragmente
- `tools/release.py`: Version, PWA-Precache, Datenschutz-Gate, Prüfsummen und ZIP
- `tools/validate_release.py`: statische Vollständigkeits-, Datenschutz- und Integritätsprüfung
- `tools/functional-smoke-test.js`: Rechner-, Inhalts- und VDE-Regeltests
- `tools/browser-smoke-test.py`: vollständiger Browser-, Responsive-, PWA- und Offline-Test
- `tools/vde-protocol-e2e-test.py`: externe End-to-End-Tests für Referenz-PDF, Fotoformate und Fremdformular
- `TESTBERICHT-UND-ABNAHME.md`: geprüfter Release-Nachweis
- `SHA256SUMS.txt`: interne SHA-256-Prüfsummen

## Testen

```bash
node tools/functional-smoke-test.js
python3 tools/validate_release.py
```

Für Browser- und Protokolltests werden die PDFs absichtlich außerhalb des Projekts übergeben:

```bash
export SK_VDE_REFERENCE_PDF=/sicherer/pfad/VDEProtokoll.pdf
export SK_VDE_FILLED_PDF=/sicherer/pfad/ausgefüllte-testdatei.pdf
python3 -m http.server 4173 --bind 127.0.0.1
# in einem zweiten Terminal:
python3 tools/browser-smoke-test.py
python3 tools/vde-protocol-e2e-test.py
```

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, App-ID, Cache-Namen und Precache, prüft das Datenschutz-Gate, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.

## Fachliche Grenze

Die Anwendung unterstützt die dokumentierte Zweitkontrolle. Sie führt keine Messung durch und ersetzt weder die Bewertung noch die Freigabe durch eine verantwortliche Elektrofachkraft.
