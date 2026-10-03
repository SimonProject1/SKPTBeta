# Architektur – SK PLT Tools Beta 2.0.5.1-Beta.1

## Leitprinzipien

1. Fachfunktionen bleiben als eigenständige Rechner- bzw. Wissensmodule erhalten.
2. Seitenübergreifende Darstellung und Laufzeitlogik werden zentral gepflegt.
3. Jede HTML-Seite bleibt ein direkter, statischer Einstiegspunkt.
4. Navigation, PWA und Offline-Betrieb funktionieren ohne Build-Server im produktiven Webroot.
5. Entfernt werden nur nachweislich unreferenzierte oder vollständig übernommene Altdateien.

## Zentrale Laufzeitdateien

- `assets/core.css` enthält die zuvor auf sechs Dateien verteilten gemeinsamen Styles für Grundlayout, Design, Favoriten, Suche/Filter, Sortierung und Seitenbaum.
- `assets/app.js` enthält Basisfunktionen, Service-Worker-Registrierung, Favoriten, Startseitensuche, Sortierung und Navigationsbaum.
- `assets/navigation-tree.json` ist die zentrale Inhaltsquelle für den Navigationsbaum. `assets/app.js` erzeugt daraus Gruppen, Knoten, Datei- und Externlinks.
- `assets/search-index.json` und `assets/materials.json` bleiben getrennte fachliche Datenquellen für Suche und Werkstoffe.

## Fachmodule

Eigene Dateien bleiben dort bestehen, wo sie fachliche Logik oder stark modulspezifische Darstellung kapseln:

- `assets/siemens-analogwert-rechner.{css,js}`
- `spannungsfall-rechner/calculator.{css,js}`
- `plausibilitaetspruefung-vde0100-600/checker.{css,js}`
- `assets/materials.{css,js,json}`
- Wissensbeitrags-Styles für Air Torque, Siemens Sitrans und Vacon

Damit bleiben Rechner und Wissensbeiträge klar getrennt, während globale Funktionen nicht mehrfach gepflegt werden.

## Gemeinsame Seitenelemente

`shared/header.html`, `shared/footer.html` und `shared/controls.html` sind die Vorlagen für die statisch ausgelieferten gemeinsamen Elemente. `shared/pages.json` enthält nur die seitenabhängigen Bezeichnungen und Rücksprungziele. `tools/sync_shared.py` synchronisiert die markierten Bereiche in allen 16 HTML-Seiten. Die ausgelieferten Seiten enthalten die Elemente weiterhin direkt, sodass Header, Footer und Schaltflächen bereits vor JavaScript sichtbar sind.

## PWA und Offline

- PWA-ID und Start-URL: `./?app=sk-plt-tools-beta-2.0.5.1-beta.1`
- Cache: `sk-plt-tools-beta-v2.0.5.1-Beta.1`
- `tools/release.py` erzeugt den Precache-Bestand automatisch aus den tatsächlich auslieferbaren Webdateien und direkten Seitenrouten.
- Navigationen nutzen Network-first mit Cache-Fallback; statische Assets nutzen Cache-first.
- Alte Beta-Caches mit gleichem Präfix werden bei Aktivierung entfernt; andere Anwendungen/Caches werden nicht berührt.

## Nachweislich entfernte Altdateien

Entfernt wurden 27 Dateien:

- 6 frühere gemeinsame CSS-Dateien, vollständig übernommen in `assets/core.css`
- 4 frühere gemeinsame JavaScript-Dateien, vollständig übernommen in `assets/app.js`
- 15 leere, unreferenzierte Kompatibilitäts-/Korrektur-Shims
- 1 unreferenziertes Logo-Fallback-Skript
- 1 unreferenzierte alte PDF-Dublette mit Doppelendung

Die aktive PDF-Beitragsvorlage und die DOCX-Quelldatei bleiben erhalten.

## Release-Automatisierung

`release-config.json` ist die zentrale Release-Konfiguration. `tools/release.py` aktualisiert Versionen in HTML, Manifest, App, Navigation und Service Worker, synchronisiert gemeinsame Seitenelemente, generiert die Offline-Liste, erstellt vollständige SHA-256-Prüfsummen und baut das komplette ZIP-Paket.
