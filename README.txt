SK PCT Tools 2.5.1.1-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.1.0-Beta.

Änderungen dieser Beta
- Das App-Raster der Startseite nutzt wieder eine feste Bezugsfläche. Dadurch
  bleiben insbesondere die Symbole der obersten Reihe an ihrer gewohnten Position.
- Das abgerundete Startseiten-Rechteck reicht bis an die untere Displaykante.
  Die iOS-Safe-Area wird jetzt innerhalb des Footers statt außerhalb des Rahmens gehalten.
- Alle Unterseiten verwenden konsequent die neue runde Formensprache.
- Alte abgeschrägte Ecken und Clip-Path-Kanten wurden für Karten, Panels, Buttons,
  Suche, Filter, Eingabefelder, Datenbankzeilen und Wissensbeiträge zentral entfernt.
- Kopfzeile und Footer schließen mit passenden Rundungen an den gemeinsamen App-Rahmen an.
- Rechnerfelder, Favoriten, Wissenskarten, Tabellen und Aktionsschalter wurden optisch vereinheitlicht.

Erhaltene Funktionen und Inhalte
- Alle 11 Startseiten-Apps und ihre eindeutigen App-Icons.
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Alle fünf fachlichen Wissensbeiträge und die PDF-Beitragsvorlage.
- Startseitensuche, Kategorienfilter, Sortierung, Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne Beitrags-URLs und abgesicherter externer Herstellerlink.

Version und PWA
- Öffentliche Version: 2.5.1.1-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.1.1-Beta.
- Laufzeitkanal: beta.
- Einstellungen: localStorage; App-Reihenfolgen, Wissensansicht und Favoriten werden nicht übertragen.

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
