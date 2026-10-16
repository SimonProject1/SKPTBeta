SK PCT Tools 2.6.3.0-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.2.1-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.0-Beta ist eine vollständige neue Version und kein Patchpaket.

ÄNDERUNG DIESER VERSION
- Versionsanzeige auf Startseite und sämtlichen Unterseiten als gemeinsames
  technisch-industrielles Schild neu aufgebaut.
- Exakter sichtbarer Herkunftstext im Versionsschild: „Tool by S.K.“.
- Schwarze Außenkontur, Stahlfläche, räumliche Tiefe und getrennte Cyan-, Blau- und
  Grün-Akzentkanten entsprechen der freigegebenen App-Icon-Familie.
- Suche, Favoritenübersicht, Zähler, Schließen sowie Home- und Zurück-Navigation sind
  als geschlossene Header-/Navigationsfamilie gestaltet.
- Header-Bedienelemente besitzen auf Smartphone und Tablet mindestens 44 × 44 px
  Touchfläche; Desktop verwendet 48 × 48 px.
- Hover, Fokus, Antippen, Drücken und aktive Zustände ändern Farbe, Leuchten oder
  Kontur, aber niemals Position oder Außenmaß.
- Lange Versionsbezeichnungen können innerhalb des flexiblen Schilds umbrechen;
  320-px-Reflow, Safe-Area und Querformat sind abgesichert.

GESCHÜTZTER FREIGABESTAND
- assets/logo-sk-pct-tools.png sowie alle Browser-, Apple- und PWA-Varianten sind
  binär identisch zur vollständigen V2.6.2.1-Beta.
- Alle 22 App-, Wissens-, Hersteller- und Navigations-PNGs sind bildlich unverändert;
  nur das Dateipräfix lautet versionsgerecht v2-6-3-0-.
- Die Favoritenbuttons der zehn Startseiten- und fünf Wissens-App-Icons bleiben
  direkte Kinder des jeweiligen .sk-app-icon-wrapper.
- 44-px-Touchfläche, 22-px-Kreis und die exakte obere rechte Icon-Ankerposition sind
  unverändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-0.css
- Zentrale Laufzeit: assets/app-v2-6-3-0.js
- Manifest: manifest-v2-6-3-0.webmanifest
- Suchindex: assets/search-index-v2-6-3-0.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-0-core-r1
- Control-Sprite: assets/pct-controls.svg
- App-Icon-Generator: tools/generate_png_icons.py
- Markenlogo-Generator: tools/generate_brand_assets.py

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die tatsächlich ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Projektdateien
außer SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
