# Testplan – SK PCT Tools V2.6.5.1-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.5.0-Beta

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
node --check assets/app-v2-6-5-1.js
python3 -m py_compile tests/*.py tools/*.py
python3 tests/validate_project.py
```

Prüft `VERSION`, Manifest, Suchindex, Service Worker, Cache-Epoch, 16 HTML-Seiten,
zentrale CSS-/JS-Referenzen, lokale Ziele, H1-Struktur, 10 Apps, 24 versionierte
Navigations-/Fachicons, geschützte PNG-Hashes, Offline-Precache und SHA256SUMS.txt.

## 2. Zielregression V2.6.5.1

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
```

103 Prüfungen in fünf Profilen:

- Desktop 1440 × 1000
- Tablet 820 × 1180
- iPhone/iOS-PWA-Hochformat 390 × 844
- Smartphone-Hochformat 412 × 915
- Smartphone-Querformat 844 × 390

Geprüft werden:

- identische Spaltenzahl von Startseiten-Apps und Hersteller-Hub je Profil
- fünf Herstellerkacheln, sichtbare Iconbreite/-höhe und Beschriftungsmaß
- ausgewogene Nutzung des Raums zwischen Suche, Kacheln und Footer
- Suche, Ergebniszähler und Hersteller-Navigation
- keine Kachelbewegung bei Hover, Fokus, Drücken und Aktivzustand
- Favoritenansicht als direktes Kind des vorhandenen App-Rahmens
- unveränderte Geometrie von Außenrahmen, Header und Footer
- kein Backdrop, kein Vollbilddrawer und keine zweite Außenkontur
- kurze Liste, 14-zeilige lange Liste, inneres Scrollen und leerer Zustand
- gespeicherte Favoriten, Alt-Icon-Migration, Einzellöschen und Alle leeren
- Escape, Fokusfalle, Fokusrückgabe, Zielöffnung und Touchbedienung

## 3. Design-Audit-Abnahme

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2651.py
```

162 Prüfungen über alle 16 Seiten, Desktop, Smartphone/iOS-PWA und Tablet:
Seitenidentität, Footer, Bilder, Überlauf, Suche, Favoriten, Sortierung, 44-px-
Touchziele, Breadcrumbs, Chevron-Zustände und Offlineaufruf.

## 4. Vollständige Browser-/Funktionsregression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

1.347 Prüfungen:

- 15 aktive Seiten × 3 Haupt-Viewports
- Reflow 320 px und Smartphone-Querformat 844 × 390
- Header, Footer, Release-Modul, Safe Area und Navigation
- Suche, Filter, Favoriten und externe Navigation
- freie Drag-and-Drop-Sortierung, Long-Press, Pointer-Abbruch, Undo/Redo,
  Standard, Speicherung, Reload und sofortige Navigation
- sechs Rechner mit Referenz-, Grenzwert-, Reset- und Vorzeichentests
- Einheiten- und Werkstoffdatenbank
- Wissens-Hub, Herstelleransichten und Beiträge
- Service-Worker-Installation, Cache-Upgrade und Offline-Navigation

## 5. Accessibility und Touch

Automatisiert:

- genau ein H1 je Seite
- ARIA-Labels, `aria-expanded`, `aria-pressed`, Dialog- und Live-Status
- sichtbare Tastaturfokusringe und Fokusfalle
- Escape und Fokusrückgabe
- Touchziele mindestens 44 × 44 px
- `prefers-reduced-motion`
- kein horizontaler Dokumentüberlauf

## 6. Visuelle QA

Sichtprüfung auf iPhone/Smartphone und Desktop:

- Hersteller-Hub im Hoch- und Querformat
- drei/fünf/sechs Spalten entsprechend dem Startseitenprofil
- identische sichtbare Hersteller-/App-Iconmaße
- kurze Favoritenliste
- 14-zeilige lange Favoritenliste mit innerem Scrollbereich
- leerer Zustand
- Header, runde Außenbegrenzung, Safe Area und Footer jederzeit im selben Rahmen
- keine abgeschnittenen Titel, keine zweite Hauptfläche und keine Lageänderung

## 7. Abschluss

1. `TEST-RESULTS.txt` finalisieren.
2. `SHA256SUMS.txt` über alle Projektdateien außer sich selbst erzeugen.
3. Strukturprüfung erneut ausführen.
4. vollständiges ZIP erzeugen.
5. ZIP entpacken und Strukturprüfung erneut ausführen.
6. ZIP-SHA-256 separat berechnen und verifizieren.
