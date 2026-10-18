# Design-Audit – SK PCT Tools V2.6.5.4-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.3-Beta

## Ergebnis

**PASS** – Der Analogsignal-Rechner ist nach Entfernung von Kicker, Aktionsleiste
und Ergebniskopierflächen kompakt, ausgewogen und vollständig bedienbar. Andere
Seiten behalten die validierte Geometrie und Gestaltung der V2.6.5.3-Beta.

## Analogsignal-Befund

- Titel beginnt ohne leere Kickerzeile direkt mit „Analogsignal-Rechner“.
- Formular folgt ohne durch entfernte Buttons erzeugte Leerfläche.
- Ergebnisbereich enthält ausschließlich Beschriftung und Ergebniswert.
- Keine Kopierhosts, Touchflächen, Tooltips oder künstlichen rechten Abstände.
- iPhone 390 × 844: beide Ergebniswerte sichtbar, ohne horizontalen Überlauf.
- Desktop 1440 × 1000: Eingaben und Ergebnisse kompakt in der bestehenden
  Rechnergeometrie; keine neuen Rahmen oder verschachtelten Panels.
- Fehlermeldung bleibt als assertive Live-Region verfügbar.
- Ergebnisbereich bleibt als polite Live-Region verfügbar.

## Geprüfte Profile

- iPhone/iOS-PWA: 390 × 844
- Smartphone: 412 × 915
- Smartphone-Querformat: 844 × 390
- Tablet: 820 × 1180
- Desktop: 1440 × 1000
- zusätzlich 320-px-Reflow in der Browserregression

## Regressionsschutz

- 16 Routen behalten gemeinsame Rahmen-, Header-, Inhalts- und Footer-Geometrie.
- 44-px-Touchziele und Fokusdarstellung bleiben für verbleibende Controls erhalten.
- Icons, Logos, Raster, Favoriten, Drag-and-Drop, Suche und andere Rechner zeigen
  keine festgestellte Regression.
- Offline-Precache und Navigation interner Unterseiten bleiben funktionsfähig.

## Automatisierte Nachweise

- `visual_shell_regression_v2654.py`: 800 PASS
- `layout_regression_v2654.py`: 1.440 PASS
- `browser_regression.py`: 1.373 PASS
- `design_audit_v2654.py`: 162 PASS
- `design_regression.py`: 103 PASS

Zusätzlich wurden zwei Analogsignal-Renderings visuell kontrolliert. Es wurden keine
Restzeilen, leeren Aktionsflächen, Kopierflächen, Überlagerungen, abgeschnittenen
Ergebnisse oder horizontalen Überläufe gefunden.
