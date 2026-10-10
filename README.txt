SK PLT Tools 2.3.3.0-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.3.2.2-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Basis: 149e0b41c694551c26dcb47dee0c16c7342139b369b845eeffe0b275e66707f2.
- ZIP-CRC und interne Prüfsummen der Basis wurden vor der Änderung bestätigt.
- Bestehende Funktionen außerhalb des vereinheitlichten Wissensbereichs bleiben erhalten.

Wissensbeitragsstandard V2.3.3.0-Beta
- Alle fünf vorhandenen Geräte-Wissensbeiträge verwenden eine gemeinsame semantische
  Struktur und die zentrale Datei assets/knowledge-article.css.
- Einheitliche Kurzfassung, Metadaten, Beitragstypen, Fachabschnitte, Prüfhinweise
  sowie Gültigkeits- und Quellenhinweise.
- Die bisher getrennten Beitrags-Styles wurden durch eine zentrale CSS-Datei ersetzt.
- Die Wissensdatenbank erläutert den Standard und stellt ihn als Markdown-Dokument bereit.
- Die PDF-Beitragsvorlage ist an denselben Pflichtfeldern ausgerichtet.
- Fachinhalte der fünf bestehenden Beiträge wurden erhalten und strukturell vereinheitlicht.

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
- Service-Worker-Caches: core-v2.3.3.0 und documents-v2.3.3.0.
- Der Kerncache enthält 48 Ziele; der Dokumentcache drei optionale Dokumente.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
