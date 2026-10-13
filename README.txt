SK PCT Tools 2.5.2.1-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.2.0-Beta.

Änderungen dieser Beta
- Startseite und alle 15 internen Seiten verwenden jetzt exakt dieselbe
  Rechteckfläche, dieselbe Kopfgeometrie und dieselben Innenabstände.
- Jeder interne Header zeigt links – wie die Startseite – Logo und Version.
  Rechts bleiben die jeweils benötigten Aktionen erhalten.
- Der Footer ist auf allen Seiten gleich breit und gleich hoch. Schwarze Kontur,
  zusätzlicher Innenschatten und abweichende Hintergrundfläche wurden entfernt.
- Das Bemerkungsfeld der Messstellen-Dokumentation wurde deutlich verkleinert;
  auch die übrigen Formularabstände sind kompakter.
- Die Layoutregeln liegen abschließend in assets/design-system.css, damit ältere
  seitenspezifische Regeln Header und Footer nicht erneut überschreiben.
- Die Browserprüfung vergleicht Header, Footer und Außenrahmen jeder Unterseite
  direkt mit der Startseite und prüft den Footer zusätzlich auf Kontur/Schatten.

Erhaltene Funktionen und Inhalte
- 11 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Messstellen-Dokumentation und fünf Wissensbeiträge.
- Herstellerwege der Wissensdatenbank und PDF-Beitragsvorlage.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Version und PWA
- Öffentliche und technische Version: 2.5.2.1-Beta.
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
