SK PCT Tools 2.6.4.0-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.9-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.4.0-Beta ist eine vollständige neue Version und kein Patchpaket.

SCHWERPUNKT V2.6.4.0-BETA
- Gemeinsamer zentraler Clean-Designblock für sämtliche Hersteller- und
  Wissenskacheln der Wissensdatenbank.
- Air Torque, Endress+Hauser, Siemens, Vacon und Sonstiges verwenden identische
  Iconmaße, Positionen, Abstände und Beschriftungsachsen.
- Historische CSS-Außenkacheln, Mehrfachkonturen, zusätzliche Hintergründe,
  Drop-Shadows und Iconfilter wurden entfernt.
- Hover, Fokus, Touch, Drücken, Auswahl und Aktivzustand verändern weder Kachel,
  Wrapper, PNG noch Textposition; Rückmeldungen erfolgen nur layoutneutral.
- Vollständig neu gestalteter Favoritendialog mit sauberer Cyan-Blau-Grün-
  Oberfläche, Favoritenanzahl, Einzellöschen, „Alle leeren“, leerem Zustand,
  Fokusführung, Escape, Tastatur-Fokusfalle und Safe-Area-Unterstützung.

AUSDRÜCKLICH UNVERÄNDERT
- Inhalte sämtlicher 24 Navigations-/App-/Wissens-/Hersteller-PNGs
- header-logo-simple.png sowie alle PWA-, Homescreen-, Maskable- und Markenlogos
- Release-Modul-Grafikinhalt
- Drag-and-Drop-Sortierung pointer-overlay-v3 und skPctHomeOrderV1
- normaler Header im Sortiermodus und separates Sortier-Dock
- Versionsmodul, Suche, Favoritenzähler und Startseiten-App-Icons
- App-Favoritenkopplung, Rechner, Datenbanken, Wissensinhalte und Offlinebetrieb

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-4-0.css
- Zentrale Laufzeit: assets/app-v2-6-4-0.js
- Sichtbares Header-Logo: assets/header-logo-simple.png
- Release-Modul-Haut: assets/release-module-v2-6-4-0.png
- Manifest: manifest-v2-6-4-0.webmanifest
- Suchindex: assets/search-index-v2-6-4-0.json
- Service-Worker-Cache: sk-pct-tools-v2-6-4-0-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 -m http.server 8080
3. SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
4. SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py

Die finalen Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
