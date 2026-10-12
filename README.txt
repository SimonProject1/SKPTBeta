SK PCT Tools 2.4.2.1-Beta

Vollständige Beta-Testversion der statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank, Werkstoffdatenbank und Dokumentation.

Änderungen in V2.4.2.1-Beta
- Der auf- und zuklappbare Bereich „Suche & Filter“ der Startseite verwendet
  mobil denselben Zustandsstandard wie die übrigen Klappbereiche.
- Geschlossen ist der Bereich eckig, kompakt und auf die Schalterzeile reduziert.
- Geöffnet besitzt der gesamte Bereich einen konsistent gerundeten Rahmen; der
  Schalter bildet den gerundeten Kopf und der Inhalt schließt ohne Formbruch an.
- ARIA-Zustand, zugängliche Beschriftung, Chevron und Inhaltsanzeige werden bei
  jedem Zustandswechsel gemeinsam aktualisiert.
- Desktop- und Tabletverhalten außerhalb der mobilen Klappansicht bleiben
  unverändert.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge und die PDF-Beitragsvorlage.
- Suche, Kategorienfilter, Sortierung und Zurücksetzen auf der Startseite.
- Mobile Kategorien, Kompaktansicht, Favoriten und Seitennavigation.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Stabile interne URLs und externe Herstellerlinks.

Version und PWA
- Öffentliche Betaversion: 2.4.2.1-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.2.1.
- Laufzeitkanal: beta.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
- SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.
