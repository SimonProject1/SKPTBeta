SK PCT Tools 2.5.2.4-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.5.2.3-Beta.

Änderungen dieser Beta
- Der runde Plus/Minus-Taster des Siemens-Rohwert-Rechners ist jetzt der verbindliche zentrale Standard für alle Vorzeichenfelder.
- Einheitliche 44 × 44 px Bedienfläche, zentrierte Ausrichtung, sichtbarer Fokus, Hover-/Druckzustand und touch-action: manipulation.
- Vorzeichenwechsel wurde per Touch auf Smartphone und Tablet sowie im responsiven Desktop-Layout geprüft.
- 17 eigenständige SVG-Navigationsgrafiken im SK-PCT-Tools-Cartoon-Tech-Stil ersetzen die bisherigen Startseiten- und Hersteller-Sprites.
- Startseite, Wissens-Herstellerkarten, Kopfzeilen-Navigation, Zurück-Aktion, Einheitendatenbank-CTA und Manifest-Shortcuts verwenden die neuen Grafiken.
- ICON-DESIGNRICHTLINIE.txt dokumentiert verbindlich Form, Konturen, Farben, Licht, Abstände, Herstellerkennzeichnungen, Zustände, Größen, Formate, Transparenz, Benennung und Einbindung.
- Sämtliche neuen Grafiken und die Richtlinie sind in die PWA-/Offline-Konfiguration aufgenommen.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Version und PWA
- Öffentliche und technische Version: 2.5.2.4-Beta.
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
