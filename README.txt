SK PCT Tools V2.6.5.2-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.5.1-Beta
Releaseart: vollständiges Projektpaket, kein Patch

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.

NEU IN V2.6.5.2-BETA
1. Analogsignal-Rechner für TÜV-Abnahmen
- Die sichtbaren Felder für Prozesskategorie, Prozesseinheit und Signaleinheit wurden
  vollständig entfernt.
- MA und ME sind bewusst einheitenlose Skalierungswerte.
- Signalarten: 4–20 mA, 0–20 mA, 0–10 V und 2–10 V.
- Umrechnung Skalierungswert → Signal und Signal → Skalierungswert.
- Die linearen Berechnungsformeln und die freie Extrapolation außerhalb des
  Nennbereichs bleiben fachlich unverändert.
- Liveberechnung, Berechnen, Zurücksetzen, Folgeeingabe, Kopieren, ±-Bedienung,
  Fehleranzeige, Tastatur- und Touchbedienung funktionieren ohne Einheitensystem.
- Keine Einheit wird gespeichert. Die fachliche Einheit wird außerhalb des Rechners
  durch den Messbereich des Geräts oder Prüfmittels bestimmt.

2. Vollständiger grafischer Positionsabgleich
- Ein äußerer Standard-App-Rahmen für Startseite und alle Unterseiten.
- Einheitliche obere Rahmenkante, Headerhöhe, Innenabstände und Mittellinie.
- Logo, Release-Modul, Suche, Favoriten, Zurück und Home bleiben in allen
  Interaktionszuständen positionsstabil.
- Konsistenter Inhaltsbeginn direkt unter der Header-Trennlinie.
- Einheitlicher Footer innerhalb des Rahmens mit Safe-Area-Behandlung.
- Kurze Seiten enden ruhig am unteren Rahmen; lange Inhalte scrollen oberhalb des
  Footers, ohne Überdeckung.
- Favoriten, Suche, Sortiermodus, Datenbanken, Rechner und Wissensseiten bleiben
  vollständig im App-Rahmen.

UNVERÄNDERT ÜBERNOMMEN
- alle 10 Startseiten-Apps und sämtliche Ziele
- freigegebene App-, Navigations-, Hersteller-, Wissens-, Header-, PWA-, Maskable-,
  Favicon- und Marken-PNG-Inhalte
- Rasterlogik, Favoriten, freie Drag-and-Drop-Sortierung, Suche und Navigation
- zentrales Einheitensystem anderer Rechner und Datenbanken
- Werkstoffdatenbank, Wissensinhalte und Siemens-Fachlogik
- PWA-Installation, lokale Speicherung und Offlinebetrieb

ZENTRALE DATEIEN
- assets/app-v2-6-5-2.css                 zentrales Design und Layout
- assets/app-v2-6-5-2.js                  Laufzeit, Favoriten, Suche und Sortierung
- assets/analogsignal-rechner.js           einheitenlose Analogsignalberechnung
- assets/search-index-v2-6-5-2.json        zentraler Suchindex
- manifest-v2-6-5-2.webmanifest           PWA-Manifest
- service-worker.js                        Offlinebetrieb, Cache v2-6-5-2-core-r1
- ANALOGSIGNAL-TUEV-HINWEIS.md             Fach- und Bedienhinweis
- TESTPLAN.md / TEST-RESULTS.txt            Testdefinition und Abnahme
- SHA256SUMS.txt                            Prüfsummen aller Projektdateien außer sich selbst

LOKAL STARTEN
  cd SK-PCT-Tools-V2.6.5.2-Beta
  python3 -m http.server 8080
  Browser: http://127.0.0.1:8080/

PRÜFUNG
  node --check assets/app-v2-6-5-2.js
  node --check assets/analogsignal-rechner.js
  python3 -m py_compile tests/*.py tools/*.py
  python3 tests/validate_project.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2652.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2652.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
  SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

DEPLOYMENT
Den vollständigen Inhalt dieses Ordners gemeinsam veröffentlichen. Keine Dateien aus
V2.6.5.1 beimischen. Nach dem Upload Browser/PWA einmal online öffnen, damit der neue
Service Worker v2-6-5-2-core-r1 aktiviert und der vollständige Offline-Cache aufgebaut
wird. Danach Offlineaufruf prüfen.
