# SK PLT Tools 2.1.6.0-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.6.0-Beta** baut direkt auf **2.1.5.2-Beta** auf; die stabile Referenz bleibt **2.1.0.0**.

## Neu in 2.1.6.0-Beta

- Die fünf übrigen Rechner **Analogsignal**, **Einheiten**, **P+F**, **Pt100/Pt1000** und **Spannungsfall** verwenden jetzt dieselbe visuelle Sprache wie der Siemens-Rohwert-Rechner aus 2.1.5.2-Beta.
- Vereinheitlicht wurden Rechnerkarten, Eingabekarten, Eingabe- und Auswahlfelder, Ergebnisfelder, Schaltflächen, Abstände, Typografie, Farben und responsive Anordnung.
- Die gemeinsame Darstellung liegt in `assets/rechner-unified.css`; `assets/core.css` und `assets/responsive.css` bleiben die zentrale Anwendungsschale.
- Die Berechnungslogik der fünf umgestalteten Rechner wurde nicht verändert. Hash-Prüfungen vergleichen die Inline-Skripte beziehungsweise `spannungsfall-rechner/calculator.js` bitgenau mit der 2.1.5.2-Beta-Quelle.
- Der Siemens-Rohwert-Rechner bleibt die unveränderte Design- und Logikreferenz.
- Mobile untere Bedienzone, dunkle iPhone-Safe-Area, vollbreite Headerlinie und rechtsbündiger Startseiten-Button bleiben erhalten.
- Manifest-ID, Service-Worker-Cache, Precache, Navigation, Versionsmetadaten, Tests, Dokumentation und Prüfsummen wurden auf 2.1.6.0-Beta aktualisiert.

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
- responsiver Aufbau für Desktop, Tablet, Smartphone und Standalone-PWA.

## Projektstruktur

- `index.html` und 14 Unterseiten,
- `assets/rechner-unified.css`: gemeinsame Gestaltung der fünf umgebauten Rechner,
- `assets/siemens-analogwert-rechner.css`: Referenzgestaltung des Siemens-Rohwert-Rechners,
- `assets/core.css` und `assets/responsive.css`: globale Anwendungsschale einschließlich Safe Areas und mobiler Bedienzone,
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente,
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Prüfsummen und ZIP,
- `tools/validate_release.py`: statische Vollständigkeits-, Design-, Logik-Baseline-, Safe-Area- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner- und Inhaltsregressionen,
- `tools/browser-smoke-test.py`: echte Rechner-, Responsive-, PWA- und Offline-Tests,
- `test-artifacts/`: Referenz-Screenshots für Desktop, Tablet und iPhone-Profil sowie Logik-Baseline,
- `TESTBERICHT-UND-ABNAHME.md`: Release-Nachweis,
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

Geprüfte Browsergrößen: Desktop **1440 × 1050**, Tablet **820 × 1180**, iPhone-Touchprofil **390 × 844** und Smartphone-Querformat **844 × 390**.

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, App-ID, Service-Worker-Cache und Precache, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
