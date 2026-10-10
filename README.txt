SK PLT Tools 2.2.0.3-Beta

Vollständige Beta der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank.

Testzweck
- Prüfung der tatsächlich umgesetzten Breitenkorrektur auf allen sechs
  Rechnerseiten.
- Ab 761 CSS-Pixeln nutzen Seitentitel, Rechnerpanel, Hinweise, Ergebnisbereich
  und Einheitenfavoriten-Balken die vollständige nutzbare Breite der gemeinsamen
  Shell wie auf der Startseite.
- Die bisherigen Maximalbreiten von 980 px beziehungsweise 920 px greifen ab
  761 CSS-Pixeln nicht mehr.
- scrollbar-gutter: stable bleibt für PC und Tablet aktiv.
- Die Smartphone-Darstellung bis einschließlich 760 CSS-Pixel bleibt unverändert.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Laufzeitkanal: beta.
- Service-Worker-Caches: core-v2.2.0.3-Beta und documents-v2.2.0.3-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
