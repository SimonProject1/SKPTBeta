SK PCT Tools 2.6.0.0-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.5.2.4-Beta.

Änderungen dieser Beta
- Neuer verbindlicher PNG-Iconstandard mit 17 transparenten Navigationsgrafiken in 512 × 512 px.
- Alle Rechner und Umrechnungen verwenden einen Taschenrechner mit Bereichsfeld PCT.
- Wissensdatenbank, Wissensbeiträge und Einheitendatenbank verwenden ein Buch mit Bereichsfeld PCT.
- Die Werkstoffdatenbank verwendet ein Buch mit Bereichsfeld PIPING.
- Externe Dienste verwenden eine WWW-Weltkugel mit Auswärtspfeil und fachlich passendem Bereichsfeld.
- Im Hersteller-Hub bleiben ausschließlich weiße Herstellernamen/Kurzmarken plus PCT-Feld sichtbar.
- Startseite, Wissensdatenbank, Navigation, Manifest und Offline-Cache sind auf PNG umgestellt.
- Nicht mehr benötigte SVG-Navigationsdateien und Referenzen wurden entfernt.
- CSA und EQP sind nur in ICON-DESIGNRICHTLINIE.txt als zukünftige Kategorien dokumentiert und werden ohne echte Inhalte nicht verwendet.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Iconpflege
- Ausgelieferte Navigationsicons: assets/navigation-icons/*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Die einzige vorläufig verbleibende SVG-Datei ist assets/pct-controls.svg für kleine, nicht navigierende Bedienpiktogramme.

Version und PWA
- Öffentliche und technische Version: 2.6.0.0-Beta.
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
