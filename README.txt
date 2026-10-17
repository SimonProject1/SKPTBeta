SK PCT Tools V2.6.5.0-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.4.0-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.5.0-Beta ist ein vollständiges Releasepaket und kein Patchpaket.

INHALT
- 10 Startseiten-Apps, darunter 6 Rechner, 2 Datenbanken, Wissensdatenbank und
  externer E+H Device Viewer
- 16 HTML-Dokumente, davon 14 aktive interne Unterseiten und eine Weiterleitung
- Wissens-Hub mit 5 Herstellerbereichen und 5 vollständigen Wissensbeiträgen
- lokale Datensätze für Einheiten und Werkstoffe
- PWA-Manifest, Service Worker, vollständiger Offline-Precache und Safe-Area-Support
- Favoriten, Suche, Filter, Sortierung und freie Drag-and-Drop-Appreihenfolge

DESIGN- UND BEDIENSTANDARD V2.6.5.0-BETA
- zentrale Designtokens für Farbe, Oberfläche, Linie, Statusfarbe, Radius,
  Typografie, Schatten und 4-/8-/12-/16-/24-/32-px-Abstandsraster
- ein klares Ebenenmodell aus App-Rahmen, Funktionspanel und Control
- Mindesttouchziele 44 × 44 px, Primäraktionen bevorzugt 46–48 px
- transparente Iconhosts; freigegebene PNGs übernehmen allein die sichtbare
  App-, Hersteller-, Wissens- und Seitenidentität
- 5 × 2-Desktop-Raster für alle 10 Apps, responsive Tablet-/Smartphone-Raster
- neue wartbare SVG-Bedienicon-Familie in assets/pct-controls.svg
- ± ausschließlich für Vorzeichenwechsel; Chevron unten/oben für Auf-/Zuklappen
- mobile Zurück-Chips, kompakter Footer und vollständig überarbeitete Suche
- Favoritenliste mit Icon links, Titel/Beschreibung mittig und Entfernen rechts

BYTEGENAU UNVERÄNDERTE FREIGEGEBENE GRAFIKEN
- sämtliche 24 App-, Navigations-, Hersteller- und Wissens-PNG-Inhalte
- logo-sk-pct-tools.png, logo-sk-pct-tools-header.png, header-logo-simple.png
- favicon.png, apple-touch-icon.png
- icon-192.png, icon-512.png, icon-maskable-192.png, icon-maskable-512.png
- Release-Modul-PNG-Inhalt
Nur versionsgebundene Dateinamen wurden von v2-6-4-0 auf v2-6-5-0 geändert.
Die festen Referenz-Hashes stehen in tests/validate_project.py.

ZENTRALE DATEIEN
- assets/app-v2-6-5-0.css          zentrales Design und responsive Layout
- assets/app-v2-6-5-0.js           Layout, Favoriten, Suche, Sortierung, Controls
- assets/pct-controls.svg           kleine Bedienicon-Familie
- assets/search-index-v2-6-5-0.json zentraler Suchindex
- manifest-v2-6-5-0.webmanifest    PWA-Manifest
- service-worker.js                 Offlinebetrieb, Cache v2-6-5-0-core-r1
- VERSION                           2.6.5.0-Beta

LOKAL STARTEN
  cd SK-PCT-Tools-V2.6.5.0-Beta
  python3 -m http.server 8080
  Browser: http://127.0.0.1:8080/

PRÜFUNG
  python3 tests/validate_project.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2650.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

TEST-RESULTS.txt enthält die finalen Resultate. SHA256SUMS.txt enthält alle
Projektdateien außer SHA256SUMS.txt selbst. Das ZIP wird zusätzlich separat per
SHA-256 verifiziert.
