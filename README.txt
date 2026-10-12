SK PCT Tools 2.5.0.3-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist 2.5.0.2-Beta.

Änderungen dieser Beta
- Startseite und Wissensdatenbank berücksichtigen die iOS-Safe-Area am oberen sowie
  an den seitlichen Bildschirmrändern. Das jeweilige abgerundete App-Paket beginnt
  unterhalb der iPhone-Statusleiste.
- In der Wissensdatenbank befinden sich Logo, Titel, Suche und Beitragsraster gemeinsam
  innerhalb des abgerundeten App-Pakets.
- Air Torque, Endress+Hauser, Siemens und Vacon verwenden reduzierte weiße Wort- bzw.
  Kurzmarken auf dem einheitlichen dunklen PCT-Icon-Grund.
- Farbige Herstellerflächen und weiße Logo-Kacheln wurden entfernt.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge und die PDF-Beitragsvorlage.
- Suche, Kategorienfilter, Sortierung, gemeinsames Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Mobile Herstellergruppen und kompakte Beitragsansicht der Wissensdatenbank.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne URLs und abgesicherter externer Herstellerlink.

Version und PWA
- Öffentliche Version: 2.5.0.3-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.0.3-Beta.
- Laufzeitkanal: beta.
- Einstellungen: localStorage; App-Reihenfolgen werden nicht übertragen.

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
