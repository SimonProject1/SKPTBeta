# Testplan · SK PCT Tools 2.6.1.2-Beta

## 1. Automatische Prüfungen

```bash
python3 tests/validate_project.py
python3 tests/browser_regression.py
```

Profile: Smartphone 390 × 844, Reflow 320 × 900, Tablet 820 × 1180 und Desktop 1440 × 1000.

## 2. Dateibestand und Altpfade
1. Genau 17 Dateien unter `assets/navigation-icons/` prüfen.
2. Jeder Dateiname muss mit `v2-6-1-2-` beginnen; Dateien der Serie `v2-6-1-1-` und unversionierte Altdateien dürfen nicht vorhanden sein.
3. Keine Navigations-SVGs, Daten-URIs, CSS-Hintergrundbilder oder JavaScript-Fallbackpfade zulassen.
4. Einzige SVG-Datei im Paket: `assets/pct-controls.svg` für aktive Bedienpiktogramme.
5. Alle lokalen HTML-/CSS-/JS-/JSON-/Manifest-Verweise müssen auf vorhandene Dateien zeigen.

## 3. Icon-Inhalt und Außenform
1. Alle 17 PNGs: 512 × 512 px, RGBA, transparente und deckende Pixel.
2. Identische Alpha-Außenmaße, Rundung, Schattenlage und kräftige schwarze Außenkontur.
3. Hintergrundprobe links grünbetont und oben rechts blaubetont; weicher sichtbarer Verlauf ohne Neonüberladung.
4. Keine kurzen inneren Linien, Rahmenbögen oder zweite CSS-Rahmenebene.
5. Weiße/hellgraue Funktionsmotive mit deutlich sichtbarer schwarzer Comic-Umrandung.
6. Sechs Rechnerdateien müssen pixelidentisch sein; drei Buchdateien ebenfalls.
7. Rechner: Displayfeld und sechs große unbeschriftete Tasten, ohne Zahlen oder Kleinsttext.
8. Buch: einfaches weißes Nachschlagewerk, ohne farbige Seiten oder Textzeilen.
9. WWW: weiße Weltkugel mit wenigen Koordinatenlinien.
10. Hersteller-, Home- und Zurück-Icons verwenden denselben Hintergrund- und Konturmaster.
11. Keine sichtbaren Kategoriefelder in PNG, HTML, CSS oder JavaScript.

## 4. Favoriten
1. Startseite und Wissens-App-Karten: Touchfläche mindestens 44 × 44 px.
2. Sichtbarer Kreis 22 × 22 px, einheitlich oben rechts am Icon.
3. Inaktiv: weiß/hellgrau, kein grünes Leuchten.
4. Aktiv: grün mit dezenter grüner Innenkante und Leuchtring.
5. Tap, Tastaturfokus, Hinzufügen, Entfernen, Zähler und Favoritenleiste prüfen.

## 5. PWA, Manifest und Cache
1. `manifest-v2-6-1-2.webmanifest`, Version und drei Shortcut-Icons prüfen.
2. Service Worker über die releasebezogene Registrierungs-URL laden.
3. Nur Caches mit Epoch `v2-6-1-2-icons-r1` behalten; ältere `sk-pct-tools-*`-Caches müssen gelöscht werden.
4. Prüfen, dass `ignoreSearch:true` nicht für Assets verwendet wird.
5. Online laden, Worker aktivieren, anschließend Startseite, Rechner, Wissensdatenbank und Wissensbeitrag offline öffnen.
6. Neuinstallation mit leerem Storage sowie Aktualisierung aus einem simulierten Alt-Cache prüfen.

## 6. Navigation und responsive Darstellung
1. Startseite, Wissensdatenbank, Hersteller-Hub und alle internen Unterseiten öffnen.
2. Home, Zurück, externe E+H-Navigation, Suche, Filter, Sortierung und eigene App-Reihenfolge prüfen.
3. Auf 390 × 844, 320 × 900, 820 × 1180 und 1440 × 1000 auf horizontales Überlaufen, abgeschnittene Titel und überlagerte Touchflächen prüfen.
4. Hoch-/Querformat und Safe Areas kontrollieren.

## 7. Funktionsregression
1. Analogsignal: 0…100 und 4…20 mA; 50 ergibt 12 mA und 50 %.
2. P+F: (0|4) und (100|20); K-Faktor 0,16, Nullpunkt 4.
3. Pt100: 0 °C ergibt ungefähr 100 Ω; Bereichsgrenzen prüfen.
4. Einheiten: 1 bar ergibt 100 kPa.
5. Siemens: 12 mA bei -50…150 °C ergibt Rohwert 13.824 und 50 °C.
6. Spannungsfall: Referenzfall ungefähr 6,93 V / 1,73 % / 393,07 V.
7. Einheitendatenbank, Werkstoffdatenbank und fünf Wissensbeiträge vollständig prüfen.

## 8. Finales ZIP
1. ZIP erstellen und in ein leeres Verzeichnis entpacken.
2. Strukturprüfung und beide automatischen Tests gegen den entpackten Inhalt wiederholen.
3. Icon-Inventar, Altpfade und SHA256SUMS.txt erneut prüfen.
4. SHA-256 des ZIPs separat erzeugen und mit dem ausgelieferten Wert vergleichen.
