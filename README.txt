SK PLT Tools 2.2.0.2-Beta

Vollständige Beta der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank.

Testzweck
- Prüfung der korrigierten Rechnerseiten-Shell auf PC und Tablet.
- Kopfzeile, Trennstrich, Logo und Startseiten-Button müssen exakt dieselbe
  Gesamtbreite und horizontale Ausrichtung wie auf der Startseite besitzen.
- Rechnerkarten bleiben kompakt und werden nicht pauschal auf 920 px verbreitert.
- Die mobile Darstellung bleibt innerhalb der verfügbaren Breite und ohne
  horizontalen Überlauf.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Laufzeitkanal: beta.
- Service-Worker-Caches: core-v2.2.0.2-Beta und documents-v2.2.0.2-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
