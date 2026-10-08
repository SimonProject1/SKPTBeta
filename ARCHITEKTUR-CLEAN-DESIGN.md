# Architektur – SK PLT Tools 2.1.1.0-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der direkten Basis 2.1.0.5-Beta bleibt außerhalb des VDE-Moduls erhalten; stabile Referenz ist 2.1.0.0.
2. Das Projekt bleibt statisch, lokal auslieferbar, PWA-fähig und ohne Serverkomponente.
3. Gemeinsame Shell, Navigation, Favoriten, Suche, Werkzeuge und Wissensdatenbank bleiben integriert.
4. Der VDE-Messwertprüfer verarbeitet ausschließlich manuelle Eingaben.
5. Kein kontextabhängiger Grenzwert wird pauschal angenommen.
6. Ein Ergebnis ist nur bei vollständiger und gültiger Berechnungsgrundlage möglich.

## Anwendungsschichten

### Gemeinsame Anwendungsschicht

- `assets/app.js` – Navigation, Suche, Favoriten und Service-Worker-Registrierung.
- `assets/core.css` und `assets/logo-layout.css` – zentrale Oberfläche.
- `shared/` – synchronisierte Header-, Footer- und Bedienelemente.
- `service-worker.js` und `manifest.webmanifest` – versionsisolierte Offline-PWA.

### VDE-Eingabeschicht

- `plausibilitaetspruefung-vde0100-600/index.html` – manueller Prüfstand mit sechs Messgrößen.
- `plausibilitaetspruefung-vde0100-600/checker.js` – dynamische Felder, gezielte Fehlermeldungen, Ergebnissperre und Sitzungsübersicht.
- `assets/vde0100-600-input-schema.json` – ausschließlich Eingabefelder und bedingte Sichtbarkeit; keine Grenzwert-Defaults.

Es gibt keinen Datei-Upload, keine PDF-/Fotoverarbeitung, keine OCR, keinen Feldlokator und keine Protokollklassifikation.

### VDE-Rechenengine

- `assets/vde0100-600-engine.js`
  - Spannungsfall direkt oder aus `ΔU / Un × 100`,
  - Isolationsmessung gegen freigegebenen Mindestwert,
  - Schleifenimpedanz gegen direkten Sollwert oder `U0 / Ia`,
  - Kurzschlussstrom gegen freigegebenes `Ia`,
  - RCD-Zeit und -Strom gegen freigegebene Grenzen,
  - Niederohmigkeit und Schutzpotentialausgleich gegen freigegebene Maximalwerte,
  - explizite Zustände `incomplete`, `error`, `pass` und `fail`.

### Regel- und Governance-Metadaten

- `assets/vde0100-600-rules.json` – dokumentierte Formeln, Ausschlüsse und Verbot numerischer Defaults.
- `VDE0100-600-MESSWERTPRUEFER.md` – fachlich-technische Projektregelung.

## Test- und Release-Architektur

- `tools/functional-smoke-test.js` – bestehende Module plus vollständige VDE-Rechenmatrix.
- `tools/vde-protocol-e2e-test.py` – manueller Browserablauf einschließlich gezielter Fehlwertabfrage; Dateiname aus Strukturkompatibilität.
- `tools/browser-smoke-test.py` – 16 Direktseiten, Responsive-Design, PWA und Offline-Cache.
- `tools/validate_release.py` – Struktur, Version, VDE-Ausschlüsse, lokale Referenzen, Syntax und Prüfsummen.
- `tools/release.py` – zentrale Versionierung, Precache, Prüfsummen und vollständiges ZIP.

## Sicherheitsgrenze

Das Modul ist eine digitale rechnerische Zweitkontrolle. Es führt keine Messung durch, deckt keine vollständige normative Anlagenbewertung ab und erteilt keine Inbetriebnahmefreigabe.
