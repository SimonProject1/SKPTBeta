# Architektur – SK PLT Tools 2.1.0.2-Beta

## Leitprinzipien

1. Der vollständige Funktionsumfang der direkten Basis 2.1.0.1-Beta bleibt erhalten; stabile Referenz ist 2.1.0.0.
2. Fachfunktionen bleiben als eigenständige Rechner-, Prüf- oder Wissensmodule gekapselt.
3. Jede HTML-Seite bleibt ein direkter, statischer Einstiegspunkt.
4. Navigation, PWA und Offline-Betrieb funktionieren ohne Build-Server im produktiven Webroot.
5. Dokumente der VDE-Prüfung werden ausschließlich lokal im Browser verarbeitet.
6. Die verbindliche leere VDE-Mustervorlage wird nicht ausgeliefert. Nur nicht rückwärts als PDF nutzbare Feld-, Linien- und Strukturmetadaten sind Bestandteil des Projekts.

## Zentrale Laufzeitdateien

- `assets/core.css`: Grundlayout, Design, Favoriten, Suche/Filter, Sortierung und Seitenbaum
- `assets/app.js`: Basisfunktionen, Service Worker, Favoriten, Suche, Sortierung und Navigation
- `assets/navigation-tree.json`: zentrale Inhaltsquelle der Navigation
- `assets/search-index.json` und `assets/materials.json`: fachliche Datenquellen für Suche und Werkstoffe

## VDE-Dokumentenpipeline

- `plausibilitaetspruefung-vde0100-600/checker.js`: Eingabe, SHA-256, PDF-/Bildaufbereitung, Ausrichtung, Strukturvergleich, Checkbox-/Feldanalyse, Vorschau des Nutzeruploads, Klärungsworkflow und Ergebnis
- `plausibilitaetspruefung-vde0100-600/checker.css`: responsive industrielle Oberfläche einschließlich Originalausschnitt im Klärungsdialog
- `assets/vde0100-600-engine.js`: DOM-unabhängige Vollständigkeits- und Messwertlogik
- `assets/vde0100-600-template.json`: abgeleitete Geometrie mit 33 Linienankern und 93 Feldzuordnungen, Mustervorlagen-Fingerabdruck nur als Herkunftsnachweis, Prüfeinstellungen und Regelübersicht
- `assets/vde0100-600-rules.json`: dokumentierte fachliche Regeldefinitionen
- `vendor/pdfjs/`: lokal eingebettete PDF.js-Laufzeit 5.4.296 und Lizenz

Erkennungsreihenfolge: Seitenrendering und Ausrichtung → Linienraster/Formularpassung → Checkboxen und visuelle Feldbelegung → eingebetteter PDF-Text beziehungsweise optionale lokale Browser-Texterkennung → geführte Bestätigung. Nicht sicher erkannte Werte bleiben offen und werden nicht erfunden.

## Datenschutz- und Sichtbarkeitsgrenze

Die Referenz-PDF `VDEProtokoll.pdf` ist weder im Projektbestand noch im Service-Worker-Precache enthalten. Die Anwendung bietet keinen Musterlade- oder Musterdownload-Link. Jede Canvas-Vorschau und jeder Feldkontext wird erst aus der aktuell vom Nutzer ausgewählten Datei erzeugt.

## Gemeinsame Seitenelemente

`shared/header.html`, `shared/footer.html` und `shared/controls.html` sind Vorlagen der statisch ausgelieferten Elemente. `shared/pages.json` enthält seitenabhängige Bezeichnungen und Rücksprungziele. `tools/sync_shared.py` synchronisiert die markierten Bereiche in allen 16 HTML-Seiten.

## PWA und Offline

- PWA-ID und Start-URL: `./?app=sk-plt-tools-2.1.0.2-beta`
- Cache: `sk-plt-tools-v2.1.0.2-Beta`
- Das Release-Skript erzeugt den Precache aus dem tatsächlichen Webbestand.
- Navigationen verwenden Network-first mit Cache-Fallback; statische Assets Cache-first.
- Ältere SK-PLT-Tools-Caches werden versionsbezogen entfernt.

## Release-Automatisierung

`release-config.json` hält Beta-Version und stabile Basis getrennt. `tools/release.py` synchronisiert Laufzeitquellen, HTML, Manifest, Navigation und Service Worker, erzeugt die Offline-Liste sowie vollständige SHA-256-Prüfsummen und baut das ZIP-Paket.
