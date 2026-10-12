SK PCT Tools 2.5.0.1-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist 2.5.0.0-Beta.

Reduzierter PCT Home-Screen
- Das App-Raster steht ohne Uhrzeit, Datum, Einführung oder Versionskarte direkt
  im Mittelpunkt.
- Die dauerhaft sichtbare Verschiebeanleitung, die App-Dichte-Auswahl sowie die
  großen Schaltflächen „Anordnen“ und „Standard“ wurden entfernt.
- Gedrückthalten einer App aktiviert den Bearbeitungsmodus und startet das
  Verschieben. Die Wackelanimation kennzeichnet den aktiven Modus.
- „Fertig“ beendet den Bearbeitungsmodus. „Zurücksetzen“ stellt innerhalb des
  Bearbeitungsmodus optional die ausgelieferte Reihenfolge wieder her.
- Für Tastaturbedienung aktiviert die Leertaste auf einer fokussierten App den
  Bearbeitungsmodus; Pfeiltasten verschieben die App, Escape beendet den Modus.
- Die eigene Reihenfolge wird ausschließlich lokal im Browser gespeichert.

Kompakte Suche
- Ein kleiner Zugriff „Suchen“ öffnet Suche, Kategorienfilter und Sortierung nur
  bei Bedarf. Das App-Raster bleibt beim Start frei sichtbar.
- Suche über Apps, Wissensbeiträge und Werkstoffbegriffe bleibt erhalten.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge und die PDF-Beitragsvorlage.
- Kategorienfilter, Sortierung, gemeinsames Zurücksetzen und Favoriten.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne URLs und abgesicherter externer Herstellerlink.

Entfernt
- Die hierarchische Seitenauswahl einschließlich Schaltfläche, Drawer, Laufzeitmodul,
  Navigationsdaten und Offline-Cache-Eintrag ist nicht Bestandteil dieser Version.

Version und PWA
- Öffentliche Version: 2.5.0.1-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.0.1-Beta.
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
