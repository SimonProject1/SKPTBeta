SK PCT Tools 2.5.2.3-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige 2.5.2.2-Beta.

Änderungen dieser Beta
- Pt100/Pt1000 prüft den IEC-60751-Bereich von -200 bis 850 °C in beiden Rechenrichtungen.
- Der Spannungsfall-Ergebnisblock respektiert das hidden-Attribut im Start- und Reset-Zustand.
- Messstellen-Dokumentation wurde vollständig aus Startseite, Offline-Cache, Tests und Paket entfernt.
- Die PDF-Beitragsvorlage und der zugehörige Download wurden entfernt; neue Beiträge werden über den Projektchat strukturiert.
- Wissensbeiträge kennzeichnen Praxiswissen als „Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)“.
- Startseite und Weiterleitungsseite besitzen eine semantische H1; Referrer-Schutz und Deployment-Hinweise wurden ergänzt.
- Nicht mehr benötigte CSS-Regeln des entfernten Moduls wurden bereinigt.

Erhaltene Funktionen und Inhalte
- 10 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank sowie fünf Wissensbeiträge.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Version und PWA
- Öffentliche und technische Version: 2.5.2.3-Beta.
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
