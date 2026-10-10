# Testbericht und Abnahme – SK PLT Tools 2.1.6.0-Beta

**Prüfdatum:** 10.10.2026  
**Direkte Basis:** 2.1.5.2-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** Vereinheitlichung aller übrigen Rechner nach dem Siemens-Rohwert-Design, unveränderte Berechnungslogik, Desktop-/Tablet-/iPhone-Darstellung, mobile Safe Areas und Bedienzone, PWA/Offline sowie Releaseintegrität

## Gesamtergebnis

**PASS – alle fünf übrigen Rechner verwenden die gemeinsame Gestaltung nach dem Siemens-Rohwert-Rechner. Die Berechnungslogik stimmt mit der 2.1.5.2-Beta-Baseline überein. Desktop, Tablet, iPhone-Touchprofil und Smartphone-Querformat wurden ohne horizontale Layoutregression geprüft.**

## Umgesetzter Designumfang

- Analogsignal-Rechner
- Einheitenrechner
- P+F Rechner
- Pt100-/Pt1000-Rechner
- Spannungsfall-Rechner

Für diese fünf Rechner wurden Karten, Eingabefelder, Auswahlfelder, Ergebnisfelder, Aktionsschaltflächen, Abstände, Typografie, Farbsystem und mobile Anordnung vereinheitlicht. `assets/rechner-unified.css` bildet die gemeinsame Stilschicht; der Siemens-Rohwert-Rechner selbst bleibt die unveränderte Referenz.

## Nachweis der unveränderten Logik

| Modul | Baseline-Nachweis | Ergebnis |
|---|---|---|
| Analogsignal-Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Einheitenrechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| P+F Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Pt100-/Pt1000-Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Spannungsfall-Rechner | SHA-256 von `calculator.js` | PASS |
| Siemens-Rohwert-Rechner | SHA-256 von `siemens-analogwert-rechner.js` | PASS |

Die Quellhashes liegen in `test-artifacts/logic-baseline-source.json`. `tools/validate_release.py` berechnet die aktuellen Hashes neu und bricht bei jeder Abweichung ab.

## Darstellungsprüfung

| Profil | Größe | Prüfumfang | Ergebnis |
|---|---:|---|---|
| Desktop | 1440 × 1050 | fünf umgestaltete Rechner, Siemens-Referenz, Rechnerlogik, Karten/Felder/Ergebnisse, Header und seitliche Bedienung | PASS |
| Tablet | 820 × 1180 | fünf umgestaltete Rechner, Siemens-Referenz, Raster, Touchflächen, Header, Überlauf | PASS |
| iPhone-Touchprofil | 390 × 844 | fünf umgestaltete Rechner, Siemens-Referenz, einspaltige Darstellung, 50 × 50 px Bedienzone, sticky Header, dunkle Safe-Area-Grundfläche, Startseiten-Button | PASS |
| Smartphone quer | 844 × 390 | vollbreite Headerlinie, Safe-Area-Abstände, untere Bedienzone und Startseiten-Button | PASS |

Die iPhone-Prüfung erfolgte automatisiert in einem mobilen Chromium-Touchprofil mit iPhone-typischem CSS-Viewport. Die Safe-Area-Regeln, PWA-Metadaten und das iOS-Statusleisten-Attribut wurden zusätzlich statisch geprüft.

## Automatisierte Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.6.0-Beta in VERSION, 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | Rechnerbestand | PASS · Siemens-Referenz plus fünf umgestaltete Rechner vollständig vorhanden |
| T03 | Gemeinsame Stilschicht | PASS · `rechner-unified.css` genau einmal und vor `responsive.css` eingebunden |
| T04 | Eingabekarten | PASS · einheitliche Feldkarten, dunkle Eingabeflächen, 12-px-Radien und fokussierte Cyan-Kontur |
| T05 | Ergebniskarten | PASS · grüne Monospace-Ergebnisse, einheitliche Beschriftung, Abstände und Hintergründe |
| T06 | Schaltflächen | PASS · Verlauf Grün/Cyan, Sekundärstil, Touchgrößen und mobile Anordnung |
| T07 | Analogsignal-Logik | PASS · 50 Prozesswert → 12,000 mA und 50,0 % |
| T08 | Einheiten-Logik | PASS · 1 bar → 1.000,000 mbar |
| T09 | P+F-Logik | PASS · K-Faktor 0,160000 und Nullpunkt 4,000000 |
| T10 | Pt-Logik | PASS · Pt100 bei 0 °C → 100,000 Ω |
| T11 | Spannungsfall-Logik | PASS · 16 A, 35 m, 2,5 mm² → 6,93 V und 1,73 % |
| T12 | Logik-Hashvergleich | PASS · sechs Logikdateien/-blöcke stimmen mit V2.1.5.2-Beta überein |
| T13 | Siemens-Regression | PASS · Reiter, Vorzeichensteuerung, Grenzfälle, Diagnosefarben und Messbereich unverändert |
| T14 | Desktop | PASS · alle fünf Rechner und alle Direktseiten ohne Überlauf/JS-Fehler |
| T15 | Tablet | PASS · 820 × 1180, passende Raster und Touchflächen |
| T16 | iPhone | PASS · 390 × 844, einspaltige Rechner, sticky Header, dunkle Safe Area und feste untere Bedienzone |
| T17 | Mobile Queransicht | PASS · 844 × 390, Headerlinie und Bedienzone korrekt |
| T18 | Startseiten-Button | PASS · rechtsbündige Ausrichtung mit 8–20 px rechtem Abstand geprüft |
| T19 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T20 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.6.0-beta`, Cache `sk-plt-tools-v2.1.6.0-Beta`, Precache und Offline-Direktaufrufe |
| T21 | Releaseintegrität | PASS · lokale Referenzen, JavaScript-Syntax, vollständige interne SHA-256-Prüfsummen und ZIP-Integrität |

## Testartefakte

Unter `test-artifacts/` liegen:

- fünf Desktop-Screenshots `rechner-*-desktop.png`,
- fünf Tablet-Screenshots `rechner-*-tablet.png`,
- fünf iPhone-Screenshots `rechner-*-mobile.png`,
- Siemens-Referenzscreenshots für Desktop, Tablet und Mobil,
- bestehende Startseiten-, Navigations- und Wissensseiten-Screenshots,
- `logic-baseline-source.json`.

## Ausgeführte Befehle

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.6.0-Beta.zip
```

## Abnahme

- Alle fünf übrigen Rechner sind visuell an die Siemens-Referenz angeglichen.
- Die vorhandene Berechnungslogik ist unverändert und hashgesichert.
- Mobile Bedienzone, dunkle iPhone-Safe-Area, Headerlinie und Startseiten-Button wurden beibehalten und geprüft.
- Version, Manifest, Service Worker, Cache, Dokumentation und Prüfsummen sind aktualisiert.
- Sämtliche unterstützten Module, Wissensinhalte, Navigation, Suche, Favoriten sowie PWA- und Offline-Funktionen bleiben erhalten.

**Abnahmestatus: PASS.**
