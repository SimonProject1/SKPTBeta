# Testbericht und Abnahme – SK PLT Tools 2.1.3.0-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.2.1-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** vollständiges Projekt mit Schwerpunkt feste mobile Schnellzugriffe

## Gesamtergebnis

**PASS – die mobile Anpassung ist zentral umgesetzt, die vollständige Beta ist konsistent und als ZIP auslieferbar.**

## Umgesetztes mobiles Verhalten

- Favoriten-Schaltfläche: `position: fixed`, links unten, 8 px plus iPhone-Safe-Area.
- Baummenü-Schaltfläche: `position: fixed`, rechts unten, 8 px plus iPhone-Safe-Area.
- Beide Schaltflächen bleiben beim vertikalen Seitenscrollen relativ zum Viewport unverändert.
- Die mobile Seite erhält unten 58 px plus Safe-Area als Freiraum, damit scrollbarer Inhalt nicht von den Schaltflächen verdeckt wird.
- Die Regel gilt zentral auf allen 15 Direktseiten bis einschließlich 760 px Breite.
- Desktop und Tablet verwenden weiterhin die vorhandene seitlich zentrierte Positionierung.

## Technische Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.3.0-Beta in VERSION, allen 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker und Release-Konfiguration |
| T02 | Mobile Positionierung | PASS · Favoriten links unten, Baummenü rechts unten, 42 × 42 px, feste Viewport-Position |
| T03 | Scrollstabilität | PASS · Position beider Schaltflächen vor und nach Scrollen identisch |
| T04 | iPhone/PWA-Safe-Area | PASS · bottom/left/right berücksichtigen die jeweiligen `env(safe-area-inset-*)`-Werte |
| T05 | Responsive Regression | PASS · Desktop 1440 px, Tablet 820 px und Mobil 390 px ohne horizontales Überlaufen |
| T06 | Statische Release-Validierung | PASS · 15 Direktseiten, lokale Referenzen, JavaScript-Syntax, Modulbestand und interne SHA-256-Liste fehlerfrei |
| T07 | Funktions-Smoke-Test | PASS · Rechner, Siemens-Eingaberichtungen, Messbereich, Einheiten und Diagnosegrenzen unverändert funktionsfähig |
| T08 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz und Baummenüstruktur funktionieren weiterhin |
| T09 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.3.0-beta`, Release-Cache `sk-plt-tools-v2.1.3.0-Beta`, vollständiger Precache und Offline-Direktaufrufe |
| T10 | ZIP-Integrität | PASS · vollständiger Projektstamm, fehlerfrei prüf- und entpackbar |

## Verwendete automatisierte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
unzip -t SK-PLT-Tools-V2.1.3.0-Beta.zip
sha256sum -c SHA256SUMS.txt
```

## Abnahme

- Die vollständige Projektstruktur der V2.1.2.1-Beta ist erhalten.
- Die Änderung ist zentral auf die mobile Positionierung der Favoriten- und Baummenü-Schaltflächen sowie die zugehörigen Tests und Release-Dokumentation begrenzt.
- Bestehende Funktionen und die Desktop-/Tablet-Darstellung bleiben erhalten.

**Abnahmestatus: PASS.**
