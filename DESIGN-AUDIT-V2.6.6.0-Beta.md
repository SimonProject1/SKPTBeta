# Design-Audit V2.6.6.0-Beta

Stand: 18.10.2026  
Ergebnis: bestanden

## Navigationsarchitektur

- Wissensdatenbank: Hersteller → Gerät/Familie/Themenbereich → Beitrag.
- Werkstoffdatenbank: direkte Werkstoffkacheln → Detail.
- Keine Werkstoffgruppen-Zwischenebene.
- Sonstiges enthält keine erfundenen Fachinhalte.

## Iconsystem

- 39 aktive PNGs, 512 × 512 px, transparente Ränder.
- Herstellericons byteidentisch zur freigegebenen Basis.
- Zwischenebenen durch Gerätesilhouetten erkennbar.
- Beiträge durch Funktion/Diagnose erkennbar.
- Werkstoffe durch große Werkstoffnummer und gemeinsames Materialtemplate erkennbar.
- Reproduzierbar über `tools/generate_png_icons.py`.

## Responsive Raster

- Gemeinsame Variablen für Icongröße, Mindestbreite und Abstand.
- 320 px: zwei kompakte Spalten ohne horizontale Überbreite.
- 390 px: iPhone-lesbare Motive, Beschriftungen und Touchflächen.
- Tablet/Desktop: automatisch breiteres Raster und vollständige Breadcrumbs.
- Hover, Fokus, Touch und Aktivzustand bleiben ortsfest.

## Wissensbeiträge

- Hero- und Abschnittsrahmen reduziert.
- Schwarze Versatz- und Textschatten entfernt.
- Ruhige Oberflächen, dezente Cyan-/Grün-Akzente und kompakte Metadaten.
- Vorhandene Fachgrafiken, Warnungen, Quellen, SCO/SCC, PIN 2457, Rohwertdaten und Parameter 2.2.3.7 erhalten.
- Progressive einklappbare Fachdetails bleiben aktiv.

## Werkstoffdatenbank

- Zehn direkte Kacheln, große Werkstoffnummer im Icon.
- Vollständige Bezeichnung unter der Kachel.
- Direkte Detail-URL, Suche, Filter, Favoriten und Vergleich gleichzeitig erreichbar.
- Detailansicht erhält alle Datensätze, Warnungen und Quellen.

## Visuelle Nachweise

`tests/screenshots-v2660/` enthält 320-, 390-, Tablet- und Desktopaufnahmen sowie Zwischen-, Beitrags-, Detail- und Iconfamilien-Nachweise.
