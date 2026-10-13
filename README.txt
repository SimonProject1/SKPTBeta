SK PCT Tools 2.5.0.7-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist 2.5.0.6-Beta.

Änderungen dieser Beta
- Das abgerundete Rechteck der Hauptstartseite nutzt die verfügbare Displayhöhe jetzt
  bis unmittelbar vor der unteren iOS-Safe-Area beziehungsweise dem Home-Indikator.
- Die Startseite ist viewportfest und verhindert Seiten- sowie Gummiband-Scrollen.
- Alle 11 App-Icons bleiben vollständig sichtbar; auch sehr schmale Smartphones
  verwenden dafür weiterhin das kompakte Vier-Spalten-Raster.
- Im Querformat werden die Apps platzsparend auf sechs Spalten und zwei Reihen verteilt.
- Suche und Wissensfundstellen öffnen als intern scrollbareres Overlay, ohne die
  Startseite selbst zu verschieben oder scrollbar zu machen.
- Obere sowie seitliche iOS-Safe-Areas, großes Logo, Versionsanzeige, Suche,
  Favoriten, integrierter Footer und alle bestehenden Funktionen bleiben erhalten.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Alle fünf fachlichen Wissensbeiträge und die PDF-Beitragsvorlage.
- Startseitensuche, Kategorienfilter, Sortierung, gemeinsames Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne Beitrags-URLs und abgesicherter externer Herstellerlink.

Version und PWA
- Öffentliche Version: 2.5.0.7-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.0.7-Beta.
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
