SK PCT Tools V2.6.5.1-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.5.0-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.5.1-Beta ist ein vollständiges Releasepaket und kein Patchpaket.

INHALT
- 10 Startseiten-Apps, darunter 6 Rechner, 2 Datenbanken, Wissensdatenbank und
  externer E+H Device Viewer
- 16 HTML-Dokumente mit 14 aktiven internen Unterseiten
- Wissens-Hub mit 5 Herstellerbereichen und 5 vollständigen Wissensbeiträgen
- lokale Datensätze für Einheiten und Werkstoffe
- PWA-Manifest, Service Worker, Offline-Precache und Safe-Area-Support
- Favoriten, Suche, Filter, Sortierung und freie Drag-and-Drop-Appreihenfolge

NEU IN V2.6.5.1-BETA
1. Hersteller-Hub der Wissensdatenbank
- Air Torque, Endress+Hauser, Siemens, Vacon und Sonstiges verwenden dieselbe
  responsive Rasterlogik wie die App-Kacheln auf der Startseite.
- Spaltenwechsel, sichtbare PNG-Größe, Beschriftungsabstand, Zentrierung und
  Flächennutzung sind über Smartphone, Querformat, Tablet und Desktop gekoppelt.
- Herstellericons und Bezeichnungen bleiben unverändert; Interaktionszustände
  verändern weder Lage noch Größe der Kacheln.
- Suche, Filterung, Navigation, Touchflächen und Herstelleransichten bleiben erhalten.

2. Favoriten als reguläre Unteransicht
- Die Favoritenübersicht bleibt vollständig im großen abgerundeten App-Rechteck.
- Der mittlere Seiteninhalt wird ersetzt; bestehender Header, Außenrahmen und Footer
  bleiben sichtbar und geometrisch unverändert.
- Kurze, lange und leere Listen werden im inneren Favoritenbereich dargestellt.
- Lange Listen scrollen innerhalb des Rahmens; die äußere App-Hülle scrollt nicht weg.
- Icon links, Titel/Beschreibung mittig und Entfernen rechts bleiben erhalten.
- Zähler, Öffnen, Einzellöschen, Alle leeren, Escape, Fokusführung und 44-px-
  Touchziele bleiben erhalten.
- Gespeicherte Favoriten aus V2.6.5.0 werden weiterverwendet; veraltete versionierte
  Icon-URLs werden auf die aktuellen V2.6.5.1-PNGs abgebildet.

UNVERÄNDERT ÜBERNOMMEN
- alle freigegebenen App-, Navigations-, Hersteller-, Wissens-, Header-, PWA-,
  Maskable-, Favicon- und Marken-PNG-Inhalte
- Header, Release-Modul, Suche, Sortiermodus und pointer-overlay-v3
- freie Drag-and-Drop-Sortierung, Undo/Redo, Standard und Speicherung
- Rechner, Datenbanken, Wissensbeiträge und fachliche Berechnungslogik
- CSS-Designtokens, Safe Area, Manifestverhalten und Offlinebetrieb

ZENTRALE DATEIEN
- assets/app-v2-6-5-1.css          zentrales Design und responsive Layout
- assets/app-v2-6-5-1.js           Layout, Favoriten, Suche, Sortierung, Controls
- assets/pct-controls.svg           Bedienicon-Familie
- assets/search-index-v2-6-5-1.json zentraler Suchindex
- manifest-v2-6-5-1.webmanifest    PWA-Manifest
- service-worker.js                 Offlinebetrieb, Cache v2-6-5-1-core-r1
- VERSION                           2.6.5.1-Beta

LOKAL STARTEN
  cd SK-PCT-Tools-V2.6.5.1-Beta
  python3 -m http.server 8080
  Browser: http://127.0.0.1:8080/

PRÜFUNG
  python3 tests/validate_project.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2651.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

TEST-RESULTS.txt enthält die finalen Resultate. SHA256SUMS.txt umfasst alle
Projektdateien außer sich selbst. Das vollständige ZIP besitzt zusätzlich eine
separat verifizierte SHA-256-Prüfsumme.
