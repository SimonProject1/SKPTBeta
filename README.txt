SK PLT Tools 2.3.2.1-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.3.2.0-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Basis: c9ca02dff080d1c7fcfe090a3d987ddc1a1dc4e11c268f7a8403bb07fc84d2b5.
- ZIP-CRC und interne Prüfsummen der Basis wurden vor der Änderung bestätigt.
- Bestehende Funktionen, Gestaltung und die eigenständige Werkstoffdatenbank wurden erhalten.

Neuer Wissensbeitrag
- Hersteller: Endress+Hauser.
- Gerätefamilie: Promass.
- Messprinzip: Coriolis-Massedurchfluss.
- Thema: Einbaulage und Einbausituation.
- Neue Route: wissensdatenbank/endress-hauser-promass-einbaulage/.
- Fachliche Grundlage: Durchfluss_Coriolis_2024.pdf, insbesondere Folien 30 bis 33 sowie ergänzend 34 und 35.
- Der Beitrag beschreibt Steigleitung und Druckseite als bevorzugte Einbausituationen,
  zu vermeidende Positionen, Besonderheiten von Zwei-Rohr-Sensoren und
  Messumformerlage sowie die Anordnung von Ventilen und Rohrerweiterungen.
- Die Schulungsunterlage selbst ist nicht Bestandteil des kompakten Deployment-ZIP.

Wissensdatenbank, Suche und Navigation
- Die Wissensdatenbank enthält fünf Gerätebeiträge in vier Herstellergruppen:
  Air Torque, Endress+Hauser, Siemens und Vacon.
- Die mobile Herstellergruppierung wird automatisch um Endress+Hauser ergänzt.
- Die Beitragssuche berücksichtigt Hersteller, Gerätefamilie, Messprinzip und
  alle wesentlichen Einbau-Schlagworte.
- Die Startseitensuche enthält den Beitrag als eigenständigen Wissensbeitrag.
- Der Navigationsbaum enthält unter Wissen eine Herstellergruppe Endress+Hauser
  mit dem Promass-Beitrag.

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
- Service-Worker-Caches: core-v2.3.2.1 und documents-v2.3.2.1.
- Der Kerncache enthält 50 Ziele; der Dokumentcache zwei optionale Dokumente.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
