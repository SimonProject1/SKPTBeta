# Testplan – SK PCT Tools V2.6.1.6-Beta

Stand: 16.10.2026

## 1. Statische Struktur- und Integritätsprüfung

Befehl:

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und eine zentrale App-JS-Datei
- Version 2.6.1.6-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Verweise auf V2.6.1.0 bis V2.6.1.5
- lokale Referenzen, H1, Referrer-Schutz, Header und Footer
- vollständige SHA256SUMS.txt
- Service-Worker-Kerncache v2-6-1-6-core-r1
- vollständiger Control-Sprite

## 2. Unveränderte Icon-Dateien

- genau 22 aktive PNGs mit Präfix `v2-6-1-6-`
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons
- PNG-Signatur, 512 × 512 px, RGBA und echte Transparenz
- SHA-256 jedes PNGs muss exakt dem korrespondierenden Original aus
  V2.6.1.5-Beta entsprechen
- 22 unterschiedliche Dateihashes
- vollständige Aufnahme in den Offline-Kerncache

## 3. Startseiten-Geometrie

Für Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000:
- alle zehn App-Icons besitzen einheitliche Außen- und Innenmaße
- App-Kachel und PNG-Icon haben im Ruhezustand `transform: none`
- für jedes App-Icon geometrischer Vorher-/Nachher-Vergleich bei:
  - Mouse-Hover
  - Tastaturfokus
  - gedrücktem Pointer-Zustand
  - Aktivklasse und `data-active`
- zulässige Abweichung je Kante höchstens 0,25 CSS-Pixel
- sichtbarer Favoritenkreis rund 22 px
- Touchfläche mindestens 44 × 44 px
- Kreismittelpunkt höchstens 1 CSS-Pixel von oberer und rechter Icon-Außenkante
  entfernt; der sichtbare Kreis muss beide Außenkanten überlappen

## 4. Browser-Regression

Befehl:

```bash
python3 tests/browser_regression.py
```

Weiterer Prüfumfang:
- 15 Routen × Smartphone, Tablet und Desktop
- Header, Footer, Rahmen, Scrollverhalten und horizontaler Überlauf
- 320-px-Reflow-Sanity
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation, Kompaktansicht und Quellenbündel
- Offline-Start und Offline-Unterseiten
- Upgrade-Test: Altcache wird entfernt, nur `v2-6-1-6-core-r1` bleibt

## 5. Visuelle Abnahme

- Screenshots der Startseite bei 390 × 844, 820 × 1180 und 1440 × 1000
- keine Kollision der Favoritensterne mit Symbolmotiv oder Titel
- keine abgeschnittenen Icons, defekten Bilder oder horizontalen Überläufe
- unveränderte Icon-Grafik gegenüber V2.6.1.5-Beta

Die real ausgeführten Ergebnisse werden in `TEST-RESULTS.txt` festgehalten.
Erst danach werden `SHA256SUMS.txt` und das ZIP-Paket erstellt.
