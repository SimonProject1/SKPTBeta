# SK PCT Tools - Wissensbeitragsstandard V2.4.1.9

Stand: 11.10.2026
Status: verbindlicher Release-Standard für alle Wissensbeiträge im Projekt

## 1. Pflichtstruktur

Jeder Wissensbeitrag enthält in dieser Reihenfolge:

1. Eindeutige Brotkrümelnavigation.
2. Hero-Bereich mit Hersteller/Gerätefamilie, Titel und Kurzfassung.
3. Metadaten: Hersteller, Gerät/Familie, Thema und Beitragstyp.
4. Fachinhalt in klar benannten Abschnitten.
5. Prüf-, Handlungs- oder Zuordnungsfolge, sofern fachlich sinnvoll.
6. Sicherheits-, Gültigkeits- und Quellenhinweis.
7. Technische Standardzuordnung über `data-knowledge-standard="2.4.1.9"`; keine sichtbare Versions- oder Standardleiste im Beitrag.

## 2. Darstellungsregeln

- Gemeinsame CSS-Datei `assets/knowledge-article.css` verwenden.
- Gemeinsame Klassen mit Präfix `kb-` verwenden.
- Inhalt semantisch als `TechArticle` auszeichnen.
- Desktop, Tablet, Smartphone-Hochformat und Smartphone-Querformat unterstützen.
- Keine fachliche Aussage allein über Farbe oder Grafik vermitteln.
- Überschriftenhierarchie, Tastaturfokus und ARIA-Beschriftungen erhalten.

## 3. Qualitätsregeln

- Hersteller, Gerät und Gerätestand eindeutig benennen, soweit bekannt.
- Messwerte, Parameter, PINs und Grenzwerte nur aus belegtem Bestand übernehmen.
- Unbestätigte Annahmen nicht als Tatsache formulieren.
- Sicherheitsrelevante Änderungen immer an Herstellerunterlagen und betriebliche Freigaben binden.
- Keine vertraulichen Anlagen-Passwörter oder personenbezogenen Daten aufnehmen.
- Bestehende Fachinhalte bei Layout-Migration inhaltlich erhalten.

## 4. Beitragsvorlage

Die PDF-Vorlage erfasst Kurzfassung, Geltungsbereich/Voraussetzungen, Vorgehen, Ergebnis/Merksatz, Warnhinweise, Quellen und Anhänge. Sie ist gemeinsam mit den genannten Anhängen einzureichen.

## 5. Abnahme

Ein Beitrag gilt als standardkonform, wenn:

- alle Pflichtmetadaten vorhanden sind,
- die Kurzfassung den Nutzen in ein bis drei Sätzen erklärt,
- Fachinhalt und Hinweise klar getrennt sind,
- Quellen/Gültigkeit sichtbar dokumentiert sind,
- interne Links funktionieren,
- die Seite ohne horizontalen Überlauf in allen unterstützten Profilen dargestellt wird,
- Online- und Offline-Aufruf über den Service Worker funktionieren.
