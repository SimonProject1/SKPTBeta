# Architektur – SK PLT Tools 2.1.7.3-Beta

## Leitprinzipien

1. Statische, lokal ausführbare Webanwendung ohne serverseitige Abhängigkeit.
2. Gemeinsame Kopfzeile, Fußzeile, Favoriten- und Navigationssteuerung auf allen Seiten.
3. Eine zentrale Einheitenquelle; keine duplizierten Umrechnungsfaktoren in Rechnern.
4. Rechner arbeiten intern mit den festen Basiseinheiten der jeweiligen Kategorie.
5. Einheitenwechsel erhalten die physikalische Größe und ändern nur Zahlenwert und Symbol.
6. Offline-First-PWA mit versionsgebundenem, vollständig validiertem Precache.

## Laufzeitschichten

- `assets/app.js`: Anwendungsschale, Seitenfavoriten, Startseitensuche, Sortierung, Navigation und Service-Worker-Registrierung.
- `assets/unit-system.js`: Laden und Validieren der Einheitendaten, Faktor-/Offset-Umrechnung, Favoriten und Dropdown-Aufbau.
- `assets/units.json`: Single Source of Truth mit 19 Kategorien und 115 Einheiten.
- Rechnerdateien: fachliche Berechnung; Einheiten werden ausschließlich über `SK_UNITS` normalisiert.
- `einheitendatenbank/`: Such-, Filter- und Favoritenoberfläche.
- `.sk-unit-database-cta`: gemeinsamer, responsiver Direktzugriff am Ende jeder Seite mit Einheiten-Auswahl; `width: 100%` und `max-width: 920px` entsprechen dem jeweiligen Rechner-Hauptbereich, das Ziel ist immer `einheitendatenbank/`.

## Datenfluss bei Einheitenwechsel

1. Dropdown meldet alte Einheit, neue Einheit und Kategorie.
2. Betroffene Eingaben werden über die Kategoriebasis umgerechnet.
3. Messbereichsgrenzen und aktueller Eingabewert bleiben physikalisch identisch.
4. Rechner normalisiert auf die feste Basiseinheit.
5. Ergebnis wird in die gewählte Anzeigeeinheit zurückgerechnet.
6. Favoritenänderungen aktualisieren Dropdowns ohne gültige Auswahl zu verlieren.

## Rechnerintegration

- Analogsignal: Prozess- und Signalwerte teilen je eine Kategorie/Einheit.
- P+F: X- und Y-Achse besitzen getrennte Kategorien.
- Pt100/Pt1000: interne IEC-60751-Näherung in °C und Ω.
- Siemens Rohwert: bestehende Rohwert-/Signal-/Diagnoselogik bleibt unverändert; physikalischer Messbereich wird vorgeschaltet umgerechnet.
- Spannungsfall: interne Berechnung in V, A, m und mm²; Ausgabe in gewählter Spannungseinheit.
- Einheitenrechner: direkte Nutzung aller Kategorien.

## Mobile und PWA

`viewport-fit=cover`, dunkle HTML-Grundfläche und Safe-Area-Paddings sichern iPhone-Standalone-Darstellung. Die beiden unteren Schnellzugriffe bleiben fixed. Service Worker und Manifest sind versionsgebunden; alte Cache-Versionen werden bei Aktivierung entfernt.

## Qualitätsbarrieren

- Datenmodellvalidierung und Roundtrips.
- Referenzumrechnungen einschließlich Temperatur-Offsets.
- Rechnerregressionen.
- statische Pfad-, Versions-, Precache- und Prüfsummenprüfung.
- Browserläufe für Desktop, Tablet, iPhone-Touchprofil und Querformat.
- Vollständigkeitsprüfung des Datenbank-Direktzugriffs auf allen sechs Einheiten-Auswahlseiten.
- Offline-Aufruf der neuen Einheitendatenbank.
