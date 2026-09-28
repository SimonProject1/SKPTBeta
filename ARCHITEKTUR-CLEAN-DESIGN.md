# Clean-Design-Architektur 2.0.1.2

## Unveränderte Grundlage

Version 2.0.1.2 baut auf Version 2.0.1.1 und dem Clean-Design-Safepoint 2.0.0.0 auf. Die Grundprinzipien bleiben unverändert:

- finale Headerstruktur direkt in jeder HTML-Datei
- Version direkt unter dem Logo in jeder HTML-Datei
- einheitlicher Footer direkt in jeder HTML-Datei
- finale Startseitenkacheln sowie Filter- und Sortieroberfläche direkt in `index.html`
- verbindliche Gestaltung in `assets/styles.css` und `assets/design.css`
- JavaScript nur für echte Interaktionen und Berechnungen
- Service Worker ohne Response-Rewriting; nur Precache, Network-first für Navigation und Cache-Fallback
- alte Patch-Dateinamen ausschließlich als wirkungslose No-op-Kompatibilitätsdateien

## Brotkrümelnavigation in 2.0.1.2

Die Werkstoffseite verwendet jetzt dieselbe statische Navigationsstruktur wie die vorhandenen Wissensbeiträge:

- semantisches `nav` mit `aria-label="Brotkrümelnavigation"`
- Link `Startseite` auf `../../`
- Link `Wissensdatenbank` auf `../`
- aktueller, nicht verlinkter Eintrag `Werkstoff-Nachschlagewerk`
- Darstellung über die vorhandene Werkstoff-Stylesheet-Datei, optisch passend zu Air Torque und Siemens Sitrans P320
- keine neue JavaScript-Logik, keine Laufzeit-Patches und keine Änderung am Navigationsbaum

## Favoritenkorrektur aus 2.0.1.1

Die vorhandene Korrektur bleibt unverändert:

- Alle drei Links im Raster `#knowledgeGrid` sind als `knowledge-entry tool-card` gekennzeichnet.
- `assets/favorites.js` bleibt die einzige Favoritenlogik und verwendet unverändert `skPltToolsFavoritesV2` im Local Storage.
- Favoriten werden weiterhin zentral im linken Drawer gerendert und sind dadurch auf allen Seiten verfügbar.
- `preventDefault()` und `stopPropagation()` gelten nur für den Stern-Button; die umgebende Kachel bleibt ein normaler Link.
- Es wurden weder zusätzlicher Speicher noch parallele Favoritenlogik, Laufzeit-Patches oder Service-Worker-Umschreibungen eingeführt.

## Werkstoff-Nachschlagewerk

Das Werkstoff-Nachschlagewerk bleibt als reguläre Wissensseite integriert:

- statisches Seitenziel `wissensdatenbank/werkstoff-nachschlagewerk/index.html`
- Darstellung in `assets/materials.css`
- Interaktion in `assets/materials.js`
- zentrale Fachdaten, Filtergruppen, Quellen und Vergleiche in `assets/materials.json`
- Einbindung über Startseitensuche, Wissenskacheln, Favoritenlogik und Navigationsbaum
- statische Ressourcen im vorhandenen Service-Worker-Precache

## Sicherheitsprinzip

Jede gerenderte Werkstoffkarte und jeder Vergleich zeigt denselben Hinweis: Das Nachschlagewerk dient nur der Orientierung. Eine Freigabe erfordert die Prüfung von Norm, Zeugnis, Erzeugnisform, Zustand, Abmessung, Temperatur, Druck und Medium durch eine fachkundige Stelle. Das System erteilt keine automatische Werkstofffreigabe und keine pauschale Medienbeständigkeitsbewertung.
