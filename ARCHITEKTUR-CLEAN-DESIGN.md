# Architektur – SK PLT Tools 2.1.4.1-Beta

## Leitprinzipien

1. Statische, lokal ausführbare Webanwendung ohne serverseitige Abhängigkeit.
2. Gemeinsame Kopfzeile, Fußzeile, Favoriten- und Navigationssteuerung auf allen Seiten.
3. Responsive Verhalten wird zentral gepflegt und nicht als seitenweiser Patch dupliziert.
4. Rechenmodule, Dokumentation, Wissensinhalte und externe Dienste bleiben fachlich getrennt.
5. Release-Identität, Manifest, Service-Worker-Cache und Prüfsummen werden automatisiert synchronisiert.

## Responsive Anwendungsschale

- `assets/core.css` enthält die gemeinsame Oberfläche; `assets/responsive.css` enthält den neuen responsiven Aufbau und wird auf allen Seiten nach den Modulsstilen geladen.
- Smartphones bis 760 px erhalten einen sticky Header, einspaltige Karten, kompakte Seitentitel, mindestens 44 px große Touch-Ziele und Safe-Area-Abstände.
- Tablets von 761 bis 1024 px verwenden ein zweispaltiges Werkzeugraster und einen angepassten Hero.
- Favoriten und Baumnavigation bleiben auf Smartphones als 50 × 50 px große Schnellzugriffe in den unteren Viewport-Ecken fixiert.
- Beide Seitendrawer verwenden `100dvh`, eigene Safe-Area-Abstände und begrenztes Overscrolling.
- Querformat, Standalone-PWA und reduzierte Bewegung besitzen eigene zentrale Regeln.
- Desktopdarstellung oberhalb 1024 px behält den geprüften Aufbau der direkten Basis.

## Laufzeit

- `assets/app.js` stellt globale Suche, Filter, Favoriten und Navigation bereit.
- Modulbezogene JavaScript- und CSS-Dateien bleiben in `assets/` oder im jeweiligen Modulordner.
- `assets/siemens-analogwert-rechner.js` kapselt Kartenprofile, Signalbereiche, Diagnosegrenzen und die lineare physikalische Skalierung.
- `service-worker.js` erzeugt einen versionsgebundenen Offline-Cache.
- `manifest.webmanifest` enthält die eindeutige App-ID und Release-Version.

## Qualitätssicherung

- `tools/functional-smoke-test.js` prüft Berechnungen und Inhaltsintegrationen.
- `tools/browser-smoke-test.py` prüft 15 Direktseiten auf Desktop, Tablet und Mobil sowie Responsive-Shell, Touch-Ziele, Navigation, PWA und Offlinebetrieb.
- `tools/validate_release.py` prüft Seitenbestand, lokale Referenzen, Ausschlussregeln, JavaScript-Syntax, Versionskonsistenz, Responsive-Merkmale und Prüfsummen.
- `tools/release.py` erzeugt reproduzierbar Precache, Prüfsummen und ZIP-Paket.
