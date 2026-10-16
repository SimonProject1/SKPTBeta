SK PCT Tools 2.6.1.6-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für Rechner, Einheiten-, Werkstoff- und
Wissensdaten sowie technische Praxishinweise der Prozessleittechnik.
V2.6.1.6-Beta basiert vollständig auf V2.6.1.5-Beta. Der dort ausdrücklich
freigegebene technisch-industrielle PNG-Icon-Standard wurde unverändert übernommen.

ÄNDERUNG DIESER VERSION
- Die zehn App-Icons der Startseite bleiben bei Mouse-Hover, Antippen, Drücken,
  Fokus und aktivem Zustand fest an derselben Position.
- Die frühere Aufwärtsverschiebung der App-Kachel wurde entfernt.
- Auch die Favoritenschalter besitzen auf der Startseite keine zustandsbedingte
  geometrische Verschiebung mehr.
- Der sichtbare Favoritenkreis liegt mit seinem Mittelpunkt exakt auf der oberen
  rechten Außenkante des jeweiligen App-Icons.
- Die 44 × 44-px-Touchfläche der Favoriten bleibt erhalten.
- Die Bilddaten aller 22 freigegebenen PNG-Icons sind gegenüber V2.6.1.5-Beta
  bitidentisch; nur Dateipräfixe und Einbindungen wurden versioniert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-1-6.css
- Zentrale Laufzeit: assets/app-v2-6-1-6.js
- Control-Sprite: assets/pct-controls.svg
- Manifest: manifest-v2-6-1-6.webmanifest
- Suchindex: assets/search-index-v2-6-1-6.json
- Service-Worker-Cache: sk-pct-tools-v2-6-1-6-core-r1
- Reproduzierbarer Icon-Generator: tools/generate_png_icons.py

ICON-SYSTEM
- 22 eigenständige 512 × 512-RGBA-PNGs.
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons.
- Große weiße Hauptsymbole mit schwarzer Kontur.
- Gemeinsamer Grün-/Türkis-/Blau-Kachelmaster.
- Cyan-/Grün-Akzentrails, Knoten und industrielle Tiefenwirkung.

BEDIENUNG UND SICHERHEIT
- App-Rahmen mit festem Header/Footer und internem Scrollbereich.
- iOS-Safe-Areas, 320-px-Reflow und Schutz vor horizontalem Überlauf.
- Externe Verweise mit no-referrer und sicheren rel-Attributen.
- Offline-Upgrade entfernt ältere sk-pct-tools-Caches.

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Dateien außer
SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
