SK PCT Tools 2.5.1.3-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.1.2-Beta.

Änderungen dieser Beta
- Die obere Aktionsreihe der Startseite ist vereinheitlicht: Suche und Favoriten
  stehen jetzt horizontal nebeneinander oben rechts.
- Logo, Versionsanzeige und Schnellzugriffe bleiben auf Desktop, Tablet,
  Smartphone und im kompakten Querformat sauber in derselben Kopfbasis ausgerichtet.
- Alle 15 gerahmten Unterseiten übernehmen den Footer der Startseite vollständig.
- Footerbreite, Position, schwarze Trennkante mit Cyan-Innenlinie, transparente
  Fläche, Typografie, Versionsanzeige und Safe-Area-Abstände stimmen überein.
- Das bisherige vollbreite dunkle Footer-Band der Unterseiten wurde entfernt.
- Die gemeinsame Rechteckbasis, das Logo oben links und die Unterseiten-Navigation
  oben rechts aus der 2.5.1.2-Beta bleiben unverändert erhalten.

Erhaltene Funktionen und Inhalte
- Alle 11 Startseiten-Apps und ihre eindeutigen App-Icons.
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Alle fünf fachlichen Wissensbeiträge und die PDF-Beitragsvorlage.
- Startseitensuche, Kategorienfilter, Sortierung, Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne Beitrags-URLs und abgesicherter externer Herstellerlink.
- Runde Formensprache der 2.5.1.1-Beta für Panels, Felder und Schalter.

Version und PWA
- Öffentliche Version: 2.5.1.3-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.1.3-Beta.
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
