# Architektur – SK PLT Tools 2.1.5.0-Beta

## Leitprinzipien

1. Statische, lokal ausführbare Webanwendung ohne serverseitige Abhängigkeit.
2. Gemeinsame Kopfzeile, Fußzeile, Favoriten- und Navigationssteuerung auf allen Seiten.
3. Responsive Verhalten wird zentral gepflegt und nicht als seitenweiser Patch dupliziert.
4. Rechenmodule, Dokumentation, Wissensinhalte und externe Dienste bleiben fachlich getrennt.
5. Release-Identität, Manifest, Service-Worker-Cache und Prüfsummen werden automatisiert synchronisiert.

## Siemens-Rohwert-Rechner

- `assets/siemens-analogwert-rechner.js` kapselt eine gemeinsame Berechnungslogik für Signal, Rohwert und physikalischen Wert.
- Drei ARIA-Reiter schalten ausschließlich die Eingabeart um; es existiert genau ein gemeinsames Vorgabefeld.
- Drei Ergebnisbausteine sind vorhanden, von denen stets nur die beiden nicht vorgegebenen Werte sichtbar sind.
- Kartenprofile, Signalbereiche, Messbereich und Diagnosegrenzen bleiben unabhängig von der aktiven Eingabeart synchron.
- Der Rohwertzustand wird semantisch über `data-state` an Eingabe, Ausgabekarte und Statuszeile ausgegeben; CSS ordnet die geprüften Farben zu.
- Nicht bestätigte Diagnosegrenzen erhalten ausschließlich den Zustand `scaleOnly` und Cyan; sie werden nicht als Unter-/Überlauf interpretiert.

## Responsive Anwendungsschale

- `assets/core.css` enthält die gemeinsame Oberfläche; `assets/responsive.css` enthält den responsiven Aufbau und wird auf allen Seiten nach den Modulstilen geladen.
- Smartphones bis 760 px erhalten einen sticky Header, einspaltige Karten, kompakte Seitentitel, mindestens 44 px große Touch-Ziele und Safe-Area-Abstände.
- Die beiden abgeleiteten Siemens-Werte bleiben gemäß Fachvorgabe auch mobil nebeneinander.
- Tablets von 761 bis 1024 px verwenden ein zweispaltiges Werkzeugraster und einen angepassten Hero.
- Favoriten und Baumnavigation bleiben auf Smartphones als 50 × 50 px große Schnellzugriffe in den unteren Viewport-Ecken fixiert.
- Beide Seitendrawer verwenden `100dvh`, eigene Safe-Area-Abstände und begrenztes Overscrolling.
- Querformat, Standalone-PWA und reduzierte Bewegung besitzen eigene zentrale Regeln.

## Laufzeit und Offlinebetrieb

- `assets/app.js` stellt globale Suche, Filter, Favoriten und Navigation bereit.
- Modulbezogene JavaScript- und CSS-Dateien bleiben in `assets/` oder im jeweiligen Modulordner.
- `service-worker.js` erzeugt den versionsgebundenen Offline-Cache `sk-plt-tools-v2.1.5.0-Beta`.
- `manifest.webmanifest` enthält die eindeutige App-ID und Release-Version.

## Qualitätssicherung

- `tools/functional-smoke-test.js` prüft Berechnungen, Reiterstruktur, Altoberflächen-Ausschluss und Inhaltsintegrationen.
- `tools/browser-smoke-test.py` prüft echte Reiterinteraktion, Diagnosefarben, 15 Direktseiten auf Desktop, Tablet und iPhone-Größen sowie Navigation, PWA und Offlinebetrieb.
- `tools/validate_release.py` prüft Seitenbestand, lokale Referenzen, Ausschlussregeln, JavaScript-Syntax, Versionskonsistenz, Responsive-Merkmale und Prüfsummen.
- `tools/release.py` erzeugt reproduzierbar Precache, Prüfsummen und ZIP-Paket.
