# Testplan – SK PCT Tools V2.6.1.9-Beta

Stand: 16.10.2026

## 1. Statische Struktur- und Integritätsprüfung

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und eine zentrale App-JS-Datei
- Version 2.6.1.9-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Verweise auf V2.6.1.0 bis V2.6.1.8
- lokale Referenzen, H1, Referrer-Schutz, Header und Footer
- vollständige SHA256SUMS.txt
- Service-Worker-Kerncache `v2-6-1-9-core-r1`
- vollständiger Control-Sprite

## 2. Unveränderte Icon-Dateien

- genau 22 aktive PNGs mit Präfix `v2-6-1-9-`
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons
- PNG-Signatur, 512 × 512 px, RGBA und echte Transparenz
- SHA-256 jedes PNGs entspricht dem freigegebenen Referenzwert
- 22 unterschiedliche Dateihashes
- vollständige Aufnahme in den Offline-Kerncache
- sichtbare Alpha-Grenze jedes Icons exakt `(13, 9, 489, 491)`
- Bilddaten gegenüber V2.6.1.8-Beta unverändert

## 3. Strukturelle Wrapperprüfung

Für zehn Startseiten- und fünf Wissens-App-Icons:
- `.sk-app-icon-wrapper` ist der feste gemeinsame Bezug für PNG und Button
- `.sk-favorite-button` ist direktes Kind des jeweiligen Wrappers
- der Wrapper stimmt mit der aus dem PNG skalierten sichtbaren Alpha-Grenze überein
- Kachel, Grid, Titelbereich und Viewportabstände sind keine Positionsbasis
- finale Favoritenposition enthält keine 50-%-/Kachelmittenberechnung
- keine breakpointabhängige Positionsregel für den Favoritenbutton

## 4. App-Icon- und Favoritengeometrie

Für Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000:
- sichtbarer Favoritenkreis 21 bis 23 px, Sollmaß 22 px
- Touchfläche mindestens 44 × 44 px
- Kreismittelpunkt höchstens 0,25 CSS-Pixel von der tatsächlichen oberen rechten
  sichtbaren PNG-/Wrapperkante entfernt
- je 48 bis 52 % sichtbare Überdeckung und Außenanteil
- aktive und inaktive Favoriten besitzen dieselbe Geometrie
- App-Kachel, Wrapper und PNG werden bei Hover, Fokus, Press und Aktivzustand
  je Kante mit höchstens 0,25 CSS-Pixel Abweichung geprüft
- dieselbe Prüfung gilt für alle fünf Wissens-App-Icons

## 5. Browser-Regression

```bash
python3 tests/browser_regression.py
```

Weiterer Prüfumfang:
- 15 Routen × Smartphone, Tablet und Desktop
- Header, Footer, Rahmen, Scrollverhalten und horizontaler Überlauf
- 320-px-Reflow-Sanity
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation, Kompaktansicht und Quellenbündel
- Offline-Start und Offline-Unterseiten
- Upgrade-Test: Altcache wird entfernt, nur `v2-6-1-9-core-r1` bleibt

## 6. Visuelle Abnahme

- Startseite bei 390 × 844, 820 × 1180 und 1440 × 1000 rendern
- aktive und inaktive Sterne zusammen prüfen
- keine Kollision mit Hauptsymbol, Titel oder Nachbarkachel
- keine abgeschnittenen Icons, defekten Bilder oder horizontalen Überläufe
- unverändertes Icon-Design gegenüber V2.6.1.8-Beta

Die real ausgeführten Ergebnisse werden in `TEST-RESULTS.txt` festgehalten. Danach
werden `SHA256SUMS.txt` und das ZIP-Paket erstellt und abschließend validiert.
