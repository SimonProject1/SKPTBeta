SK PCT Tools 2.6.0.2-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.6.0.1-Beta.

Änderungen dieser Beta
- Alle sechs PNG-Rechner-Icons wurden aus einer gemeinsamen Mastergeometrie neu erzeugt.
- Der Taschenrechner ist deutlich kleiner und liegt vollständig innerhalb der definierten PNG-Safe-Zone.
- Zwischen Taschenrechner und gemeinsamem grün-blauen, schwarz konturierten App-Rahmen besteht nun ein klarer Innenabstand.
- Außenmaß, Rahmenstärke, Perspektive, Schatten und Favoritensternposition werden für Rechner-, Buch- und WWW-Icons unverändert zentral durch dieselbe App-Kachel gesteuert.
- Das PCT-Bereichsfeld ist genau einmal sichtbar, fest in die PNG-Datei integriert und nicht als HTML-/CSS-/JavaScript-Overlay vorhanden.
- Die Icon-Designrichtlinie enthält jetzt die verbindliche Rechner-Safe-Zone und gemeinsame Rahmenregeln.
- Statische und browserbasierte Regressionstests prüfen zusätzlich Rechner-Pixelgleichheit, Safe-Zone, Rahmengeometrie, Schatten und Sternposition.
- Öffentliche Version, Manifest, Offline-Cache, Cache-Busting-Parameter und Prüfsummen wurden auf 2.6.0.2-Beta aktualisiert.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige interne und externe Navigation, Suche, Filter, Sortierung und Favoritensterne.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- Hersteller-Hub mit fünf Herstellerzielen.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.
- 17 transparente PNG-Navigationsgrafiken in 512 × 512 px.

Iconpflege
- Ausgelieferte Navigationsicons: assets/navigation-icons/*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Betroffene Rechner-PNGs: app-analogsignal.png, app-pf-rechner.png, app-pt-rechner.png, app-einheitenrechner.png, app-spannungsfall.png und app-siemens-rohwert.png.
- Das Fachbereichsfeld wird ausschließlich in der PNG-Datei erzeugt.
- Die einzige zulässige SVG-Datei ist assets/pct-controls.svg für kleine, nicht navigierende Bedienpiktogramme.

Version und PWA
- Öffentliche und technische Version: 2.6.0.2-Beta.
- Laufzeitkanal: beta.
- Einstellungen bleiben lokal im Browser; es erfolgt keine Übertragung durch SK PCT Tools.

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. manifest.webmanifest und service-worker.js im Projektstamm belassen.
3. SECURITY-DEPLOYMENT.md für serverseitige Sicherheitsheader beachten.
4. Lokaler Test: python3 -m http.server 8080
5. Anschließend http://localhost:8080/ öffnen.
6. SHA256SUMS.txt enthält die SHA-256-Prüfsumme jeder weiteren Projektdatei.

Tests
- Statische Struktur-/Integritätsprüfung: python3 tests/validate_project.py
- Browser-Regression (Playwright): python3 tests/browser_regression.py
- Manueller Abnahmeplan: TESTPLAN.md
