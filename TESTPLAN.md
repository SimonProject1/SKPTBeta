# Testplan · SK PCT Tools 2.5.0.7-Beta

## 1. Hauptstartseite, Viewport und iOS-Safe-Areas
1. Projekt über HTTP/HTTPS öffnen und als iOS-PWA zum Home-Bildschirm hinzufügen.
2. Auf einem iPhone mit Displayausschnitt/Dynamic Island prüfen, dass die obere Kante des abgerundeten PCT-Home-Pakets vollständig unterhalb der Statusleiste beginnt.
3. Prüfen, dass die Unterkante des Rechtecks bis unmittelbar vor die untere Safe Area beziehungsweise den Home-Indikator reicht und diesen nicht überlagert.
4. Im Hochformat wischen: Die Hauptstartseite darf weder scrollen noch das iOS-Gummibandverhalten zeigen.
5. Im Querformat prüfen, dass die linke und rechte Safe Area eingehalten werden und ebenfalls kein Seitenscrollen möglich ist.
6. Desktop prüfen: Das PCT-Logo ist 98 px hoch und entspricht exakt 46 px Suche + 6 px Abstand + 46 px Favoriten.
7. Mobil im Hochformat prüfen: Das PCT-Logo ist 89 px hoch und entspricht exakt 42 px Suche + 5 px Abstand + 42 px Favoriten.
8. Prüfen, dass `V2.5.0.7-Beta`, Suche, Favoriten, alle 11 App-Icons und der vollständige Footer sichtbar innerhalb des Rechtecks liegen.

## 2. Responsive Icon-Anordnung
1. Desktop prüfen: sechs Spalten und zwei Icon-Reihen.
2. Mittlere Breite prüfen: vier Spalten und drei Icon-Reihen.
3. Smartphones bis einschließlich 380 px prüfen: weiterhin vier Spalten und drei Reihen; kein Umbruch auf vier Reihen.
4. Smartphone-Querformat mit geringer Höhe prüfen: sechs Spalten und zwei kompakte Reihen.
5. Bei allen geprüften Größen sicherstellen, dass kein Icon oder Titel abgeschnitten ist.

## 3. Startseitensuche und Favoriten
1. Suche öffnen: Das Overlay muss über dem unveränderten Home-Raster erscheinen; die Seite selbst darf nicht verschoben oder scrollbar werden.
2. Bei kleinem Viewport prüfen, dass nur das Such-Overlay intern scrollt.
3. Nach `Pt100`, `316L`, `SCO` und `Siemens` suchen; App- und Wissensfundstellen prüfen.
4. Kategorien Rechner, Dokumentation, Wissen und Externe Dienste prüfen.
5. Sortierung und gemeinsames Zurücksetzen prüfen; Such-Overlay mit Escape schließen.
6. Favorit hinzufügen/entfernen, Zähler prüfen und Favoritendrawer öffnen/schließen.
7. Favoritendrawer bei vielen Einträgen intern scrollen; die Startseite im Hintergrund muss feststehen.
8. Long-Press-Verschieben, Tastaturverschieben, Fertig und Zurücksetzen prüfen.

## 4. Hersteller-Hub der Wissensdatenbank
1. Wissensdatenbank öffnen; die Startansicht muss ausschließlich die Hersteller-Icons Air Torque, Endress+Hauser, Siemens, Vacon und Sonstiges zeigen.
2. Jedes Hersteller-Icon öffnen und URL-Parameter, Titel, Beschreibung sowie Zurück-Navigation prüfen.
3. Zuordnung prüfen: Air Torque 1, Endress+Hauser 1, Siemens 2, Vacon 1, Sonstiges 0 Beiträge.
4. Sonstiges öffnen; der vorbereitete Leerzustand für Beiträge ohne Hersteller muss erscheinen.
5. Browser-Zurück/-Vorwärts zwischen Hub und Herstelleransichten prüfen.
6. Direktaufruf `wissensdatenbank/?manufacturer=siemens` online und offline prüfen.
7. Alle fünf Beiträge öffnen und unveränderte Inhalte sowie URLs prüfen.
8. „Beitrag vorschlagen“ öffnen und die PDF-Beitragsvorlage prüfen.

## 5. Rechner, Datenbanken und externer Dienst
1. Alle sechs Rechner mit einer bekannten Eingabe testen.
2. Messstellen-Dokumentation sowie Einheiten- und Werkstoffdatenbank stichprobenartig prüfen.
3. E+H Device Viewer auf neuen Tab, `noopener`, `noreferrer` und externe Kennzeichnung prüfen.

## 6. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Herstelleransichten und Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.0.7-Beta verwendet werden.

## 7. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
