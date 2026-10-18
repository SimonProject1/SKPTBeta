SK PCT Tools V2.6.5.3-Beta
Stand: 18.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.5.2-Beta
Releaseart: vollständiges Projektpaket, kein Patch

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.

NEU IN V2.6.5.3-BETA
- Die in V2.6.5.2 eingeführte gemeinsame Geometrie von Standard-App-Rechteck,
  Header, Hauptinhalt und Footer bleibt unverändert.
- Die stark abgedunkelten Eigenflächen von Header und Footer wurden entfernt.
- Header, Inhalt und Footer zeigen wieder denselben durchgängigen Cyan-Blau-
  App-Hintergrund des großen abgerundeten Standard-App-Rechtecks.
- Die horizontalen Strukturkanten sind nur noch mit 8 % beziehungsweise 6 %
  transparenter Cyan-Deckkraft ausgeführt.
- Header und Footer bleiben funktional klar, wirken aber nicht mehr wie schwarze,
  angeheftete Balken oder eigenständige Kästen.
- Die Korrektur gilt über die zentrale CSS-Schicht für Startseite, Favoriten,
  Suche, Sortiermodus, alle Rechner, Datenbanken, Wissens-Hub, Herstelleransichten,
  Beiträge, Dialoge, Leerzustände und Offlineaufrufe.

UNVERÄNDERT AUS V2.6.5.2 ÜBERNOMMEN
- positionsstabile gemeinsame Referenzachsen, Headerhöhen und Außenrahmen
- Analogsignal-Rechner ohne Einheitenauswahl; MA, ME und Skalierungswerte
  einheitenlos; Signalarten 4–20 mA, 0–20 mA, 0–10 V und 2–10 V
- vollständige Vorwärts-/Umkehrrechnung, Extrapolation, Reset, Liveberechnung,
  Kopier-, Tastatur- und Touchbedienung
- alle übrigen Rechner- und Datenbanklogiken
- freigegebene Icons, Logos, Raster und Hersteller-/Wissensgrafiken
- Favoriten, freie Drag-and-Drop-Sortierung, unveränderter Sortiermodus-Header,
  Navigation, Suche und lokale Speicher-Keys
- bestehende CSS-Designtokens, PWA-Installation und Offlinefunktionen

ZENTRALE DATEIEN
- assets/app-v2-6-5-3.css
- assets/app-v2-6-5-3.js
- assets/analogsignal-rechner.js
- assets/search-index-v2-6-5-3.json
- manifest-v2-6-5-3.webmanifest
- service-worker.js / Cache-Epoch v2-6-5-3-core-r1
- TESTPLAN.md / TEST-RESULTS.txt
- DESIGN-AUDIT-V2.6.5.3-Beta.md
- UEBERGABE-V2.6.5.3-Beta.txt
- SHA256SUMS.txt

LOKAL STARTEN
  cd SK-PCT-Tools-V2.6.5.3-Beta
  python3 -m http.server 8080
  Browser: http://127.0.0.1:8080/

PRÜFUNG
  node --check assets/app-v2-6-5-3.js
  node --check assets/analogsignal-rechner.js
  python3 -m py_compile tests/*.py tools/*.py
  python3 tests/validate_project.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2653.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/visual_shell_regression_v2653.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2653.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

DEPLOYMENT
Den vollständigen Inhalt dieses Ordners gemeinsam veröffentlichen. Keine Dateien aus
V2.6.5.2 oder älteren Versionen beimischen. Nach dem Upload die PWA einmal online
öffnen, bis der Service Worker v2-6-5-3-core-r1 aktiv ist und der Offline-Cache
vollständig aufgebaut wurde. Danach Startseite und mindestens eine Unterseite offline
aufrufen.
