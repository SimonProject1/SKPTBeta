# Testplan – SK PCT Tools V2.6.5.0-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.4.0-Beta

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
python3 tests/validate_project.py
```

Prüft unter anderem:

- `VERSION`, Manifest, Suchindex, Service Worker und Cache-Epoch
- 16 HTML-Dokumente, 14 gerahmte Unterseiten, genau ein H1 je Seite
- zentrale CSS-/JS-Dateien und alle lokalen Referenzen
- zehn eindeutige Startseiten-Apps
- App-, Hersteller-, Wissens-, PWA-, Maskable-, Favicon- und Markenassets
- feste Referenz-Hashes der geschützten PNG-Dateien
- 24 versionierte Navigations-/Fachicons inklusive Maße und Alpha-Grenzen
- vollständiges Offline-Precache-Inventar
- vollständige `SHA256SUMS.txt`
- Python- und JavaScript-Syntax

## 2. Design-Audit-Abnahme V2.6.5.0

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2650.py
```

Prüft:

- alle 16 Seiten auf Desktop
- Seite/Version/H1/Bilder/Überlauf/Footer
- Seitenidentität auf allen aktiven Unterseiten
- 5-mal-2-Desktop-Raster und responsive Smartphone-/Tablet-Raster
- transparente Iconhosts ohne zusätzliche Rahmen, Schatten oder Pseudokacheln
- Kartenlabels ab 12 px
- Suche/Filter mit Siemens-Trefferliste auf Desktop und Mobil
- Suchsymbol-/Platzhalterabstände
- Favoritenicon links, Text mittig, Entfernen rechts sowie Speicherung/Reload
- ortsfesten Header und 44-px-Controls im Sortiermodus
- 44-px-Kopier- und Rechnercontrols
- mobile Zurück-Chips
- Chevron unten/oben in Einheiten- und Werkstoffdatenbank
- vollständigen Offlineaufruf einer internen Unterseite

## 3. Clean-Design-, Touch- und Favoritenregression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
```

Prüft 345 Zustände in iPhone-PWA-, Tablet-Touch- und Desktopprofilen:

- fünf Herstellerkacheln und fünf Wissensbeiträge
- Ruhe, Hover, Fokus, Drücken und aktiv
- ortsfeste Kachel-/Icon-/Textgeometrie
- transparente Hosts und unveränderte PNG-Darstellung
- Favoritendialog, Safe Area, Touchziele, Tastatur und Fokusfalle
- Reload, Einzellöschen, „Alle leeren“, leerer Zustand und Zähler

## 4. Vollständige Browser-/Funktionsregression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Prüft alle aktiven Routen und Kernfunktionen in mehreren Viewports:

- Smartphone 390 × 844, Tablet 820 × 1180, Desktop 1440 × 1000
- Reflow 320 × 700 und Smartphone-Landscape 844 × 390
- Header, Footer, Release-Modul, Navigation und Safe Area
- Suche, Filter, Favoriten und externe Navigation
- freie Drag-and-Drop-Sortierung, Long-Press, Pointer-Abbruch, Undo/Redo,
  Standardreihenfolge, Speicherung, Reload und sofortige Navigation
- sechs Rechner mit Referenz-, Grenzwert-, Reset- und Vorzeichentests
- Einheiten- und Werkstoffdaten
- Wissens-Hub, Herstelleransichten und Beiträge
- Service-Worker-Installation, Cache-Upgrade und Offline-Navigation

## 5. Accessibility und Touch

Automatisierte Kriterien:

- genau ein H1, semantische Dialog-/Tab-/Detailszustände
- ARIA-Labels/-Expanded/-Pressed und Live-Status
- sichtbare Tastaturfokusringe
- Touchziele mindestens 44 × 44 px
- keine fachliche Aussage nur über Farbe
- `prefers-reduced-motion`
- kein horizontaler Überlauf

Manuelle Sichtkontrolle:

- Fokusreihenfolge und Lesbarkeit bei 200 % Zoom
- Screenreader-Bezeichnungen für Header, Favoriten, Suche und Aufklappbereiche
- Kontrast der Haupttexte, Controls und Zustandsmeldungen

## 6. Visuelle QA

Vollseiten-Renderings für Startseite, Suche, Favoriten, Sortiermodus, Rechner,
Einheitendatenbank, Werkstoffdatenbank, Wissens-Hub und Wissensbeitrag auf
Desktop, Smartphone/iOS-PWA und Tablet.

Abnahmekriterien:

- keine abgeschnittenen Texte oder ungewollten Überläufe
- keine doppelten Iconrahmen, Cyan-Ringe oder Versatzschatten
- eine klare Ebenenstruktur
- sichtbare Ergebnisse direkt unter Suche/Filter
- mobile Breadcrumb-Chips und Safe-Area-Abstände
- geöffnete/geschlossene Chevrons eindeutig
- Ergebnis, Warnung, Fehler, Erfolg, Fokus und Aktivzustand konsistent

## 7. Abschluss

Nach erfolgreicher Abnahme:

1. `TEST-RESULTS.txt` finalisieren.
2. `SHA256SUMS.txt` über alle Projektdateien außer sich selbst erzeugen.
3. Strukturprüfung erneut ausführen.
4. vollständiges ZIP erzeugen.
5. ZIP-SHA-256 separat berechnen und verifizieren.
