# Deployment – SK PLT Tools 2.1.7.0-Beta

## Voraussetzungen

- Statischer Webserver mit HTTPS im Zielbetrieb; localhost ist für Tests zulässig.
- MIME-Typen für `.webmanifest`, `.json`, `.js`, `.css`, `.png`, `.pdf` und `.docx`.
- Service Worker muss im Projektstamm `service-worker.js` erreichbar sein.

## Bereitstellung

1. Inhalt des Ordners `SK-PLT-Tools-V2.1.7.0-Beta/` vollständig in ein gemeinsames Webverzeichnis kopieren.
2. Keine Dateien aus `assets/`, `einheitendatenbank/`, `shared/` oder Rechnerordnern auslassen.
3. `manifest.webmanifest` und `service-worker.js` nicht umbenennen.
4. Anwendung einmal online öffnen, bis der Cache `sk-plt-tools-v2.1.7.0-Beta` installiert ist.
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

## Update von 2.1.6.1-Beta

Der neue Service Worker verwendet einen neuen Cache-Namen und entfernt ältere `sk-plt-tools-*`-Caches bei Aktivierung. Seitenfavoriten (`skPltToolsFavoritesV2`) bleiben bestehen. Einheitenfavoriten werden ab dieser Version getrennt unter `skPltUnitFavoritesV1` gespeichert.

## Rollback

1. Vorherigen vollständigen Releaseordner erneut bereitstellen.
2. Seite online laden und Service Worker aktivieren lassen.
3. Bei hartnäckigem Clientcache Site-Daten löschen oder Anwendung neu installieren.

Einheitenfavoriten aus 2.1.7.0-Beta werden von älteren Versionen ignoriert, aber nicht aktiv entfernt.
