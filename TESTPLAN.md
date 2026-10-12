# Testplan · SK PCT Tools 2.5.0.0-Beta

## 1. Start und Darstellung
1. Projekt über HTTP/HTTPS öffnen.
2. Prüfen, dass **PCT Home** mit 11 eigenständigen App-Icons angezeigt wird.
3. Desktop, Tablet sowie Smartphone in Hoch- und Querformat prüfen.
4. „Kompakte Apps“ ein-/ausschalten und Seite neu laden; die Einstellung muss erhalten bleiben.

## 2. Anordnen
1. **Anordnen** wählen; alle Apps müssen in den Bearbeitungszustand wechseln.
2. Eine App per Maus auf eine andere Position ziehen.
3. Auf einem Touch-Gerät eine App per Finger verschieben.
4. Alternativ eine App gedrückt halten und direkt verschieben.
5. **Fertig** wählen, neu laden und die gespeicherte Reihenfolge prüfen.
6. Im Anordnen-Modus eine fokussierte App mit den Pfeiltasten verschieben.
7. **Standard** wählen; die Auslieferungsreihenfolge muss wiederhergestellt werden.

## 3. Navigation und Funktionen
- Jede der 11 Apps öffnen und korrekten Zielpfad prüfen.
- Für alle sechs Rechner je eine bekannte Eingabe und Ergebnisänderung prüfen.
- Messstellen-Dokumentation: neuen Eintrag/Fotoplatzhalter und PDF-/Druckfunktion prüfen.
- Einheiten- und Werkstoffdatenbank: Suche, Filter, Vergleich/Favorit prüfen.
- Wissensdatenbank: Herstellerbereiche und alle fünf Beiträge öffnen.
- E+H Device Viewer: neuer Tab, `noopener`, `noreferrer` und externe Kennzeichnung.

## 4. Erhaltene Startseitenfunktionen
- Suche nach `Pt100`, `316L`, `SCO` und `Siemens`.
- Kategorien **Rechner**, **Dokumentation**, **Wissen** und **Externe Dienste**.
- Sortierung nach Kategorie und Titel; Rückkehr zu **Eigene Reihenfolge**.
- Favorit hinzufügen/entfernen und Favoritendrawer öffnen.
- Seitennavigation öffnen, Gruppen ein-/ausklappen und Ziele aufrufen.

## 5. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Datenbanken und Wissensbeiträge öffnen.
4. Prüfen, dass der alte Cache der Version 2.4.2.1 nicht weiter verwendet wird.

## 6. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
