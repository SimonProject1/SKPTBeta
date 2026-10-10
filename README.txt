SK PLT Tools 2.3.4.0-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.3.3.0-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Basis: e4f644bdd39f3a76d5556b5fd0aa20568460c6a39154abfd6953c69cca9e80a2.
- ZIP-CRC und interne Prüfsummen der Basis wurden vor der Änderung bestätigt.
- Bestehende Funktionen, Inhalte und Gestaltung bleiben erhalten.

Änderung in V2.3.4.0-Beta
- Ausschließlich das bisherige PLT-Logo wurde durch die PCT-Variante ersetzt.
- Ersetzt wurden assets/logo.png, favicon.png, apple-touch-icon.png,
  icon-192.png, icon-512.png, icon-maskable-192.png und icon-maskable-512.png.
- Die bisherigen Pixelabmessungen und Dateiformate bleiben erhalten.
- Außer dem Logo-Austausch und der konsistenten Versionsanhebung wurden keine
  Layout-, Farb-, Typografie-, Navigations-, Inhalts- oder Funktionsänderungen vorgenommen.

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
- Service-Worker-Caches: core-v2.3.4.0 und documents-v2.3.4.0.
- Der Kerncache enthält 48 Ziele; der Dokumentcache drei optionale Dokumente.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
