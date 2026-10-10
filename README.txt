SK PLT Tools 2.3.3.2-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Verbindliche Ausgangsbasis
- Projektbasis: SK-PLT-Tools-V2.3.3.1-Beta.zip vom 10.10.2026.
- SHA-256 der Projektbasis:
  cee81ec58481f1bf3b06a2a35610c30412bbc76e6226d53a9a36cb0998c0d4f8
- Referenz der wiederhergestellten Breitenkorrektur:
  SK-PLT-Tools-V2.2.0.3-Beta.zip
- SHA-256 der Breitenreferenz:
  6e16f25b1549387c56d5f569a7dee16538f51617974d73bab58d6785c79e7c1c
- Beide Archive wurden vor der Änderung per SHA-256, ZIP-CRC und interner
  SHA256SUMS.txt verifiziert.

Änderung V2.3.3.2-Beta
- Die bestätigte Desktop-/Tablet-Breitenkorrektur aus V2.2.0.3-Beta wurde auf
  der vollständigen Funktionsbasis V2.3.3.1-Beta wiederhergestellt.
- Ab 761 CSS-Pixeln haben calc-page-title, analog-page-title, calc-panel,
  analog-panel, calc-notice, voltage-result und sk-unit-database-cta keine
  980-/920-px-Maximalbreite mehr.
- Alle sechs Rechnerseiten verwenden wieder die volle nutzbare Breite der
  gemeinsamen Startseiten-Shell.
- scrollbar-gutter: stable bleibt ab 761 CSS-Pixeln aktiv.
- Die Mobilansicht bis einschließlich 760 CSS-Pixel bleibt unverändert.

Erhaltene spätere Funktionen aus V2.3.3.1-Beta
- Mobile Wissensdatenbank mit Herstellergruppen.
- Eigenständige Werkstoffdatenbank mit Suche, Gruppenfiltern und Direktvergleich.
- Endress+Hauser-Promass-Beitrag.
- Einheitlicher Wissensbeitragsstandard für alle fünf Gerätebeiträge.
- Bereinigte Wissensdatenbank-Startseite ohne sichtbaren Standardkasten.
- Mobile Startseite mit einklappbaren Werkzeugkategorien und Kompaktansicht.
- 11 Werkzeug-/Dienstkarten, Suche, Kategorienfilter und Sortierung.
- Favoriten, Seitennavigation, sechs Rechner, Einheitendatenbank,
  Messstellen-Dokumentation und E+H Device Viewer.
- Alte Werkstoffroute bleibt als kompatible Weiterleitung erhalten.
- Das verworfene VDE-0100-600-Modul bleibt entfernt.

Produktidentität
- Produktbezeichnung: SK PLT Tools.
- Das bestätigte PLT-Logo und alle sechs zugehörigen App-/Iconvarianten wurden
  bytegleich aus V2.3.3.1-Beta übernommen.
- Die Logoänderungen der verworfenen V2.3.4.x-PCT-Reihe sind nicht enthalten.

PWA
- Öffentliche Betaversion: 2.3.3.2-Beta.
- Technische Versionskennung und Cache-Buster: 2.3.3.2.
- Laufzeitkanal: beta.
- Kerncache: sk-plt-tools-core-v2.3.3.2 mit 48 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.3.3.2 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.

Deployment zum Testen
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar
  bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen 17 HTML-Routen
  einschließlich der alten Werkstoff-Weiterleitungsroute offline bereit.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im
  Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.
- Testbericht und Projektübergabe liegen außerhalb des Deployment-ZIP.

Release Notes
- Siehe RELEASE-NOTES.txt.
