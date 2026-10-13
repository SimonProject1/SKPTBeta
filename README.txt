SK PCT Tools 2.5.2.0-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.1.4-Beta.

Änderungen dieser Beta
- Der E+H Device Viewer verweist auf die konkrete offizielle Device-Viewer-Adresse
  und ist sichtbar sowie technisch als externer Onlinedienst gekennzeichnet.
- Header und Footer verwenden auf Startseite und allen internen Seiten gemeinsame
  Größen, Abstände, Touchziele und Design-Tokens.
- Rechnerfelder bleiben mobil kompakt, zeigen vollständige Feldbezeichnungen und
  kurze Einheitensymbole; Ergebnisse nutzen einheitliche deutsche Praxisformate.
- Das Startseitenraster hat bis 430 px drei Spalten, saubere Titelumbrüche und
  mindestens 44 × 44 px große Favoriten-Touchflächen.
- Die Einheitendatenbank startet mit eingeklappten Kategorien, kompakten Zeilen,
  Favoriten oben, automatisch geöffneten Suchtreffern und Details auf Abruf.
- Der Werkstoffvergleich wird mobil als gestapelte Schlüssel-Wert-Darstellung gezeigt.
- Lange Wissensbeiträge zeigen eine Kurzantwort, aufklappbare Fachdetails und ein
  gebündeltes Quellen-/Gültigkeitsfeld; Sicherheitswarnungen bleiben sichtbar.
- Die CSS-Kaskade nutzt zentrale Design-Tokens und gemeinsame Komponenten. Veraltete
  Eskalationen wurden bereinigt; die Zahl der !important-Deklarationen wurde deutlich
  gegenüber der Ausgangsversion reduziert.

Erhaltene Funktionen und Inhalte
- 11 Startseiten-Apps, vollständige Navigation, Suche, Filter, Sortierung und Favoriten.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Messstellen-Dokumentation und fünf Wissensbeiträge.
- Herstellerwege der Wissensdatenbank und PDF-Beitragsvorlage.
- PWA-Installation, Offline-Kerncache, lokale Einstellungen und eigene App-Reihenfolge.

Version und PWA
- Öffentliche und technische Version: 2.5.2.0-Beta.
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
