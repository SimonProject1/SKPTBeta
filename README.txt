SK PCT Tools 2.6.3.1-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.0-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.1-Beta ist eine vollständige neue Version und kein Patchpaket.

ÄNDERUNGEN DIESER VERSION
- Zusätzliche schwarze Außenkacheln bei Home, Zurück, Suche und Favoriten entfernt.
- Suche und Favoriten besitzen neue eigenständige 512-px-PNG-Grafiken im
  freigegebenen technisch-industriellen Stil.
- Versionsschild mit V2.6.3.1-Beta und „Tool by S.K.“ an dieselbe Designfamilie
  angeglichen; nur ein sichtbares Gehäuse, keine zusätzliche Außenkachel.
- Logo-/PWA-Familie neu erzeugt: Herkunftstext vollständig aus der Grafik entfernt,
  Zahnrad deutlich vergrößert und exakt bei 256/256 zentriert.
- Logo, Versionsschild und Headeraktionen auf eine gemeinsame vertikale Mittellinie
  und einheitliche optische Höhe gesetzt.
- Headergrafiken: 52 × 52 px auf Desktop/Tablet, 44 × 44 px auf Smartphones.
- Hover, Fokus, Press, Aktiv und aria-Zustände verändern weder Position noch Außenmaß.

GESCHÜTZTER FUNKTIONSSTAND
- Die 10 App-, 5 Wissens-, 5 Hersteller- sowie Home-/Zurück-Grafiken sind binär
  unverändert zur V2.6.3.0-Beta; lediglich Präfix/Referenzen lauten v2-6-3-1-.
- Die Favoritenbuttons der zehn Startseiten- und fünf Wissens-App-Icons bleiben
  direkte Kinder des jeweiligen .sk-app-icon-wrapper.
- 44-px-Touchfläche, 22-px-Kreis und obere rechte Icon-Ankerposition bleiben erhalten.
- Navigation, Favoritenzähler, Suche, Tastaturbedienung und Offlinebetrieb bleiben aktiv.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-1.css
- Zentrale Laufzeit: assets/app-v2-6-3-1.js
- Manifest: manifest-v2-6-3-1.webmanifest
- Suchindex: assets/search-index-v2-6-3-1.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-1-core-r1
- Control-Sprite: assets/pct-controls.svg
- Icon-Generator: tools/generate_png_icons.py
- Markenlogo-Generator: tools/generate_brand_assets.py

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
