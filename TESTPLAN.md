# Testplan · SK PCT Tools 2.5.0.4-Beta

## 1. Startseite, Kopf und iOS-Safe-Area
1. Projekt über HTTP/HTTPS öffnen und als iOS-PWA zum Home-Bildschirm hinzufügen.
2. Auf einem iPhone mit Displayausschnitt/Dynamic Island im Hochformat prüfen, dass die obere Kante des abgerundeten PCT-Home-Pakets vollständig unterhalb von Uhrzeit, Empfang, WLAN und Akku beginnt.
3. Im Querformat prüfen, dass zusätzlich die linke und rechte Safe Area eingehalten werden.
4. Prüfen, dass Logo, Versionsnummer, Produktname, Suche, Favoriten, Bearbeitungszugriffe und alle 11 App-Icons innerhalb des abgerundeten Pakets liegen.
5. Das gegenüber V2.5.0.3-Beta moderat größere PCT-Logo und die direkt daneben stehende Version `V2.5.0.4-Beta` prüfen.
6. Prüfen, dass der Favoriten-Stern unmittelbar unter der Suchlupe sitzt und das PCT-Home-Gehäuse mit schwarzer Außenkontur und grüner innerer Signalkante verwendet.
7. Prüfen, dass die Suche beim Start geschlossen und das Raster direkt sichtbar ist.

## 2. Wissensdatenbank und Herstellerkennzeichnungen
1. Wissensdatenbank im iOS-PWA-Modus im Hoch- und Querformat öffnen.
2. Prüfen, dass das gesamte abgerundete Paket einschließlich Logo, Titel, Suche, Darstellungssteuerung und Beiträgen unterhalb der Statusleiste liegt.
3. Prüfen, dass Air Torque, E+H, Siemens und Vacon als reduzierte weiße Wort- bzw. Kurzmarken auf dunklem PCT-Grund erscheinen.
4. Prüfen, dass keine farbigen Herstellerflächen und keine weißen Logo-Kacheln vorhanden sind.
5. Nach `Promass`, `Siemens`, `SCO` und `Vacon` suchen und jeweils die Treffer prüfen.
6. Mobil vier Herstellergruppen, Auf-/Zuklappen und Kompaktansicht prüfen.
7. Alle fünf Beiträge und die PDF-Beitragsvorlage öffnen.

## 3. Anordnen und Icon-Raster
1. Desktop: sechs Spalten, mittlere Breite: vier Spalten, Mobil: vier Spalten und bis 380 px: drei Spalten prüfen.
2. Prüfen, dass alle 11 Apps und alle 11 eindeutigen Symbole vorhanden sind.
3. Eine App etwa eine halbe Sekunde gedrückt halten; Bearbeitungsmodus und Wackelanimation müssen starten.
4. Die App per Maus bzw. Finger auf eine andere Position ziehen.
5. **Fertig** wählen, neu laden und die gespeicherte Reihenfolge prüfen.
6. Auf einer fokussierten App die Leertaste drücken; der Bearbeitungsmodus muss starten.
7. **Zurücksetzen** wählen; die Auslieferungsreihenfolge muss wiederhergestellt werden.
8. Escape muss den Bearbeitungsmodus beenden.
9. Beim Scrollen darf der fixierte Bearbeitungskopf nicht in die iOS-Statusleiste laufen.

## 4. Suche, Favoriten, Navigation und Funktionen
1. Startseitensuche öffnen und nach `Pt100`, `316L`, `SCO` und `Siemens` suchen.
2. Kategorien **Rechner**, **Dokumentation**, **Wissen** und **Externe Dienste** prüfen.
3. Sortierung nach Kategorie und Titel sowie Rückkehr zu **Eigene Reihenfolge** prüfen.
4. Jede der 11 Apps öffnen und korrekten Zielpfad prüfen.
5. Favorit hinzufügen/entfernen, Zähler prüfen und den Favoritendrawer über das neue Icon unter der Lupe öffnen/schließen.
6. Für alle sechs Rechner je eine bekannte Eingabe und Ergebnisänderung prüfen.
7. Messstellen-Dokumentation: neuen Eintrag/Fotoplatzhalter und PDF-/Druckfunktion prüfen.
8. Einheiten- und Werkstoffdatenbank: Suche, Filter, Vergleich/Favorit prüfen.
9. E+H Device Viewer: neuer Tab, `noopener`, `noreferrer` und externe Kennzeichnung.

## 5. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Datenbanken und Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.0.4-Beta verwendet werden.

## 6. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
