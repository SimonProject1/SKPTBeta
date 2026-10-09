# Testbericht und Abnahme – SK PLT Tools 2.1.4.2-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.4.1-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** vollständiger Neuaufbau des Releasepakets mit Versionssynchronisierung, Dokumentationskorrekturen und unverändertem Funktionsumfang

## Gesamtergebnis

**PASS – das Projekt wurde vollständig als 2.1.4.2-Beta neu aufgebaut; Versionsidentität, PWA-/Offline-Bestand, responsive Oberfläche, Rechner, Inhalte, Navigation und Prüfsummen sind konsistent.**

## Umgesetzte Releasekorrekturen

- Alle technischen Versionsstellen wurden von 2.1.4.1-Beta auf 2.1.4.2-Beta synchronisiert.
- Manifest-ID, Start-URL und Service-Worker-Cache sind versionsspezifisch neu aufgebaut.
- Die direkte Basis ist in Release Notes, README, Baseline, Deployment, Testbericht und Projektübergabe korrekt als 2.1.4.1-Beta dokumentiert.
- Veraltete Versionsverweise in Baseline und Deployment wurden entfernt.
- Precache, interne SHA-256-Liste und vollständiges ZIP-Paket wurden neu erzeugt.
- Fachliche Funktionen und sichtbares Design bleiben gegenüber 2.1.4.1-Beta unverändert.

## Technische Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.4.2-Beta in VERSION, allen 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | iPhone-/PWA-Metadaten | PASS · `viewport-fit=cover`, PWA-Fähigkeit und dunkler Statusbereich auf allen 15 Seiten |
| T03 | Smartphone Hochformat | PASS · 390 × 844 px, vollbreiter Header, feste Schnellzugriffe, kein horizontales Überlaufen |
| T04 | Smartphone Querformat | PASS · 844 × 390 px, vollbreiter sticky Header, bündige Trennlinie und feste Schnellzugriffe |
| T05 | Unterschiedliche Seitenstrukturen | PASS · Header innerhalb von `.shell` sowie direkt unter `body` auf allen 15 Direktseiten bündig |
| T06 | Tablet und Desktop | PASS · bestehende zwei- bzw. dreispaltige Darstellung ohne Layoutregression |
| T07 | Funktions-Smoke-Test | PASS · Rechner, Siemens-Eingaberichtungen, Messbereich, Einheiten, Diagnosegrenzen und Wissensinhalte funktionsfähig |
| T08 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T09 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.4.2-beta`, Release-Cache `sk-plt-tools-v2.1.4.2-Beta`, vollständiger Precache und Offline-Direktaufrufe |
| T10 | Statische Release-Validierung | PASS · Direktseiten, lokale Referenzen, JavaScript-Syntax, Ausschlussregeln, Safe-Area-Metadaten und interne SHA-256-Liste fehlerfrei |
| T11 | Integrität | PASS · vollständige interne SHA-256-Prüfsummen validiert und Release-ZIP fehlerfrei getestet |

## Verwendete automatisierte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.4.2-Beta.zip
```

## Abnahme

- Die vollständige Projektstruktur der V2.1.4.1-Beta ist erhalten.
- Bestehende Berechnungen, Wissensinhalte, Navigation, Suche, Favoriten, responsive Oberfläche sowie PWA- und Offline-Funktionen bleiben erhalten.
- Die Release-Identität ist konsistent und ältere versionsgebundene Caches werden getrennt.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
