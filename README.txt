SK PLT Tools 2.2.3.1-Beta

Beta-Version der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank. Diese Version ist zum kontrollierten Testen vorgesehen.

Änderung dieser Version
- Technische Basis ist der korrigierte vollständige Projektstand 2.2.2.2-Beta.
- Die Werkzeugkarten der mobilen Startseite werden nach Rechner, Dokumentation, Wissen und externen Diensten gruppiert.
- Jede mobile Kategorie kann über eine eigene, barrierearme Schaltfläche ein- und ausgeklappt werden.
- Sichtbare Treffer und Gesamtzahl werden je Kategorie angezeigt; leere Kategorien werden bei aktiver Suche oder Filterung ausgeblendet.
- Eine optionale kompakte Kartenansicht reduziert Kartenhöhe und blendet Beschreibungstexte aus.
- Kategorie- und Ansichtsstatus bleiben lokal im Browser gespeichert.
- Desktop und Tablet behalten die flache, vollständige Kartenansicht unverändert.

Bewahrte Funktionen
- Alle 10 Werkzeug-/Dienstkarten, Suche, Kategorienfilter, Sortierung und Wissensbeitragssuche bleiben vollständig erhalten.
- Favoriten, Seitennavigation, Rechner, Einheitendatenbank und Wissensdatenbank bleiben unverändert.
- Der vorhandene mobile Schalter für Suche und Filter bleibt erhalten.

Bedienung auf der mobilen Startseite
- Kategoriezeile antippen, um die zugehörigen Karten ein- oder auszuklappen.
- Unter „Kartenansicht“ die Option „Kompakte Karten“ ein- oder ausschalten.
- Die Einstellungen werden ausschließlich lokal in localStorage gespeichert.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Neue Versionen am selben Pfad bereitstellen; die versionsunabhängige PWA-ID behandelt sie als Update derselben App.

PWA
- Installation über die Installationsfunktion des verwendeten Browsers.
- Start-URL und App-ID sind versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Release-Caches core-v2.2.3.1-Beta und documents-v2.2.3.1-Beta.

Integrität
- Interne Dateien: SHA256SUMS.txt mit einem SHA-256-Eintrag je weiterer Datei.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
