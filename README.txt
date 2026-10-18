SK PCT Tools V2.6.5.4-Beta
Stand: 18.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.5.3-Beta
Releaseart: vollständiges Projektpaket, kein Patch

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.

NEU IN V2.6.5.4-BETA
Ausschließlich der Analogsignal-Rechner wurde entsprechend dem aktuellen
Benutzerfeedback überarbeitet:
- Kicker „SIGNALTECHNIK · TÜV-PRAXIS“ vollständig entfernt.
- sichtbare Buttons „Berechnen“ und „Zurücksetzen“ einschließlich Aktionswrappern
  und zugehörigen Analogsignal-spezifischen CSS-Regeln entfernt.
- automatische Liveberechnung bleibt für jede Eingabe und Auswahl aktiv.
- Kopierbuttons der beiden Ergebnisfelder einschließlich Hosts, Touchflächen,
  Tooltips und dafür reservierter Abstände vollständig entfernt.
- Ergebniswerte bleiben vollständig sichtbar und werden per aria-live aktualisiert.
- Layout nach Entfernung der Bedienelemente kompakt und ausgewogen geschlossen.

FACHLICH ERHALTEN
- Messbereichsanfang MA und Messbereichsende ME
- Signalarten 4–20 mA, 0–20 mA, 0–10 V und 2–10 V
- Skalierungswert → Signal und Signal → Skalierungswert
- einheitenlose Skalierung, Formeln, Umkehrrechnung und Extrapolation
- Validierung für unvollständige/ungültige Werte und MA = ME
- Tastatur-, Touch-, Fokus-, Accessibility- und Offlineverhalten

UNVERÄNDERT
Alle anderen Rechner, Datenbanken, Wissensbereiche, Icons, Logos, Header, Footer,
Favoriten, Raster, Suche und die Drag-and-Drop-Sortierung wurden unverändert aus
der vollständigen V2.6.5.3-Beta übernommen.

VERSIONIERTE KERNDATEIEN
- assets/app-v2-6-5-4.css
- assets/app-v2-6-5-4.js
- assets/analogsignal-rechner.js
- assets/search-index-v2-6-5-4.json
- manifest-v2-6-5-4.webmanifest
- service-worker.js / Cache-Epoch v2-6-5-4-core-r1
- assets/navigation-icons/v2-6-5-4-*.png
- assets/release-module-v2-6-5-4.png
- TESTPLAN.md / TEST-RESULTS.txt
- DESIGN-AUDIT-V2.6.5.4-Beta.md
- UEBERGABE-V2.6.5.4-Beta.txt
- SHA256SUMS.txt

LOKAL STARTEN
  cd SK-PCT-Tools-V2.6.5.4-Beta
  python3 -m http.server 8080
  Browser: http://127.0.0.1:8080/

PRÜFUNG
  node --check assets/app-v2-6-5-4.js
  node --check assets/analogsignal-rechner.js
  python3 -m py_compile tests/*.py tools/*.py
  python3 tests/validate_project.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2654.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/visual_shell_regression_v2654.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2654.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

DEPLOYMENT
Den vollständigen Inhalt dieses Ordners gemeinsam veröffentlichen. Keine Dateien
aus V2.6.5.3 oder älteren Versionen beimischen. Nach dem Upload die PWA einmal
online öffnen, bis der Service Worker v2-6-5-4-core-r1 aktiv ist und der Offline-
Cache vollständig aufgebaut wurde. Danach Startseite und Analogsignal-Rechner
offline prüfen.
