# SK PLT Tools 2.1.2.1-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.2.1-Beta** basiert vollständig auf dem geprüften Stand **2.1.2.0-Beta**; die stabile Referenz bleibt **2.1.0.0**.

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
