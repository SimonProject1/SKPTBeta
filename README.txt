SK PCT Tools 2.6.3.4-Beta
Stand: 17.10.2026
Projektinhaber: Simon Kiesler
Basis: vollständige V2.6.3.3-Beta

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.3.4-Beta ist eine vollständige neue Version und kein Patchpaket.

NEUE ICON-SORTIERUNG
- Die bisherige Drag-/Drop- und Klicksperrlogik wurde vollständig ersetzt.
- Navigationsmodus und Sortiermodus sind als getrennte Zustände umgesetzt.
- Im Navigationsmodus öffnet ein kurzer Tap die App; eine beginnende Scrollgeste bleibt Scrollen.
- Ein Long-Press nimmt das Icon auf, schaltet den Sortiermodus ein und zeigt das sichtbare Wackeln.
- Im Sortiermodus ist die App-Navigation vollständig gesperrt; Favoriten bleiben fest am Icon,
  werden während des Ziehens aber ausgeblendet und gegen Fehlbedienung geschützt.
- Beim Ziehen werden Pointer-Capture, Ghost, Zielbestimmung und Rand-Autoscroll zentral verwaltet.
- Nach Drop oder Abbruch endet der Sortiermodus automatisch. Der vom Drag stammende Abschlussklick
  wird einmal kartenbezogen unterdrückt; der nächste echte Pointerdown hebt diese Sperre sofort auf.
  Es gibt kein zeitabhängiges Sperrfenster.
- „Fertig“, Escape, pointercancel, lostpointercapture, blur, pagehide und Hintergrundwechsel
  räumen alle aktiven Zustände auf.
- Mehrfaches Sortieren, Tastatur-Umordnung, Zurücksetzen und Wiederherstellung nach Neustart sind
  unter dem kompatiblen Schlüssel skPctHomeOrderV1 abgesichert.

BEDIENUNG
1. App-Icon kurz antippen: App öffnen.
2. App-Icon gedrückt halten: Sortiermodus startet, Icons wackeln, gewähltes Icon wird aufgenommen.
3. Icon an die gewünschte Position ziehen und loslassen: Reihenfolge wird gespeichert und der
   Navigationsmodus ist sofort wieder aktiv.
4. Ohne Verschieben beenden: „Fertig“ oder Escape.
5. Standardreihenfolge: im Sortiermodus „Zurücksetzen“ wählen.

UNVERÄNDERTER FUNKTIONS- UND DESIGNSTAND
- Grafik, Headerdesign, Layout, Farben, Abstände, Icon-Geometrie und allgemeine Touchflächen
  entsprechen der vollständigen V2.6.3.3-Beta.
- Alle 24 Navigations-PNGs sowie Logo-, PWA-, Apple- und Browserbilder sind binär unverändert;
  nur die versionierten Dateinamen lauten v2-6-3-4-.
- Favoriten, Suche, Filter, Sortierauswahl, Rechner, Wissensdatenbank, Datenbanken und
  Offlinebetrieb bleiben erhalten.
- Am CSS wurden nur Versionsangaben sowie die funktionalen Selektoren des Sortiermodus korrigiert;
  das freigegebene Grafik- und Headerdesign wurde nicht verändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-3-4.css
- Zentrale Laufzeit: assets/app-v2-6-3-4.js
- Manifest: manifest-v2-6-3-4.webmanifest
- Suchindex: assets/search-index-v2-6-3-4.json
- Service-Worker-Cache: sk-pct-tools-v2-6-3-4-core-r1
- Control-Sprite: assets/pct-controls.svg

PRÜFUNG
1. python3 tests/validate_project.py
2. python3 tests/browser_regression.py

Die ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. SHA256SUMS.txt erfasst alle
Projektdateien außer der Prüfsummendatei selbst.
