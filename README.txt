SK PLT Tools 2.3.2.2-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.3.2.1-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Basis: 72c705ab8b676ff9a75bbc33bdb7ebf7c798c371452d719438052a48676f635f.
- ZIP-CRC und interne Prüfsummen der Basis wurden vor der Änderung bestätigt.
- Bestehende Funktionen und Gestaltung bleiben außerhalb der ausdrücklich angepassten
  mobilen Hero-Fläche erhalten.

Mobile Hero-Erweiterung
- Nur auf Smartphones wird rechts neben dem großen Logo die Kennzeichnung
  „PLT-TOOL · PCT-TOOL“ angezeigt.
- Darunter stehen dezent die ausgeschriebenen Begriffe „Prozessleittechnik“ und
  „Process Control Technology“.
- Die Versionsnummer 2.3.2.2-Beta bleibt als größtes Textelement im Mittelpunkt.
- Desktop- und Tablet-Layout bleiben unverändert; die Ergänzung ist außerhalb der
  Smartphone-Media-Queries ausgeblendet.

Bewahrte Funktionen
- Mobile Startseite mit einklappbaren Werkzeugkategorien und optionaler Kompaktansicht.
- 11 Werkzeug-/Dienstkarten, Suche, Kategorienfilter, Sortierung und Unterseitensuche.
- Favoriten, Seitennavigation, alle sechs Rechner, Einheitendatenbank,
  fünf Wissensbeiträge und Werkstoffdatenbank.
- Messstellen-Dokumentation und externer E+H Device Viewer.
- Das verworfene VDE-0100-600-Funktionsmodul ist nicht Bestandteil dieser Anwendung.

Deployment zum Testen
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen 17 HTML-Routen einschließlich
  der alten Werkstoff-Weiterleitungsroute offline bereit.
- Für einen lokalen Funktionstest kann ein statischer HTTP-Server verwendet werden;
  Service Worker und Installation anschließend unter HTTPS prüfen.

PWA
- Start-URL, Scope und App-ID bleiben versionsunabhängig auf ./ gesetzt.
- Service-Worker-Caches: core-v2.3.2.2 und documents-v2.3.2.2.
- Der Kerncache enthält 50 Ziele; der Dokumentcache zwei optionale Dokumente.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
