SK PCT Tools 2.4.2.0-Beta

Vollständige Beta-Testversion der statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank, Werkstoffdatenbank und Dokumentation.

Änderungen in V2.4.2.0-Beta
- Alle 17 Seiten wurden auf Desktop und Mobil visuell und technisch geprüft.
- Interne Haupttitel skalieren nun einheitlich und umbrechen lesbar, statt per
  JavaScript bis auf sehr kleine Einzeilen-Schriftgrößen verkleinert zu werden.
- Das Startseitenlogo wurde deutlich platzsparender als WebP abgelegt.
- Unnötige Titeldateien, eine ungenutzte CSS-Datei und eine separate Siemens-
  Integrationsdatei wurden entfernt bzw. zusammengeführt.
- Die Messstellen-Dokumentation erhielt eindeutige Namen für Fotoeingaben und
  dynamische Bedienelemente sowie eine sichere Maskierung von Beschriftungen.
- Offline-Cache, Versionsangaben und Referenzen wurden vollständig aktualisiert.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge und die PDF-Beitragsvorlage.
- Suche, Filter, Sortierung, Favoriten, Navigation und stabile interne URLs.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.

Version und PWA
- Öffentliche Betaversion: 2.4.2.0-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.2.0.
- Laufzeitkanal: beta.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
- SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.
