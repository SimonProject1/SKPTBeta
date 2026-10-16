SK PCT Tools 2.6.1.9-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für Rechner, Einheiten-, Werkstoff- und
Wissensdaten sowie technische Praxishinweise der Prozessleittechnik.
V2.6.1.9-Beta basiert vollständig auf V2.6.1.8-Beta.

ÄNDERUNG DIESER VERSION
- Jeder Favoritenbutton der zehn Startseiten-App-Kacheln ist strukturell direkter
  Bestandteil des zugehörigen festen Icon-Wrappers `.sk-app-icon-wrapper`.
- Derselbe Aufbau gilt für die fünf favoritenfähigen Wissens-App-Icons.
- PNG und Favoritenbutton verwenden damit denselben lokalen Positionierungsbezug;
  Kachel, Grid, Beschriftungsbereich und Viewportabstände sind keine Positionsbasis.
- Der Wrapper entspricht den tatsächlichen sichtbaren Alpha-Grenzen des unveränderten
  512-px-Icons: links 13 px, oben 9 px, rechts 489 px, unten 491 px.
- Der sichtbare Favoritenkreis ist 22 × 22 px groß. Sein Mittelpunkt sitzt fest auf
  der oberen rechten sichtbaren Icon-/Wrapperkante.
- Die unabhängige Touchfläche bleibt 44 × 44 px groß.
- Aktive und inaktive Favoriten verwenden exakt dieselbe Geometrie.
- App-Kachel, Icon-Wrapper und PNG bleiben bei Hover, Fokus, Antippen, Drücken und
  Aktivzustand positionsfest.
- Icon-Design, Rechnerlogik, Wissensinhalte und Datenbestände wurden nicht verändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-1-9.css
- Zentrale Laufzeit: assets/app-v2-6-1-9.js
- Control-Sprite: assets/pct-controls.svg
- Manifest: manifest-v2-6-1-9.webmanifest
- Suchindex: assets/search-index-v2-6-1-9.json
- Service-Worker-Cache: sk-pct-tools-v2-6-1-9-core-r1
- Reproduzierbarer Icon-Generator: tools/generate_png_icons.py

ICON-SYSTEM
- 22 eigenständige 512 × 512-RGBA-PNGs.
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons.
- Alle PNG-Bilddaten sind gegenüber V2.6.1.8-Beta bitidentisch; nur Präfixe und
  Referenzen wurden auf v2-6-1-9 aktualisiert.
- Große weiße Hauptsymbole mit schwarzer Kontur, gemeinsamer
  Grün-/Türkis-/Blau-Kachelmaster und Cyan-/Grün-Akzentrails bleiben erhalten.

BEDIENUNG UND SICHERHEIT
- App-Rahmen mit festem Header/Footer und internem Scrollbereich.
- iOS-Safe-Areas, 320-px-Reflow und Schutz vor horizontalem Überlauf.
- Externe Verweise mit no-referrer und sicheren rel-Attributen.
- Offline-Upgrade entfernt ältere sk-pct-tools-Caches.

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Projektdateien außer
SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
