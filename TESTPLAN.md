# Testplan · SK PCT Tools 2.5.0.5-Beta

## 1. Hauptstartseite, Kopf und iOS-Safe-Area
1. Projekt über HTTP/HTTPS öffnen und als iOS-PWA zum Home-Bildschirm hinzufügen.
2. Auf einem iPhone mit Displayausschnitt/Dynamic Island prüfen, dass die obere Kante des abgerundeten PCT-Home-Pakets vollständig unterhalb der Statusleiste beginnt.
3. Im Querformat prüfen, dass zusätzlich die linke und rechte Safe Area eingehalten werden.
4. Prüfen, dass das PCT-Logo gegenüber V2.5.0.4-Beta deutlich größer ist.
5. Prüfen, dass der sichtbare weiße Text „SK PCT Tools“ neben dem Logo entfernt ist und `V2.5.0.5-Beta` weiterhin sinnvoll direkt am Logo steht.
6. Prüfen, dass die Suchlupe horizontal und vertikal exakt in ihrer 46 × 46 px beziehungsweise mobilen 42 × 42 px Schaltfläche zentriert ist.
7. Prüfen, dass Suche, Favoriten und alle 11 App-Icons innerhalb des abgerundeten Pakets liegen.

## 2. Hersteller-Hub der Wissensdatenbank
1. Wissensdatenbank öffnen; die Startansicht muss ausschließlich die Hersteller-Icons Air Torque, Endress+Hauser, Siemens, Vacon und Sonstiges zeigen.
2. Prüfen, dass keine Wissensbeitrags-Icons direkt im Hersteller-Hub stehen.
3. Jedes Hersteller-Icon öffnen und URL-Parameter, Titel, Beschreibung sowie Zurück-Navigation prüfen.
4. Zuordnung prüfen: Air Torque 1, Endress+Hauser 1, Siemens 2, Vacon 1, Sonstiges 0 Beiträge.
5. Sonstiges öffnen; der vorbereitete Leerzustand für Beiträge ohne Hersteller muss erscheinen.
6. Browser-Zurück/-Vorwärts zwischen Hub und Herstelleransichten prüfen.
7. Direktaufruf `wissensdatenbank/?manufacturer=siemens` online und offline prüfen.

## 3. Suche, Favoriten und Beitragsvorlage
1. Im Hub nach `Promass`, `Siemens`, `SCO` und `Vacon` suchen; jeweils muss das passende Hersteller-Icon übrig bleiben.
2. In der Siemens-Ansicht nach `P320`, `SPS` und `Rohwert` suchen.
3. Alle fünf Beiträge öffnen und unveränderte Inhalte sowie URLs prüfen.
4. Favorit hinzufügen/entfernen, Zähler prüfen und Favoritendrawer öffnen/schließen.
5. Mobil die Kompaktansicht in einer Herstelleransicht ein- und ausschalten.
6. „Beitrag vorschlagen“ öffnen und die PDF-Beitragsvorlage prüfen.

## 4. Hauptstartseite und bestehende Funktionen
1. Desktop: sechs Spalten, mittlere Breite: vier Spalten, Mobil: vier Spalten und bis 380 px: drei Spalten prüfen.
2. Alle 11 Apps und alle 11 eindeutigen Symbole prüfen.
3. Startseitensuche nach `Pt100`, `316L`, `SCO` und `Siemens` testen.
4. Kategorien Rechner, Dokumentation, Wissen und Externe Dienste prüfen.
5. Sortierung, Long-Press-Verschieben, Tastaturverschieben, Fertig und Zurücksetzen prüfen.
6. Alle sechs Rechner mit einer bekannten Eingabe testen.
7. Messstellen-Dokumentation sowie Einheiten- und Werkstoffdatenbank stichprobenartig prüfen.
8. E+H Device Viewer auf neuen Tab, `noopener`, `noreferrer` und externe Kennzeichnung prüfen.

## 5. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Browser in den Offline-Modus versetzen.
3. Startseite, alle internen Apps, Herstelleransichten und Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.0.5-Beta verwendet werden.

## 6. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
