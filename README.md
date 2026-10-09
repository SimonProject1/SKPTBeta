# SK PLT Tools 2.1.5.2-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.5.2-Beta** basiert vollständig auf **2.1.5.1-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Neu in 2.1.5.2-Beta

- Eigener **±-Vorzeichenwechsel** am gemeinsamen aktiven Eingabefeld für **Signal**, **Rohwert** oder **Phys. Wert**.
- Eigene ±-Schaltflächen an **Minimum** und **Maximum** des physikalischen Messbereichs.
- Sofortige Neuberechnung aller abgeleiteten Werte und des Diagnosezustands nach jedem gültigen Vorzeichenwechsel.
- Touch-/Fokusbehandlung ohne automatisches Fokussieren des Zahlenfelds; dadurch öffnet der ±-Touch auf dem iPhone nicht automatisch die Bildschirmtastatur.
- Leere oder ungültige Zahlenfelder werden nicht verfälscht, sondern über die bestehende Eingabeprüfung abgewiesen.
- Drei-Reiter-Aufbau, Reiter-Fokuskorrektur aus 2.1.5.1-Beta, Diagnosefarben, responsive Bedienzone und PWA-/Offline-Funktion bleiben erhalten.

## Enthaltene Funktionen

- Analogsignal-Rechner,
- P+F Rechner,
- Pt100-/Pt1000-Rechner,
- Einheitenrechner,
- Spannungsfall-Rechner,
- Siemens-SPS-Analogwert-Rechner mit drei Eingabearten, frei definierbarem Messbereich, Einheit und Karten-/Diagnoseprofilen,
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
- `tools/validate_release.py`: statische Vollständigkeits-, Altoberflächen-, Safe-Area- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner-, Reiterstruktur- und Inhaltsregressionen,
- `tools/browser-smoke-test.py`: echte Reiterwechsel, Farbstati, Responsive-, PWA- und Offline-Test,
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

Der Build synchronisiert Version, Manifest, App-ID, Service-Worker-Cache und Precache, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
