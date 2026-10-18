# Design-Audit – SK PCT Tools V2.6.5.3-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.2-Beta  
Visuelle Referenz: harmonische Einbettung der V2.6.5.1-Beta

## Ergebnis

**PASS** – Header, Hauptinhalt und Footer sind wieder als zusammenhängende Oberfläche
innerhalb eines einzigen großen, abgerundeten Standard-App-Rechtecks wahrnehmbar.
Die gemeinsame Geometrie und alle Referenzpositionen aus V2.6.5.2 bleiben erhalten.

## Gestaltungsbefund

- Standard-App-Rechteck: unveränderter mehrlagiger Cyan-Blau-Hintergrund und eine
  einzige sichtbare Außenkontur.
- Header: transparente Fläche; keine schwarze Eigenfläche und kein Balkenschatten.
- Footer: transparente Fläche; keine schwarze Eigenfläche und kein Balkenschatten.
- Header-Unterkante: `rgba(119,239,248,.08)`.
- Footer-Oberkante: `rgba(119,239,248,.06)`.
- Keine zusätzlichen Rahmen, Leisten oder angehefteten Fremdelemente.
- Funktionale Gliederung, Fokusdarstellung und Touchziele bleiben erhalten.

## Vergleichsmessung auf iPhone 390 × 844

Mittlere absolute RGB-Differenz zwischen je zwei Pixelzeilen ober- und unterhalb der
Header-/Footergrenze:

| Version | Headergrenze | Footergrenze |
|---|---:|---:|
| V2.6.5.1-Beta | 0,355 | 0,297 |
| V2.6.5.2-Beta | 25,627 | 12,161 |
| V2.6.5.3-Beta | 0,339 | 0,315 |

V2.6.5.3 beseitigt damit den starken Flächensprung aus V2.6.5.2 und erreicht wieder
die harmonische Größenordnung der V2.6.5.1, ohne die V2.6.5.2-Positionen zu ändern.

## Geprüfte Profile

- iPhone/iOS-PWA: 390 × 844
- Smartphone: 412 × 915
- Smartphone-Querformat: 844 × 390
- Tablet: 820 × 1180
- Desktop: 1440 × 1000
- zusätzlich 320-px-Reflow in der Browserregression

## Geprüfter Umfang

Startseite, Favoriten kurz/lang/leer, Suche, Filter, Sortiermodus,
Analogsignal-Rechner, fünf weitere Rechner, Einheitendatenbank,
Werkstoffdatenbank, Wissensdatenbank-Hub, fünf Herstellerbereiche,
Wissensbeiträge, Dialoge, Leerzustände und Offlineaufrufe.

## Positions- und Funktionsschutz

- Außenrahmen, Headerhöhe und obere Referenz je Profil unverändert.
- Logo, Release-Modul und Kopfaktionen auf gemeinsamer Mittellinie.
- 44-px-Touchziele; keine Lageänderung bei Hover, Fokus, Drücken oder Sortierung.
- Inhalt beginnt direkt unter dem Header und endet vor dem Footer.
- Footer bleibt innerhalb des Rahmens und berücksichtigt Safe Areas.
- kurze und lange Seiten ohne Überdeckung oder horizontalen Überlauf.
- Icons, Raster, Favoriten, Drag-and-Drop, Navigation, Suche, Rechnerlogik und
  Offlinefunktion ohne Regression.

## Automatisierte Nachweise

- `visual_shell_regression_v2653.py`: 800 PASS
- `layout_regression_v2653.py`: 1.440 PASS
- `browser_regression.py`: 1.366 PASS
- `design_audit_v2653.py`: 162 PASS
- `design_regression.py`: 103 PASS

13 Renderings wurden zusätzlich visuell kontrolliert. Keine sichtbaren schwarzen
Header-/Footerbalken, harten Flächenwechsel, Überlagerungen oder Überläufe gefunden.
