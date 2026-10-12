# Testplan · SK PCT Tools 2.5.0.2-Beta

## 1. Start und reduzierte Darstellung
1. Projekt über HTTP/HTTPS öffnen.
2. Prüfen, dass das Raster mit 11 App-Icons ohne Uhrzeit, Datum, PCT-Home-Einführung,
   Versionsfeld, Verschiebeanleitung oder App-Dichte-Auswahl sichtbar ist.
3. Desktop, Tablet sowie Smartphone in Hoch- und Querformat prüfen.
4. Prüfen, dass die Suche beim Start geschlossen und das Raster direkt sichtbar ist.
5. Prüfen, dass das S.K.-PCT-Logo innerhalb des großen abgerundeten Home-Screens
   steht und oberhalb davon kein separater Startseiten-Header verbleibt.

## 2. Anordnen
1. Eine App etwa eine halbe Sekunde gedrückt halten; Bearbeitungsmodus und
   Wackelanimation müssen starten.
2. Die App per Maus bzw. Finger auf eine andere Position ziehen.
3. **Fertig** wählen, neu laden und die gespeicherte Reihenfolge prüfen.
4. Im Bearbeitungsmodus eine fokussierte App mit den Pfeiltasten verschieben.
5. Auf einer fokussierten App die Leertaste drücken; der Bearbeitungsmodus muss starten.
6. **Zurücksetzen** wählen; die Auslieferungsreihenfolge muss wiederhergestellt werden.
7. Escape muss den Bearbeitungsmodus beenden.

## 3. Kompakte Suche
1. **Suchen** öffnen und nach `Pt100`, `316L`, `SCO` und `Siemens` suchen.
2. Kategorien **Rechner**, **Dokumentation**, **Wissen** und **Externe Dienste** prüfen.
3. Sortierung nach Kategorie und Titel sowie Rückkehr zu **Eigene Reihenfolge** prüfen.
4. Escape schließt die Suche und setzt den Fokus auf den Suchzugriff.

## 4. Navigation und Funktionen
- Jede der 11 Apps öffnen und korrekten Zielpfad prüfen.
- Für alle sechs Rechner je eine bekannte Eingabe und Ergebnisänderung prüfen.
- Messstellen-Dokumentation: neuen Eintrag/Fotoplatzhalter und PDF-/Druckfunktion prüfen.
- Einheiten- und Werkstoffdatenbank: Suche, Filter, Vergleich/Favorit prüfen.
- Wissensdatenbank: Herstellerbereiche und alle fünf Beiträge öffnen.
- Wissensdatenbank: identisches PCT-Icon-Raster sowie sichtbare Kennzeichnungen für
  Air Torque, Endress+Hauser, Siemens und Vacon prüfen.
- Wissensdatenbank mobil: vier Herstellergruppen, Auf-/Zuklappen und Kompaktansicht prüfen.
- E+H Device Viewer: neuer Tab, `noopener`, `noreferrer` und externe Kennzeichnung.
- Favorit hinzufügen/entfernen und Favoritendrawer öffnen.
- Prüfen, dass auf keiner Seite eine hierarchische Seitenauswahl-Schaltfläche oder ein Drawer erscheint.

## 5. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Datenbanken und Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.0.2-Beta verwendet werden.

## 6. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
