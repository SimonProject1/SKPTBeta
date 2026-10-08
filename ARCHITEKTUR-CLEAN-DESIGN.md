# Architektur – SK PLT Tools 2.1.0.5-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der direkten Basis 2.1.0.4-Beta bleibt erhalten; stabile Referenz ist 2.1.0.0.
2. Das Projekt bleibt statisch, lokal auslieferbar, PWA-fähig und ohne Serverkomponente.
3. Gemeinsame Shell, Navigation, Favoriten, Suche, Werkzeuge und Wissensdatenbank bleiben unverändert integriert.
4. Die VDE-Prüfung trennt Dokumentverarbeitung, Messwertzuordnung, Rechenengine und Nutzerklärung strikt voneinander.
5. Nur Mess- und notwendige Bezugswerte dürfen die VDE-Entscheidung beeinflussen.

## Schichten

### Gemeinsame Anwendungsschicht

- `assets/app.js` – Navigation, Suche, Favoriten und Service-Worker-Registrierung.
- `assets/core.css` und `assets/logo-layout.css` – zentrale Oberfläche.
- `shared/` – synchronisierte Header-, Footer- und Bedienelemente.
- `service-worker.js` und `manifest.webmanifest` – versionsisolierte Offline-PWA.

### VDE-Dokumentadapter

- `plausibilitaetspruefung-vde0100-600/checker.js`
  - lokales Einlesen von PDF und Smartphone-Foto,
  - PDF.js-Rendering,
  - Ausrichtung und Kontrastnormalisierung,
  - eingebettete PDF-Texterkennung,
  - optionale lokale `TextDetector`-Bildtexterkennung,
  - interne Feldlokalisierung,
  - Einzelabfrage fehlender/unsicherer Werte,
  - Sperre des Endergebnisses bei offenen Werten.

### Interner Messfeld-Lokator

- `assets/vde0100-600-template.json`
  - externer Herkunftsnachweis der nicht eingebetteten Vorlage,
  - Struktur-Fingerabdruck zur Seitenausrichtung,
  - 18 Feldzonen ausschließlich für Mess- und Bezugswerte,
  - leere Feldbaselines zur Erkennung visueller Einträge.

Der Lokator erzeugt keinen fachlichen Status und wird nicht sichtbar ausgegeben.

### VDE-Rechenengine

- `assets/vde0100-600-engine.js`
  - 19 zugelassene Mess-/Bezugsfelder,
  - 12 auswählbare Messgrößengruppen,
  - Bedarfsauflösung notwendiger Bezugsdaten,
  - Rechenregeln und Grenzwerte,
  - neutrale Offenpunkte für fehlende/unsichere Werte,
  - grünes Ergebnis nur bei Vollständigkeit und bestandenen Regeln,
  - rotes Ergebnis nur bei bestätigter Rechenabweichung.

Formale Felder existieren in dieser Engine nicht.

### Regel- und Governance-Metadaten

- `assets/vde0100-600-rules.json`
  - explizite Ausschlussliste formaler Angaben,
  - Ergebnis-Governance,
  - dokumentierte Grenzwerte und Formeln.

## Test- und Release-Architektur

- `tools/functional-smoke-test.js` – deterministische Engine- und Rechenregressionen.
- `tools/vde-protocol-e2e-test.py` – Positiv-PDF, fehlende Bezugsgröße, bestätigter Negativwert und Smartphone-Foto.
- `tools/browser-smoke-test.py` – 16 Direktseiten, Responsive-Design, PWA und Offline-Cache.
- `tools/validate_release.py` – Struktur, Versionskonsistenz, formale Ausschlüsse, interne Vorlage, Datenschutz, lokale Referenzen, Syntax und Prüfsummen.
- `tools/release.py` – zentrale Versionierung, Precache, Prüfsummen und vollständiges ZIP.

## Sicherheitsgrenze

Das Modul ist eine lokale rechnerische Zweitkontrolle. Es führt keine Messung durch, bewertet keine normativen Sonderfälle vollständig und erteilt keine Inbetriebnahmefreigabe.
