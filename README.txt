SK PCT Tools 2.6.0.1-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.6.0.0-Beta.

Änderungen dieser Beta
- Doppelte Fachbereichskennzeichnungen auf den neuen PNG-Navigationsicons entfernt.
- Startseite und externer E+H Device Viewer erzeugen kein zusätzliches PCT-Feld mehr per CSS-Pseudoelement.
- Wissensdatenbank und Hersteller-Hub enthalten weder CSS-, HTML- noch JavaScript-Badges für PCT, PIPING, CSA oder EQP.
- Pro Navigationsicon ist ausschließlich das fest in der PNG-Datei integrierte Fachbereichsfeld sichtbar.
- Die Icon-Designrichtlinie verbietet zusätzliche Bereichsfelder per HTML, CSS und JavaScript verbindlich.
- Statische und browserbasierte Regressionstests erkennen künftige Icon-Overlays automatisch.
- Öffentliche Version, Manifest, Cacheversion und alle Cache-Busting-Parameter wurden auf 2.6.0.1-Beta aktualisiert.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige interne und externe Navigation, Suche, Filter, Sortierung und Favoritensterne.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- Hersteller-Hub mit fünf Herstellerzielen.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.
- 17 transparente PNG-Navigationsgrafiken in 512 × 512 px; die PNG-Dateien selbst wurden nicht verändert.

Iconpflege
- Ausgelieferte Navigationsicons: assets/navigation-icons/*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Das Fachbereichsfeld wird ausschließlich in der PNG-Datei erzeugt.
- Die einzige vorläufig verbleibende SVG-Datei ist assets/pct-controls.svg für kleine, nicht navigierende Bedienpiktogramme.

Version und PWA
- Öffentliche und technische Version: 2.6.0.1-Beta.
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
