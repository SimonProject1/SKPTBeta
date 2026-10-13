SK PCT Tools 2.5.1.0-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.0.7-Beta.

Änderungen dieser Beta
- Die Startseite ist nun am HTML-Wurzelelement und am Body viewportfest gesperrt.
  Seitenscrollen, iOS-Overscroll und Gummiband-Scrollen sind damit vollständig unterbunden.
- Alle Unterseiten verwenden denselben sichtbaren PCT-App-Rahmen wie die Startseite.
- Kopfzeile, Inhaltsbereich und Footer bleiben gemeinsam in einem abgerundeten Rechteck.
- Auf Unterseiten scrollt ausschließlich der Inhaltsbereich innerhalb dieses Rechtecks;
  Kopfzeile, Navigation und Footer bleiben im Rahmen sichtbar.
- Safe Areas von iPhone und iPad werden oben, unten und seitlich berücksichtigt.
- Favoriten-, Zurück- und Startseiten-Schalter sind gemeinsam in der Kopfzeile angeordnet.
- Aktionsschalter, Links und Symbole wurden auf den einheitlichen rechteckigen
  PCT-Bedienstil mit schwarzer Kontur und Cyan-/Grün-Statuskante umgestellt.
- Neue PCT-Symbole kennzeichnen Berechnen, Datenbank, Download und Fertig.
- Der neue gemeinsame Rahmenstil ist vollständig im Offline-Kerncache enthalten.

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
- Öffentliche Version: 2.5.1.0-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.1.0-Beta.
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
