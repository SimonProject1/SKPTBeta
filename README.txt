SK PCT Tools 2.6.3.5-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.4-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.5-Beta ist eine vollständige neue Version und kein Patchpaket.

SORTIERMODUS V2.6.3.5
- Der normale Home-Header bleibt außerhalb des Sortiermodus unverändert.
- Im Sortiermodus werden Logo, Versionsfeld, Suche und Favoriten vorübergehend durch eine
  kompakte, vollständig innerhalb der reservierten Headerhöhe liegende Sortierleiste ersetzt.
- Die Sortierleiste enthält Rückgängig, Wiederholen, Standardreihenfolge und Fertig.
- Weder Sortierleiste noch Drag-Icon überdecken die erste App-Reihe.
- Nur das sichtbare PNG des Iconkörpers wackelt dezent. Kachel, Wrapper, Titel, Favoritenbutton,
  Rastermaße und Header bleiben geometrisch unverändert.
- Ein Long-Press nimmt die App auf. Die Originalkachel wird durch einen gleich großen,
  klar markierten Rasterplatzhalter ersetzt.
- Das gezogene Icon liegt in einer eigenen, viewportfesten Ebene direkt unter body. Diese Ebene
  ist unabhängig von Grid, overflow, transform, containment, Parentgrenzen und Stacking-Kontexten.
- Das Drag-Icon bleibt unterhalb des Sortier-Headers und innerhalb der sichtbaren Viewportränder.
- Zielpositionen werden mit elementsFromPoint und einer abstandsbezogenen Rückfallebene erkannt.
- Nach Drop oder Abbruch werden Overlay, Platzhalter, Pointer-Capture und Sortierzustand vollständig
  entfernt. Danach sind normales Design, Favoriten und App-Navigation sofort wieder aktiv.
- pointercancel, lostpointercapture, Escape, blur, pagehide, visibilitychange und Hintergrundwechsel
  besitzen definierte Cleanup- beziehungsweise Rollback-Pfade.
- Mehrfachsortierung, Rand-Autoscroll, Tastaturverschiebung, Rückgängig/Wiederholen,
  Standardreihenfolge, Speicherung und Wiederherstellung nach Reload sind abgesichert.
- Speicherung bleibt kompatibel unter skPctHomeOrderV1.

BEDIENUNG
1. App kurz antippen: App öffnen.
2. App gedrückt halten: Sortiermodus und freie Drag-Ebene starten.
3. Icon über Reihen und Spalten ziehen und loslassen: Reihenfolge speichern, Normalmodus aktivieren.
4. Ohne Änderung abbrechen: Escape, Pointer-Abbruch oder Fertig.
5. Rückgängig/Wiederholen: im getrennt gestarteten Sortiermodus über Toolbar oder Strg/Cmd+Z.
6. Standardreihenfolge: in der Sortierleiste ↺ wählen.

UNVERÄNDERTES NORMALDESIGN
- Grafik, Farben, Logo, Header, Versionsfeld, App-Icons, Favoritenpositionen und Layout außerhalb
  des Sortiermodus entsprechen der vollständigen V2.6.3.4-Beta.
- Alle 24 Navigations-PNGs sowie Logo-, PWA-, Apple- und Browserbilder sind bytegenau unverändert;
  ausschließlich ihre versionierten Dateinamen tragen v2-6-3-5-.
- Suche, Filter, Sortierauswahl, Rechner, Wissensdatenbank, Datenbanken und Offlinebetrieb bleiben erhalten.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-5.css
- Zentrale Laufzeit: assets/app-v2-6-3-5.js
- Manifest: manifest-v2-6-3-5.webmanifest
- Suchindex: assets/search-index-v2-6-3-5.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-5-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
