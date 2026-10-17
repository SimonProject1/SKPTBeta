# Testplan – SK PCT Tools V2.6.3.5-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.4-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 82 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.5-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Service-Worker-Kerncache `v2-6-3-5-core-r1`
- vollständige `SHA256SUMS.txt`
- feste Referenzhashes für alle geschützten Grafiken
- neue Toolbar-, Overlay-, Platzhalter-, History- und Cleanup-Struktur

## 2. Sortier-Header und visuelle Stabilität

Zu prüfen auf 320 px, iPhone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000:
- normale Headerbestandteile bleiben außerhalb des Sortiermodus unverändert
- im Sortiermodus sind Logo, Version, Suche und Favorit kontrolliert ausgeblendet
- kompakte Toolbar enthält Rückgängig, Wiederholen, Standard und Fertig
- Toolbar liegt vollständig innerhalb des Headerrechtecks
- Headerunterkante liegt vor der ersten Rasterreihe; keine Überdeckung
- Drag-Ebene besitzt niedrigeren Z-Index als der Sortier-Header
- nach Drop ist der normale Header sofort wieder aktiv

## 3. Wackelanimation

- Kachel, Wrapper, Titel und Favoritenbutton haben `animation-name: none`
- ausschließlich das direkte Icon-PNG verwendet `pct-home-icon-wiggle`
- Außenmaße und Positionen von Kachel, Wrapper, Titel und Favorit bleiben bis 0,5 px stabil
- keine Skalierung, Verschiebung oder Layoutänderung durch die Animation
- `prefers-reduced-motion` deaktiviert Wackeln und Drag-Rotation

## 4. Drag-Overlay und Rasterplatzhalter

- Long-Press erzeugt genau eine body-direkte Drag-Ebene und genau einen Platzhalter
- während des Drags sind neun reale Apps plus ein maßgleicher Platzhalter im Raster
- Overlay bewegt sich frei über mehrere Reihen und Spalten
- Overlay bleibt innerhalb der Viewportränder und unterhalb des Headers
- Zielposition wird am überfahrenen Rasterplatz erkannt
- Drop übernimmt die Platzhalterposition und entfernt Overlay/Platzhalter vollständig
- pointercancel, lostpointercapture, Escape und Hintergrundwechsel rollen zurück
- Rand-Autoscroll und Resize aktualisieren Overlay und Zielerkennung

## 5. Interaktion, History und Speicherung

- kurzer Tap öffnet im Normalmodus
- Bewegung vor Long-Press bleibt Scrollgeste
- Sortiermodus blockiert Navigation kontrolliert
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
- 1.353 Browserprüfungen
- zusätzliche Reorder-Profile für iPhone-PWA, Tablet-Touch und Desktop-Pointer
- 320-px-Reflow und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home- und Zurücknavigation
- sechs Rechnerreferenzen einschließlich Grenzwerte, Reset und Vorzeichen-Touchziele
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-5-core-r1`

## 7. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`, das
Übergabeprotokoll und das vollständige ZIP-Paket aktualisiert und erneut verifiziert.
