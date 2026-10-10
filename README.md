# SK PLT Tools 2.1.7.0-Beta

Vollständige statische, offline-fähige Webanwendung für PLT-/MSR-Aufgaben. **2.1.7.0-Beta** baut auf der vollständig getesteten **2.1.6.1-Beta** auf; die stabile Referenz bleibt **2.1.0.0**.

## Neu in 2.1.7.0-Beta

- Neue Seite **Einheitendatenbank** mit Suche, Kategorienfilter, 19 Messarten und 115 Einheiten.
- Persönliche Einheitenfavoriten per Stern; lokale Speicherung unter `skPltUnitFavoritesV1`.
- Zentrale Datei `assets/units.json` als Single Source of Truth für Namen, Symbole, Kategorien, Standardeinheiten, Faktoren, Offsets und Referenzfälle.
- Gemeinsame Laufzeit `assets/unit-system.js` mit affiner Umrechnung `Basis = Wert × Faktor + Offset`.
- Einheitliche Einheiten-Dropdowns mit den Gruppen **Standardeinheit**, **Favoriten** und **Weitere Einheiten**.
- Automatische Umrechnung bereits eingegebener Werte beim Einheitenwechsel, einschließlich °C, K und °F.
- Integration in Analogsignal-, Siemens-Rohwert-, Einheiten-, P+F-, Pt100/Pt1000- und Spannungsfall-Rechner.
- Navigation, Startseitensuche, Suchindex, Service-Worker-Precache, Offline-PWA und Manifest-Shortcuts ergänzt.
- Vorhandene Rechnerlogik, Design, mobile Zahlentastatur, ±-Bedienung, untere Bedienzone, dunkle iPhone-Safe-Area, Headerlinie und Startseiten-Button bleiben erhalten.

## Einheitenkategorien

Druck; Durchfluss/Volumenstrom; Massendurchfluss; Temperatur; Länge; Fläche; Volumen; Masse; Zeit; elektrische Spannung; Strom; Widerstand; Leistung; Energie; Drehzahl; Frequenz; Geschwindigkeit; Dichte; dynamische Viskosität.

Feste Grundeinheiten umfassen mindestens **bar**, **°C**, **m³/h**, **m**, **V**, **A** und **Ω**. Jede Kategorie besitzt genau eine feste Standardeinheit.

## Projektstruktur

- `assets/units.json`: zentrale Einheitendatenbank.
- `assets/unit-system.js`: Datenvalidierung, Umrechnung, Dropdowns und Favoritenspeicherung.
- `einheitendatenbank/`: Suche, Kategorienfilter und Favoritenverwaltung.
- `assets/*-rechner.js` und `spannungsfall-rechner/calculator.js`: integrierte Rechnerlogik.
- `assets/navigation-tree.json` und `assets/search-index.json`: Navigation und Suche.
- `manifest.webmanifest` und `service-worker.js`: PWA, Shortcuts und vollständiger Offline-Cache.
- `tools/release.py`: Versionssynchronisierung, Precache, Prüfsummen und ZIP.
- `tools/functional-smoke-test.js`: Datenmodell-, Formel-, Roundtrip- und Integrationsprüfungen.
- `tools/browser-smoke-test.py`: echte Browser-, Rechner-, Favoriten-, Responsive- und Offline-Tests.
- `tools/validate_release.py`: statische Vollständigkeits- und Integritätsprüfung.
- `EINHEITEN-DATENMODELL.md`: Schema und Erweiterungsregeln.
- `TESTBERICHT-UND-ABNAHME.md`: ausgeführte Prüfungen und Grenzen.

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

Geprüfte Viewports: Desktop **1440 × 1050**, Tablet **820 × 1180**, iPhone-Touchprofil **390 × 844** und Smartphone-Querformat **844 × 390**.

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, Navigation, App-ID, Service-Worker-Cache und Precache, erzeugt `SHA256SUMS.txt` und baut `SK-PLT-Tools-V2.1.7.0-Beta.zip`.
