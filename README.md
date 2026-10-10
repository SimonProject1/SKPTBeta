# SK PLT Tools 2.1.7.3-Beta

Vollständige statische, offline-fähige Webanwendung für PLT-/MSR-Aufgaben. **2.1.7.3-Beta** baut auf der vollständigen **2.1.7.2-Beta** auf; die stabile Referenz bleibt **2.1.0.0**.

## Neu in 2.1.7.3-Beta

- Der Bereich **Einheitenfavoriten** ist auf allen sechs Rechnerseiten wieder an die Breite des jeweiligen Rechner-Hauptbereichs gekoppelt.
- Seine linke und rechte Kante fluchten mit `.calc-panel` beziehungsweise `.analog-panel`.
- Die gemeinsame Geometrie verwendet `box-sizing: border-box`, `width: 100%` und `max-width: 920px`. Dadurch folgt der Balken auf Desktop, Tablet und Smartphone automatisch derselben verfügbaren Inhaltsbreite wie der Rechner.
- Unter 760 px bleibt die vorhandene mobile Stapelung erhalten; Text und Button bleiben innerhalb des Balkens, der Button bleibt touchfreundlich vollbreit.
- Der bereits korrekte Herstellerlink `https://www.de.endress.com/de/onlinetools?store_locale=de` bleibt unverändert.
- Manifest, App-ID, Service-Worker-Release und Cache wurden auf 2.1.7.3-Beta angehoben.

## Unverändert enthalten

- Einheitendatenbank mit 19 Kategorien und 115 Einheiten.
- Persönliche Einheitenfavoriten per Stern und lokale Speicherung unter `skPltUnitFavoritesV1`.
- Zentrale Datei `assets/units.json` als Single Source of Truth für Namen, Symbole, Kategorien, Standardeinheiten, Faktoren, Offsets und Referenzfälle.
- Gemeinsame Laufzeit `assets/unit-system.js` mit affiner Umrechnung `Basis = Wert × Faktor + Offset`.
- Einheitliche Einheiten-Dropdowns mit den Gruppen **Standardeinheit**, **Favoriten** und **Weitere Einheiten**.
- Automatische Umrechnung bereits eingegebener Werte beim Einheitenwechsel, einschließlich °C, K und °F.
- Integration in Analogsignal-, Siemens-Rohwert-, Einheiten-, P+F-, Pt100/Pt1000- und Spannungsfall-Rechner.
- Mobile Zahlentastatur, ±-Vorzeichenwechsel, mobile untere Bedienzone, dunkle iPhone-Safe-Area, Headerlinie und Startseiten-Button.
- Navigation, Startseitensuche, Suchindex, Service-Worker-Precache, Offline-PWA und Manifest-Shortcuts.
- Herstellerlink mit `target="_blank"` und `rel="noopener noreferrer"`.

## Projektstruktur

- `assets/core.css`: gemeinsamer Seitenstil und responsiver, rechnerbreiter `.sk-unit-database-cta`.
- `assets/rechner-unified.css`: gemeinsames 920-px-Maximum der Rechner-Hauptbereiche.
- `assets/siemens-analogwert-rechner.css`: entsprechendes 920-px-Maximum des Siemens-Hauptbereichs.
- `assets/units.json`: zentrale Einheitendatenbank.
- `assets/unit-system.js`: Datenvalidierung, Umrechnung, Dropdowns und Favoritenspeicherung.
- `einheitendatenbank/`: Suche, Kategorienfilter und Favoritenverwaltung.
- `assets/*-rechner.js` und `spannungsfall-rechner/calculator.js`: integrierte Rechnerlogik.
- `assets/navigation-tree.json` und `assets/search-index.json`: Navigation und Suche.
- `manifest.webmanifest` und `service-worker.js`: PWA, Shortcuts und Offline-Cache.
- `tools/release.py`: Versionssynchronisierung, Precache, Prüfsummen und ZIP.
- `tools/functional-smoke-test.js`: Datenmodell-, Formel-, Roundtrip- und Integrationsprüfungen.
- `tools/browser-smoke-test.py`: Browser-, Rechner-, Favoriten-, Responsive-, Link- und Offline-Tests einschließlich Kantenvergleich.
- `tools/validate_release.py`: statische Vollständigkeits- und Integritätsprüfung.
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

Der Build synchronisiert Version, Manifest, Navigation, App-ID, Service-Worker-Cache und Precache, erzeugt `SHA256SUMS.txt` und baut `SK-PLT-Tools-V2.1.7.3-Beta.zip`.
