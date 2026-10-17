# Testplan – SK PCT Tools V2.6.3.3-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.2-Beta

## 1. Statische Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 82 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.3-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Service-Worker-Kerncache `v2-6-3-3-core-r1`
- vollständige `SHA256SUMS.txt`

## 2. Drag-/Touch-/Pointer-Zustandsmaschine

Zu prüfen auf Smartphone-Touch, Tablet-Touch und Desktop-Pointer:
- kurzer Tap ohne Drag wird nicht unterdrückt
- Long-Press startet Drag und zeigt einen einzelnen Ghost
- Ziehen und Ablegen speichert die neue Reihenfolge
- der durch Drag erzeugte Klick öffnet keine App versehentlich
- ein neuer Tap direkt nach dem Ablegen öffnet die App sofort
- zweites Sortieren ohne Neustart funktioniert
- `pointercancel` bereinigt Drag, Ghost, Timer und Capture
- Tap nach abgebrochenem Drag funktioniert sofort
- DOM-Reihenfolge und `skPctHomeOrderV1` stimmen überein
- `lostpointercapture`, `blur`, `pagehide` und `visibilitychange` besitzen Cleanup-Pfade

## 3. Geschützte Grafik und Design

- sieben freigegebene Marken-/Browser-/Apple-/PWA-Dateien gegen feste Hashes
- 24 Navigations-PNGs gegen feste Hashes, Geometrie und Alpha-Grenzen
- CSS gegenüber V2.6.3.2 nur auf Versionsreferenzen umgestellt
- 44-px-Favoriten-Touchfläche und 22-px sichtbarer Kreis
- feste obere rechte Icon-Verankerung
- unveränderte Geometrie in Ruhe, Hover, Fokus, Press und Aktivzustand

## 4. Browserregression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- iPhone-PWA-nahe Touch-/Pointer-Sequenzen im mobilen Browserkontext
- 320-px-Reflow-Sanity und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home- und Zurücknavigation
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-3-core-r1`

## 5. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`, das
Übergabeprotokoll und das vollständige ZIP-Paket aktualisiert und erneut geprüft.
