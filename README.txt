SK PCT Tools 2.5.0.0-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte und vollständig übernommene Ausgangsbasis ist die veröffentlichte
Version 2.4.2.1.

Neuer PCT Home-Screen
- Die bisherige Kachelansicht wurde durch einen iOS-artigen PCT Home-Screen ersetzt.
- Alle sechs Rechner, alle drei Datenbanken/Wissensbereiche, die
  Messstellen-Dokumentation und der externe E+H Device Viewer besitzen ein eigenes,
  zur PCT-App-Icon-Familie passendes Symbol.
- Apps können über „Anordnen“ oder durch Gedrückthalten mit Finger oder Maus
  verschoben werden.
- Die eigene Reihenfolge wird ausschließlich lokal im Browser gespeichert.
- Im Anordnen-Modus sind auch Tastaturverschiebungen mit den Pfeiltasten möglich.
- „Standard“ stellt die ausgelieferte Reihenfolge wieder her.
- Eine kompakte App-Dichte steht für kleine Displays und dichte Übersichten bereit.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge und die PDF-Beitragsvorlage.
- Suche über Apps, Wissensbeiträge und Werkstoffbegriffe.
- Kategorienfilter, Sortierung, gemeinsames Zurücksetzen, Favoriten und
  Seitennavigation.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne URLs und abgesicherter externer Herstellerlink.

Version und PWA
- Öffentliche Version: 2.5.0.0-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.0.0-Beta.
- Laufzeitkanal: beta.
- Einstellungen: localStorage; es werden keine App-Reihenfolgen übertragen.

Deployment
1. Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
2. manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
3. Für lokale Tests einen HTTP-Server verwenden, z. B.:
   python3 -m http.server 8080
4. Anschließend http://localhost:8080/ öffnen.
5. SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.

Tests
- Automatische Struktur- und Integritätsprüfung:
  python3 tests/validate_project.py
- Manueller Testplan: TESTPLAN.md
