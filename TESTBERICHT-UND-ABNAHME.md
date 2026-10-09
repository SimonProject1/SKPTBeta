# Testbericht und Abnahme – SK PLT Tools 2.1.4.1-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.4.0-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** vollständiges Projekt mit Korrektur der mobilen Kopfzeile und iPhone-/PWA-Safe-Area

## Gesamtergebnis

**PASS – der weiße obere Bereich ist technisch beseitigt, Header, Trennlinie und Startseiten-Link sind auf allen 15 Direktseiten bündig ausgerichtet, und der bestehende Funktionsumfang bleibt erhalten.**

## Umgesetzte Korrekturen

- `html` erhält einen festen dunkelblauen Hintergrund, damit oberhalb des Body keine weiße Dokumentfläche sichtbar wird.
- Alle HTML-Seiten enthalten `viewport-fit=cover`, `apple-mobile-web-app-capable=yes` und `apple-mobile-web-app-status-bar-style=black-translucent`.
- Der Smartphone-Header verwendet `100vw` und eine containerunabhängige Zentrierung; dadurch funktioniert er innerhalb von `.shell` sowie direkt unter `body`.
- Die Header-Innenabstände berücksichtigen linke und rechte Safe-Areas.
- Dieselbe Korrektur gilt für breite Smartphone-Querformate.
- Die automatischen Tests sichern Headerbreite, Trennlinie, Startseiten-Link und Hintergrund künftig gegen Regressionen ab.

## Technische Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.4.1-Beta in VERSION, allen 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker und Release-Konfiguration |
| T02 | iPhone-/PWA-Metadaten | PASS · `viewport-fit=cover`, PWA-Fähigkeit und dunkler Statusbereich auf allen 15 Seiten |
| T03 | Smartphone Hochformat | PASS · 390 × 844 px, Header x=0 und 390 px breit, Startseiten-Link mit 12 px rechtem Abstand, kein horizontales Überlaufen |
| T04 | Smartphone Querformat | PASS · 844 × 390 px, vollbreiter sticky Header, bündige Trennlinie und feste Schnellzugriffe |
| T05 | Unterschiedliche Seitenstrukturen | PASS · Header sowohl in `.shell` als auch direkt unter `body` auf allen 15 Direktseiten bündig |
| T06 | Tablet und Desktop | PASS · bestehende zwei- bzw. dreispaltige Darstellung ohne Layoutregression |
| T07 | Funktions-Smoke-Test | PASS · Rechner, Siemens-Eingaberichtungen, Messbereich, Einheiten, Diagnosegrenzen und Wissensinhalte funktionsfähig |
| T08 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T09 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.4.1-beta`, Release-Cache `sk-plt-tools-v2.1.4.1-Beta`, vollständiger Precache und Offline-Direktaufrufe |
| T10 | Statische Release-Validierung | PASS · Direktseiten, lokale Referenzen, JavaScript-Syntax, Ausschlussregeln, Safe-Area-Metadaten und interne SHA-256-Liste fehlerfrei |
| T11 | Integrität | PASS · 69 interne SHA-256-Prüfsummen validiert |

## Verwendete automatisierte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
```

## Sichtprüfung

Die neu erzeugten Screenshots wurden für Startseite und Siemens-Rohwert-Rechner in Smartphone-Hochformat, Smartphone-Querformat und Desktop geprüft. Es ist kein weißer Seitenstreifen sichtbar; Header, Trennlinie und Startseiten-Link sind bündig und konsistent.

## Abnahme

- Die vollständige Projektstruktur der V2.1.4.0-Beta ist erhalten.
- Bestehende Berechnungen, Wissensinhalte, Navigation, Suche, Favoriten, PWA- und Offline-Funktionen bleiben erhalten.
- Die Korrektur ist zentral umgesetzt und auf allen Direktseiten regressionsgeprüft.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
