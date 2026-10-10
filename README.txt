SK PLT Tools 2.2.2.2-Beta

Beta-Version der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank. Diese Version ist zum kontrollierten Testen vorgesehen.

Änderung dieser Version
- Technische Basis ist der vollständige Projektstand 2.2.2.1-Beta.
- Auf der mobilen Startseite steht das große Logo im Hero-Bereich links.
- Rechts daneben wird die aktuelle Version 2.2.2.2-Beta kompakt angezeigt.
- Der mobile Hero-Bereich ist niedriger und platzsparender ausgeführt.
- Der in 2.2.2.1-Beta mobil entfernte weiße Textblock bleibt ausgeblendet.
- Suche, Kategorienfilter und Sortierung bleiben mobil standardmäßig eingeklappt und über „Werkzeuge durchsuchen“ erreichbar.
- Desktop und Tablet behalten die bisherige Darstellung unverändert.

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
- Der Service Worker verwendet die Release-Caches core-v2.2.2.2-Beta und documents-v2.2.2.2-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
