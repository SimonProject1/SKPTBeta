# Testplan – SK PCT Tools V2.6.5.3-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.2-Beta

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
node --check assets/app-v2-6-5-3.js
node --check assets/analogsignal-rechner.js
python3 -m py_compile tests/*.py tools/*.py
python3 tests/validate_project.py
```

Prüfumfang: VERSION, 16 HTML-Dokumente, 14 aktive interne Unterseiten, zentrale
CSS-/JS-Referenzen, Manifest, Suchindex, Cache-Epoch, lokale Ziele, H1, Header/Footer,
10 Apps, 24 versionierte Navigationsicons, geschützte PNG-Inhalte, Offline-Precache,
Analogsignal-Einheitenbereinigung und SHA256SUMS.txt.

## 2. Visuelle Einbettung von Header und Footer

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/visual_shell_regression_v2653.py
```

800 Prüfungen über 16 Routen und fünf Profile:

- Header und Footer ohne deckende Eigenfläche
- kein eigener Hintergrundverlauf, Balkenschatten oder zweiter Rahmen
- Strukturkanten höchstens 10 % Alpha; Sollwerte 8 % und 6 % Cyan
- mehrlagiger App-Hintergrund ausschließlich am Standard-App-Rechteck
- Header und Footer vollständig innerhalb dieses Rechtecks
- Startseite, Unterseiten, kurze/lange Seiten und Wissensansichten

Zusätzlich werden V2.6.5.1, V2.6.5.2 und V2.6.5.3 bei 390 × 844 gerendert.
Der mittlere absolute RGB-Sprung an Header-/Footergrenze muss gegenüber V2.6.5.2
deutlich sinken und die Größenordnung der harmonischen V2.6.5.1 erreichen.

## 3. Vollständiger Positionsabgleich

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2653.py
```

1.440 Prüfungen über 16 Routen und fünf Profile:

- iPhone/iOS-PWA 390 × 844
- Smartphone 412 × 915
- Smartphone-Querformat 844 × 390
- Tablet 820 × 1180
- Desktop 1440 × 1000

Rahmenlage, Headerhöhe, Logo-/Versions-/Button-Mittellinien, Inhaltsbeginn,
Footerabschluss, Safe Area, Überlauf, Bildintegrität und Interaktionsstabilität müssen
unverändert dem erfolgreichen V2.6.5.2-Positionsstandard entsprechen.

## 4. Berechnung und Analogsignal-Regression

Automatisiert in `browser_regression.py`:

- keine Prozesskategorie, Prozess-/Signaleinheit, s0/s1 oder `unit-system.js`
- 4–20 mA, 0–20 mA, 0–10 V und 2–10 V
- Vorwärts- und Umkehrrechnung; MA kleiner ME
- Messbereiche 0…100, −50…150 und 10…110
- leere/ungültige Eingabe und MA = ME
- Reset, Folgeeingabe, Liveberechnung, Ergebnisprozent, Kopieren, Enter und ±
- Referenz-, Grenz-, Reset-, Kopier- und Vorzeichentests aller sechs Rechner

## 5. Design, Touch, Accessibility und Offline

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2653.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Geprüft werden Favoriten kurz/lang/leer, Suche und Filter, Hersteller-Hub,
Breadcrumbs, Chevron, Tastaturfokus, Fokusfalle, Escape, Fokusrückgabe,
44-px-Touchziele, unveränderter Header im Sortiermodus, Drag-and-Drop mit
Pointer-/Touch-Abbruch, 320-px-Reflow, Service-Worker-Upgrade und Offlineaufruf.

## 6. Visuelle QA

13 Renderings: Drei-Versionen-Vergleich der Startseite sowie zehn repräsentative
V2.6.5.3-Screenshots auf iPhone und Desktop für Analogsignal, Wissens-Hub,
Wissensbeitrag, Einheitendatenbank und Werkstoffdatenbank. Kriterien: harmonischer
Flächenübergang, keine Balkenwirkung, keine Überlagerung, kein Abschneiden, keine
Layoutsprünge und kein horizontaler Überlauf.

## 7. Abschluss

1. TEST-RESULTS.txt finalisieren.
2. Temporäre QA-Dateien und `__pycache__` aus dem Projekt entfernen.
3. SHA256SUMS.txt über alle Projektdateien außer sich selbst erzeugen.
4. Struktur- und Prüfsummenprüfung erneut ausführen.
5. vollständiges ZIP erzeugen und separat per SHA-256 prüfen.
6. ZIP erneut entpacken und die Strukturprüfung in der Kopie wiederholen.
