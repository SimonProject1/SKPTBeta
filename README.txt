SK PLT Tools 2.3.2.0-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis ist SK-PLT-Tools-V2.3.1.0-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Basis: 4aa3cd3171889a7f7be5115608e24a03bb0c7dcce708880ecf81126a52153fb6.
- Die bestätigten Funktionen und das Design wurden erhalten; geändert wurde gezielt die organisatorische Auslagerung des Werkstoff-Nachschlagewerks.

Eigenständige Werkstoffdatenbank
- Neuer Hauptordner werkstoffdatenbank/ mit eigener index.html.
- Die Startseite enthält eine eigene Karte „Werkstoffdatenbank“ in der Kategorie Wissen.
- Werkstoffsuche, Gruppenfilter, Direktvergleiche, Datenquellen und Sicherheitshinweis bleiben vollständig erhalten.
- Der Breadcrumb lautet nun „Startseite › Werkstoffdatenbank“.
- Suchindex und Startseitensuche führen direkt zur neuen Route und reichen Suchbegriffe weiterhin als q-Parameter durch.
- Der Navigationsbaum enthält eine eigene Gruppe „Werkstoffe“ analog zur Gruppe „Einheiten“.
- Das PWA-Manifest bietet zusätzlich einen Shortcut zur Werkstoffdatenbank.

Wissensdatenbank und mobile Kategorien
- Die Werkstoffdatenbank ist kein Wissensbeitrag mehr.
- Die Wissensdatenbank enthält weiterhin vier Gerätebeiträge in den drei Herstellergruppen Air Torque, Siemens und Vacon.
- Mobile Herstellergruppen, Suchtrefferzählung, Persistenz und Kompaktansicht bleiben erhalten.
- Die mobile Startseite nimmt die neue Karte automatisch in die Kategorie Wissen auf und aktualisiert sichtbare sowie gesamte Kartenzahlen.

Kompatibilität alter Links
- Der bisherige Pfad wissensdatenbank/werkstoff-nachschlagewerk/ bleibt als Weiterleitungsseite bestehen.
- Die Weiterleitung führt zu werkstoffdatenbank/ und erhält Suchparameter sowie URL-Fragmente.
- Dadurch funktionieren alte Favoriten, Lesezeichen und gespeicherte Links weiterhin.
- Neue interne Links verwenden ausschließlich die kanonische Route werkstoffdatenbank/.

Bewahrte Funktionen
- Mobile Startseite mit einklappbaren Werkzeugkategorien und optionaler Kompaktansicht.
- 11 Werkzeug-/Dienstkarten, Suche, Kategorienfilter, Sortierung und Unterseitensuche.
- Favoriten, Seitennavigation, alle sechs Rechner, Einheitendatenbank, vier Wissensbeiträge und Werkstoffdatenbank.
- Messstellen-Dokumentation und externer E+H Device Viewer.
- Das verworfene VDE-0100-600-Funktionsmodul ist nicht Bestandteil dieser Anwendung.

Deployment zum Testen
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen 16 HTML-Routen einschließlich der alten Weiterleitungsroute offline bereit.
- Für einen lokalen Funktionstest kann ein statischer HTTP-Server verwendet werden; Service Worker und Installation anschließend unter HTTPS prüfen.

PWA
- Start-URL, Scope und App-ID bleiben versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Beta-Caches core-v2.3.2.0 und documents-v2.3.2.0.
- Der Kerncache enthält 49 Ziele; der Dokumentcache enthält zwei optionale Dokumente.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
