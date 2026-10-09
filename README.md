# SK PLT Tools 2.1.4.2-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.4.2-Beta** basiert auf **2.1.4.1-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Neuaufbau in 2.1.4.2

- vollständiger Neuaufbau des Releasepakets aus der validierten V2.1.4.1-Beta,
- konsistente Synchronisierung aller technischen Versionsstellen,
- neue PWA-App-ID und neuer versionsgebundener Service-Worker-Cache,
- korrigierte Versionskette in Baseline- und Deployment-Dokumentation,
- neu erzeugte Prüfsummen und vollständiges ZIP-Paket,
- keine fachlichen oder visuellen Funktionsänderungen gegenüber V2.1.4.1-Beta.

## Enthaltene Funktionen

- Analogsignal-Rechner,
- P+F Rechner,
- Pt100-/Pt1000-Rechner,
- Einheitenrechner,
- Spannungsfall-Rechner,
- Siemens-SPS-Analogwert-Rechner mit frei definierbarem physikalischem Messbereich, beliebiger Einheit und Umrechnung aus Rohwert, Signalwert oder physikalischem Istwert,
- Messstellen-Dokumentation,
- Wissensdatenbank mit Werkstoff-Nachschlagewerk,
- externer E+H Device Viewer,
- Favoriten, Suche, Filter, Navigation und Offline-PWA,
- zentraler responsiver Aufbau für Desktop, Tablet, Smartphone und Standalone-PWA.

## Projektstruktur

- `index.html` und 14 Unterseiten,
- `assets/`: zentrale Laufzeitdateien, Datenkataloge und Modulressourcen,
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente,
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Prüfsummen und ZIP,
- `tools/validate_release.py`: statische Vollständigkeits-, Safe-Area-, Ausschluss- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner- und Inhaltsregressionen,
- `tools/browser-smoke-test.py`: Browser-, Header-, Responsive-, PWA- und Offline-Test,
- `TESTBERICHT-UND-ABNAHME.md`: geprüfter Release-Nachweis,
- `SHA256SUMS.txt`: vollständige interne SHA-256-Prüfsummen.

## Testen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
# in einem zweiten Terminal
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
```

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, App-ID, Cache, Precache und Dokumentationsreferenzen, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
