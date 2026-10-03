# Deployment – SK PLT Tools Beta 2.0.5.1-Beta.1

## Voraussetzungen

- Statischer Webserver mit HTTPS für Produktion; `localhost` ist für lokale PWA-Tests zulässig
- Alle Dateien und Ordner des ZIP-Pakets unverändert gemeinsam bereitstellen
- Beta in einen eigenen Webroot entpacken und die stabile Version 2.0.2.0 nicht überschreiben

## Installation

1. `SK-PLT-Tools-V2.0.5.1-Beta.1.zip` entpacken.
2. Den enthaltenen Ordner vollständig auf den Ziel-Webserver kopieren.
3. Prüfen, dass `index.html`, `manifest.webmanifest`, `service-worker.js`, `assets/` und alle Modulordner unter demselben Webroot liegen.
4. Startseite und mindestens einen direkten Unterseitenlink ohne vorherigen Startseitenbesuch öffnen.
5. Bestehende Installation einmal online laden, bis der neue Service Worker aktiviert ist; anschließend Offline-Prüfung durchführen.

## Integritätsprüfung

Im Projektordner:

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

Der Browser-Test prüft Desktop, Tablet, Mobilansicht, Direktlinks, Navigation, Suche, Sortierung, Favoriten, Rechnerinteraktionen, PWA-Registrierung und Offline-Aufrufe.

## Update- und Rollback-Hinweise

- Der neue Cache heißt `sk-plt-tools-beta-v2.0.5.1-Beta.1`.
- Der Service Worker löscht nur ältere Caches mit dem Präfix `sk-plt-tools-beta-`.
- Ein Rollback erfolgt durch vollständiges Wiederherstellen des vorherigen Webroots. Danach die vorherige Version einmal online öffnen, damit deren Service Worker wieder aktiv wird.

## Neues Release erzeugen

```bash
python tools/release.py --version X.Y.Z.W-Beta.N --all
```

Vor der Weitergabe immer die drei Tests erneut ausführen und anschließend `SHA256SUMS.txt` sowie das ZIP neu erzeugen.
