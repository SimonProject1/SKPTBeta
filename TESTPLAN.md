# Testplan – SK PCT Tools V2.6.1.5-Beta

Stand: 16.10.2026

## 1. Statische Struktur- und Integritätsprüfung

Befehl:

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und eine zentrale App-JS-Datei
- Version 2.6.1.5-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Verweise auf V2.6.1.0 bis V2.6.1.4
- lokale Referenzen, H1, Referrer-Schutz, Header und Footer
- vollständige SHA256SUMS.txt
- Service-Worker-Kerncache v2-6-1-5-core-r1
- vollständiger, rekonstruierter Control-Sprite

## 2. Icon-Abnahme

- genau 22 aktive PNGs mit Präfix `v2-6-1-5-`
- 10 App-, 5 Wissens-, 5 Hersteller- und 2 Navigationsicons
- PNG-Signatur, 512 × 512 px, RGBA und echte Transparenz
- gemeinsamer Außenmaster und technisch-industrielle Cyan-/Grün-Akzentrails
- ausreichende weiße Motivmasse und schwarze Kontur
- 22 unterschiedliche Dateihashes
- 10 unterschiedliche App-Icons auf der Startseite
- 5 unterschiedliche Wissensicons und 5 Herstellericons im Wissensbereich
- vollständige Aufnahme in den Offline-Kerncache

## 3. Browser-Regression

Befehl:

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- Header, Footer, Rahmen, Scrollverhalten und horizontaler Überlauf
- Icon-Darstellung, natürliche 512-px-Größe und Favoritenposition
- 320-px-Reflow-Sanity
- 44 × 44-px-Touchziele und reale Touch-Auslösung
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation, Kompaktansicht und Quellenbündel
- Offline-Start und Offline-Unterseiten
- Upgrade-Test: Altcache wird entfernt, nur `v2-6-1-5-core-r1` bleibt

## 4. Dokumentation

Die real ausgeführten Ergebnisse werden nach Abschluss in `TEST-RESULTS.txt`
festgehalten. Erst danach werden `SHA256SUMS.txt` und das ZIP-Paket erstellt.
