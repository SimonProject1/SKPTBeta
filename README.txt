SK PLT Tools 2.2.1.1-Beta

Beta-Version der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank. Diese Version ist zum kontrollierten Testen vorgesehen.

Änderung dieser Version
- Werkstoffe im Werkstoff-Nachschlagewerk sind einzeln ein- und ausklappbar.
- Beim Seitenaufruf sind alle Werkstoffe eingeklappt, um insbesondere auf dem iPhone weniger scrollen zu müssen.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Installation über die Installationsfunktion des verwendeten Browsers.
- Start-URL und App-ID sind versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Release-Caches core-v2.2.1.1-Beta und documents-v2.2.1.1-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
