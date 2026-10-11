SK PLT Tools 2.4.1.3-Beta

Vollständige Beta-Testversion der statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank, Werkstoffdatenbank und Dokumentation.

Direkte Ausgangsbasis
- SK-PLT-Tools-V2.4.1.2-Beta.zip vom 11.10.2026.
- Alle dort enthaltenen Funktionen, Inhalte, Routen und Offline-Komponenten wurden übernommen.

Design in V2.4.1.3-Beta
- Die Oberfläche ist enger an das S.K.-PCT-Logo angelehnt: tiefes Schwarz,
  Signalblau, Cyan, Grün, helle Metalltöne und technische Leuchtkanten.
- Schwarze Trennlinien gliedern Kopfzeile, Abschnitte, Karten, Datenreihen,
  Filter und Aktionsbereiche im Stil technischer Comic-Panels.
- Das echte Logo wird auf der Startseite und in der PCT-Designseite deutlich
  präsenter verwendet.
- Abgeschrägte Kanten, mechanische Schalterzustände und PCT-Statuslichter bleiben erhalten.

Stern- und Reihenfix
- Favoritensterne sind in einem festen 44-px-Raster zentriert.
- Werkzeugkarten, Einheitenzeilen und Favoritenlisten besitzen konsistente Sternachsen.
- Die Einheitenzeilen behalten ihre Ausrichtung auch bei längeren Bezeichnungen und auf Smartphones.
- Das neue Sternsymbol hat eine kräftige schwarze Kontur und klare Cyan-/Grün-Zustände.

Erhaltene Funktionen und Inhalte
- Alle sechs Rechner und sämtliche Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge mit Sicherheits- und Gültigkeitshinweisen.
- Suche, Filter, Sortierung, Favoriten, Navigation und stabile interne URLs.
- PCT-Designseite, Desktop-, Tablet-, Smartphone- und Standalone-PWA-Darstellung.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- PDF-Beitragsvorlage mit editierbaren AcroForm-Feldern.

Version und PWA
- Öffentliche Betaversion: 2.4.1.3-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.1.3.
- Laufzeitkanal: beta.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
- SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.
