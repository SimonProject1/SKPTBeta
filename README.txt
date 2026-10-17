SK PCT Tools 2.6.3.9-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.8-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.9-Beta ist eine vollständige neue Version und kein Patchpaket.

ÜBERARBEITETES VEREINFACHTES HEADER-LOGO
- Ausschließlich assets/header-logo-simple.png wurde gestalterisch überarbeitet.
- Reproduzierbare Quelle: tools/generate_header_logo_simple.py.
- Die große dunkle Innenfläche des PCT-Zahnrads wurde durch eine helle, ruhige
  Cyan-Stahl-Innenfläche mit schmaler schwarzer Kontur und dezenter Cyan-Lichtkante ersetzt.
- Der gemessene dunkle Flächenanteil im zentralen Prüfradius sank von 84,9 % auf 37,1 %;
  die mittlere Innenhelligkeit stieg von 41,1 auf 138,6 von 255.
- Der PCT-Schriftzug bleibt in dunkler, kontrastreicher Ausführung bei 44 und 52 px klar lesbar.
- Zahnradform, zehn klare Zähne, schwarze Außenkontur, Cyan-Blau-Grün-Grundkörper,
  Rundung, Lichtkante, räumliche Tiefe und visuelle Identität bleiben erhalten.
- Das Logo wird weiterhin ausschließlich als sichtbares Header-Logo auf Startseite und
  Unterseiten verwendet.

AUSDRÜCKLICH UNVERÄNDERT
- assets/logo-sk-pct-tools.png und assets/logo-sk-pct-tools-header.png
- assets/apple-touch-icon.png und assets/favicon.png
- assets/icon-192.png und assets/icon-512.png
- assets/icon-maskable-192.png und assets/icon-maskable-512.png
- Manifest-Iconzuordnung, PWA-/Homescreen-/installierte App-Icons
- alle 24 Navigations-/App-/Wissens-/Hersteller-PNGs inhaltlich und binär
- Release-Modul-Grafik inhaltlich und binär
- Drag-and-Drop-Sortierung, pointer-overlay-v3 und skPctHomeOrderV1
- normaler Header im Sortiermodus und separates viewportfestes Sortier-Dock
- Suche, Favoriten, Favoritenzähler, Navigation, Touchflächen und Barrierefreiheit
- Rechner, Datenbanken, Wissensbeiträge und Offlinefunktion

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-9.css
- Zentrale Laufzeit: assets/app-v2-6-3-9.js
- Sichtbares Header-Logo: assets/header-logo-simple.png
- Release-Modul-Haut: assets/release-module-v2-6-3-9.png
- Manifest: manifest-v2-6-3-9.webmanifest
- Suchindex: assets/search-index-v2-6-3-9.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-9-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 -m http.server 8080
3. SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

Die finalen Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
