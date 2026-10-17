SK PCT Tools 2.6.3.3-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.2-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.3-Beta ist eine vollständige neue Version und kein Patchpaket.

BEHOBENER FEHLER
- Nach dem Neuordnen eines App-Icons bleibt keine globale Klicksperre mehr aktiv.
- Ein unmittelbar vom Drag erzeugter Ghost-Klick wird weiterhin einmalig blockiert.
- Ein neuer echter Tap hebt diese Drag-Sperre sofort auf und öffnet das App-Icon.
- Im Bearbeitungsmodus startet eine Bewegung den nächsten Drag; ein ruhiger kurzer Tap
  öffnet dagegen die gewählte App. Mehrfaches Sortieren bleibt dadurch möglich.
- Pointer-, Touch- und Drag-Zustände werden bei pointerup, pointercancel,
  lostpointercapture, Fensterwechsel, pagehide und Sichtbarkeitswechsel bereinigt.
- Reihenfolge und Speicherung bleiben unter skPctHomeOrderV1 kompatibel.

UNVERÄNDERTER FUNKTIONS- UND DESIGNSTAND
- Grafik, Layout, Farben, Abstände, Icon-Geometrie und Touchflächen entsprechen der
  V2.6.3.2-Beta.
- Alle 24 Navigations-PNGs sowie alle Logo-/PWA-/Apple-/Browserbilder sind binär
  unverändert; nur die versionierten Dateinamen lauten v2-6-3-3-.
- Favoritenbuttons, Suche, Filter, Sortierauswahl, Scrollen, feste Icon-Positionen,
  Tastaturbedienung, Rechner und Offlinebetrieb bleiben erhalten.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-3.css
- Zentrale Laufzeit: assets/app-v2-6-3-3.js
- Manifest: manifest-v2-6-3-3.webmanifest
- Suchindex: assets/search-index-v2-6-3-3.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-3-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
