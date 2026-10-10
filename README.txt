SK PLT Tools 2.2.0.1-Beta

Vollständige Beta der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank.

Testzweck
- Prüfung des Breiten-Bugfixes auf allen sechs Rechnerseiten.
- Seitentitel, Rechner-Hauptbereich, Hinweise/Ergebnisse und der Balken für
  Einheitenfavoriten sind bis maximal 920 px bündig ausgerichtet.
- Die mobile Darstellung bleibt innerhalb der verfügbaren Breite und ohne
  horizontalen Überlauf.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Laufzeitkanal: beta.
- Service-Worker-Caches: core-v2.2.0.1-Beta und documents-v2.2.0.1-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
