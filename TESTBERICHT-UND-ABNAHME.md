# Testbericht und Abnahme – SK PLT Tools 2.1.6.1-Beta

**Prüfdatum:** 10.10.2026  
**Direkte Basis:** 2.1.6.0-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** mobile Zahlentastatur in sämtlichen Zahlen-Eingabefeldern aller Rechner-Tools, unverändertes Design und unveränderte Berechnungslogik, Desktop-/Tablet-/iPhone-Darstellung, PWA/Offline und Releaseintegrität

## Gesamtergebnis

**PASS – alle 19 Zahlen-Eingabefelder der sechs Rechner-Tools besitzen den expliziten mobilen Tastaturhinweis `inputmode="decimal"` oder `inputmode="numeric"`. Die Berechnungslogik stimmt weiterhin bitgenau mit der bestehenden 2.1.5.2-Beta-Logikbaseline überein. Das bestehende Rechnerdesign sowie Desktop-, Tablet-, iPhone- und Smartphone-Querformatdarstellung blieben ohne Regression.**

## Geprüfte Zahlenfelder

| Rechner | Zahlenfelder | Mobile Eingabevorgabe | Ergebnis |
|---|---:|---|---|
| Analogsignal | 5 | `inputmode="decimal"` | PASS |
| Einheiten | 1 | `inputmode="decimal"` | PASS |
| P+F | 4 | `inputmode="decimal"` | PASS |
| Pt100/Pt1000 | 1 | `inputmode="decimal"` | PASS |
| Spannungsfall | 5 | `inputmode="decimal"` | PASS |
| Siemens Rohwert | 3 | `decimal`; Vorgabefeld im Rohwertmodus dynamisch `numeric` | PASS |
| **Gesamt** | **19** | ausschließlich `decimal` oder `numeric` | **PASS** |

Die elf zuvor nicht entsprechend gekennzeichneten Felder in Analogsignal, Einheiten, P+F und Pt100/Pt1000 wurden ergänzt. Spannungsfall und Siemens Rohwert waren bereits korrekt konfiguriert und wurden als Referenz beziehungsweise Regression mitgeprüft. `inputmode` ist der standardisierte Hinweis an mobile Browser zur Auswahl der passenden Bildschirmtastatur; die konkrete Darstellung der Tastatur wird vom jeweiligen Betriebssystem und Browser bereitgestellt.

## Nachweis der unveränderten Logik

| Modul | Baseline-Nachweis | Ergebnis |
|---|---|---|
| Analogsignal-Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Einheitenrechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| P+F Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Pt100-/Pt1000-Rechner | SHA-256 des unveränderten Inline-Skripts | PASS |
| Spannungsfall-Rechner | SHA-256 von `calculator.js` | PASS |
| Siemens-Rohwert-Rechner | SHA-256 von `siemens-analogwert-rechner.js` | PASS |

Die Quellhashes liegen in `test-artifacts/logic-baseline-source.json`. `tools/validate_release.py` berechnet die aktuellen Hashes neu und bricht bei jeder Abweichung ab. Standardwerte, Element-IDs, Ereignisse, Rechenwege, Grenzwerte und Ergebnisformate blieben unverändert.

## Darstellungsprüfung

| Profil | Größe | Prüfumfang | Ergebnis |
|---|---:|---|---|
| Desktop | 1440 × 1050 | sechs Rechner, Rechnerlogik, Karten/Felder/Ergebnisse, Header und seitliche Bedienung | PASS |
| Tablet | 820 × 1180 | fünf vereinheitlichte Rechner, Siemens-Referenz, Raster, Touchflächen, Header und Überlauf | PASS |
| iPhone-Touchprofil | 390 × 844 | alle Rechner-Zahlenfelder, einspaltige Darstellung, 50 × 50 px Bedienzone, sticky Header, Safe Area und Startseiten-Button | PASS |
| Smartphone quer | 844 × 390 | vollbreite Headerlinie, Safe-Area-Abstände, untere Bedienzone und Startseiten-Button | PASS |

Die iPhone-Prüfung erfolgte automatisiert in einem mobilen Chromium-Touchprofil. Für alle `input[type="number"]` wurden die DOM-Eigenschaften `decimal` oder `numeric` geprüft; beim Siemens-Vorgabefeld wurde zusätzlich die dynamische Umschaltung von `decimal` auf `numeric` im Rohwertmodus und zurück auf `decimal` geprüft.

## Automatisierte Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.6.1-Beta in VERSION, 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | Rechnerbestand | PASS · Siemens-Referenz plus fünf vereinheitlichte Rechner vollständig vorhanden |
| T03 | Zahlenfeld-Inventar | PASS · 19 Zahlenfelder in sechs Rechnern |
| T04 | Mobile Tastaturattribute | PASS · jedes Zahlenfeld verwendet `inputmode="decimal"` oder `inputmode="numeric"` |
| T05 | Dynamischer Siemens-Rohwertmodus | PASS · Rohwert `numeric`, Signal/physikalischer Wert `decimal` |
| T06 | Gemeinsame Stilschicht | PASS · `rechner-unified.css` unverändert eingebunden |
| T07 | Analogsignal-Logik | PASS · 50 Prozesswert → 12,000 mA und 50,0 % |
| T08 | Einheiten-Logik | PASS · 1 bar → 1.000,000 mbar |
| T09 | P+F-Logik | PASS · K-Faktor 0,160000 und Nullpunkt 4,000000 |
| T10 | Pt-Logik | PASS · Pt100 bei 0 °C → 100,000 Ω |
| T11 | Spannungsfall-Logik | PASS · 16 A, 35 m, 2,5 mm² → 6,93 V und 1,73 % |
| T12 | Logik-Hashvergleich | PASS · sechs Logikdateien/-blöcke stimmen mit der Baseline überein |
| T13 | Siemens-Regression | PASS · Reiter, Vorzeichensteuerung, Grenzfälle, Diagnosefarben und Messbereich unverändert |
| T14 | Desktop | PASS · Rechner und Direktseiten ohne Überlauf oder JavaScript-Fehler |
| T15 | Tablet | PASS · 820 × 1180, passende Raster und Touchflächen |
| T16 | iPhone | PASS · 390 × 844, Zahlentastatur-Hinweise, einspaltige Rechner und feste Bedienzone |
| T17 | Mobile Queransicht | PASS · 844 × 390, Headerlinie und Bedienzone korrekt |
| T18 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T19 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.6.1-beta`, Cache `sk-plt-tools-v2.1.6.1-Beta`, Precache und Offline-Direktaufrufe |
| T20 | Releaseintegrität | PASS · lokale Referenzen, JavaScript-Syntax, interne SHA-256-Prüfsummen und ZIP-Integrität |

## Ausgeführte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.6.1-Beta.zip
```

## Abnahme

- Alle Zahlen-Eingabefelder der sechs Rechner-Tools fordern mobil die passende Zahlentastatur an.
- Design, responsive Anordnung und Funktionslogik sind unverändert.
- Mobile Bedienzone, dunkle iPhone-Safe-Area, Headerlinie und Startseiten-Button wurden beibehalten und geprüft.
- Version, Manifest, Service Worker, Cache, Dokumentation und Prüfsummen sind aktualisiert.
- Sämtliche unterstützten Module, Wissensinhalte, Navigation, Suche, Favoriten sowie PWA- und Offline-Funktionen bleiben erhalten.

**Abnahmestatus: PASS.**
