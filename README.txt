SK PLT Tools 2.2.1.2-Beta

Beta-Version der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank. Diese Version ist zum kontrollierten Testen vorgesehen.

Änderung dieser Version
- In der PC-Darstellung stehen Werkstoff-Kurznamen vollständig in genau einer Zeile.
- In der PC-Darstellung stehen die Werkstoffgruppen-Kennzeichnungen oben rechts ebenfalls vollständig in genau einer Zeile.
- Die bestätigte mobile Darstellung bleibt unverändert: Alle Werkstoffe starten eingeklappt und lassen sich einzeln sowie unabhängig voneinander öffnen und schließen.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Installation über die Installationsfunktion des verwendeten Browsers.
- Start-URL und App-ID sind versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Release-Caches core-v2.2.1.2-Beta und documents-v2.2.1.2-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
