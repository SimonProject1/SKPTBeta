# SK PLT Tools 2.1.0.1-Beta

Vollständiges, statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. Diese Beta basiert vollständig auf der stabilen Version **2.1.0.0** und erweitert ausschließlich die Plausibilitätsprüfung VDE 0100-600 um eine lokale Dokumentenanalyse mit geführter Klärung.

## Enthaltene Module

- Rechner: Analogsignal, Siemens Rohwert, P+F, Pt100/Pt1000, Einheiten und Spannungsfall
- Dokumentation: Messstellen-Dokumentation
- Prüfung: Plausibilitätsprüfung VDE 0100-600 mit Foto-/PDF-Eingabe, automatischer Voranalyse, Messwertregeln, sequentieller Klärung und grünem/rotem Abschluss
- Wissen: Wissensdatenbank mit fünf Beiträgen, Werkstoff-Nachschlagewerk und Beitragsvorlagen
- Gemeinsame Funktionen: Suche, Filter, Sortierung, Favoriten, Seitenbaum, responsive Darstellung, PWA und Offline-Cache
- Direkter Bestandslink: `servicewerte/` bleibt für bestehende Direktaufrufe erhalten, ist aber nicht auf der Startseite verlinkt

## Neue VDE-Dokumentenprüfung

1. Ein oder mehrere Fotos oder PDFs laden.
2. PDFs werden mit der lokal enthaltenen PDF.js-Laufzeit gerendert; es erfolgt kein Upload.
3. Eingebetteter PDF-Text, eine gegebenenfalls im Browser vorhandene lokale TextDetector-Schnittstelle, Formularlayout und Dokumentfingerabdruck werden ausgewertet.
4. Das Muster `test-fixtures/vde0100-600/228_SR4_K06_E07.1.pdf` ist über SHA-256 eindeutig mit dem hinterlegten Formularprofil verknüpft.
5. Vollständigkeit sowie hinterlegte Regeln für Isolationswiderstand, Schleifenimpedanz, Ib/In, Spannungsfall und RCD-Werte werden automatisch geprüft.
6. Unsichere, fehlende oder auffällige Angaben werden nacheinander angeboten. Je Punkt kann eine Korrektur/Auswahl, „nicht relevant“ oder bei einer Abweichung „als n.i.O. bestätigen“ gewählt werden.
7. Nach vollständiger Klärung erscheint ein grüner Haken für „Plausibel“ oder ein rotes X für „Nicht plausibel“.

Die Prüfung ist eine dokumentbezogene Zweitkontrolle und keine Inbetriebnahmefreigabe. Einzelheiten: `VDE0100-600-AUTOMATIK.md`.

## Projektstruktur

- `assets/core.css`: gemeinsame seitenübergreifende Styles
- `assets/app.js`: Basisfunktionen, Favoriten, Suche, Sortierung und Navigation
- `assets/vde0100-600-engine.js`: testbare Fachlogik der Dokumentenprüfung
- `assets/vde0100-600-template.json`: Formularschema, Musterfingerabdruck, Layoutzonen und Prüfeinstellungen
- `plausibilitaetspruefung-vde0100-600/`: Oberfläche und Dokumentenpipeline
- `vendor/pdfjs/`: lokal eingebundener PDF-Renderer einschließlich Lizenz
- `test-fixtures/vde0100-600/`: unverändertes Musterprotokoll
- `assets/navigation-tree.json`: zentrale Inhaltsquelle des Navigationsbaums
- `shared/`: Vorlagen für Header, Footer, Bedienelemente und Seitenmetadaten
- `tools/sync_shared.py`: Synchronisierung gemeinsamer Seitenelemente
- `release-config.json`: zentrale Release-Konfiguration
- `tools/release.py`: Versions-, Manifest-, PWA-, Prüfsummen- und ZIP-Erstellung; unterstützt Release und Beta

## Lokaler Start und Prüfungen

```bash
python -m http.server 4173
# in weiteren Terminals:
node tools/functional-smoke-test.js
python tools/validate_release.py
python tools/browser-smoke-test.py
```

Für PWA-, PDF-Worker- und Service-Worker-Prüfungen ist HTTP(S) erforderlich; ein direkter `file://`-Aufruf reicht nicht.

## Release bauen

```bash
python tools/release.py --version 2.1.0.1-Beta --all
```

Der Befehl synchronisiert Version, HTML, Laufzeitdaten, Manifest, Navigation und PWA-Cache, erzeugt den Offline-Precache, erstellt `SHA256SUMS.txt` und baut das vollständige ZIP neben dem Projektordner. `stableBaseline` bleibt bei einer Beta auf der stabilen Version 2.1.0.0.

## Integrität

```bash
sha256sum -c SHA256SUMS.txt
```
