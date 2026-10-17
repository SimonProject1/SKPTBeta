# Testplan – SK PCT Tools V2.6.4.0-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.9-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 86 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, 14 gerahmte Unterseiten und 15 aktive Browserrouten
- zentrale CSS-/JS-Datei, Manifest, Suchindex, Service Worker und Cache-Epoch
- Version `2.6.4.0-Beta` und sämtliche versionierten Dateinamen/Referenzen
- lokale Ziele, H1, Referrer-Schutz, Header, Footer und Offline-Cache-Inventar
- feste SHA-256-Referenzwerte für alle geschützten Marken-/PWA-/Icondateien
- vollständiger SHA-256-Bestand aller Projektdateien
- Python- und JavaScript-Syntax
- zentrale Clean-Design- und Favoritendialog-Tokens

## 2. Unveränderte Grafikdateien

Bytevergleich und feste SHA-256 für:
- alle 24 Navigations-/App-/Wissens-/Hersteller-PNG-Inhalte gegen V2.6.3.9-Beta
- `header-logo-simple.png` und Release-Modul-PNG
- `logo-sk-pct-tools.png`, `logo-sk-pct-tools-header.png`
- `favicon.png`, `apple-touch-icon.png`
- `icon-192.png`, `icon-512.png`, `icon-maskable-192.png`, `icon-maskable-512.png`

Zusätzlich: PNG-Signatur, 512 × 512 px, Alpha-Grenzen, Manifest-Pfade und Purpose.

## 3. Browser-, Touch-, Reorder- und Offline-Regressionslauf

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Prüfumfang:
- 1.431 Browserprüfungen
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- fünf Reorder-Profile einschließlich 320 × 700 und iPhone-Landscape 844 × 390
- 320-px-Reflow, Safe-Area und horizontale Überläufe
- pixelidentischer normaler Header vor, während und nach Sortierung
- Drag/Drop, Long-Press, Pointer-Abbruch, History, Speicherung und Reload
- Suche, Favoritenzähler, Headernavigation und feste App-Favoritenkopplung
- sechs Rechnerreferenzen einschließlich Reset, Grenzwerte und Vorzeichen-Touch
- Wissensnavigation, Offline-Start, Offline-Unterseiten und Cache-Upgrade

## 4. Spezifische Clean-Design- und Favoritenregression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
```

Prüfumfang:
- 345 Designprüfungen auf iPhone-PWA, Tablet-Touch und Desktop
- alle fünf Herstellerkacheln und fünf Wissensbeiträge
- Kachel-, Wrapper-, PNG- und Textgeometrie in Ruhe, Hover, Fokus, Drücken und aktiv
- `transform: none`, `translate: none`, `scale: none` in allen geprüften Zuständen
- transparente Wrapper ohne Border, Hintergrund, Shadow, Filter oder Pseudorahmen
- korrekte 512-px-PNG-Dateien mit Präfix `v2-6-4-0-`
- Favoritendialog: Semantik, Viewportgrenzen, Safe-Area, Einzelkontur und 44-px-Touchziele
- gespeicherte Favoriten nach Reload, Einzellöschen, „Alle leeren“, leerer Zustand und Zähler
- Escape, Fokuswiederherstellung und Tastaturbedienung

## 5. Visuelle QA

Je drei Renderings für iPhone/Smartphone, Tablet und Desktop:
- Hersteller-Hub mit Air Torque, Endress+Hauser, Siemens, Vacon und Sonstiges
- Siemens-Herstelleransicht mit beiden Wissensbeiträgen
- geöffnete Favoritenübersicht mit gespeichertem Eintrag

Abnahmekriterien:
- keine zusätzliche CSS-Iconkachel, Mehrfachkontur oder übermäßiger Schatten
- identische Icongrößen, Abstände, Textachsen und unveränderte PNG-Grafiken
- keine Lageänderung bei Interaktion
- sauberer Favoritendialog ohne alte schwarze Außenkästen oder Zierleisten
- lesbare Beschriftungen, keine Überläufe, stimmige Cyan-Blau-Grün-Familie

## 6. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`,
`UEBERGABE-V2.6.4.0-Beta.txt` und das vollständige ZIP-Paket finalisiert.
