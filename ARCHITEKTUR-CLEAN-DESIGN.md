# Architektur – SK PLT Tools 2.1.0.3-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der direkten Basis 2.1.0.2-Beta bleibt erhalten; stabile Referenz ist 2.1.0.0.
2. Das Projekt bleibt statisch, lokal betreibbar, offline-fähig und ohne Cloud-Abhängigkeit.
3. Fachliche Erkennung, UI-Klärung und Release-Integrität sind getrennte Schichten.
4. Unsicherheit wird sichtbar gemacht; die Anwendung erzeugt keine scheinbar sicheren Werte.
5. Sicherheitsrelevante Abweichungen können nicht durch UI-Aktionen ausgeblendet werden.

## Schichten

### Shell und PWA

`assets/app.js`, `assets/core.css`, statische HTML-Seiten, Manifest und Service Worker bilden die gemeinsame Anwendungsschale. Der Service Worker verwendet ausschließlich den Release-Cache `sk-plt-tools-v2.1.0.3-Beta` und bereinigt ältere Cache-Versionen.

### VDE-Domänenengine

`assets/vde0100-600-engine.js` enthält Feldschema, Auflösungs-Governance, Vollständigkeitsregeln und Messwert-Plausibilität. Die Engine ist DOM-unabhängig und wird im Node-Smoke-Test geprüft.

### VDE-Dokumentenerkennung

`plausibilitaetspruefung-vde0100-600/checker.js` übernimmt ausschließlich lokale Datei-, Bild- und UI-Verarbeitung:

- PDF.js-Rendering und Foto-Skalierung,
- Kontrastnormalisierung und Ausrichtung,
- Struktur-Ensemble für die Formularidentität,
- referenzbereinigte Evidenz für Felder, Checkboxen und Unterschriften,
- Konfidenzbildung und sequentielle Klärung,
- Ausschnitte aus dem Nutzeroriginal.

`assets/vde0100-600-template.json` enthält 93 Feldzonen, Struktur-Fingerabdruck und Blank-Baselines. Die leere Referenz-PDF selbst ist nicht Bestandteil der Webanwendung.

### Release- und Testschicht

- `tools/release.py`: Versionssynchronisierung, Precache, Datenschutz-Gate, Prüfsummen, ZIP.
- `tools/validate_release.py`: Struktur-, Referenz-, Manifest-, Datenschutz- und Integritätsprüfung.
- `tools/functional-smoke-test.js`: DOM-unabhängige Funktions- und VDE-Regeltests.
- `tools/browser-smoke-test.py`: 16 Direktseiten, Responsive-Ansichten, PWA und Offline.
- `tools/vde-protocol-e2e-test.py`: externe Protokolldateien; keine reale ausgefüllte Fixture im Release.

## Erkennungs-Governance

- Akzeptiert: Strukturwert ≥ 0,90 oder exakter Referenz-Hash.
- Klärbar: 0,84 bis < 0,90.
- Hart abgelehnt: < 0,84; kein positionsgebundenes Feldmapping.
- Feldkonfidenz: 0,80 für Choice/Zahl/Datum, 0,74 für Text.
- „Nicht relevant“: nur gemäß Felddefinition; niemals für bestätigte n.i.O.-, Grenzwert-, Signatur- oder Formularfehler.

## PWA-Identität

- Version: `2.1.0.3-Beta`
- PWA-ID und Start-URL: `./?app=sk-plt-tools-2.1.0.3-beta`
- Cache: `sk-plt-tools-v2.1.0.3-Beta`
- Release-ZIP: `SK-PLT-Tools-V2.1.0.3-Beta.zip`
