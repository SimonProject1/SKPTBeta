# Testplan · SK PCT Tools 2.6.1.3-Beta

## 1. Automatische Prüfungen

```bash
python3 tests/validate_project.py
python3 tests/browser_regression.py
```

Profile: Smartphone 390 × 844, Reflow 320 × 900, Tablet 820 × 1180 und Desktop 1440 × 1000.

## 2. Dateibestand und Altpfade
1. Genau 17 Dateien unter `assets/navigation-icons/` prüfen.
2. Jeder Dateiname muss mit `v2-6-1-3-` beginnen; Serien `v2-6-1-2-`, `v2-6-1-1-` und unversionierte Altdateien dürfen nicht vorhanden sein.
3. Keine Navigations-SVGs, Daten-URIs, CSS-Hintergrundbilder oder dynamischen JavaScript-Fallbackpfade zulassen.
4. Einzige SVG-Datei im Paket: `assets/pct-controls.svg` für Bedienpiktogramme.
5. Alle lokalen HTML-/CSS-/JS-/JSON-/Manifest-Verweise müssen auf vorhandene Dateien zeigen.

## 3. Unveränderter Hintergrundmaster
1. Alle 17 PNGs: 512 × 512 px, RGBA, transparente und deckende Pixel.
2. Identische Alpha-Außenmaße, Rundung, Schattenlage und schwarze Rahmenkontur.
3. Linke Probe grünbetont und obere rechte Probe blaubetont; weicher Verlauf ohne Neonüberladung.
4. Geschützte Randzone jedes PNGs gegen den V2.6.1.2-Referenzhash `63f387a45785714c19b416ffbabe702908b9b873e4918f4cd846a3bd638aad10` prüfen.
5. Keine zweite CSS-Rahmenebene, kurzen Akzentlinien oder zusätzlichen Hintergrundvarianten.

## 4. Symbolraster, Zentrierung und visuelle Masse
1. Gemeinsames Raster x=112…400, y=106…386; maximale Abmessung 288 × 280 px.
2. Optischer Zielmittelpunkt (256, 246); Weißflächen-Boundingbox jedes Motivs höchstens 3 px Abweichung pro Achse.
3. Motivfläche je Iconklasse 20.000…55.000 deckend weiße Pixel.
4. Äußere schwarze Comic-Kontur 16 px, innere geschlossene Details 10 px.
5. Konturen geschlossen und rund geführt; keine versetzten Drop-Shadows, Doppelkonturen oder ungleichmäßigen schwarzen Flächen.
6. Weiße Innenflächen geschlossen; Hintergrund darf nicht unbeabsichtigt durch Motivflächen scheinen.
7. Sechs Rechnerdateien pixelidentisch; drei Buchdateien pixelidentisch.
8. Rechner: ein Display und sechs gleich große Tasten in symmetrischem 3×2-Raster.
9. Buch: zwei spiegelgleiche weiße Seiten, klare einzelne Mittelfalte.
10. WWW: symmetrischer Kreis, wenige Koordinatenlinien, geschlossenes Mittelband; WWW bei kleiner Darstellung lesbar.
11. Hersteller: fünf gleich große weiße Namensfelder auf identischem Mittelpunkt.
12. Home und Zurück: geschlossene weiße Piktogramme auf demselben Raster.
13. Keine sichtbaren Kategoriefelder in PNG, HTML, CSS oder JavaScript.

## 5. Favoriten
1. Startseite und Wissens-App-Karten: Touchfläche mindestens 44 × 44 px.
2. Sichtbarer Kreis 22 × 22 px, einheitlich oben rechts am Icon.
3. Hauptsymbol ohne Rücksicht auf den Stern zentriert; Stern darf Symbolposition und -größe nicht verändern.
4. Inaktiv: hell, kein grünes Leuchten.
5. Aktiv: grün mit dezenter grüner Innenkante und Leuchtring.
6. Tap, Tastaturfokus, Hinzufügen, Entfernen, Zähler und Favoritenleiste prüfen.

## 6. PWA, Manifest und Cache
1. `manifest-v2-6-1-3.webmanifest`, Version und drei Shortcut-Icons prüfen.
2. Service Worker über die releasebezogene Registrierungs-URL laden.
3. Nur Caches mit Epoch `v2-6-1-3-icons-r1` behalten; ältere `sk-pct-tools-*`-Caches löschen.
4. Prüfen, dass `ignoreSearch:true` nicht für Assets verwendet wird.
5. Online laden, Worker aktivieren, anschließend Startseite, Rechner, Wissensdatenbank und Wissensbeitrag offline öffnen.
6. Neuinstallation mit leerem Storage sowie Aktualisierung aus einem simulierten Alt-Cache prüfen.

## 7. Nebeneinander- und Responsive-Vergleich
1. Alle Startseitenicons nebeneinander auf 390 × 844, 820 × 1180 und 1440 × 1000 erfassen.
2. Hersteller- und Beitragsicons in der Wissensdatenbank auf denselben Viewports erfassen.
3. Je Ansicht Zentrierung, Konturstärke, Weißflächen, Größenverhältnis, WWW-Lesbarkeit und Sternposition kontrollieren.
4. Auf 320 × 900 horizontalen Reflow, abgeschnittene Titel und überlagerte Touchflächen prüfen.
5. Hoch-/Querformat und Safe Areas kontrollieren.
6. Home, Zurück, externe E+H-Navigation, Suche, Filter, Sortierung und eigene App-Reihenfolge prüfen.

## 8. Funktionsregression
1. Analogsignal: 50 % ergibt 12 mA.
2. P+F: K-Faktor 0,16 und Nullpunkt 4.
3. Pt100: 0 °C ergibt ungefähr 100 Ω; Bereichsgrenzen prüfen.
4. Einheiten: 1 bar ergibt 100 kPa.
5. Siemens: 12 mA bei -50…150 °C ergibt Rohwert 13.824 und 50 °C.
6. Spannungsfall: Referenzfall ungefähr 6,93 V / 1,73 % / 393,07 V.
7. Einheitendatenbank, Werkstoffdatenbank und fünf Wissensbeiträge vollständig prüfen.

## 9. Finales ZIP
1. SHA256SUMS.txt über alle Projektdateien außer sich selbst neu erzeugen.
2. ZIP erstellen und in ein leeres Verzeichnis entpacken.
3. Strukturprüfung und beide automatischen Tests gegen den entpackten Inhalt wiederholen.
4. Icon-Inventar, Altpfade, Hintergrundhash und interne Prüfsummen erneut prüfen.
5. SHA-256 des ZIPs separat erzeugen und mit dem ausgelieferten Wert vergleichen.
