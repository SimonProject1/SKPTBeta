# Testplan – SK PCT Tools V2.6.3.7-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.6-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 83 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, 14 gerahmte interne Seiten und 15 aktive Browserrouten
- genau eine zentrale CSS- und App-JS-Datei
- Version 2.6.3.7-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- vollständige lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Service-Worker-Kerncache `v2-6-3-7-core-r1`
- vollständige Prüfsummen und feste Referenzhashes

## 2. Neues Release-Modul

- keine operative Nutzung der alten Versionsfeld-/Textpanel-Klassen
- `release-module-v2-6-3-7.png`: 1536 × 512 px, RGBA, feste Alpha-Grenzen und SHA-256
- Cyan-/Blau-/Grün-Materialität und schwarze Außenkontur
- Host ohne Border, Hintergrund, Schatten, äußere Kachel oder Pseudoelemente
- exakt `V2.6.3.7-Beta` und `Tool by S.K.`
- Grafik vollständig geladen; Text ohne horizontalen/vertikalen Überlauf
- gleiche sichtbare Höhe und Mittellinie wie Logo und Headerbuttons
- 320-px-Test mit längerem Stand `V2.6.3.7-RC.12-Beta`

## 3. Header- und Zustandsstabilität

Auf 320 × 700, 390 × 844, 844 × 390, 820 × 1180 und 1440 × 1000:
- Hover, Fokus, Drücken und aktiv verändern keine Position oder Größe
- Header-DOM, Geometrie und berechnete Styles vor/während/nach Sortierung identisch
- Header-Screenshot Normal/Sortieren: 0 geänderte Pixel
- Logo, Release-Modul, Suche, Favoritenbutton und Zähler bleiben sichtbar
- Sortier-Dock liegt fixed außerhalb des Headers und überdeckt keine Apps/Titel

## 4. Drag-and-Drop und Sortierregression

- Wackeln ausschließlich auf dem direkten Icon-PNG
- maßgleicher Platzhalter und body-direkte viewportfeste Drag-Ebene
- Ziehen über Reihen/Spalten, Zielerkennung, Randbegrenzung und Auto-Scroll
- Drop, pointercancel, lostpointercapture, Escape, blur und pagehide
- Rückgängig/Wiederholen, Tastaturverschiebung und Standardreihenfolge
- Speicherung in `skPctHomeOrderV1` und Reload-Wiederherstellung
- normaler Header bleibt im Sortiermodus unverändert

## 5. Browser-, Touch- und Funktionsregression

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Prüfumfang:
- 1.430 Browserprüfungen
- 15 aktive Routen × Smartphone, Tablet und Desktop
- fünf Reorder-Profile einschließlich iPhone-Portrait/-Landscape
- 320-px-Reflow und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home-/Zurücknavigation
- sechs Rechnerreferenzen einschließlich Grenzwerte, Reset und Vorzeichen
- Wissensnavigation, lokale Referenzen und externe Zielabsicherung
- Offline-Start, Offline-Unterseiten und Cache-Upgrade

## 6. Visuelle QA

Screenshots für Normal- und Sortierzustand auf allen fünf Reorder-Profilen:
- keine Headeränderung oder Header-/Dock-/App-Kollision
- kein horizontaler Überlauf und keine abgeschnittenen Texte
- Release-Modul wirkt als Teil derselben Icon-Familie
- ausgewogene Proportionen auf Phone, iPhone-PWA, Querformat, Tablet und Desktop

## 7. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`,
`UEBERGABE-V2.6.3.7-Beta.txt` und das vollständige ZIP-Paket finalisiert.
