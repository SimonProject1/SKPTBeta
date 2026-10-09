# Architektur – SK PLT Tools 2.1.2.1-Beta

## Leitprinzipien

1. Statische, lokal ausführbare Webanwendung ohne serverseitige Abhängigkeit.
2. Gemeinsame Kopfzeile, Fußzeile, Favoriten- und Navigationssteuerung auf allen Seiten.
3. Klare Trennung von Rechenmodulen, Dokumentation, Wissensinhalten und externen Diensten.
4. Release-Identität, Manifest, Service-Worker-Cache und Prüfsummen werden automatisiert synchronisiert.

## Laufzeit

- `assets/app.js` stellt globale Suche, Filter, Favoriten und Navigation bereit.
- Modulbezogene JavaScript- und CSS-Dateien bleiben in `assets/` oder im jeweiligen Modulordner.
- `assets/siemens-analogwert-rechner.js` kapselt Kartenprofile, Signalbereiche, Diagnosegrenzen und die lineare physikalische Skalierung. Rohwert, Signalwert und physikalischer Istwert werden auf den gemeinsamen Prozentanteil des Nennbereichs 0…27.648 abgebildet.
- `service-worker.js` erzeugt einen versionsgebundenen Offline-Cache.
- `manifest.webmanifest` enthält die eindeutige App-ID und Release-Version.

## Qualitätssicherung

- `tools/functional-smoke-test.js` prüft Berechnungen und Inhaltsintegrationen einschließlich negativer Messbereichsgrenzen, Einheiten sowie Unter- und Überbereich.
- `tools/browser-smoke-test.py` prüft Desktop, Tablet, Mobil, Navigation, Offline-Cache und PWA-Metadaten.
- `tools/validate_release.py` prüft Seitenbestand, lokale Referenzen, JavaScript-Syntax, Versionskonsistenz und Prüfsummen.
- `tools/release.py` erzeugt reproduzierbar Precache, Prüfsummen und ZIP-Paket.
