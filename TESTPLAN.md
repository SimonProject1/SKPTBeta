# Testplan – SK PCT Tools V2.6.3.2-Beta

Stand: 16.10.2026  
Basis: vollständige V2.6.3.1-Beta

## 1. Statische Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.2-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Manifest-, Favicon- und Apple-Touch-Verweise
- Service-Worker-Kerncache `v2-6-3-2-core-r1`
- vollständige `SHA256SUMS.txt`

## 2. Geschützte App-/PWA-Icons und separates Headerlogo

- sieben freigegebene Marken-/Browser-/Apple-/PWA-Dateien gegen feste V2.6.3.1-Hashes
- PWA-, Apple-Touch-, Maskable-, Favicon- und App-Icons bytegenau unverändert
- separate Datei `logo-sk-pct-tools-header.png` mit eigenem Referenzhash
- Headerzahnrad exakt bei 256/256 sowie root/tooth 112/138 im Generator
- Headerlogo nur im sichtbaren Header, nicht in Manifest/PWA-Iconslots
- vollständige Aufnahme beider Familien in den Offline-Kerncache

## 3. Navigationsgrafiken

- 20 bestehende App-/Wissens-/Hersteller-PNGs binär unverändert
- vier bereinigte Header-PNGs: Home, Zurück, Suche und Favoriten
- genau 24 aktive Dateien mit Präfix `v2-6-3-2-`
- PNG-Signatur, 512 × 512 px, RGBA, Alpha-Grenze und Referenzhash
- ein einzelner farbiger Grundkörper ohne CSS-Außenkachel
- Lupenmitte nicht schwarz; Favoritenzentrum klar weiß

## 4. Header und Versionsfeld

Auf Startseite und internen Seiten:
- `V2.6.3.2-Beta` und `Tool by S.K.` sichtbar
- Logo, Versionsfeld und Aktionen auf gemeinsamer vertikaler Mittellinie
- Versionsfeld: 1-px-Grundkontur, 4-px-Cyan-/Grün-Seitenakzente, keine Pseudoelement-Zierlinien
- transparente Button-Touchflächen ohne CSS-Außenkachel
- je Button genau ein geladenes 512 × 512 PNG
- Desktop/Tablet 52 px, Smartphone mindestens 44 px
- sichtbarer Fokus und `touch-action: manipulation`
- identische Geometrie in Ruhe, Hover, Fokus, Press und Aktivzustand
- 320-px-Reflow und Querformat ohne Überlauf

## 5. App-Favoritenkopplung

Für zehn Startseiten- und fünf Wissens-App-Icons:
- `.sk-favorite-button` bleibt direktes Kind von `.sk-app-icon-wrapper`
- sichtbarer Kreis 21 bis 23 px, Sollmaß 22 px
- Touchfläche mindestens 44 × 44 px
- Mittelpunkt auf der oberen rechten sichtbaren PNG-/Wrapperkante
- aktive und inaktive Zustände geometrisch identisch
- App-Kachel, Wrapper und PNG in allen Interaktionszuständen pixelstabil

## 6. Browserregression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- 320-px-Reflow-Sanity und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Fokus, Home- und Zurücknavigation
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-2-core-r1`

## 7. Visuelle Abnahme

- Startseite und Unterseite bei 390 × 844, 820 × 1180 und 1440 × 1000 rendern
- PCT-Zahnrad kleiner als in V2.6.3.1, mittig und mit gleichmäßigem Freiraum
- kompaktes Versionsfeld ohne alte Paneloptik oder untere Farblinie
- Lupe ohne schwarzen Innenkreis; keine dekorativen Leiterbahnen in Headerbuttons
- keine zusätzlichen schwarzen Außenkacheln oder horizontalen Überläufe
- App-Icons und feste Favoritenanker optisch unverändert

Nach der Abnahme werden `TEST-RESULTS.txt`, `SHA256SUMS.txt` und das vollständige
ZIP-Paket aktualisiert und erneut geprüft.
