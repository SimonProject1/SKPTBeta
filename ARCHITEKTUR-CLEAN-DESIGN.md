# Architektur – SK PLT Tools 2.1.6.1-Beta

## Leitprinzipien

1. Statische, lokal ausführbare Webanwendung ohne serverseitige Abhängigkeit.
2. Gemeinsame Kopfzeile, Fußzeile, Favoriten- und Navigationssteuerung auf allen Seiten.
3. Responsive Verhalten und Rechnergestaltung werden zentral gepflegt und nicht als seitenweise Patches dupliziert.
4. Rechenmodule, Dokumentation, Wissensinhalte und externe Dienste bleiben fachlich getrennt.
5. Designänderungen dürfen die bestehende Berechnungslogik nicht verändern.
6. Release-Identität, Manifest, Service-Worker-Cache, Precache und Prüfsummen werden automatisiert synchronisiert.

## Rechner-Designsystem

- Der Siemens-Rohwert-Rechner aus 2.1.5.2-Beta ist die visuelle Referenz.
- `assets/rechner-unified.css` überträgt die Referenzsprache auf Analogsignal, Einheiten, P+F, Pt100/Pt1000 und Spannungsfall.
- Gemeinsame Bausteine:
  - `.calc-page-title` für Seitenüberschrift und Einleitung,
  - `.calc-panel` und `.calc-panel-title` für die Rechnerkarte,
  - `.calc-field-grid` und `.calc-field-card` für Eingaben,
  - `.calc-result-grid` und `.calc-value-card` für Ergebnisse,
  - `.calc-actions` für Primär- und Sekundäraktionen,
  - `.voltage-result` für die umfangreichere Spannungsfall-Ausgabe.
- Farben, Radien, Typografie, Monospace-Zahlen, Abstände, Fokuszustände und mobile Touchgrößen leiten sich aus den vorhandenen Siemens-Variablen und -Werten ab.
- `assets/rechner-unified.css` wird auf jeder der fünf Seiten genau einmal nach `core.css` und vor der abschließenden `responsive.css` geladen.
- Jedes `input[type="number"]` der sechs Rechner verwendet explizit `inputmode="decimal"` oder `inputmode="numeric"`, damit mobile Browser die Zahlentastatur statt der vollständigen Texteingabetastatur anfordern.

## Logiktrennung

- Die Inline-Skripte von Analogsignal, Einheiten, P+F und Pt100/Pt1000 bleiben unverändert.
- `spannungsfall-rechner/calculator.js` bleibt unverändert.
- `assets/siemens-analogwert-rechner.js` bleibt unverändert.
- `test-artifacts/logic-baseline-source.json` enthält die SHA-256-Quellhashes aus 2.1.5.2-Beta.
- `tools/validate_release.py` extrahiert die aktuellen Inline-Skripte beziehungsweise liest die externen JavaScript-Dateien und vergleicht sie bitgenau mit der Baseline.

## Siemens-Rohwert-Rechner

- `assets/siemens-analogwert-rechner.js` kapselt die gemeinsame Berechnungslogik für Signal, Rohwert und physikalischen Wert.
- Drei ARIA-Reiter schalten ausschließlich die Eingabeart um; es existiert genau ein gemeinsames Vorgabefeld.
- Drei statische ±-Buttons sind dem Vorgabefeld sowie Messbereichsminimum und -maximum zugeordnet.
- Drei Ergebnisbausteine sind vorhanden, von denen stets nur die beiden nicht vorgegebenen Werte sichtbar sind.
- Kartenprofile, Signalbereiche, Messbereich und Diagnosegrenzen bleiben unabhängig von der aktiven Eingabeart synchron.
- Der Rohwertzustand wird semantisch über `data-state` an Eingabe, Ausgabekarte und Statuszeile ausgegeben.

## Responsive Anwendungsschale

- `assets/core.css` enthält die gemeinsame Oberfläche; `assets/responsive.css` enthält den responsiven Aufbau und wird auf allen Seiten zuletzt geladen.
- Smartphones bis 760 px erhalten einen sticky Header, einspaltige Rechnerfelder, kompakte Seitentitel, mindestens 44 px große Touchziele und Safe-Area-Abstände.
- Favoriten und Baumnavigation bleiben als 50 × 50 px große Schnellzugriffe in den unteren Viewport-Ecken fixiert.
- `html` und `body` verwenden eine dunkle Grundfläche, damit iPhone-Status- und Safe-Areas keinen hellen Streifen zeigen.
- Der mobile Header spannt sich über die gesamte Viewportbreite; die Trennlinie und der rechtsbündige Startseiten-Button bleiben unverändert ausgerichtet.
- Tablets von 761 bis 1024 px verwenden angepasste zwei- beziehungsweise dreispaltige Rechnerfelder.
- Beide Seitendrawer verwenden `100dvh`, eigene Safe-Area-Abstände und begrenztes Overscrolling.
- Querformat, Standalone-PWA und reduzierte Bewegung besitzen eigene zentrale Regeln.

## Laufzeit und Offlinebetrieb

- `assets/app.js` stellt globale Basisfunktionen, Favoriten, Suche, Filter, Sortierung und Navigation bereit.
- `service-worker.js` erzeugt den versionsgebundenen Offline-Cache `sk-plt-tools-v2.1.6.1-Beta` und enthält `assets/rechner-unified.css` im Precache.
- `manifest.webmanifest` enthält die eindeutige App-ID `./?app=sk-plt-tools-2.1.6.1-beta` und Release-Version.
- Ältere `sk-plt-tools-*`-Caches werden bei Aktivierung des neuen Service Workers entfernt.

## Qualitätssicherung

- `tools/functional-smoke-test.js` prüft Rechnerergebnisse, Siemens-Reiterstruktur, Grenzfälle und Inhaltsintegrationen.
- `tools/browser-smoke-test.py` prüft alle fünf umgestalteten Rechner und die Siemens-Referenz auf Desktop, Tablet und iPhone-Touchprofil, einschließlich der mobilen Tastaturattribute, erzeugt Screenshots und testet zusätzlich Navigation, PWA und Offlinebetrieb.
- `tools/validate_release.py` prüft Seitenbestand, gemeinsame Rechnerstruktur, sämtliche Rechner-Zahlenfelder, Logik-Baseline, lokale Referenzen, JavaScript-Syntax, Versionskonsistenz, Responsive-Merkmale und Prüfsummen.
- `tools/release.py` erzeugt reproduzierbar Precache, Prüfsummen und ZIP-Paket.
