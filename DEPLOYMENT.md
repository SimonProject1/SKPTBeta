# Deployment – SK PLT Tools 2.1.0.1-Beta

## Voraussetzungen

- Statischer Webserver mit HTTPS für Produktion; `localhost` ist für lokale PWA-Tests zulässig
- Alle Dateien und Ordner des ZIP-Pakets unverändert gemeinsam bereitstellen
- MIME-Typen für `.mjs` (`text/javascript`), `.json`, `.pdf` und `.wasm` zulassen
- Vor dem Austausch des produktiven Webroots eine Sicherung der bestehenden Installation erstellen

## Installation

1. `SK-PLT-Tools-V2.1.0.1-Beta.zip` entpacken.
2. Den enthaltenen Ordner vollständig auf den Ziel-Webserver kopieren.
3. Prüfen, dass `index.html`, `manifest.webmanifest`, `service-worker.js`, `assets/`, `vendor/`, `test-fixtures/` und alle Modulordner unter demselben Webroot liegen.
4. Startseite und `plausibilitaetspruefung-vde0100-600/` direkt öffnen.
5. In der VDE-Prüfung „Muster laden“ wählen und den automatischen Ablauf bis zur geführten Klärung prüfen.
6. Die Anwendung einmal online laden, bis der neue Service Worker aktiviert ist; danach die Offline-Prüfung durchführen.

## Integritätsprüfung

```bash
sha256sum -c SHA256SUMS.txt
```

Alle Einträge müssen `OK` melden.

## Technische Abnahme

```bash
node tools/functional-smoke-test.js
python tools/validate_release.py
python -m http.server 4173
# in einem zweiten Terminal:
python tools/browser-smoke-test.py
```

Der Browser-Test prüft Desktop, Tablet, Mobilansicht, Direktlinks, Navigation, Suche, Sortierung, Favoriten, Rechnerinteraktionen, VDE-Musteranalyse, PDF-Rendering, Klärungsablauf, PWA-Registrierung und Offline-Aufrufe.

## Update und Rollback

- Der neue Cache heißt `sk-plt-tools-v2.1.0.1-Beta`.
- Der Service Worker entfernt ältere Caches mit dem Präfix `sk-plt-tools-`; andere Anwendungen und Caches bleiben unberührt.
- Ein Rollback erfolgt durch vollständiges Wiederherstellen des Webroots von 2.1.0.0. Danach die stabile Version einmal online öffnen, damit deren Service Worker wieder aktiv wird.

## Neues Release erzeugen

```bash
python tools/release.py --version X.Y.Z.W-Beta --all
```

Vor der Weitergabe immer die drei Tests erneut ausführen und anschließend `SHA256SUMS.txt` sowie das ZIP neu erzeugen.
