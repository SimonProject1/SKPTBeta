SK PCT Tools 2.5.2.2-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.2.1-Beta.

Änderungen dieser Beta
- Der ±-Taster des Siemens-Rohwertrechners ist jetzt ein kompakter runder
  42-px-Schalter im gemeinsamen Cyan-/Grün-Design statt einer vollflächigen Wippe.
- Hauptwert, Minimum und Maximum verwenden dieselbe Tastergeometrie mit klaren
  Fokus-, Hover- und Aktivzuständen.
- Der Siemens-Rechner besitzt einen eindeutigen internen vertikalen Scrollbereich.
  Kopf und Footer bleiben im App-Rahmen stehen, während der vollständige Inhalt
  per Touch, Mausrad oder Tastatur bewegt werden kann.
- Die Scrollkorrektur verhindert besonders auf kleinen iPhone-/iPad-Höhen und im
  Querformat, dass Rechnerbereiche zusammengedrückt oder abgeschnitten werden.
- Statische Prüfung und Browser-Regression kontrollieren Tastergeometrie,
  Vorzeichenfunktion, Inhaltsüberlauf und tatsächliche Scrollbewegung.

Erhaltene Funktionen und Inhalte
- 11 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Messstellen-Dokumentation und fünf Wissensbeiträge.
- Herstellerwege der Wissensdatenbank und PDF-Beitragsvorlage.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Version und PWA
- Öffentliche und technische Version: 2.5.2.2-Beta.
- Laufzeitkanal: beta.
- Einstellungen bleiben lokal im Browser; es erfolgt keine Übertragung durch SK PCT Tools.

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. manifest.webmanifest und service-worker.js im Projektstamm belassen.
3. Lokaler Test: python3 -m http.server 8080
4. Anschließend http://localhost:8080/ öffnen.
5. SHA256SUMS.txt enthält die SHA-256-Prüfsumme jeder weiteren Projektdatei.

Tests
- Statische Struktur-/Integritätsprüfung: python3 tests/validate_project.py
- Browser-Regression (Playwright): python3 tests/browser_regression.py
- Manueller Abnahmeplan: TESTPLAN.md
