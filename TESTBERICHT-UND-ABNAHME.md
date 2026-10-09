# Testbericht und Abnahme – SK PLT Tools 2.1.4.0-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.3.0-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** vollständiges Projekt mit neuem responsivem Aufbau

## Gesamtergebnis

**PASS – der neue responsive Aufbau ist zentral umgesetzt, der vollständige Funktionsumfang bleibt erhalten und die Beta ist als ZIP auslieferbar.**

## Umgesetzter Aufbau

- Sticky Mobile-Header mit oberer Safe-Area und stabilem Raster für Logo, Titel und Startseiten-Link.
- Einspaltige Smartphone- und zweispaltige Tablet-Werkzeugübersicht.
- Kompakter Startseiten-Hero mit mobil vorangestelltem Logo; im Smartphone-Querformat steht das Logo rechts neben dem Text.
- Mindestens 44 px große zentrale Touch-Ziele; mobile Formfelder sind 48 px hoch.
- Favoriten- und Baummenü-Schaltfläche: mobil 50 × 50 px, fest in den unteren Viewport-Ecken und Safe-Area-fähig.
- Seitendrawer mit dynamischer Viewport-Höhe, Safe-Area-Innenabständen und begrenztem Overscrolling.
- Eigene Regeln für breite Smartphone-Querformate, Standalone-PWA und reduzierte Bewegung.
- Einheitliche Tastatur-Fokusmarkierung für Links, Schaltflächen, Formfelder und aufklappbare Bereiche.
- Responsive Regeln zentral in `assets/responsive.css`, auf allen 15 Seiten als letzte Stilschicht geladen.

## Technische Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.4.0-Beta in VERSION, allen 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker und Release-Konfiguration |
| T02 | Smartphone Hochformat | PASS · 390 × 844 px, einspaltige Karten, sticky Header, 50-px-Schnellzugriffe, kein horizontales Überlaufen |
| T03 | Smartphone Querformat | PASS · 844 × 390 px, zweispaltige Karten, zweispaltiger Hero, sticky Header und feste untere Schnellzugriffe |
| T04 | Tablet | PASS · 820 × 1180 px, zweispaltige Werkzeugübersicht und unveränderte Modulfunktionen |
| T05 | Desktop | PASS · 1440 × 1050 px, bestehender dreispaltiger Aufbau ohne Layoutregression |
| T06 | Touch-Ziele und Formulare | PASS · zentrale Ziele mindestens 44 px; mobile Eingaben und Auswahllisten 48 px |
| T07 | Safe-Area/PWA-Shell | PASS · obere, untere, linke und rechte Safe-Areas in Header, Schnellzugriffen und Drawern berücksichtigt |
| T08 | Statische Release-Validierung | PASS · 15 Direktseiten, lokale Referenzen, JavaScript-Syntax, Ausschlussregeln, Modulbestand und interne SHA-256-Liste fehlerfrei |
| T09 | Funktions-Smoke-Test | PASS · Rechner, Siemens-Eingaberichtungen, Messbereich, Einheiten, Diagnosegrenzen und Wissensinhalte funktionsfähig |
| T10 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T11 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.4.0-beta`, Release-Cache `sk-plt-tools-v2.1.4.0-Beta`, vollständiger Precache und Offline-Direktaufrufe |
| T12 | Responsive Stilschicht | PASS · `assets/responsive.css` auf allen 15 Seiten vorhanden, zuletzt geladen und im Offline-Cache enthalten |

## Verwendete automatisierte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.4.0-Beta.zip
```

## Sichtprüfung

Die durch den Browser-Smoke-Test erzeugten Screenshots wurden für folgende Ansichten geprüft:

- Startseite Desktop,
- Startseite Smartphone Hochformat,
- Startseite Smartphone Querformat,
- Siemens-Rohwert-Rechner Desktop, Tablet und Smartphone,
- mobile Baumnavigation,
- Wissens- und Rechnerseiten ohne horizontales Überlaufen.

## Abnahme

- Die vollständige Projektstruktur der V2.1.3.0-Beta ist erhalten und um genau eine zentrale responsive Stilschicht erweitert.
- Bestehende Berechnungen, Wissensinhalte, Navigation, Suche, Favoriten, PWA- und Offline-Funktionen bleiben erhalten.
- Der neue Aufbau ist für Smartphone, Smartphone-Querformat, Tablet, Desktop und Standalone-PWA zentral definiert und regressionsgeprüft.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
