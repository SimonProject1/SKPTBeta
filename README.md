# SK PLT Tools 2.1.4.0-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.4.0-Beta** basiert vollständig auf dem geprüften Stand **2.1.3.0-Beta**; die stabile Referenz bleibt **2.1.0.0**. Der neue zentrale Responsive-Aufbau optimiert Header, Hero, Karten, Formulare, Schnellzugriffe und Drawer für Smartphone, Tablet, Desktop und Standalone-PWA.

## Responsive-Aufbau 2.1.4.0

- sticky Mobile-Header mit iPhone-Safe-Area,
- einspaltige Smartphone- und zweispaltige Tablet-Werkzeugübersicht,
- mindestens 44 px große Touch-Ziele und 48 px hohe mobile Formfelder,
- 50 × 50 px große, fest positionierte Favoriten- und Navigationsschaltflächen,
- Drawer mit dynamischer Viewport-Höhe und Safe-Area-Innenabständen,
- eigene Regeln für Querformat, Standalone-PWA und reduzierte Bewegung,
- unveränderte fachliche Funktionen und geprüfte Desktopdarstellung.

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
- Favoriten, Suche, Filter, Navigation und Offline-PWA.

## Projektstruktur

- `index.html` und 14 Unterseiten,
- `assets/`: zentrale Laufzeitdateien, Datenkataloge und Modulressourcen,
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente,
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Prüfsummen und ZIP,
- `tools/validate_release.py`: statische Vollständigkeits-, Ausschluss- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner- und Inhaltsregressionen,
- `tools/browser-smoke-test.py`: Browser-, Responsive-, PWA- und Offline-Test,
- `TESTBERICHT-UND-ABNAHME.md`: geprüfter Release-Nachweis,
- `SHA256SUMS.txt`: vollständige interne SHA-256-Prüfsummen.

## Testen

```bash
node tools/functional-smoke-test.js
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
# in einem zweiten Terminal
python3 tools/browser-smoke-test.py
```

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, App-ID, Cache, Precache und Dokumentationsreferenzen, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
