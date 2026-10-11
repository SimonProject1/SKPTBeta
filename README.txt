SK PLT Tools 2.3.3.3-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Verbindliche Ausgangsbasis
- Projektbasis: SK-PLT-Tools-V2.3.3.2-Beta.zip vom 10.10.2026.
- Bestätigte SHA-256 der Projektbasis:
  6e2cdcd963b7db9af4c3fa3b83ab901ae798a2543632736775210154cc1c6c85
- ZIP-CRC, Pfadsicherheit und 55 interne Prüfsummen der Basis wurden vor der
  Änderung erfolgreich verifiziert.

Änderung V2.3.3.3-Beta
- Der sichtbare Kasten mit der Kennzeichnung des Wissensbeitragsstandards wurde
  aus allen fünf bestehenden Geräte-Wissensbeiträgen entfernt.
- Die Texte „Wissensbeitragsstandard V2.3.3.2-Beta“ und „Einheitliche Struktur ·
  mobil optimiert · Gültigkeit vor Ort prüfen“ werden in den Beiträgen nicht mehr
  angezeigt.
- Der Promass-Beitrag enthält keinen sichtbaren PDF-Dateinamen, keine Folienangabe
  und keinen Hinweis auf eine konkrete Schulungsunterlage mehr.
- Der allgemeine Quellen-, Gültigkeits- und Sicherheitshinweis im Promass-Beitrag
  bleibt erhalten.
- Endress+Hauser ist im Navigationsbaum und im Breadcrumb nach dem Schema
  Wissensdatenbank > Endress+Hauser > Promass > Beitrag gegliedert.
- Suchindex und Wissensübersicht bilden Hersteller und Gerätefamilie konsistent ab.

Erhaltene Funktionen und Gestaltung
- Alle fünf fachlichen Wissensbeiträge und ihre Sicherheits-/Gültigkeitshinweise.
- Mobile Wissensdatenbank mit Herstellergruppen und Kompaktansicht.
- Eigenständige Werkstoffdatenbank mit Suche, Gruppenfiltern und Direktvergleich.
- Bestätigte volle Rechnerbreite ab 761 CSS-Pixeln.
- Bestätigtes PLT-Logo und alle App-/Iconvarianten.
- 11 Werkzeug-/Dienstkarten, Suche, Filterung, Sortierung, Favoriten und Navigation.
- Sechs Rechner, Einheitendatenbank und Messstellen-Dokumentation.
- Alte Werkstoffroute als kompatible Weiterleitung.
- Das verworfene VDE-0100-600-Modul bleibt entfernt.

Technischer Wissensbeitragsstandard
- WISSENSBEITRAGS-STANDARD.md bleibt als technischer und redaktioneller Standard
  erhalten.
- Alle fünf Beiträge tragen unsichtbar data-knowledge-standard="2.3.3.3-Beta".
- Die gemeinsame Darstellung erfolgt weiterhin über assets/knowledge-article.css.
- Die zweitseitige PDF-Beitragsvorlage mit 14 editierbaren Feldern bleibt erhalten
  und ist auf V2.3.3.3-Beta aktualisiert.

PWA
- Öffentliche Betaversion: 2.3.3.3-Beta.
- Technische Versionskennung und Cache-Buster: 2.3.3.3.
- Laufzeitkanal: beta.
- Kerncache: sk-plt-tools-core-v2.3.3.3 mit 48 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.3.3.3 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.

Deployment zum Testen
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar
  bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen 17 HTML-Routen einschließlich
  der alten Werkstoff-Weiterleitungsroute offline bereit.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.
- Testbericht und Projektübergabe liegen außerhalb des Deployment-ZIP.

Release Notes
- Siehe RELEASE-NOTES.txt.
