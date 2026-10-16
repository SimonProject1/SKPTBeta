# Testplan – SK PCT Tools V2.6.2.0-Beta

Stand: 16.10.2026

## 1. Statische Struktur- und Integritätsprüfung

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und eine zentrale App-JS-Datei
- Version 2.6.2.0-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Referenzen auf V2.6.1.x
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Manifest-, Favicon- und Apple-Touch-Verweis in allen 16 HTML-Dokumenten
- vollständige SHA256SUMS.txt
- Service-Worker-Kerncache `v2-6-2-0-core-r1`

## 2. Neue Marken-/PWA-Familie

- reproduzierbare Erzeugung mit `python3 tools/generate_brand_assets.py`
- logo-sk-pct-tools.png und icon-512.png: 512 × 512, RGBA, transparent
- icon-192.png: 192 × 192, RGBA, transparent
- favicon.png: 64 × 64, RGBA, transparent
- apple-touch-icon.png: 180 × 180, vollständig opak
- icon-maskable-192.png und icon-maskable-512.png: vollständig opak
- ausreichende schwarze Kontur-, weiße Motiv-, Cyan- und Grünmasse
- zentrale kontrastreiche Markeninformation innerhalb des 80-%-Safe-Zone-Kreises
- `any`/`maskable`-Purpose im Manifest korrekt
- sichtbares Startseiten-, Header- und Seitenkopf-Logo verweist auf den Markenmaster
- alle sieben Dateien im Offline-Kerncache

## 3. Unveränderte freigegebene Navigationsicons

- genau 22 aktive PNGs mit Präfix `v2-6-2-0-`
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons
- PNG-Signatur, 512 × 512 px, RGBA und echte Transparenz
- SHA-256 jedes PNGs entspricht dem freigegebenen Referenzwert
- Bilddaten gegenüber V2.6.1.9-Beta bitidentisch
- sichtbare Alpha-Grenze jedes Icons exakt `(13, 9, 489, 491)`
- vollständige Aufnahme in den Offline-Kerncache

## 4. Strukturelle Favoritenkopplung

Für zehn Startseiten- und fünf Wissens-App-Icons:
- `.sk-app-icon-wrapper` bleibt fester gemeinsamer Bezug für PNG und Button
- `.sk-favorite-button` bleibt direktes Kind des Wrappers
- sichtbarer Favoritenkreis 21 bis 23 px, Sollmaß 22 px
- Touchfläche mindestens 44 × 44 px
- Kreismittelpunkt maximal 0,25 CSS-Pixel von der tatsächlichen oberen rechten
  sichtbaren PNG-/Wrapperkante entfernt
- aktive und inaktive Zustände geometrisch identisch
- keine Verschiebung in Ruhe, Hover, Fokus, Press oder Aktivzustand

## 5. Browser-Regression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- neues Startseiten- und Headerlogo vollständig geladen, natürliche Größe 512 × 512
- Manifest-Version und PWA-Icon-Purpose im echten Browser
- Header, Footer, Rahmen, Scrollverhalten und horizontaler Überlauf
- 320-px-Reflow-Sanity
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation, Kompaktansicht und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-2-0-core-r1`

## 6. Visuelle Abnahme

- Startseite und interne Seite bei Smartphone, Tablet und Desktop rendern
- PCT bei kleinen Header-/Favicon-Abmessungen eindeutig erkennbar
- SK und TOOL'S BY S.K. bei regulären App-/PWA-Größen lesbar
- keine abgeschnittenen Markenbestandteile in Standardvarianten
- Maskable-Vorschau für Kreis-/Squircle-Beschnitt ohne Verlust zentraler Information
- App-Icons, Favoritenposition und Favoritenzustände optisch unverändert
- keine defekten Bilder oder horizontalen Überläufe

Die tatsächlich ausgeführten Ergebnisse werden in `TEST-RESULTS.txt` festgehalten.
Danach werden `SHA256SUMS.txt` und das vollständige ZIP-Paket erstellt und geprüft.
