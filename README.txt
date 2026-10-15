SK PCT Tools 2.6.0.3-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.6.0.2-Beta.

Änderungen dieser Beta
- Vollständig alternative, neu gezeichnete Serie aller 17 transparenten PNG-Navigationsgrafiken.
- Hochwertigere Cartoon-Tech-Motive mit schwarzer Kontur, klaren Verläufen, Glanzkante, Schatten und plastischer Tiefenwirkung.
- Funktionsmotiv: Taschenrechner für Rechner, aufgeschlagenes Buch für interne Nachschlagewerke, WWW-Weltkugel mit Auswärtspfeil für externe Ziele.
- Genau ein integriertes Kategoriefeld je fachlich gekennzeichnetem PNG: RECHNER, WISSEN, EXTERN, MATERIAL oder bei Hersteller-Kurzmarken PCT.
- Keine zusätzlichen HTML-, CSS- oder JavaScript-Overlays für Kategoriefelder.
- Gemeinsamer grün-blauer Außenrahmen, Außenmaße, Perspektive, Schatten, Innenabstand und Favoritensternposition bleiben unverändert in der Oberfläche vereinheitlicht.
- Icon-Designrichtlinie, statische Prüfung, Browser-Regression, Offline-Cache, Cache-Busting-Parameter und Prüfsummen wurden aktualisiert.

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
- Sechs Rechner-PNGs: identischer Taschenrechner mit integriertem Feld RECHNER.
- app-einheitendatenbank.png und app-wissensdatenbank.png: Buch mit WISSEN.
- app-werkstoffdatenbank.png: Buch mit MATERIAL.
- app-eh-viewer.png: WWW-Weltkugel mit EXTERN.
- Hersteller-PNGs: ausschließlich weiße Kurzmarke beziehungsweise Name mit PCT.
- Das Kategoriefeld wird ausschließlich in den PNG-Pixeln erzeugt.
- Einzige zulässige SVG-Datei: assets/pct-controls.svg für kleine, nicht navigierende Bedienpiktogramme.

Version und PWA
- Öffentliche und technische Version: 2.6.0.3-Beta.
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
