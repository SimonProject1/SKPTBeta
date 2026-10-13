# Testplan · SK PCT Tools 2.5.1.4-Beta

## 1. Hauptstartseite ohne Dokument-Scroll
1. Projekt über HTTP/HTTPS öffnen und optional als iOS-PWA installieren.
2. Im Hoch- und Querformat wischen: Die Startseite darf nicht als Dokument scrollen.
3. Logo, Version `V2.5.1.4-Beta`, Suche, Favoriten, 11 App-Icons und Footer müssen im Rahmen bleiben.
4. iPhone/iPad: Statusleiste, Dynamic Island und Home-Indikator-Safe-Area prüfen.

## 2. Einheitlicher Rahmen und internes Scrollen
1. Alle sechs Rechner, Datenbanken, Dokumentation und fünf Wissensbeiträge öffnen.
2. Außenbreite, Ober-/Unterkante, Rundung und Seitenabstand mit Home vergleichen.
3. Nur `.sk-app-scroll` darf auf Unterseiten scrollen; Header und Footer bleiben sichtbar.
4. Favoriten-, Zurück- und Home-Schalter dürfen nicht umbrechen oder das Logo überlagern.
5. Am Anfang und Ende jedes Inhalts prüfen, dass nichts abgeschnitten ist.

## 3. Kritischer Test: Wissensnavigation
1. Wissensdatenbank über die Startseite öffnen.
2. Air Torque öffnen und den Beitrag `Drehrichtung` aufrufen.
3. Endress+Hauser öffnen und `Einbaulage` aufrufen.
4. Siemens öffnen und beide Beiträge nacheinander aufrufen.
5. Vacon öffnen und den Frequenzumrichter-Beitrag aufrufen.
6. Auf jeder Karte getrennt Kartenfläche und Favoritenstern testen.
7. Browser-Zurück, `Alle Hersteller`, Kopf-Zurück und Home testen.
8. Direkt mit `/wissensdatenbank/?manufacturer=siemens` starten.
9. Falls der Server es zulässt, die Wissensdatenbank auch über `index.html` testen.
10. Den Ablauf online, nach PWA-Installation und anschließend offline wiederholen.

## 4. Kompakte Rechnerseiten
1. Analogsignal-, P+F-, Pt100/Pt1000-, Einheiten-, Spannungsfall- und Siemens-Rohwert-Rechner öffnen.
2. Desktop ab 1000 px: Standardrechner zeigen Eingaben links und Ergebnisse rechts.
3. Desktop: bis zu vier Eingabefelder pro Reihe prüfen; keine Überlagerung oder abgeschnittene Auswahltexte.
4. Tablet 761–999 px: dreispaltige Eingaben und vollständig erreichbare Ergebnisse prüfen.
5. Smartphone 341–760 px: zweispaltige Eingaben, lesbare Labels und Touch-Ziele ≥ 42 px prüfen.
6. Sehr schmal unter 341 px: sicherer einspaltiger Rückfall ohne horizontales Scrollen.
7. Einheitendatenbank-Leiste muss flach bleiben und vollständig bedienbar sein.
8. Bildschirmtastatur auf iPhone prüfen: fokussiertes Feld bleibt erreichbar.

## 5. Rechner-Funktionstest
1. Analogsignal: 0…100 °C und 4…20 mA; 50 °C muss 12 mA ergeben.
2. P+F: (0|4) und (100|20); K-Faktor 0,16 und Nullpunkt 4 prüfen.
3. Pt100: 0 °C muss ungefähr 100 Ω ergeben.
4. Einheitenrechner: 1 bar in kPa muss 100 kPa ergeben.
5. Spannungsfall: gültige Strom-, Längen- und Querschnittswerte eingeben; Status, fünf Ergebnisse, Formel und Protokoll prüfen.
6. Siemens Rohwert: 4–20 mA, 12 mA und −50…150 °C; Rohwert 13.824 und physikalisch 50 °C prüfen.
7. Vorzeichen-, Reset-, Berechnen- und Kopierknöpfe testen.

## 6. Übrige Inhalte und Funktionen
1. Einheitensuche/Favoriten, Werkstoffsuche/Gruppenfilter und Direktvergleich prüfen.
2. Messstellen-Dokumentation einschließlich Fotos, Löschen, Reset und PDF-Druck prüfen.
3. PDF-Beitragsvorlage herunterladen.
4. E+H Device Viewer auf neuen Tab, `noopener`, `noreferrer` und externe Kennzeichnung prüfen.

## 7. PWA und Offline
1. Seite online laden und Service-Worker-Installation abwarten.
2. Offline-Modus aktivieren.
3. Startseite, Rechner, Herstelleransichten und alle Wissensbeiträge öffnen.
4. Prüfen, dass nur Caches der Version 2.5.1.4-Beta verwendet werden.

## 8. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
