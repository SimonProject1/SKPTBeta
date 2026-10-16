# Testplan – SK PCT Tools V2.6.3.1-Beta

Stand: 16.10.2026  
Basis: vollständige V2.6.3.0-Beta

## 1. Statische Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.1-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Manifest-, Favicon- und Apple-Touch-Verweise
- Service-Worker-Kerncache `v2-6-3-1-core-r1`
- vollständige `SHA256SUMS.txt`

## 2. Bildbestände

- 22 bestehende App-/Wissens-/Hersteller-/Home-/Zurück-PNGs binär unverändert
- 2 neue eigenständige PNGs für Suche und Favoriten
- genau 24 aktive Dateien mit Präfix `v2-6-3-1-`
- 7 neu erzeugte Logo-/Browser-/Apple-/PWA-PNGs
- PNG-Signatur, Sollgröße, RGBA/Opazität, Alpha-Grenze und Safe-Zone
- zentriertes Zahnrad bei 256/256 und kein Herkunftstext im Generator
- vollständige Aufnahme in den Offline-Kerncache

## 3. Header und Versionsschild

Auf Startseite und internen Seiten:
- `V2.6.3.1-Beta` und `Tool by S.K.` sichtbar
- Logo, Versionsschild und Aktionen auf gemeinsamer vertikaler Mittellinie
- Versionsschild mit genau einem sichtbaren Gehäuse
- Home, Zurück, Suche und Favoriten: transparente Touchfläche ohne CSS-Außenkachel
- je Button genau ein geladenes 512 × 512 PNG
- Desktop/Tablet 52 px, Smartphone mindestens 44 px
- sichtbarer Fokus und `touch-action: manipulation`
- identische Geometrie in Ruhe, Hover, Fokus, Press und Aktivzustand
- 320-px-Reflow und Querformat ohne Überlauf

## 4. App-Favoritenkopplung

Für zehn Startseiten- und fünf Wissens-App-Icons:
- `.sk-favorite-button` bleibt direktes Kind von `.sk-app-icon-wrapper`
- sichtbarer Kreis 21 bis 23 px, Sollmaß 22 px
- Touchfläche mindestens 44 × 44 px
- Mittelpunkt auf der oberen rechten sichtbaren PNG-/Wrapperkante
- aktive und inaktive Zustände geometrisch identisch
- App-Kachel, Wrapper und PNG in allen Interaktionszuständen pixelstabil

## 5. Browserregression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- 320-px-Reflow-Sanity und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Fokus und Navigation
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-1-core-r1`

## 6. Visuelle Abnahme

- Header auf 320, 390, 820 und 1440 CSS-Pixeln
- keine zusätzlichen schwarzen Außenkacheln um Header-PNGs
- zentriertes, vergrößertes PCT-Zahnrad ohne Herkunftstext
- keine abgeschnittenen Headerteile, defekten Bilder oder horizontalen Überläufe
- App-Icons und feste Favoritenanker optisch unverändert

Die ausgeführten Ergebnisse werden in `TEST-RESULTS.txt` dokumentiert. Danach werden
`SHA256SUMS.txt` und das vollständige ZIP-Paket erzeugt und erneut geprüft.
