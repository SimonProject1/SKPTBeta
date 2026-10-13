SK PCT Tools 2.5.1.2-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.1.1-Beta.

Änderungen dieser Beta
- Startseite und sämtliche Unterseiten verwenden jetzt exakt dieselbe äußere
  Rechteckbasis: identische Maximalbreite, Höhe, Rundung, Kontur, Hintergrundfläche
  und seitliche Safe-Area-Abstände.
- Das Rechteck reicht auf allen Seiten bis an den unteren Displayrand. Die untere
  iOS-Safe-Area wird innerhalb des Footers berücksichtigt.
- Auf der Startseite und jeder Unterseite sitzt das originale S.K.-PCT-Logo
  fest oben links. Die Startseite nutzt dafür jetzt die volle Kopfbreite.
- Favoriten, Zurück und Startseite bleiben als gemeinsame Aktionsgruppe oben rechts.
- Das bisherige separate dunkle Header-Querband der Unterseiten wurde entfernt.
  Dadurch wirkt der Kopf nun wie ein Teil derselben Rechteckfläche wie auf Home.
- Desktop, Tablet, Smartphone und kompaktes Querformat besitzen abgestimmte
  Logo- und Schaltergrößen. Auf kleinen Displays wird der zusätzliche Markenname
  ausgeblendet, damit Logo und drei Navigationsschalter sauber nebeneinander bleiben.

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
- Öffentliche Version: 2.5.1.2-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.1.2-Beta.
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
