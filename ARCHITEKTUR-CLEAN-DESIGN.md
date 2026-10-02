# Clean-Design-Architektur 2.0.3.5-Beta.2

## Unveränderte Grundlage

Version 2.0.3.5-Beta.2 führt die vorhandene Beta-Linie auf Basis der unveränderten stabilen Version 2.0.2.0 fort. Die Grundprinzipien bleiben erhalten:

- finale Headerstruktur direkt in jeder HTML-Datei
- Version direkt unter dem Logo in jeder HTML-Datei
- einheitlicher Footer direkt in jeder HTML-Datei
- statische Startseitenkacheln sowie Filter- und Sortieroberfläche in `index.html`
- verbindliche Gestaltung in `assets/styles.css` und `assets/design.css`
- JavaScript nur für Interaktion und Berechnung
- Service Worker ohne Response-Rewriting; Precache, Network-first für Navigation und Cache-Fallback
- alte Patch-Dateien ausschließlich als wirkungslose No-op-Kompatibilitätsdateien

## Siemens-SPS-Analogwert-Rechner

Der Rechner bleibt als reguläres Werkzeug vollständig in die Anwendung eingebunden:

- Seite `siemens-analogwert-rechner/index.html`
- Gestaltung `assets/siemens-analogwert-rechner.css`
- Berechnung `assets/siemens-analogwert-rechner.js`
- Startseitenkachel, Favoritenfähigkeit und Navigationsbaumeintrag bleiben bestehen
- Seite und Assets verbleiben im Service-Worker-Precache
- keine eigene Persistenz und keine Laufzeit-Patchlogik

Die Fachlogik ist bewusst auf zwei Größen begrenzt: Siemens-Rohwert und ausgewähltes mA-/V-Signal. Die vier Signalbereiche sind als unveränderliche Konfigurationen hinterlegt. Die Statusfunktion ordnet jeden Rohwert genau einem der fünf Zustände Unterlauf, Unterbereich, Nennbereich, Überbereich oder Überlauf zu.

Der Schieberegler arbeitet über den vollständigen INT16-Bereich und ist bidirektional an Eingabefeld und Ergebnisdarstellung gekoppelt. Manuelle Eingaben außerhalb des Reglerbereichs bleiben möglich und werden als Unterlauf beziehungsweise Überlauf gekennzeichnet.

## Beta-Konfiguration

- Kanal: `beta`
- PWA-ID/start_url: `./?app=sk-plt-tools-beta-2.0.3.5-beta.2`
- Cache-Präfix: `sk-plt-tools-beta-`
- Release-Cache: `sk-plt-tools-beta-v2.0.3.5-Beta.2`
- Cache-Bereinigung greift ausschließlich innerhalb des Beta-Präfixes

## Erhaltene Systeme

- Favoriten mit dem bestehenden Local-Storage-Schlüssel `skPltToolsFavoritesV2`
- Startseitenfilter und Sortierung
- zentrale Suche und Werkstoffkatalog
- Navigationsbaum
- Wissensdatenbank einschließlich Vorlagen
- responsive Layoutregeln und mobile Drawer

## Sicherheitsprinzip

Die dargestellten Bereichsgrenzen sind ein Rechen- und Diagnosemodell. Baugruppenabhängige Mess-, Diagnose- und NE43-Grenzen werden nicht ersetzt; die Dokumentation und Parametrierung des eingesetzten Siemens-Moduls bleibt maßgeblich.

## Kompaktierungsrelease Beta.2

Die bestehende Farb-, Typografie-, Karten- und Navigationssprache bleibt unverändert. Beta.2 reduziert ausschließlich Größen und vertikale Abstände in den bestehenden Stylesheets. Karteninformationen des Siemens-Rechners verwenden ein natives `details`/`summary`-Element; Berechnungs- und Persistenzlogik bleiben unverändert.
