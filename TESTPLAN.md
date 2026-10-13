# Testplan · SK PCT Tools 2.5.2.1-Beta

## 1. Automatische Prüfungen

```bash
python3 tests/validate_project.py
python3 tests/browser_regression.py
```

Browserprofile: Smartphone 390 × 844, Tablet 820 × 1180, Desktop 1440 × 1000.
Der Browsertest öffnet 16 interne Seiten in allen drei Profilen, prüft Überläufe,
Header/Footer, mobile Sonderdarstellungen, sechs Rechnerreferenzen und Offline-Aufrufe.

## 2. Header, Footer und Navigation

1. Startseite sowie alle 15 internen Unterseiten öffnen.
2. Gleiche Header-/Footer-Höhe, Breite, Innenabstände, Safe-Area-Abstände und Touchziele prüfen.
3. Header links immer mit Logo und Versionsplakette kontrollieren.
4. Footer ohne schwarze Kontur, Outline, Schatten oder separate dunkle Fläche prüfen.
5. Zurück, Startseite und Favoriten testen; kein Element darf Logo oder Text überlagern.
6. Nur der interne Inhaltsbereich darf auf Unterseiten vertikal scrollen.

## 3. Startseite

1. Bei 390, 414 und 430 px drei Spalten prüfen; ab 431 px responsive Erweiterung prüfen.
2. App-Titel dürfen nicht mitten im Wort umbrechen oder abgeschnitten werden.
3. Favoritenstern jeder App mit Finger und Tastatur bedienen.
4. Suche, Kategorien, Sortierung, Zurücksetzen, Long-Press-Anordnung und Fertig testen.
5. E+H Viewer: konkrete Device-Viewer-Adresse, neuer Tab und externe Kennzeichnung prüfen.

## 4. Rechner-Referenzwerte

1. Analogsignal: 0…100 und 4…20 mA; 50 ergibt 12 mA und 50 %.
2. P+F: (0|4) und (100|20); K-Faktor 0,16, Nullpunkt 4.
3. Pt100: 0 °C ergibt ungefähr 100 Ω.
4. Einheiten: 1 bar ergibt 100 kPa.
5. Siemens: 4–20 mA, 12 mA, −50…150 °C; Rohwert 13.824 und 50 °C.
6. Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1:
   ΔU ≈ 6,93 V, ε ≈ 1,73 %, Lastspannung ≈ 393,07 V.
7. Vorzeichen, Einheitenwechsel, Reset, Berechnen und Kopieren prüfen.
8. Einheitenauswahlen zeigen kurze Symbole; Feldlabels/ARIA enthalten volle Bezeichnungen.

## 5. Einheitendatenbank

1. Ohne Suche müssen alle 19 Kategorien eingeklappt sein.
2. Suche nach „Fahrenheit“ öffnet den passenden Treffer automatisch.
3. Favorit setzen/entfernen und Favoritenbereich oben prüfen.
4. Kompakte Zeile und aufklappbare Formel/Aliase prüfen.

## 6. Werkstoffe und Wissensbeiträge

1. Werkstoffsuche, Gruppenfilter, Kartendetails und Quellenlinks prüfen.
2. Vergleich mobil als gestapelte Schlüssel-Wert-Karten ohne horizontales Scrollen prüfen.
3. Jeden der fünf Wissensbeiträge öffnen: Kurzantwort sichtbar, Fachdetails geschlossen.
4. Gefahren-/Warnhinweise müssen trotz geschlossener Details sichtbar bleiben.
5. Quellen-/Gültigkeitsbündel und alle Herstellerwege prüfen.

## 7. Messstellen-Dokumentation

1. Fotos hinzufügen, anzeigen und löschen.
2. Eingaben zurücksetzen und Druck-/PDF-Ansicht prüfen.
3. Bemerkungsfeld kontrollieren: Smartphone höchstens 60 px hoch, reguläre Eingaben höchstens 44 px.
4. Lokale Datenhaltung und Bedienung auf Smartphone/Tablet/Desktop prüfen.

## 8. PWA und Offline

1. Online laden und Service Worker aktivieren lassen.
2. Offline schalten und Startseite, alle Rechner, Datenbanken, Herstelleransichten und
   fünf Wissensbeiträge öffnen.
3. Prüfen, dass nur Caches der Version 2.5.2.1-Beta aktiv sind.
