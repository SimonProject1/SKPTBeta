# Clean-Design-Architektur 2.0.4.2-Beta.1

## Unveränderte Grundlage

Version 2.0.4.2-Beta.1 führt die vorhandene Beta-Linie auf Basis der unveränderten stabilen Version 2.0.2.0 fort. Die Grundprinzipien bleiben erhalten:

- finale Headerstruktur direkt in jeder HTML-Datei
- sichtbare Versionsanzeige ausschließlich im Hero der Startseite
- einheitlicher Footer direkt in jeder HTML-Datei
- statische Startseitenkacheln sowie Filter- und Sortieroberfläche in `index.html`
- verbindliche Gestaltung in `assets/styles.css` und `assets/design.css`
- JavaScript nur für Interaktion und Berechnung
- Service Worker ohne Response-Rewriting; Precache, Network-first für Navigation und Cache-Fallback
- alte Patch-Dateien ausschließlich als wirkungslose No-op-Kompatibilitätsdateien

## Navigationsbaum

Die Navigation wird aus `assets/navigation-tree.json` durch `assets/navigation-tree.js` erzeugt und durch `assets/navigation-tree.css` gestaltet.

Knoten mit Untereinträgen verwenden eine semantisch gültige Struktur:

- `.sk-tree-node-row` bildet die gemeinsame dunkelblaue, abgerundete Kachel.
- `.sk-tree-node-toggle` ist eine eigenständige 42-px-Pfeilschaltfläche mit `aria-expanded` und `aria-controls`.
- `.sk-tree-link` liegt als Geschwisterelement neben der Schaltfläche und bleibt vollständig innerhalb der Kachel.
- Links werden nie in Buttons verschachtelt. Dadurch kann der HTML-Parser den Link nicht aus der vorgesehenen Knoten-Kachel verschieben.
- Der Pfeil wird per Grid-Zentrierung optisch mittig ausgerichtet; Hover, Fokus und Aktivzustand gelten für die vollständige Knoten-Zeile.

## Siemens-SPS-Analogwert-Rechner

Der Rechner bleibt als reguläres Werkzeug vollständig in die Anwendung eingebunden:

- Seite `siemens-analogwert-rechner/index.html`
- Gestaltung `assets/siemens-analogwert-rechner.css`
- Berechnung `assets/siemens-analogwert-rechner.js`
- Startseitenkachel, Favoritenfähigkeit und Navigationsbaumeintrag bleiben bestehen
- Seite und Assets verbleiben im Service-Worker-Precache
- keine eigene Persistenz und keine Laufzeit-Patchlogik

Die Fachlogik ist bewusst auf zwei Größen begrenzt: Siemens-Rohwert und ausgewähltes mA-/V-Signal. Die vier Signalbereiche sind als unveränderliche Konfigurationen hinterlegt. Die Statusfunktion ordnet jeden Rohwert genau einem der fünf Zustände Unterlauf, Unterbereich, Nennbereich, Überbereich oder Überlauf zu.

## Beta-Konfiguration

- Kanal: `beta`
- PWA-ID/start_url: `./?app=sk-plt-tools-beta-2.0.4.2-beta.1`
- Cache-Präfix: `sk-plt-tools-beta-`
- Release-Cache: `sk-plt-tools-beta-v2.0.4.2-Beta.1`
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
