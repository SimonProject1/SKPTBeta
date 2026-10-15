SK PCT Tools 2.6.0.4-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.6.0.3-Beta.

Änderungen dieser Beta
- Alle 17 transparenten PNG-Navigationsgrafiken wurden als deutlich entschlackte Cartoon-Tech-Serie neu erzeugt.
- Die integrierten Felder RECHNER, WISSEN, MATERIAL, EXTERN und PCT wurden aus den PNGs entfernt.
- Ein Icon besteht verbindlich aus einem gemeinsamen schwarzen Außenrahmen, einem klaren Hauptmotiv und einem kleinen Favoritenstern; die Erklärung steht ausschließlich im Titel darunter.
- Taschenrechner: großes Display, sechs große Tasten und deutliches ±.
- Buch: zwei klare farbige Seiten und schwarze Mittelfalte.
- Weltkugel: klare Längen-/Breitengrade und kleines WWW.
- Hersteller-Kurzmarken, Home und Zurück wurden ebenfalls ohne Kategoriefelder neu erzeugt.
- Nur ein Blau-Cyan-Grün-Rahmenbogen, ein dezenter Tiefenversatz und ein ruhiger Schlagschatten; keine doppelte Leuchtkontur oder Leiterbahndetails.
- Sichtbarer Favoritenkreis von 28 auf 22 px verkleinert; unsichtbare Touchfläche bleibt 44 × 44 px.
- Favorit inaktiv ruhig, aktiv grün leuchtend.
- Titelkontur feiner; Startseitentitel Umrechnen, Siemens RAW, Werkstoffe und Wissen gekürzt.
- Drei-Spalten-Raster auf dem iPhone bleibt erhalten.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige interne und externe Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- Hersteller-Hub mit fünf Herstellerzielen.
- Eigene App-Reihenfolge und lokale Einstellungen.
- PWA-Installation und Offline-Kerncache.
- Smartphone-, Tablet-, Desktop- und 320-px-Reflow-Unterstützung.

Iconpflege
- Navigationsicons: assets/navigation-icons/*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Format: 512 × 512 px, RGBA, transparenter Hintergrund.
- Sechs Rechner-PNGs sind pixelidentisch.
- Drei Buch-PNGs sind pixelidentisch.
- Kategoriefelder dürfen weder in PNGs noch als sichtbare HTML-/CSS-/JavaScript-Overlays erscheinen.
- Einzige zulässige SVG-Datei: assets/pct-controls.svg für kleine Bedienpiktogramme.

Version und PWA
- Öffentliche und technische Version: 2.6.0.4-Beta.
- Laufzeitkanal: beta.
- Service-Worker-Cache: sk-pct-tools-*-v2.6.0.4-Beta.
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
