SK PCT Tools 2.5.0.6-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist 2.5.0.5-Beta.

Änderungen dieser Beta
- Das PCT-Logo auf der Hauptstartseite ist exakt so hoch wie die beiden rechts
  gestapelten Schnellzugriffe zusammen: 98 px auf Desktop und 89 px auf Mobilgeräten.
- Der Startseitenfooter liegt vollständig im abgerundeten PCT-Home-Rechteck.
- Das Rechteck wurde dafür in Höhe und unterem Innenabstand erweitert.
- Die iOS-Safe-Area bleibt oben, unten sowie links und rechts erhalten.
- Versionsanzeige, Suche, Favoriten, Icon-Raster, Wissensdatenbank und alle bestehenden
  Funktionen bleiben erhalten.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Alle fünf fachlichen Wissensbeiträge und die PDF-Beitragsvorlage.
- Startseitensuche, Kategorienfilter, Sortierung, gemeinsames Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne Beitrags-URLs und abgesicherter externer Herstellerlink.

Version und PWA
- Öffentliche Version: 2.5.0.6-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.0.6-Beta.
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
