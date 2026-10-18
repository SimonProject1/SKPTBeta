# Design-Audit – SK PCT Tools V2.6.5.5-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.4-Beta  
Scope: ausschließlich Fahrplan-Punkt 1

## Ergebnis

**PASS** – der kleine Korrekturblock verbessert Textfluss, Auswahlwertsichtbarkeit
und leere Favoritenzustände, ohne den bestehenden visuellen Grundstil oder die
Funktionsgeometrie zu verändern.

## Geprüfte Korrekturen

- App-, Hersteller-, Seiten- und Wissensbeitragstitel verwenden keine
  automatische Silbentrennung.
- Kontrollierte Umbruchstellen sind fachlich sinnvoll gesetzt und erzeugen bei
  320 px und 390 px keinen horizontalen Titelüberlauf.
- Das mobile Startseitenraster bleibt dreispaltig; die gemessenen Icongrößen und
  Favoritenanker bleiben unverändert.
- Analogsignal-Richtung und Spannungsfall-Stromart erhalten unter 430 px gezielt
  volle Feldbreite; alle Optionswerte bleiben vollständig.
- Der Hersteller-Hub behält seine Abstände und Rasterlogik; Endress+Hauser wird
  kontrolliert getrennt.
- Sichtbare Mikrotexte liegen regulär bei etwa 10 bis 11 px, Hilfstexte bei
  mindestens etwa 13 px. Header-, Versions- und Footerhöhe bleiben unverändert.
- Der mobile redundante Werkstoff-Startseitenchip ist entfernt; Desktop-
  Breadcrumb und Wissensdatenbank-Chip in Beiträgen sind erhalten.
- Leere Favoritenzustände sind kompakte horizontale Zeilen; gefüllte Listen
  bleiben vollständig und bedienbar.

## Unverändertheitsprüfung

- fünf Wissensbeiträge: Aufbau, Kartenstil, Fachgrafiken und Inhalte unverändert
- große PNG-Icons, Logos und PWA-Grafiken: Binärinhalte unverändert
- Headergeometrie, Footerabschluss und App-Rahmen unverändert
- Rechner-Ergebnisdarstellungen unverändert
- Drag-and-Drop-Sortierung, Touch, Pointer, Undo/Redo und Speicherung unverändert

## Viewports und Bedienarten

Geprüft: 320 × 800, 390 × 844, 412 × 915, 844 × 390, 820 × 1180 und
1440 × 1000. Zusätzlich geprüft: Touch, Tastaturfokus, Reflow, reduzierte
Bewegung, Offlinebetrieb und Service-Worker-Upgrade.

## Automatisierte Abdeckung

- 163 gezielte Korrekturblockprüfungen
- 1.440 Positionsprüfungen
- 800 visuelle Shell-Prüfungen
- 162 Design-/Accessibility-/Offline-Auditprüfungen
- 103 Raster-/Favoritenprüfungen
- 1.373 vollständige Browser-/Funktionsprüfungen

Gesamt: **4.041 Browserprüfungen**, alle PASS.
