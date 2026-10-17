# Design-Audit – SK PCT Tools V2.6.5.2-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.5.1-Beta

## Ergebnis

**PASS** – der globale Positionsstandard ist über Startseite, Favoritenansicht,
Suche, Sortiermodus, Rechner, Datenbanken, Wissens-Hub, Herstelleransichten,
Wissensbeiträge, Dialog-/Leerzustände und Offlineaufrufe konsistent.

## Geprüfte Profile

- iPhone/iOS-PWA: 390 × 844
- Smartphone: 412 × 915
- Smartphone-Querformat: 844 × 390
- Tablet: 820 × 1180
- Desktop: 1440 × 1000
- zusätzlich 320-px-Reflow

## Verbindliche Geometrie

- Startseite und Unterseiten verwenden je Profil exakt dieselbe Außenrahmenlage,
  Breite, Höhe, Kontur und Rundung.
- Headerhöhe: 76 px Standard, 66 px Smartphone, 58 px niedriges Querformat.
- Logo, Release-Modul und Kopfaktionen liegen auf einer gemeinsamen optischen
  Mittellinie.
- Headerbuttons besitzen 44 × 44 px Bedienfläche und verändern ihre Lage bei Hover,
  Fokus, Pointerdown, aktivem Zustand oder Sortierung nicht.
- Der Inhaltsbereich beginnt direkt unter derselben Header-Trennlinie.
- Der Footer bleibt innerhalb des App-Rahmens, berücksichtigt die Safe Area und
  überdeckt den scrollbaren Inhalt nicht.
- Favoritenunteransicht und leere Zustände ersetzen nur den mittleren Inhalt;
  Außenrahmen, Header und Footer bleiben erhalten.

## Funktionsbereiche

- Startseite: Raster, Suche, Filter, Sortierung und Drag-and-Drop unverändert.
- Analogsignal-Rechner: kompakte MA-/ME-Skalierung ohne Einheitenauswahl.
- Weitere Rechner: keine fachliche Änderung; 44-px-Touchziele und Kopierfunktionen.
- Einheitendatenbank: unverändertes zentrales Einheitensystem.
- Werkstoffdatenbank: Suche, Filter, Karten und mobiler Vergleich im Rahmen.
- Wissensdatenbank: fünf Hersteller, Suchfeld, Ansichten und Beiträge ohne Überlauf.
- Navigation: Favoriten, Zurück und Home positionsstabil.
- Offline: gecachte Unterseiten behalten denselben Rahmen.

## Automatisierte Nachweise

- `layout_regression_v2652.py`: 1.440 PASS
- `browser_regression.py`: 1.366 PASS
- `design_audit_v2652.py`: 162 PASS
- `design_regression.py`: 103 PASS

## Visuelle Nachweise

12 repräsentative Screenshots für Mobile und Desktop wurden als Kontaktbogen geprüft.
Keine abgeschnittenen Hauptbeschriftungen, keine Header-/Footer-Überlagerung, keine
zweite Außenfläche und keine horizontalen Überläufe festgestellt.
