# Design-Audit-Abnahme – SK PCT Tools V2.6.5.0-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.4.0-Beta  
Status: Umsetzung vollständig; technische Abnahme über die im Testplan genannten Prüfungen

## 1. Verbindliches Ebenenmodell

1. **App-Rahmen:** äußere, safe-area-fähige Hülle mit einer Kontur.
2. **Funktionspanel:** zusammengehöriger Arbeitsbereich mit höchstens einer Kontur.
3. **Control:** Eingabe, Auswahl oder Aktion mit mindestens 44 × 44 px nutzbarer Fläche.

Historische Mehrfachrahmen werden durch die abschließende Token-/Komponentenschicht
neutralisiert. Grün kennzeichnet Ergebnis, positive Primäraktion, aktive Auswahl oder
Erfolg. Cyan kennzeichnet Navigation, Fokus, neutrale Aktion und Information.

## 2. Designtokens

Die zentrale Datei `assets/app-v2-6-5-0.css` definiert verbindlich:

- Hintergrund, Oberfläche, erhöhte und weiche Oberfläche
- Linie und starke Linie
- Text und Sekundärtext
- Cyan, Grün, Warnung und Gefahr
- Control-, Panel- und App-Radien
- Mikro-, Kicker-, Label-, Hilfe-, Fließtext-, Eingabe- und Kartenstufen
- App-/Panel-Schatten
- 4-, 8-, 12-, 16-, 24- und 32-px-Abstände
- 44-px-Mindesttouchziel und 48-px-Primärziel

## 3. Audit-Matrix

| Bereich | Umgesetzter Zustand | Nachweis |
|---|---|---|
| Startseitenicons | PNG sichtbar; Host transparent, ohne Border/Shadow/Pseudokachel | `design_audit_v2650.py`, `design_regression.py` |
| App-Raster | Desktop 5 × 2, responsive Tablet-/Smartphone-Raster | `design_audit_v2650.py` |
| Seitenidentität | vorhandenes App-/Beitragsicon auf 14 aktiven Unterseiten | Struktur- und Browserprüfung |
| Kartenlabels | mindestens 12 px, verständliche ausgeschriebene Namen | Browserprüfung |
| Bedienicons | gemeinsame SVG-Familie, konsistente Kontur und Akzentfarben | Sprite- und Browserprüfung |
| Auf-/Zuklappen | Chevron unten/oben; kein Plus/Minus-Pseudoicon | Audit-Browserprüfung |
| Vorzeichen | ± nur an echten Vorzeichenaktionen | Struktur- und Browserprüfung |
| Touchziele | wichtige Controls mindestens 44 px | Audit- und Browserprüfung |
| Favoriten | Icon links, Text mittig, Entfernen rechts; alte Daten kompatibel | Audit-/Designregression |
| Suche | kollisionsfreie Innenabstände, Desktop-Popover, mobiles Panel, echte Trefferliste | Audit-Browserprüfung |
| Sortiermodus | freie Drag-Ebene, ortsfester Header, Icon-Wackeln, Undo/Redo/Standard/Fertig | Browserregression |
| Einheitendatenbank | flache Kategorien, Chevron, kompakter Leerzustand | Audit-Browserprüfung |
| Werkstoffdatenbank | reduzierte Chips/Rahmen, mobile Vergleichsdarstellung | visuelle und Browserprüfung |
| Wissens-Hub | fünf Hersteller gleichmäßig, größere Labels, Icon im Titel | Audit-/Designregression |
| Wissensbeiträge | mobile Zurück-Chips, Beitragsicon, eine Metadatenebene, flache Abschnitte | Audit-Browserprüfung |
| Footer | eine kompakte Zeile, keine zweite Versionsangabe | alle Routen |
| PWA/Offline | neues Manifest, Cache-Epoch, vollständiger Precache | Integritäts-/Offlineprüfung |
| Geschützte Grafiken | feste SHA-256-Referenzwerte unverändert | `validate_project.py` |

## 4. Unterstützte Profile

- iPhone-/Smartphone-Hochformat: 390 × 844
- schmaler Reflow: 320 × 700
- Smartphone-Querformat: 844 × 390
- Tablet-Touch: 820 × 1180
- Desktop: 1440 × 1000

Zusätzlich werden Safe Area, dynamische Viewporthöhe, Offlineaufruf, Tastaturfokus,
Hover, Touch, Aktivzustand, Fehler-/Warn-/Erfolgsdarstellung, leere Zustände sowie
geöffnete Karten geprüft.

## 5. Geschützte Grafikfamilie

Die Inhalte der freigegebenen PNGs wurden nicht neu gerendert. Versionsgebundene
Dateien wurden nur auf das Präfix `v2-6-5-0-` beziehungsweise den Dateinamen
`release-module-v2-6-5-0.png` umbenannt. Die Hashwerte bleiben gegenüber der
vollständigen V2.6.4.0-Beta identisch.

## 6. Abnahmeregel

Ein Build ist nur freigabefähig, wenn:

1. `tests/validate_project.py` erfolgreich ist,
2. `tests/design_audit_v2650.py` erfolgreich ist,
3. `tests/design_regression.py` erfolgreich ist,
4. `tests/browser_regression.py` erfolgreich ist,
5. keine JavaScript-/Bild-/Referenzfehler auftreten,
6. `SHA256SUMS.txt` vollständig und korrekt ist,
7. Projekt-ZIP und separat veröffentlichte ZIP-Prüfsumme übereinstimmen.
