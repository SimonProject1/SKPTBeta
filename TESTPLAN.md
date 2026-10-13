# Testplan · SK PCT Tools 2.5.1.2-Beta

## 1. Hauptstartseite ohne Dokument-Scroll
1. Projekt über HTTP/HTTPS öffnen und optional als iOS-PWA installieren.
2. Im Hochformat nach oben und unten wischen: Die Startseite darf weder scrollen noch Gummibandverhalten zeigen.
3. Im Querformat seitlich und vertikal wischen: Es darf kein Dokument-Scroll entstehen.
4. Prüfen, dass Logo, Version `V2.5.1.2-Beta`, Suche, Favoriten, alle 11 App-Icons und Footer innerhalb des abgerundeten Rechtecks bleiben.
5. Prüfen, dass die Symbole der obersten App-Reihe ihre gewohnte Position behalten und das Rechteck bis an die untere Displaykante reicht.
6. iPhone/iPad prüfen: Statusleiste und Dynamic Island werden nicht überlagert; die Home-Indikator-Safe-Area liegt innerhalb des Footers.
7. Suche öffnen: Nur das Such-Overlay darf bei Bedarf intern scrollen.

## 2. Einheitliches Rechteck und internes Scrollen
1. Alle sechs Rechner, Messstellen-Dokumentation, Einheiten- und Werkstoffdatenbank öffnen.
2. Wissensdatenbank und alle fünf Wissensbeiträge öffnen.
3. Startseite und jede Unterseite bei identischer Viewportgröße direkt vergleichen: Außenbreite, Oberkante, Unterkante, Rundung und Seitenabstand müssen exakt übereinstimmen.
4. Auf jeder Unterseite prüfen: Der Browser-Body bleibt fest; nur der mittlere Inhaltsbereich scrollt.
5. Logo prüfen: Das originale S.K.-PCT-Logo bleibt auf Home und jeder Unterseite oben links sichtbar; auf Desktop darf der Home-Kopf nicht mehr als kompakte Gruppe mittig stehen.
6. Favoriten, Zurück und Startseite bleiben gemeinsam oben rechts; kein Schalter darf auf mobilen Breiten umbrechen oder das Logo überlagern.
7. Der Unterseitenkopf darf kein separates vollflächiges dunkles Querband mehr bilden, sondern muss optisch in der Rechteckfläche liegen.
8. Kopf und Footer müssen während des internen Scrollens sichtbar im abgerundeten Rechteck bleiben.
9. Rahmen, schwarze Kontur, Cyan-Innenkante und Hintergrund müssen auf allen Seiten konsistent sein.
10. Karten, Panels, Buttons, Such-/Filterfelder, Eingaben und Wissensbeiträge auf durchgehend runde Ecken prüfen; abgeschrägte Clip-Path-Ecken dürfen nicht mehr sichtbar sein.
11. Hochformat, Querformat, Desktop, Tablet und Smartphone testen.
12. Am Anfang und Ende des Inhalts prüfen, dass kein Inhalt abgeschnitten oder unerreichbar ist.

## 3. Icons, Buttons und Navigation
1. Favoriten-, Zurück- und Startseiten-Schalter in jeder Unterseiten-Kopfzeile prüfen.
2. Favorit hinzufügen/entfernen, Zähler und Favoritendrawer testen.
3. Berechnen-, Reset-, Druck-, Löschen-, Kopieren-, Datenbank-, Download- und Fertig-Symbole prüfen.
4. Tastaturfokus, Enter/Leertaste und sichtbare Fokusmarkierung prüfen.
5. Mindestgröße der Touch-Ziele auf Smartphone prüfen.

## 4. Startseite, Suche und App-Anordnung
1. Desktop: sechs Spalten und zwei Icon-Reihen prüfen.
2. Smartphones: vier Spalten und drei Reihen prüfen; kein abgeschnittenes Icon.
3. Smartphone-Querformat: sechs kompakte Spalten und zwei Reihen prüfen.
4. Nach `Pt100`, `316L`, `SCO` und `Siemens` suchen.
5. Kategorienfilter, Sortierung und Zurücksetzen prüfen.
6. Long-Press-Verschieben, Tastaturverschieben, Fertig und Anordnung zurücksetzen prüfen.

## 5. Inhalte und Funktionen
1. Alle sechs Rechner mit bekannten Eingaben testen.
2. Einheitenfavoriten, Einheitensuche und Umrechnung prüfen.
3. Werkstoffsuche, Gruppenfilter und Direktvergleich prüfen.
4. Messstellen-Dokumentation einschließlich Fotos, Löschen, Reset und PDF-Druck prüfen.
5. Hersteller-Hub prüfen: Air Torque 1, Endress+Hauser 1, Siemens 2, Vacon 1, Sonstiges 0 Beiträge.
6. Alle fünf Wissensbeiträge und die PDF-Beitragsvorlage öffnen.
7. E+H Device Viewer auf neuen Tab, `noopener`, `noreferrer` und externe Kennzeichnung prüfen.

## 6. PWA und Offline
1. Seite einmal online laden und Service-Worker-Installation abwarten.
2. Offline-Modus aktivieren.
3. Startseite, alle internen Apps, Herstelleransichten und Wissensbeiträge öffnen.
4. Prüfen, dass `assets/pct-frame.css` offline verfügbar ist.
5. Prüfen, dass nur Caches der Version 2.5.1.2-Beta verwendet werden.

## 7. Automatische Prüfung
```bash
python3 tests/validate_project.py
```
Erwartung: `PASS` ohne Fehler.
