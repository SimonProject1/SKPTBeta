# SK PCT Tools – Wissensbeitragsstandard V2.6.5.5-Beta

Stand: 18.10.2026  
Status: verbindlicher Standard für alle Wissensbeiträge

## 1. Pflichtstruktur

Jeder Wissensbeitrag enthält:

1. vollständige Breadcrumb-Kette für Tablet/Desktop;
2. mobilen Zurück-Chip „Wissensdatenbank“;
3. Hero mit passendem vorhandenen Beitrags- oder Herstellericon, Kicker, Titel und Kurzbeschreibung;
4. genau eine sichtbare, kompakte Metadatenebene mit Hersteller, Gerät/Familie, Thema und Beitragstyp;
5. sichtbare Kurzantwort;
6. fachlich gegliederte Abschnitte, Prozesse, Diagramme oder einklappbare Details;
7. sichtbare Warn-/Sicherheitsinformationen;
8. Quellenart und Gültigkeit am Beitragsende;
9. `data-knowledge-standard="2.6.5.5-Beta"`.

## 2. Gestaltung

- Zentrale CSS-Datei: `assets/app-v2-6-5-5.css`.
- Gemeinsame Klassen mit Präfix `kb-`.
- Semantische Auszeichnung als `TechArticle`.
- Beitragsicon statt generischem PCT-Wasserzeichen.
- Iconhost transparent, rahmenlos und schattenfrei.
- Abschnitte werden primär durch Abstand und eine ruhige Trennlinie gegliedert;
  keine gestapelten Panelrahmen.
- Diagramm-/Prozesssprache: kräftige dunkle Kontur, Weiß, Cyan und Grün;
  Warnung Gelb, Gefahr Rot.
- Einheitliche Strichstärke und keine Information ausschließlich über Farbe.
- Auf-/Zuklappen ausschließlich mit Chevron unten/oben.
- wichtige Links als cyanfarbene PCT-Links.

## 3. Responsive Regeln

- Smartphone-Hoch- und -Querformat, Tablet und Desktop unterstützen.
- kein horizontaler Überlauf.
- Fließtext 15–17 px, Hilfstext 13–14 px, Labels 12–14 px, Kicker 11–12 px.
- Touchziele mindestens 44 × 44 px.
- iOS/PWA-Safe-Area und Footerabstand berücksichtigen.
- lange Überschriften umbrechen, ohne Icons oder Controls zu überdecken.

## 4. Inhaltliche Qualitätsregeln

- Hersteller, Gerät/Familie und Thema eindeutig benennen.
- Parameter, PINs, Messwerte und Grenzwerte nur aus belegtem Bestand übernehmen.
- Praxiswissen als „Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis
  (anonymisiert)“ kennzeichnen.
- Herstellerunterlagen, konkrete Gerätestände sowie betriebliche Sicherheits- und
  Freigabevorgaben bleiben maßgeblich.
- keine vertraulichen Passwörter, personenbezogenen Daten oder anlagenspezifischen
  Sicherheitsinformationen aufnehmen.
- bestehende Fachinhalte, Quellen, Warnungen, Links und Diagramme bei Layoutänderungen
  vollständig erhalten.

## 5. Accessibility

- genau ein H1 und konsistente Überschriftenhierarchie;
- sichtbarer Tastaturfokus;
- ARIA-Beschriftung für Navigation, Details und Controls;
- verständliche Linktexte;
- Warnung/Erfolg/Fehler zusätzlich durch Text und Icon;
- `prefers-reduced-motion` berücksichtigen.

## 6. Abnahme

Ein Beitrag gilt als standardkonform, wenn:

- Pflichtstruktur und Metadaten vorhanden sind;
- Beitragsicon korrekt und byteunverändert referenziert ist;
- mobile und vollständige Breadcrumbs funktionieren;
- Kurzantwort, Fachinhalt, Warnungen, Quellen und Gültigkeit sichtbar sind;
- interne/externe Links funktionieren;
- geöffnete/geschlossene Bereiche Chevron unten/oben verwenden;
- Online- und Offlineaufruf funktionieren;
- die Browser- und Design-Audit-Tests erfolgreich sind.
