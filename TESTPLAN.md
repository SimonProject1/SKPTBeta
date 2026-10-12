# Testplan · SK PCT Tools 2.5.0.3-Beta

## 1. Startseite und iOS-Safe-Area
1. Projekt über HTTP/HTTPS öffnen und als iOS-PWA zum Home-Bildschirm hinzufügen.
2. Auf einem iPhone mit Displayausschnitt/Dynamic Island im Hochformat prüfen, dass die obere Kante des abgerundeten PCT-Home-Pakets vollständig unterhalb von Uhrzeit, Empfang, WLAN und Akku beginnt.
3. Im Querformat prüfen, dass zusätzlich die linke und rechte Safe Area eingehalten werden.
4. Prüfen, dass Logo, Produktname, Suche, Bearbeitungszugriffe und alle 11 App-Icons innerhalb des abgerundeten Pakets liegen.
5. Prüfen, dass die Suche beim Start geschlossen und das Raster direkt sichtbar ist.

## 2. Wissensdatenbank und Herstellerkennzeichnungen
1. Wissensdatenbank im iOS-PWA-Modus im Hoch- und Querformat öffnen.
2. Prüfen, dass das gesamte abgerundete Paket einschließlich Logo, Titel, Suche, Darstellungssteuerung und Beiträgen unterhalb der Statusleiste liegt.
3. Prüfen, dass Air Torque, E+H, Siemens und Vacon als reduzierte weiße Wort- bzw. Kurzmarken auf dunklem PCT-Grund erscheinen.
4. Prüfen, dass keine farbigen Herstellerflächen und keine weißen Logo-Kacheln vorhanden sind.
5. Nach `Promass`, `Siemens`, `SCO` und `Vacon` suchen und jeweils die Treffer prüfen.
6. Mobil vier Herstellergruppen, Auf-/Zuklappen und Kompaktansicht prüfen.
7. Alle fünf Beiträge und die PDF-Beitragsvorlage öffnen.

## 3. Anordnen
1. Eine App etwa eine halbe Sekunde gedrückt halten; Bearbeitungsmodus und Wackelanimation müssen starten.
2. Die App per Maus bzw. Finger auf eine andere Position ziehen.
3. **Fertig** wählen, neu laden und die gespeicherte Reihenfolge prüfen.
4. Auf einer fokussierten App die Leertaste drücken; der Bearbeitungsmodus muss starten.
5. **Zurücksetzen** wählen; die Auslieferungsreihenfolge muss wiederhergestellt werden.
6. Escape muss den Bearbeitungsmodus beenden.
7. Beim Scrollen darf der fixierte Bearbeitungskopf nicht in die iOS-Statusleiste laufen.

## 4. Suche, Navigation und Funktionen
1. Startseitensuche öffnen und nach `Pt100`, `316L`, `SCO` und `Siemens` suchen.
2. Kategorien **Rechner**, **Dokumentation**, **Wissen** und **Externe Dienste** prüfen.
3. Sortierung nach Kategorie und Titel sowie Rückkehr zu **Eigene Reihenfolge** prüfen.
4. Jede der 11 Apps öffnen und korrekten Zielpfad prüfen.
5. Für alle sechs Rechner je eine bekannte Eingabe und Ergebnisänderung prüfen.
6. Messstellen-Dokumentation: neuen Eintrag/Fotoplatzhalter und PDF-/Druckfunktion prüfen.
7. Einheiten- und Werkstoffdatenbank: Suche, Filter, Vergleich/Favorit prüfen.
8. E+H Device Viewer: neuer Tab, `noopener`, `noreferrer` und externe Kennzeichnung.
9. Favorit hinzufügen/entfernen und Favoritendrawer öffnen.

## 5. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Datenbanken und Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.0.3-Beta verwendet werden.

## 6. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
