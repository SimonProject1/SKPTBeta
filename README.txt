SK PCT Tools 2.6.1.5-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für Rechner, Einheiten-, Werkstoff- und
Wissensdaten sowie technische Praxishinweise der Prozessleittechnik.
V2.6.1.5-Beta basiert vollständig auf V2.6.1.4-Beta und ersetzt das komplette
Navigationsicon-System durch den freigegebenen technisch-industriellen Standard.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-1-5.css
- Zentrale Laufzeit: assets/app-v2-6-1-5.js
- Control-Sprite: assets/pct-controls.svg
- Manifest: manifest-v2-6-1-5.webmanifest
- Suchindex: assets/search-index-v2-6-1-5.json
- Service-Worker-Cache: sk-pct-tools-v2-6-1-5-core-r1
- Reproduzierbarer Icon-Generator: tools/generate_png_icons.py

ICON-SYSTEM V2.6.1.5
- 22 vollständig neu erzeugte, eigenständige 512 × 512-RGBA-PNGs.
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons.
- Große weiße Hauptsymbole mit schwarzer Kontur.
- Gemeinsamer Grün-/Türkis-/Blau-Kachelmaster.
- Cyan-/Grün-Akzentrails, Knoten und industrielle Tiefenwirkung.
- Startseite und Wissensdatenbank verwenden keine identischen Platzhalter mehr.

BEDIENUNG UND SICHERHEIT
- Favoritensteuerung separat vom PNG, Touchziel mindestens 44 × 44 px.
- App-Rahmen mit festem Header/Footer und internem Scrollbereich.
- iOS-Safe-Areas, 320-px-Reflow und Schutz vor horizontalem Überlauf.
- Externe Verweise mit no-referrer und sicheren rel-Attributen.
- Offline-Upgrade entfernt ältere sk-pct-tools-Caches.

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Dateien außer
SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
