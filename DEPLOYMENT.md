# Deployment – SK PLT Tools 2.1.0.3-Beta

## Voraussetzungen

- statischer Webserver mit HTTPS oder localhost für Service Worker,
- korrekte MIME-Typen für `.webmanifest`, `.mjs`, `.json`, `.pdf`, `.png`, `.jpg` und `.webp`,
- keine serverseitige Anwendung erforderlich.

## Bereitstellung

1. `SK-PLT-Tools-V2.1.0.3-Beta.zip` entpacken.
2. Den einzigen Projektstamm `SK-PLT-Tools-V2.1.0.3-Beta/` unverändert unter dem Webroot bereitstellen.
3. Prüfen, dass `index.html`, `manifest.webmanifest`, `service-worker.js`, `assets/`, `vendor/` und alle Modulordner unter demselben Webroot liegen.
4. Keine reale ausgefüllte VDE-Testdatei in den Webroot kopieren.
5. Browserdaten einer älteren Beta bei Bedarf neu laden; der Service Worker löscht ältere `sk-plt-tools-*`-Caches automatisch.

## Release-Identität

- Version: `2.1.0.3-Beta`
- Manifest-ID/Start-URL: `./?app=sk-plt-tools-2.1.0.3-beta`
- Cache: `sk-plt-tools-v2.1.0.3-Beta`

## Vor Deployment ausführen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
```

Browser- und VDE-End-to-End-Tests benötigen einen lokalen Server und externe Testpfade:

```bash
export SK_VDE_REFERENCE_PDF=/sicherer/pfad/VDEProtokoll.pdf
export SK_VDE_FILLED_PDF=/sicherer/pfad/ausgefüllte-testdatei.pdf
python3 -m http.server 4173 --bind 127.0.0.1
```

Danach in einem zweiten Terminal:

```bash
python3 tools/browser-smoke-test.py
python3 tools/vde-protocol-e2e-test.py
```

## Rollback

Die stabile Referenz bleibt 2.1.0.0. Für einen Rollback den Webroot vollständig auf das gewünschte, separat geprüfte Paket zurücksetzen und bestehende `sk-plt-tools-*`-Caches im Browser löschen.
