SK PCT Tools 2.6.1.8-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für Rechner, Einheiten-, Werkstoff- und
Wissensdaten sowie technische Praxishinweise der Prozessleittechnik.
V2.6.1.8-Beta basiert vollständig auf V2.6.1.7-Beta. Das freigegebene
technisch-industrielle PNG-Icon-Design wurde ohne grafische Änderung übernommen.

ÄNDERUNG DIESER VERSION
- Bei allen zehn Startseiten-App-Icons liegt der Mittelpunkt des sichtbaren
  Favoritenkreises exakt auf der oberen rechten Ecke der sichtbaren Iconfläche.
- Der sichtbare Kreis überlappt die Iconkante damit horizontal und vertikal je zur
  Hälfte: bei 22 px Kreisdurchmesser 11 px innen und 11 px außen.
- Ausschließlich das sichtbare ::after-Pseudoelement bestimmt den optischen Anker.
  Die unsichtbare Favoriten-Touchfläche bleibt unabhängig davon 44 × 44 px groß.
- Dieselbe sichtbare Eckverankerung gilt für die favoritenfähigen Wissens-App-Icons.
- Aktive und inaktive Favoriten verwenden dieselbe Geometrie.
- App-Kachel und PNG-Icon bleiben bei Mouse-Hover, Fokus, Antippen, Drücken und
  aktivem Zustand geometrisch unverändert.
- Icon-Design, Rechnerlogik, Wissensinhalte und Datenbestände wurden nicht verändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-1-8.css
- Zentrale Laufzeit: assets/app-v2-6-1-8.js
- Control-Sprite: assets/pct-controls.svg
- Manifest: manifest-v2-6-1-8.webmanifest
- Suchindex: assets/search-index-v2-6-1-8.json
- Service-Worker-Cache: sk-pct-tools-v2-6-1-8-core-r1
- Reproduzierbarer Icon-Generator: tools/generate_png_icons.py

ICON-SYSTEM
- 22 eigenständige 512 × 512-RGBA-PNGs.
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons.
- Alle PNG-Bilddaten sind gegenüber V2.6.1.7-Beta bitidentisch; nur Präfixe
  und Referenzen wurden auf V2.6.1.8 aktualisiert.
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
