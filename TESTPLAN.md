# Testplan – SK PCT Tools V2.6.5.5-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.4-Beta  
Scope: ausschließlich Punkt 1 des abgestimmten Fahrplans

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
node --check assets/app-v2-6-5-5.js
node --check assets/analogsignal-rechner.js
node --check assets/knowledge-overview.js
python3 -m py_compile tests/*.py tools/*.py
python3 tests/validate_project.py
```

Prüfumfang: VERSION, 16 HTML-Dokumente, 14 aktive interne Unterseiten, zentrale
CSS-/JS-Referenzen, Manifest, Suchindex, Service Worker, Cache-Epoche, lokale
Ziele, H1, Header/Footer, Offline-Precache und SHA256SUMS.txt.

## 2. Gezielter Korrekturblock V2.6.5.5

```bash
SK_BASE_URL=http://127.0.0.1:8080/ \
python3 tests/correction_block_v2655.py
```

Geprüft werden:

- 320 × 800, 390 × 844, 412 × 915, 820 × 1180 und 1440 × 1000
- mobiles Dreispaltenraster mit 10 Apps
- deaktivierte automatische Silbentrennung und kontrollierte `<wbr>`-Stellen
- vollständige Titel ohne horizontalen Überlauf
- Analogsignal-Umrechnungsrichtung bis 430 px in voller Feldbreite
- Spannungsfall-Stromart bis 430 px in voller Feldbreite
- vollständige Optionswerte ohne Ellipsen oder fachliche Kürzung
- mindestens etwa 10 px im aktuellen Versionsmodul und Footer
- mindestens etwa 13 px für sichtbare Hilfstexte
- Endress+Hauser mit kontrollierter Trennstelle im Wissens-Hub
- mobiler Werkstoff-Breadcrumb verborgen, Desktop-Breadcrumb sichtbar
- mobiler Wissensdatenbank-Chip im Wissensbeitrag sichtbar
- kompakte leere Favoritenzeilen in beiden Zielansichten
- Screenshots der Kernzustände je Profil

## 3. Layout und visuelle Shell

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2655.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/visual_shell_regression_v2655.py
```

- 16 Routen × 5 Profile
- iPhone/iOS-PWA 390 × 844
- Smartphone 412 × 915
- Smartphone-Querformat 844 × 390
- Tablet 820 × 1180
- Desktop 1440 × 1000
- Rahmenlage, Header, Inhalt, Footer, Safe Area, Reflow und
  Interaktionsstabilität

## 4. Design, Touch, Tastatur und Favoriten

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2655.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
```

Geprüft werden Touchziele, Fokus, Fokusfalle, Escape, Fokusrückgabe, Suche,
Filter, leere/kurze/lange Favoritenlisten, Hersteller-Hub, Breadcrumbs,
Hoch-/Querformat und unveränderte Raster-/Icongeometrie.

## 5. Funktionen, Rechner, Sortierung und Offline

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

- 15 aktive Seiten × 3 Haupt-Viewports
- 5 Reorder-Profile einschließlich 320-px-Reflow und 844 × 390
- Drag-and-Drop, Touch, Pointer, Long-Press, Abbruch, Undo/Redo und Speicherung
- sechs Rechnerreferenzen einschließlich Analogsignal und Spannungsfall
- Datenbanken, Wissens-Hub und fünf Wissensbeiträge
- Service-Worker-Upgrade, Cache-Löschung und Offline-Unterseiten
- geschützte Logo-/PWA-Dateien per Browser-SHA-256

## 6. Unverändertheits- und Bildprüfung

- alle PNG-Dateien gegen die V2.6.5.4-Basis nach normalisierter
  Versionspfadzuordnung vergleichen
- keine Änderung der Binärinhalte großer PNG-Icons, Logos oder Fachgrafiken
- keine Änderung der fünf Wissensbeitragsgrafiken und Ergebnisdarstellungen
- keine Änderung der Drag-and-Drop-Funktionen

## 7. Abschluss und Paket

1. Dokumentation finalisieren.
2. Temporäre QA-Dateien und `__pycache__` entfernen.
3. `SHA256SUMS.txt` über jede Projektdatei außer sich selbst erzeugen.
4. Struktur-, Syntax- und Prüfsummenprüfung erneut ausführen.
5. vollständiges ZIP erzeugen und separat per SHA-256 prüfen.
6. ZIP erneut entpacken und Validierung in der Kopie wiederholen.
