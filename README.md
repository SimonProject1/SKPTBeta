# SK PLT Tools Beta 2.0.5.1-Beta.1

Vollständiges, statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. Dieser Stand basiert funktional auf **2.0.4.2-Beta.1** und optimiert ausschließlich Struktur, Wartbarkeit, Release-Erstellung und Prüfabdeckung. Die stabile Referenz **2.0.2.0** bleibt unverändert.

## Enthaltene Module

- Rechner: Analogsignal, Siemens Rohwert, P+F, Pt100/Pt1000, Einheiten und Spannungsfall
- Dokumentation: Messstellen-Dokumentation
- Prüfung: Plausibilitätsprüfung VDE 0100-600
- Wissen: Wissensdatenbank mit fünf Beiträgen, Werkstoff-Nachschlagewerk und Beitragsvorlagen
- Gemeinsame Funktionen: Suche, Filter, Sortierung, Favoriten, Seitenbaum, responsive Darstellung, PWA und Offline-Cache
- Direkter Bestandslink: `servicewerte/` bleibt für bestehende Direktaufrufe erhalten, ist aber weiterhin nicht auf der Startseite verlinkt

## Optimierte Struktur

- `assets/core.css`: alle seitenübergreifenden Styles in einer zentralen Datei
- `assets/app.js`: Basisfunktionen, Favoriten, Suche, Sortierung und Navigation in einer zentralen Datei
- `assets/navigation-tree.json`: einzige Inhaltsquelle des seitenweiten Navigationsbaums
- `shared/`: Vorlagen für Header, Footer und globale Bedienelemente sowie Seitenmetadaten
- `tools/sync_shared.py`: synchronisiert gemeinsame Seitenelemente in die statischen HTML-Dateien
- `release-config.json`: zentrale technische Release-Konfiguration
- `tools/release.py`: synchronisiert Version, Manifest, PWA-Precache und Seitenelemente, erzeugt SHA-256-Prüfsummen und baut das vollständige ZIP
- Rechner- und Wissensmodule behalten ihre fachlich getrennten CSS-/JavaScript-Dateien, sofern sie eigene Logik oder Darstellung benötigen

## Lokaler Start

```bash
python -m http.server 4173
```

Danach `http://127.0.0.1:4173/` öffnen. Für PWA- und Service-Worker-Prüfungen ist ein HTTP(S)-Ursprung erforderlich; ein direkter `file://`-Aufruf reicht dafür nicht.

## Prüfungen

```bash
node tools/functional-smoke-test.js
python tools/validate_release.py
python tools/browser-smoke-test.py
```

Der Browser-Test erwartet einen lokalen Server auf Port 4173. Alternativ kann der mitgelieferte Testhelfer oder ein eigener Serverprozess verwendet werden.

## Release bauen

```bash
python tools/release.py --version 2.0.5.1-Beta.1 --all
```

Der Befehl aktualisiert die technische Version, synchronisiert gemeinsame Seitenelemente und den Offline-Precache, erstellt `SHA256SUMS.txt` und schreibt ein vollständiges ZIP neben den Projektordner.

## Integrität

Im Projektordner:

```bash
sha256sum -c SHA256SUMS.txt
```

Weitere Details: `ARCHITEKTUR-CLEAN-DESIGN.md`, `DEPLOYMENT.md`, `RELEASE-NOTES.txt` und `TESTBERICHT-UND-ABNAHME.md`.
