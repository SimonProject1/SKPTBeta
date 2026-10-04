# Architektur – SK PLT Tools 2.1.0.1-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der stabilen Basis 2.1.0.0 bleibt erhalten.
2. Fachfunktionen bleiben als eigenständige Rechner-, Prüf- oder Wissensmodule gekapselt.
3. Jede HTML-Seite bleibt ein direkter, statischer Einstiegspunkt.
4. Navigation, PWA und Offline-Betrieb funktionieren ohne Build-Server im produktiven Webroot.
5. Dokumente der VDE-Prüfung werden ausschließlich lokal im Browser verarbeitet.

## Zentrale Laufzeitdateien

- `assets/core.css`: Grundlayout, Design, Favoriten, Suche/Filter, Sortierung und Seitenbaum
- `assets/app.js`: Basisfunktionen, Service Worker, Favoriten, Suche, Sortierung und Navigation
- `assets/navigation-tree.json`: zentrale Inhaltsquelle der Navigation
- `assets/search-index.json` und `assets/materials.json`: fachliche Datenquellen für Suche und Werkstoffe

## VDE-Dokumentenpipeline

- `plausibilitaetspruefung-vde0100-600/checker.js`: Eingabe, SHA-256, PDF-/Bildaufbereitung, Erkennungsorchestrierung, Vorschau, Klärungsworkflow und Ergebnis
- `plausibilitaetspruefung-vde0100-600/checker.css`: eigenständige responsive Oberfläche
- `assets/vde0100-600-engine.js`: DOM-unabhängige Vollständigkeits- und Messwertlogik
- `assets/vde0100-600-template.json`: Formulartyp, Layoutzonen, Musterfingerabdruck, Prüfeinstellungen und Referenzwerte
- `vendor/pdfjs/`: lokal eingebettete PDF.js-Laufzeit 5.4.296 und Lizenz
- `test-fixtures/vde0100-600/228_SR4_K06_E07.1.pdf`: unveränderter Muster-Testfall

Erkennungsreihenfolge: bekannter Dokumentfingerabdruck → eingebetteter PDF-Text → optionale lokale Browser-TextDetector-Schnittstelle → formularbezogene visuelle Layoutanalyse. Nicht sicher erkannte Werte bleiben offen und werden nicht erfunden.

## Fachmodule

Eigene Dateien bleiben dort bestehen, wo sie Fachlogik oder modulspezifische Darstellung kapseln, darunter Siemens-Rohwert, Spannungsfall, VDE-Prüfung, Werkstoffe und Wissensbeiträge.

## Gemeinsame Seitenelemente

`shared/header.html`, `shared/footer.html` und `shared/controls.html` sind Vorlagen der statisch ausgelieferten Elemente. `shared/pages.json` enthält seitenabhängige Bezeichnungen und Rücksprungziele. `tools/sync_shared.py` synchronisiert die markierten Bereiche in allen 16 HTML-Seiten.

## PWA und Offline

- PWA-ID und Start-URL: `./?app=sk-plt-tools-2.1.0.1-beta`
- Cache: `sk-plt-tools-v2.1.0.1-Beta`
- Das Release-Skript erzeugt den Precache aus dem tatsächlichen Webbestand einschließlich PDF-Renderer und Musterformular.
- Navigationen verwenden Network-first mit Cache-Fallback; statische Assets Cache-first.
- Ältere SK-PLT-Tools-Caches werden versionsbezogen entfernt.

## Release-Automatisierung

`release-config.json` hält Beta-Version und stabile Basis getrennt. `tools/release.py` akzeptiert `X.Y.Z.W` und `X.Y.Z.W-Beta[.N]`, synchronisiert technische Laufzeitquellen, HTML, Manifest, App, Navigation und Service Worker, erzeugt Offline-Liste sowie vollständige SHA-256-Prüfsummen und baut das ZIP-Paket.
