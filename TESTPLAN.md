# Testplan – SK PCT Tools V2.6.3.6-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.5-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 82 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.6-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Service-Worker-Kerncache `v2-6-3-6-core-r1`
- vollständige `SHA256SUMS.txt`
- feste Referenzhashes für alle geschützten Grafiken
- separates Sortier-Dock, Overlay-, Platzhalter-, History- und Cleanup-Struktur
- keine modusspezifische CSS-Regel, die den normalen Header verändert

## 2. Headeridentität und Dock-Sicherheit

Zu prüfen auf 320 × 700, 390 × 844, 844 × 390, 820 × 1180 und 1440 × 1000:
- Header-DOM bleibt vor, während und nach dem Sortiermodus identisch
- Geometrie und berechnete Styles von Header, Marke, Logo, Versionsfeld, Versionsnummer,
  Zusatztext, Utility-Bereich, Suche, Favoritenbutton und Zähler bleiben identisch
- Header-Screenshot ist im Normal- und Sortierzustand bytegenau gleich
- alle normalen Headerbestandteile bleiben sichtbar
- das Sortier-Dock ist fixed, außerhalb des Headers und außerhalb des Dokumentflusses
- Dock überdeckt weder Header noch erste App-Reihe oder App-Beschriftungen
- Undo, Redo, Standard und Fertig besitzen mindestens 44 × 44 px Touchflächen
- Dock berücksichtigt Safe-Area und bleibt vollständig im Viewport
- nach Drop, Abbruch und Fertig ist das Dock ausgeblendet und Navigation sofort aktiv

## 3. Wackelanimation und Rasterstabilität

- Kachel, Wrapper, Titel und Favoritenbutton haben `animation-name: none`
- ausschließlich das direkte Icon-PNG verwendet `pct-home-icon-wiggle`
- Außenmaße und Positionen von Kachel, Wrapper, Titel und Favorit bleiben bis 0,5 px stabil
- Platzhalter übernimmt Breite und Höhe der aufgenommenen Kachel ohne Mindesthöhen-Sprung
- keine Skalierung, Verschiebung oder Layoutänderung durch die Animation
- `prefers-reduced-motion` deaktiviert Wackeln und Drag-Rotation

## 4. Drag-Overlay und Rasterplatzhalter

- Long-Press erzeugt genau eine body-direkte Drag-Ebene und genau einen Platzhalter
- während des Drags sind neun reale Apps plus ein maßgleicher Platzhalter im Raster
- Overlay bewegt sich frei über mehrere Reihen und Spalten
- Overlay bleibt innerhalb der Viewportränder, unterhalb des Headers und außerhalb des Docks
- Zielposition wird am überfahrenen Rasterplatz erkannt und klar markiert
- Drop übernimmt die Platzhalterposition und entfernt Overlay/Platzhalter vollständig
- pointercancel, lostpointercapture, Escape und Hintergrundwechsel rollen zurück
- Rand-Autoscroll aktualisiert die Zielerkennung nur bei tatsächlicher Scrollbewegung
- Resize aktualisiert die sichere Overlay-Position

## 5. Interaktion, History und Speicherung

- kurzer Tap öffnet im Normalmodus
- Bewegung vor Long-Press bleibt Scrollgeste
- Sortiermodus blockiert App-Navigation kontrolliert
- Drag-Abschlussklick wird einmal kartenbezogen unterdrückt
- erster echter Folgetap ist sofort frei
- zweiter und weiterer Sortiervorgang funktioniert ohne Reload
- Tastaturpfeile verschieben Apps
- Rückgängig stellt die vorige Reihenfolge her; Wiederholen stellt die Änderung wieder her
- Fertig und Standardreihenfolge aktivieren den Normalmodus
- DOM-Reihenfolge und `skPctHomeOrderV1` stimmen überein
- Reload stellt die gespeicherte Reihenfolge wieder her

## 6. Browser-, Touch- und Funktionsregression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone, Tablet und Desktop
- 1.422 Browserprüfungen
- fünf zusätzliche Reorder-Profile: 320 × 700, 390 × 844, 844 × 390,
  820 × 1180 und 1440 × 1000
- 320-px-Reflow und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home- und Zurücknavigation
- sechs Rechnerreferenzen einschließlich Grenzwerte, Reset und Vorzeichen-Touchziele
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-6-core-r1`

## 7. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`, das
Übergabeprotokoll und das vollständige ZIP-Paket aktualisiert und erneut verifiziert.
