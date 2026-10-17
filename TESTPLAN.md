# Testplan – SK PCT Tools V2.6.3.9-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.3.8-Beta

## 1. Syntax, Struktur und Integrität

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 85 Projektdateien einschließlich `SHA256SUMS.txt`
- 16 HTML-Dokumente, 14 gerahmte Unterseiten und 15 aktive Browserrouten
- zentrale CSS-/JS-Datei, Manifest, Suchindex, Service Worker und Cache-Epoch
- Version `2.6.3.9-Beta` und versionierte Dateinamen/Referenzen
- vollständige lokale Ziele, H1, Referrer-Schutz, Header und Footer
- feste SHA-256-Referenzwerte für geschützte Marken-/PWA-Dateien
- vollständiger SHA-256-Bestand aller Projektdateien
- Python- und JavaScript-Syntax

## 2. Helleres vereinfachtes Header-Logo

- `assets/header-logo-simple.png`: 512 × 512 px, RGBA, feste SHA-256 und Alpha-Grenze
- eigenständiger Generator schreibt ausschließlich diese Datei
- zehnzahniger PCT-Körper, klare schwarze Kontur, helle Cyan-Stahl-Innenfläche
- dunkler Flächenanteil im zentralen Radius zwischen 26,0 % und 43,3 %
- mittlere Innenhelligkeit mindestens 130/255
- PCT-Schriftmasse und Kontrast bei 44/52 px visuell prüfen
- Grundkörper und Materialität entsprechen `navigation_frame()`
- operative Referenz auf Startseite und allen gerahmten Unterseiten
- alte `logo-sk-pct-tools-header.png` bleibt unverändert und operativ unreferenziert
- Simple-Datei ist im Service-Worker-Kerncache enthalten

## 3. Unveränderte PWA-/Homescreen-/App-Icons

Statisch und im Browser werden die fest hinterlegten SHA-256-Werte geprüft für:
- `logo-sk-pct-tools.png`, `logo-sk-pct-tools-header.png`
- `favicon.png`, `apple-touch-icon.png`
- `icon-192.png`, `icon-512.png`
- `icon-maskable-192.png`, `icon-maskable-512.png`

Zusätzlich:
- Manifest-Pfade, Größen und `purpose` (`any`/`maskable`)
- alle 24 Navigations-/App-/Wissens-/Hersteller-PNG-Inhalte gegen V2.6.3.8-Beta
- Release-Modul-PNG-Inhalt gegen V2.6.3.8-Beta

## 4. Header-, Touch- und Zustandsstabilität

Auf 320 × 700, 390 × 844, 844 × 390, 820 × 1180 und 1440 × 1000:
- Logo, Versionsmodul und Headerbuttons auf gemeinsamer vertikaler Mittellinie
- 44-/52-px-Darstellung ohne Überlauf oder Abschneiden
- Hover, Fokus, Drücken, aktiv und geöffnet ohne Positions-/Größenänderung
- Header-DOM, Geometrie, Styles und Screenshot vor/während/nach Sortierung identisch
- separates Sortier-Dock ohne Kollision mit Header, Apps oder Titeln

## 5. Browser-, Touch- und Funktionsregression

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Prüfumfang:
- 1.431 Browserprüfungen
- 15 aktive Routen × Smartphone, Tablet und Desktop
- fünf Reorder-Profile einschließlich iPhone-Portrait/-Landscape
- 320-px-Reflow und Safe-Area-Geometrie
- Suche, Favoritenübersicht, Zähler, Home-/Zurücknavigation
- Drag/Drop, Long-Press, Pointer-Abbruch, History, Speicherung und Reload
- sechs Rechnerreferenzen einschließlich Grenzwerte, Reset und Vorzeichen-Touch
- Wissensnavigation, lokale Referenzen und externe Zielabsicherung
- Offline-Start, Offline-Unterseiten und Cache-Upgrade

## 6. Visuelle QA

Gerenderte Startseiten- und Unterseitenheader auf iPhone/Smartphone, Tablet und Desktop:
- deutlich helleres, ruhigeres Zahnradzentrum
- PCT in tatsächlicher kleiner Anzeigegröße klar lesbar
- identischer Cyan-/Blau-/Grün-Grundkörper wie Versionsmodul und Headerbuttons
- keine Leiterbahnen, Punktknoten, Zusatzrahmen oder Dekorschienen
- keine Verschiebung der optischen Höhe oder vertikalen Mittellinie
- normaler Header im Sortiermodus pixelidentisch

## 7. Abschluss

Nach erfolgreicher Prüfung werden `TEST-RESULTS.txt`, `SHA256SUMS.txt`,
`UEBERGABE-V2.6.3.9-Beta.txt` und das vollständige ZIP-Paket finalisiert.
