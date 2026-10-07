# Architektur – SK PLT Tools 2.1.0.4-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der direkten Basis 2.1.0.3-Beta bleibt erhalten; stabile Referenz ist 2.1.0.0.
2. Das Projekt bleibt statisch, lokal betreibbar, offline-fähig und ohne Cloud-Abhängigkeit.
3. Formularidentität, Feldzuordnung, fachliche Regeln, UI-Klärung und Release-Integrität sind getrennte Schichten.
4. Unsicherheit wird sichtbar gemacht und nie automatisch in ein negatives Endergebnis umgedeutet.
5. Pflichtfelder und sicherheitsrelevante Abweichungen können nicht durch „nicht relevant“ ausgeblendet werden.

## Schichten

### Shell und PWA

`assets/app.js`, `assets/core.css`, statische HTML-Seiten, Manifest und Service Worker bilden die gemeinsame Anwendungsschale. Der Service Worker verwendet ausschließlich den Release-Cache `sk-plt-tools-v2.1.0.4-Beta` und bereinigt ältere Cache-Versionen.

### VDE-Domänenengine

`assets/vde0100-600-engine.js` enthält Feldschema, Genau-ein-Kreuz-Regel, Auflösungs-Governance, Pflichtfeldprüfung und Messwert-Plausibilität. Die Engine ist DOM-unabhängig und wird im Node-Smoke-Test geprüft.

Die Formularidentität erzeugt ausschließlich `FORM-IDENTITY` mit Status `open` und Kennzeichen `technicalOnly`. Sie erzeugt niemals einen fachlichen `fail`. Mehrfach- und ungültige Kreuze werden als `CHOICE-MULTIPLE-*` beziehungsweise `CHOICE-INVALID-*` geführt.

### VDE-Dokumentenerkennung

`plausibilitaetspruefung-vde0100-600/checker.js` übernimmt lokale Datei-, Bild- und UI-Verarbeitung:

- PDF.js-Rendering und Foto-Skalierung,
- Kontrastnormalisierung und Ausrichtung,
- Struktur-Ensemble für die technische Formularidentität,
- Referenzmapping ab 0,68 Strukturpassung,
- referenzbereinigte Evidenz für Felder, Checkboxen und Unterschriften,
- getrennte sichere und unsichere Checkbox-Kandidaten,
- sequentielle Klärung mit Originalausschnitten,
- eigener Drei-Optionen-Dialog für unsichere Formulare,
- Ergebnis-Gate bis zur vollständigen Klärung.

`assets/vde0100-600-template.json` enthält 93 Feldzonen, Struktur-Fingerabdruck und Blank-Baselines. Die leere Referenz-PDF selbst ist nicht Bestandteil der Webanwendung.

### Release- und Testschicht

- `tools/release.py`: Versionssynchronisierung, Precache, Datenschutz-Gate, Prüfsummen und ZIP.
- `tools/validate_release.py`: Struktur-, Referenz-, Manifest-, Datenschutz- und Integritätsprüfung.
- `tools/functional-smoke-test.js`: DOM-unabhängige Funktions- und VDE-Regeltests.
- `tools/browser-smoke-test.py`: 16 Direktseiten, Responsive-Ansichten, PWA und Offline.
- `tools/vde-protocol-e2e-test.py`: Referenz-PDF/PNG/JPEG sowie externe ausgefüllte PDF und daraus nur temporär erzeugtes Smartphone-Foto.

## Erkennungs-Governance

- Eindeutige Identität: Strukturwert ≥ 0,90 oder exakter Referenz-Hash.
- Technisch mappbar, aber unsicher: 0,68 bis < 0,90.
- Stark unsicher: < 0,68; Pflichtfelder werden manuell zugeordnet.
- Feldkonfidenz: 0,80 für Auswahl/Zahl/Datum, 0,74 für Text.
- „Nicht relevant“: nur gemäß Felddefinition; niemals als Überspringen von Pflichtfeldern oder bestätigten Sicherheitsabweichungen.
- Ergebnis: erst nach leerer Offenpunkt-Warteschlange.

## PWA-Identität

- Version: `2.1.0.4-Beta`
- PWA-ID und Start-URL: `./?app=sk-plt-tools-2.1.0.4-beta`
- Cache: `sk-plt-tools-v2.1.0.4-Beta`
- Release-ZIP: `SK-PLT-Tools-V2.1.0.4-Beta.zip`
