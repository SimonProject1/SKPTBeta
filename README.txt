SK PCT Tools 2.6.3.2-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.1-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.2-Beta ist eine vollständige neue Version und kein Patchpaket.

ÄNDERUNGEN DIESER VERSION
- Separate sichtbare Headerlogo-Datei assets/logo-sk-pct-tools-header.png.
- Das PCT-Zahnrad dieser Header-Variante ist exakt bei 256/256 zentriert und kleiner
  als in V2.6.3.1, damit zu Außenkante und Leiterbahndetails gleichmäßiger Abstand bleibt.
- Die freigegebene App-/Homescreen-Iconfamilie ist bytegenau unverändert geblieben.
- Versionsfeld vollständig neu: kompakte 52/44-px-Fläche ohne alte breite Paneloptik,
  schwarze Doppelkontur, inneren Rahmen oder dekorative Farblinie am unteren Rand.
- Home, Zurück, Suche und Favoriten nutzen neue, bereinigte 512-px-PNGs auf einem
  einzelnen Cyan-/Blau-/Grün-Grundkörper ohne Innenkachel oder Leiterbahndekoration.
- Suche besitzt keine schwarze Innenfläche; Such- und Sternsymbol sind groß, weiß und
  klar schwarz konturiert. Der Favoritenzähler bleibt erhalten.
- Logo, Versionsfeld und Headeraktionen liegen auf einer gemeinsamen vertikalen
  Mittellinie und besitzen 52 px auf Desktop/Tablet beziehungsweise 44 px mobil.
- Touchflächen, Fokus-, Hover-, Press- und Aktivzustände bleiben geometrisch stabil.

GESCHÜTZTER FUNKTIONSSTAND
- Favicon, Apple-Touch-, Standard-, Maskable- und App-Icon-Dateien sind per SHA-256
  gegen V2.6.3.1 geschützt und unverändert.
- 20 App-, Wissens- und Herstellergrafiken sind inhaltlich/binär unverändert; nur das
  Versionspräfix lautet v2-6-3-2-.
- Die Favoritenbuttons der zehn Startseiten- und fünf Wissens-App-Icons bleiben direkte
  Kinder des jeweiligen .sk-app-icon-wrapper.
- 44-px-Touchfläche, 22-px-Kreis und obere rechte Icon-Ankerposition bleiben erhalten.
- Navigation, Suche, Favoritenzähler, Tastaturbedienung und Offlinebetrieb bleiben aktiv.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-2.css
- Zentrale Laufzeit: assets/app-v2-6-3-2.js
- Manifest: manifest-v2-6-3-2.webmanifest
- Suchindex: assets/search-index-v2-6-3-2.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-2-core-r1
- Control-Sprite: assets/pct-controls.svg
- Icon-Generator: tools/generate_png_icons.py
- Markenlogo-Generator: tools/generate_brand_assets.py

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
