# SK PLT Tools 2.1.0.4-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.0.4-Beta** basiert auf dem vollständigen Bestand von **2.1.0.3-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Schwerpunkt dieser Beta

Die Plausibilitätsprüfung VDE 0100-600 trennt ab dieser Version strikt zwischen technischer Formularidentität und fachlichem Prüfergebnis:

- Eine teilweise oder abweichende Formularidentität, auch beispielsweise 78 % Strukturpassung, ist nur ein technischer Hinweis.
- Eine unsichere Formularidentität erzeugt weder automatisch n.i.O. noch ein rotes X und blockiert die fachliche Prüfung nicht.
- Bei unsicherer Identität stehen exakt die Optionen **„Formular trotzdem verwenden“**, **„Zuordnung manuell prüfen“** und **„Andere Datei hochladen“** bereit.
- Für jeden erforderlichen Auswahlpunkt muss genau ein zulässiges Kreuz vorliegen; kein, mehrere oder unsichere Kreuze werden einzeln geklärt.
- Erforderliche Messwerte müssen vorhanden, lesbar und rechnerisch plausibel sein; fehlende oder unsichere Werte werden sequenziell geklärt.
- Solange offene Punkte bestehen, wird kein Endergebnis angezeigt.
- Ein rotes X entsteht nur durch bestätigte Mängel, bestätigte fehlende Pflichtangaben oder rechnerisch unplausible Messwerte.
- Sind alle erforderlichen Kreuze, Pflichtangaben und Messwerte geklärt und plausibel, erscheint der grüne Haken.
- Pflichtfelder und sicherheitsrelevante Abweichungen bleiben nicht als „nicht relevant“ überspringbar. Der im Formular ausdrücklich zulässige Status „nicht relevant“ bleibt für fachlich bedingte Statuspunkte erhalten.

## Erkennung und Datenschutz

- `VDEProtokoll.pdf` ist die verbindliche externe Referenz für Hash, Geometrie, Strukturmerkmale, 93 Feldzonen und Blank-Baselines.
- Die Referenz-PDF selbst wird nicht in die Webanwendung eingebettet und nicht als Download ausgeliefert.
- Die ausgefüllte Test-PDF wird ausschließlich über `SK_VDE_FILLED_PDF` an Tests übergeben und ist kein Bestandteil des Releases.
- PDF, JPEG, PNG und WebP werden vollständig lokal im Browser verarbeitet.
- Bei Strukturpassung ab 90 % gilt die Formularidentität als eindeutig. Ab 68 % kann das Referenzmapping technisch verwendet werden; darunter werden die erforderlichen Angaben ohne automatische Negativbewertung manuell geklärt.
- Konfidenzschwellen: 80 % für Auswahl-, Zahlen- und Datumsfelder, 74 % für Freitext.

## Projektstruktur

- `index.html` und 15 Direktseiten
- `assets/`: zentrale Laufzeitdateien, Datenkataloge, VDE-Engine, Regeln und Referenzprofil
- `plausibilitaetspruefung-vde0100-600/`: Upload-, Analyse-, Klärungs- und Ergebnisoberfläche
- `vendor/pdfjs/`: lokale PDF.js-Laufzeit
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Datenschutz-Gate, Prüfsummen und ZIP
- `tools/validate_release.py`: statische Vollständigkeits-, Datenschutz- und Integritätsprüfung
- `tools/functional-smoke-test.js`: Rechner-, Inhalts- und VDE-Regeltests
- `tools/browser-smoke-test.py`: vollständiger Browser-, Responsive-, PWA- und Offline-Test
- `tools/vde-protocol-e2e-test.py`: externe End-to-End-Tests für Referenz-PDF, Rasterbilder, ausgefüllte Test-PDF und Smartphone-Foto
- `TESTBERICHT-UND-ABNAHME.md`: geprüfter Release-Nachweis
- `SHA256SUMS.txt`: interne SHA-256-Prüfsummen

## Testen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
```

Browser- und Protokolltests verwenden externe PDF-Pfade:

```bash
export SK_VDE_REFERENCE_PDF=/sicherer/pfad/VDEProtokoll.pdf
export SK_VDE_FILLED_PDF=/sicherer/pfad/ausgefüllte-testdatei.pdf
export SK_TEST_ARTIFACT_DIR=/sicherer/pfad/testausgaben
python3 -m http.server 4173 --bind 127.0.0.1
# In einem zweiten Terminal:
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
