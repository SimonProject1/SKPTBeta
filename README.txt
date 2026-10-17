SK PCT Tools 2.6.3.8-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.7-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.8-Beta ist eine vollständige neue Version und kein Patchpaket.

NEUES VEREINFACHTES HEADER-LOGO
- Neue eigenständige Datei: assets/header-logo-simple.png, 512 × 512 px, RGBA.
- Reproduzierbare Quelle: tools/generate_header_logo_simple.py.
- Das sichtbare Logo auf Startseite und Unterseiten verwendet ausschließlich diese Datei.
- Der Cyan-/Blau-/Grün-Grundkörper, die schwarze Kontur, Rundung, Lichtkante und
  räumliche Materialwirkung stammen aus derselben navigation_frame()-Familie wie
  Versionsmodul, Suche und Favoriten.
- Das große PCT-Zahnrad besitzt nur zehn klare Zähne, eine ruhige dunkle Mitte,
  einen zurückhaltenden Cyan-Lichtbogen und gut lesbaren PCT-Schriftzug.
- Leiterbahn-, Punkt-, Rahmen-, Schatten- und Dekordetails wurden nur in dieser neuen
  sichtbaren Header-Variante reduziert.
- Logo, Versionsmodul und Headerbuttons teilen weiterhin dieselbe vertikale Mittellinie
  und sichtbare Höhe: 52 px auf Desktop/Tablet, 44 px auf Smartphone/Querformat.

AUSDRÜCKLICH UNVERÄNDERT
- assets/logo-sk-pct-tools.png und assets/logo-sk-pct-tools-header.png
- assets/apple-touch-icon.png und assets/favicon.png
- assets/icon-192.png und assets/icon-512.png
- assets/icon-maskable-192.png und assets/icon-maskable-512.png
- Manifest-Iconzuordnung, PWA-/Homescreen-/installierte App-Icons
- alle 24 Navigations-/App-/Wissens-/Hersteller-PNGs inhaltlich und binär
- Drag-and-Drop-Sortierung, pointer-overlay-v3, skPctHomeOrderV1
- normaler Header im Sortiermodus und separates viewportfestes Sortier-Dock
- Suche, Favoriten, Favoritenzähler, Navigation, Touchflächen und Barrierefreiheit
- Rechner, Datenbanken, Wissensbeiträge und Offlinefunktion

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-8.css
- Zentrale Laufzeit: assets/app-v2-6-3-8.js
- Sichtbares Header-Logo: assets/header-logo-simple.png
- Release-Modul-Haut: assets/release-module-v2-6-3-8.png
- Manifest: manifest-v2-6-3-8.webmanifest
- Suchindex: assets/search-index-v2-6-3-8.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-8-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 -m http.server 8080
3. SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

Die finalen Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
