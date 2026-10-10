# Deployment – SK PLT Tools 2.1.7.3-Beta

## Voraussetzungen

- Statischer Webserver mit HTTPS im Zielbetrieb; localhost ist für Tests zulässig.
- MIME-Typen für `.webmanifest`, `.json`, `.js`, `.css`, `.png`, `.pdf` und `.docx`.
- Service Worker muss im Projektstamm als `service-worker.js` erreichbar sein.

## Bereitstellung

1. Inhalt des Ordners `SK-PLT-Tools-V2.1.7.3-Beta/` vollständig in ein gemeinsames Webverzeichnis kopieren.
2. Keine Dateien aus `assets/`, `einheitendatenbank/`, `shared/` oder Rechnerordnern auslassen.
3. `manifest.webmanifest` und `service-worker.js` nicht umbenennen.
4. Anwendung einmal online öffnen, bis der Cache `sk-plt-tools-v2.1.7.3-Beta` installiert ist.
5. Einheitendatenbank und mindestens einen Rechner offline öffnen.

## Releaseprüfung

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
sha256sum -c SHA256SUMS.txt
```

Für Browser-/Responsive-Tests zusätzlich:

```bash
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
```

## Update von 2.1.7.2-Beta

Der neue Service Worker verwendet den Cache-Namen `sk-plt-tools-v2.1.7.3-Beta` und entfernt ältere `sk-plt-tools-*`-Caches bei Aktivierung. Seitenfavoriten (`skPltToolsFavoritesV2`) und Einheitenfavoriten (`skPltUnitFavoritesV1`) bleiben bestehen.

Geändert ist ausschließlich die Breitenlogik des Bereichs `.sk-unit-database-cta`: `width: 100%`, `max-width: 920px` und `box-sizing: border-box` lassen den Balken mit dem Rechner-Hauptbereich fluchten. Die mobile Stapelung bleibt erhalten. Der Herstellerlink `https://www.de.endress.com/de/onlinetools?store_locale=de` bleibt unverändert.

## Rollback

1. Vorherigen vollständigen Releaseordner erneut bereitstellen.
2. Seite online laden und Service Worker aktivieren lassen.
3. Bei hartnäckigem Clientcache Site-Daten löschen oder Anwendung neu installieren.

Einheitenfavoriten aus 2.1.7.3-Beta verwenden denselben Schlüssel wie 2.1.7.2-Beta; ein Rollback entfernt sie nicht aktiv.
