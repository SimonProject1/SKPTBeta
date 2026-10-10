SK PLT Tools 2.2.2.1-Beta

Beta-Version der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank. Diese Version ist zum kontrollierten Testen vorgesehen.

Änderung dieser Version
- Die mobile Startseite zeigt im großen Startseitenbereich nur noch das Logo; der darunterliegende Textblock entfällt auf Smartphones.
- Suche, Kategorienfilter und Sortierung sind auf der mobilen Startseite standardmäßig eingeklappt und über „Werkzeuge durchsuchen“ erreichbar.
- Smartphone-Querformate bis 932 CSS-Pixel Breite und 520 CSS-Pixel Höhe verwenden ebenfalls die kompakte Startseite.
- Desktop ab 933 CSS-Pixel sowie Tablets, insbesondere 820 × 1180 CSS-Pixel, behalten die bisherige Darstellung unverändert.

Bewahrte Funktionen
- Alle 10 Werkzeug-/Dienstkarten, Suche, Kategorienfilter, Sortierung und Wissensbeitragssuche bleiben vollständig erhalten.
- Favoriten, Seitennavigation, Rechner, Einheitendatenbank und Wissensdatenbank bleiben unverändert.
- Der Filterzustand kann mobil barrierearm per Schaltfläche, Touch und Tastatur geöffnet und geschlossen werden; aria-expanded und aria-controls werden synchron gehalten.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Installation über die Installationsfunktion des verwendeten Browsers.
- Start-URL und App-ID sind versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Release-Caches core-v2.2.2.1-Beta und documents-v2.2.2.1-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
