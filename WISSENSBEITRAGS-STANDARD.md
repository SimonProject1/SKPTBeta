# SK PCT Tools – Wissensbeitragsstandard V2.6.6.0-Beta

Stand: 18.10.2026  
Status: verbindlich

## 1. Verbindliche Navigation

`Startseite → Wissensdatenbank → Hersteller → Gerät/Familie/Themenbereich → Wissensbeitrag`

Keine Ebene darf übersprungen oder durch eine rein dekorative Kategorie ersetzt werden. Hersteller-, Zwischen- und Beitragsebene verwenden dieselbe kompakte App-Kachel-Logik. Die Kachelbezeichnung steht vollständig unter dem Icon.

Vorhandene Zuordnung:

- Air Torque → Pneumatischer Antrieb → Drehrichtung SCO/SCC
- Endress+Hauser → Promass → Einbaulage und Einbausituation
- Siemens → SITRANS P320 → SIL-Verriegelung
- Siemens → SPS / Analogkarte → Rohwert und Skalierung
- Vacon → Frequenzumrichter → Ist-/Sollwert-Abweichung im PLS
- Sonstiges enthält nur tatsächlich vorhandene herstellerunabhängige Beiträge; V2.6.6.0-Beta enthält dort keinen Beitrag.

## 2. Navigation und Auffindbarkeit

- Smartphone: kompakter kontextueller Zurück-Chip exakt zur übergeordneten Ebene.
- Tablet/Desktop: vollständige Breadcrumb-Kette.
- Suche und Suchindex erfassen Hersteller, Gerät/Familie/Themenbereich und Beitrag.
- Jeder Navigationsknoten besitzt eine direkt adressierbare URL.
- Favoriten speichern die direkte URL und das zugehörige Icon.
- Zurück-/Vorwärtsnavigation des Browsers muss jede Ebene wiederherstellen.

## 3. Pflichtstruktur eines Wissensbeitrags

1. vollständige Breadcrumb-Kette;
2. mobiler Zurück-Chip zum Gerät/zur Familie/zum Themenbereich;
3. Hero mit dem konkreten Beitragsicon, Kicker, Titel und Kurzbeschreibung;
4. kompakte Metadaten mit Hersteller, Gerät/Familie, Thema und Beitragstyp;
5. sichtbare Kurzantwort;
6. fachlich gegliederte Abschnitte, Prozesse, Diagramme oder einklappbare Details;
7. sichtbare Warn-/Sicherheitsinformationen;
8. Quellenart und Gültigkeit;
9. `data-knowledge-standard="2.6.6.0-Beta"` und `data-sk-style="knowledge-article knowledge-flat"`.

## 4. Flaches Beitragsdesign

- Zentrale CSS-Datei: `assets/app-v2-6-6-0.css`.
- Keine starken schwarzen Versatzschatten oder Textschatten.
- Hero und Abschnitte werden durch Abstand und ruhige Trennlinien gegliedert.
- Panels nur dort, wo sie fachlich zusammengehörige Informationen bündeln.
- Cyan/Grün als dezente Akzente; Warnung Gelb, Gefahr Rot.
- Fachgrafiken, Merksätze und Prozessdarstellungen bleiben erhalten.
- Auf-/Zuklappen ausschließlich über Chevron unten/oben; Kurzantwort bleibt sichtbar.

## 5. Inhalts- und Sicherheitsregeln

- Hersteller, Gerät/Familie und Thema eindeutig benennen.
- Parameter, PINs, Messwerte und Grenzwerte nur aus belegtem Projektbestand übernehmen.
- Praxiswissen als „Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)“ kennzeichnen.
- Herstellerunterlagen, Gerätestand sowie betriebliche Sicherheits- und Freigabevorgaben bleiben maßgeblich.
- Bestehende Fachinhalte, Quellen, Warnungen, Links, Diagramme und einklappbare Bereiche bei Layoutänderungen vollständig erhalten.
- Keine erfundenen Beiträge oder Zuordnungen.

## 6. Accessibility und Interaktion

- genau ein H1;
- konsistente Überschriftenhierarchie;
- sichtbarer Tastaturfokus;
- Touchziele mindestens 44 × 44 px;
- keine Lage- oder Größenänderung bei Hover, Fokus, Touch oder Aktivzustand;
- Information nie ausschließlich über Farbe;
- `prefers-reduced-motion` berücksichtigen;
- kein horizontaler Überlauf ab 320 px.

## 7. Direkte Werkstoffnavigation

`Startseite → Werkstoffdatenbank → Werkstoff/Werkstoffdetails`

- Keine Werkstoffgruppen-Zwischenebene und kein zusätzlicher Kategorieklick.
- Werkstoffe erscheinen direkt als App-Kacheln.
- Antippen öffnet unmittelbar die vorhandene Detailansicht.
- Suche, Filter und Direktvergleich bleiben parallel und unmittelbar erreichbar.
- Werkstoffgruppen dürfen nur als Filter/Metadatum dienen, nicht als Navigationsebene.

## 8. Abnahme

Ein Beitrag gilt als standardkonform, wenn Navigation, Icon, Metadaten, Kurzantwort, Fachinhalt, Warnungen, Quellen, Links, Rückwege, Suche, Favoriten und Offlineaufruf funktionieren und die Testprogramme erfolgreich sind.
