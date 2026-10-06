# SK PLT Tools 2.1.0.2-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. Diese Beta basiert vollständig auf **2.1.0.1-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Enthaltene Module

- Rechner: Analogsignal, Siemens Rohwert, P+F, Pt100/Pt1000, Einheiten und Spannungsfall
- Dokumentation: Messstellen-Dokumentation
- Prüfung: Plausibilitätsprüfung VDE 0100-600 mit Foto-/PDF-Eingabe, formulargebundener Erkennung, Messwertregeln, sequentieller Klärung und grünem/rotem Abschluss
- Wissen: Wissensdatenbank mit fünf Beiträgen, Werkstoff-Nachschlagewerk und Beitragsvorlagen
- Gemeinsame Funktionen: Suche, Filter, Sortierung, Favoriten, Seitenbaum, responsive Darstellung, PWA und Offline-Cache
- Direkter Bestandslink: `servicewerte/` bleibt für bestehende Direktaufrufe erhalten, ist aber nicht auf der Startseite verlinkt

## Formulargebundene VDE-Prüfung

1. Ein oder mehrere Fotos oder PDFs des vom Nutzer bereitgestellten Prüfberichts laden.
2. PDF-Seiten werden mit der lokal enthaltenen PDF.js-Laufzeit gerendert; es erfolgt kein Upload.
3. Das Seitenformat und Linienraster werden mit den abgeleiteten Strukturmerkmalen des verbindlichen Prüfberichts Lfd. Nr. 12782 verglichen.
4. Formularfelder, Checkboxen, Prüfpunkt-Raster und Messwertzonen werden positionsbezogen zugeordnet. Eingebetteter PDF-Text und eine gegebenenfalls vorhandene lokale `TextDetector`-Schnittstelle ergänzen die Bildanalyse.
5. Vollständigkeit sowie Regeln für Isolationswiderstand, Durchgängigkeit, Schleifenimpedanz, Ib/In, Spannungsfall und RCD-Werte werden geprüft.
6. Unsichere, fehlende oder auffällige Angaben werden mit einem markierten Ausschnitt des hochgeladenen Protokolls nacheinander angeboten. Je Punkt sind Auswahl/Korrektur, „nicht relevant“ oder bei einer Abweichung „als n.i.O. bestätigen“ möglich.
7. Nach vollständiger Klärung erscheint ein grüner Haken für „Plausibel“ oder ein rotes X für „Nicht plausibel“.

Die leere Mustervorlage `VDEProtokoll.pdf` wird nicht ausgeliefert, nicht angezeigt und nicht zum Download angeboten. Im Projekt befinden sich ausschließlich abgeleitete Geometrie-, Feld- und Strukturmerkmale. In der Oberfläche wird nur das vom Nutzer hochgeladene Protokoll dargestellt.

Die Prüfung ist eine dokumentbezogene Zweitkontrolle und keine Inbetriebnahmefreigabe. Einzelheiten: `VDE0100-600-AUTOMATIK.md`.

## Projektstruktur

- `assets/core.css`: gemeinsame seitenübergreifende Styles
- `assets/app.js`: Basisfunktionen, Favoriten, Suche, Sortierung und Navigation
- `assets/vde0100-600-engine.js`: DOM-unabhängige Vollständigkeits- und Messwertlogik
- `assets/vde0100-600-template.json`: ausschließlich abgeleitete Formulargeometrie, Feldzuordnung, Strukturmerkmale und Prüfeinstellungen
- `assets/vde0100-600-rules.json`: dokumentierte Regeldefinitionen
- `plausibilitaetspruefung-vde0100-600/`: Oberfläche und lokale Dokumentenpipeline
- `vendor/pdfjs/`: lokal eingebundener PDF-Renderer einschließlich Lizenz
- `test-fixtures/vde0100-600/`: unveränderte Regressionstest-Fixture der Vorgängerversion; keine UI-Verknüpfung und keine Mustervorlage
- `assets/navigation-tree.json`: zentrale Inhaltsquelle des Navigationsbaums
- `shared/`: Vorlagen für Header, Footer, Bedienelemente und Seitenmetadaten
- `tools/`: Synchronisierung, Funktions-, Browser-, Release- und Integritätsprüfungen

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
python tools/release.py --version 2.1.0.2-Beta --all
```

Der Befehl synchronisiert Version, HTML, Laufzeitdaten, Manifest, Navigation und PWA-Cache, erzeugt den Offline-Precache, erstellt `SHA256SUMS.txt` und baut das vollständige ZIP. `stableBaseline` bleibt bei **2.1.0.0**.

## Integrität

```bash
sha256sum -c SHA256SUMS.txt
```
