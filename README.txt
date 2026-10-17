SK PCT Tools 2.6.3.7-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.6-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.7-Beta ist eine vollständige neue Version und kein Patchpaket.

NEUES RELEASE-MODUL IM HEADER
- Die bisherige Versionsfeld-/Textpanel-Implementierung wird im DOM nicht mehr verwendet.
- Das breite flache Panel mit seitlichen Cyan-/Grünstreifen wurde entfernt.
- Das neue Release-Modul verwendet assets/release-module-v2-6-3-7.png als einzigen
  sichtbaren Cyan-/Blau-/Grün-Grundkörper.
- Die PNG-Haut stammt aus demselben Generator und derselben Materiallogik wie Home,
  Zurück, Suche und Favoriten: ein schwarzer Außenkonturzug, identische Rundung,
  Lichtkante, Verlauf und räumliche Wirkung.
- Der HTML/CSS-Host ist transparent, rahmenlos und schattenfrei. Es gibt keine
  zusätzliche Kachel, keinen Panelrahmen und keine isolierten farbigen Seitenlinien.
- Die Texte „V2.6.3.7-Beta“ und „Tool by S.K.“ bleiben zugänglicher HTML-Text.
- Eine Laufzeit-Anpassung verkleinert ausschließlich die Versionsschrift bei längeren
  Versionsständen, ohne Modulgröße, Position oder Headergeometrie zu verändern.
- Sichtbare Höhe und vertikale Mittellinie entsprechen Logo, Suche und Favoriten:
  52 px auf Desktop/Tablet, 44 px auf Smartphone und kleinen Querformaten.

UNVERÄNDERTE FUNKTIONEN
- Drag-and-Drop-Sortierung, Pointer-Overlay, Platzhalter und skPctHomeOrderV1
- normaler Header im Sortiermodus und separates viewportfestes Sortier-Dock
- alle 24 Navigations-/App-/Wissens-/Hersteller-PNGs bytegenau unverändert
- Logo- und PWA-Grafiken bytegenau unverändert
- Suche, Favoriten, Favoritenzähler, Navigation und Touchflächen
- Rechner, Datenbanken, Wissensbeiträge, Barrierefreiheit und Offlinebetrieb
- Keine Größen- oder Positionsänderung bei Hover, Fokus, Antippen, Drücken,
  aktivem Zustand oder Sortiermodus.

BEDIENUNG DER APP-SORTIERUNG
1. App kurz antippen: App öffnen.
2. App gedrückt halten: Sortiermodus und freie Drag-Ebene starten.
3. Icon ziehen und loslassen: Reihenfolge speichern, Normalmodus aktivieren.
4. Rückgängig, Wiederholen, Standard und Fertig: separates Dock verwenden.
5. Escape/Pointer-Abbruch: laufenden Vorgang vollständig zurückrollen.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-7.css
- Zentrale Laufzeit: assets/app-v2-6-3-7.js
- Release-Modul-Haut: assets/release-module-v2-6-3-7.png
- PNG-Generator: tools/generate_png_icons.py
- Manifest: manifest-v2-6-3-7.webmanifest
- Suchindex: assets/search-index-v2-6-3-7.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-7-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 -m http.server 8080
3. SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
