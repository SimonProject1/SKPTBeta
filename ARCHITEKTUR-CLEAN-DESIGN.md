# Clean-Design-Architektur 2.0.2.0

## Unveränderte Grundlage

Version 2.0.2.0 baut auf Version 2.0.1.2 und dem Clean-Design-Safepoint 2.0.0.0 auf. Die Grundprinzipien bleiben unverändert:

- finale Headerstruktur direkt in jeder HTML-Datei
- Version direkt unter dem Logo in jeder HTML-Datei
- einheitlicher Footer direkt in jeder HTML-Datei
- finale Startseitenkacheln sowie Filter- und Sortieroberfläche direkt in `index.html`
- verbindliche Gestaltung in `assets/styles.css` und `assets/design.css`
- JavaScript nur für echte Interaktionen und Berechnungen
- Service Worker ohne Response-Rewriting; nur Precache, Network-first für Navigation und Cache-Fallback
- alte Patch-Dateinamen ausschließlich als wirkungslose No-op-Kompatibilitätsdateien

## Vacon-Wissensbeitrag in 2.0.2.0

Der neue Beitrag wird wie die vorhandenen Wissensseiten statisch integriert:

- Seitenziel `wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html`
- responsives Beitragslayout in `assets/vacon-wissen.css`
- statische Brotkrümelnavigation zu Startseite und Wissensdatenbank
- Wissenskachel als `knowledge-entry tool-card` für das bestehende Favoritensystem
- Eintrag in `assets/search-index.json` für Startseitensuche und Suchbegriffe
- Eintrag in `assets/navigation-tree.json`
- Seite und Stylesheet im Service-Worker-Precache
- keine neue Laufzeit-Patchlogik und kein neuer Persistenzmechanismus

## Favoriten

- Alle vier Links im Raster `#knowledgeGrid` sind als `knowledge-entry tool-card` gekennzeichnet.
- `assets/favorites.js` bleibt die einzige Favoritenlogik und verwendet unverändert `skPltToolsFavoritesV2` im Local Storage.
- Favoriten werden weiterhin zentral im linken Drawer gerendert und sind dadurch auf allen Seiten verfügbar.
- `preventDefault()` und `stopPropagation()` gelten nur für den Stern-Button; die umgebende Kachel bleibt ein normaler Link.

## Werkstoff-Nachschlagewerk

Das Werkstoff-Nachschlagewerk bleibt unverändert als reguläre Wissensseite integriert:

- statisches Seitenziel `wissensdatenbank/werkstoff-nachschlagewerk/index.html`
- Darstellung in `assets/materials.css`
- Interaktion in `assets/materials.js`
- zentrale Fachdaten, Filtergruppen, Quellen und Vergleiche in `assets/materials.json`
- Einbindung über Startseitensuche, Wissenskacheln, Favoritenlogik und Navigationsbaum
- statische Ressourcen im vorhandenen Service-Worker-Precache

## Sicherheitsprinzip

Der Vacon-Beitrag ist als praktischer Prüfhinweis formuliert. Vor Parameteränderungen sind Herstellerdokumentation, Gerätestand sowie Motor-, Anlagen- und Inbetriebnahmevorgaben zu prüfen. Das Werkstoff-Nachschlagewerk erteilt weiterhin keine automatische Werkstofffreigabe und keine pauschale Medienbeständigkeitsbewertung.
