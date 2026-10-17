# Testplan – SK PCT Tools V2.6.3.4-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.3-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 82 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.4-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Service-Worker-Kerncache `v2-6-3-4-core-r1`
- vollständige `SHA256SUMS.txt`
- feste Referenzhashes für alle geschützten Grafiken

## 2. Reorder-Zustandsmaschine

Zu prüfen auf iPhone-PWA-Emulation, Tablet-Touch und Desktop-Pointer:
- Ausgangszustand ist eindeutig `navigate`
- kurzer Tap öffnet im Navigationsmodus
- Bewegung vor Long-Press bleibt Scrollgeste
- Long-Press schaltet auf `sort`, erzeugt genau einen Ghost und aktiviert sichtbares Wackeln
- im Sortiermodus gilt `touch-action:none` und Navigation ist gesperrt
- Ziehen über mehrere Rasterpositionen ordnet zuverlässig um
- Drop speichert, entfernt Ghost/Capture/Drag-Klasse und kehrt zu `navigate` zurück
- synthetischer Abschlussklick wird blockiert, erster echter Folgetap ist sofort frei
- zweiter und weiterer Sortiervorgang funktioniert ohne Reload
- `pointercancel` rollt auf die Reihenfolge vor dem Drag zurück
- `pagehide` beziehungsweise Hintergrundunterbrechung bereinigt vollständig
- `lostpointercapture`, `blur` und `visibilitychange` besitzen geprüfte Cleanup-Pfade
- Tastatur-Sortiermodus blockiert Navigation bis „Fertig“
- Escape, „Fertig“ und Zurücksetzen stellen den Navigationsmodus her
- DOM-Reihenfolge und `skPctHomeOrderV1` stimmen überein
- Reload stellt die gespeicherte Reihenfolge wieder her

## 3. Favoriten und Modustrennung

- Favoritenbutton bleibt direkt im `sk-app-icon-wrapper`
- Favoriten sind im Sortiermodus gegen Fehlbedienung geschützt
- Favorit lässt sich nach Drop, Abbruch, „Fertig“ und Reload sofort bedienen
- echter App-Wechsel funktioniert nach mehreren Sortierungen ohne PWA-Neustart

## 4. Grafik- und Designregression

- sieben Marken-/Browser-/Apple-/PWA-Dateien gegen feste Hashes
- 24 Navigations-PNGs gegen feste Hashes, Geometrie und Alpha-Grenzen
- unveränderte Header-, Logo-, Icon-, Favoriten- und Rahmengeometrie
- Sortierleiste und Wackeln nur im aktiven Sortiermodus
- keine defekten Bilder oder horizontalen Überläufe

## 5. Browser-, Touch- und Funktionsregression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- drei zusätzliche Reorder-Profile mit realistischen Pointerfolgen
- 320-px-Reflow und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home- und Zurücknavigation
- sechs Rechnerreferenzen einschließlich Grenzwerte, Reset und Vorzeichen-Touchziele
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-4-core-r1`

## 6. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`, das
Übergabeprotokoll und das vollständige ZIP-Paket aktualisiert und erneut geprüft.
