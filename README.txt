SK PLT Tools 2.4.0.0

Veröffentlichungsfertige statische Web-App für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.

Release-Basis
- Verifizierter Vorgängerstand: 2.3.3.3.
- SHA-256 des unveränderten Ausgangsarchivs:
  757e635a516feccff01d400abf7d60aadd219f19331c5ff3b412a6ff9e2a3e2b
- ZIP-CRC, Pfadsicherheit und 55 interne Prüfsummen der Basis wurden vor der
  Änderung erfolgreich verifiziert.

Änderungen in Version 2.4.0.0
- Siemens ist in der Wissensdatenbank analog zur bestehenden
  Endress+Hauser-Hierarchie als Hersteller > Gerät/System > Beitrag gegliedert.
- Unter Siemens > Sitrans P320 ist der Beitrag „SIL Verriegelung“ verfügbar.
- Unter Siemens > SPS ist der Beitrag „Rohwert“ verfügbar.
- Kartenbeschriftungen, Breadcrumbs, Navigationsbaum, Suchindex und interne
  Verlinkungen wurden auf dieselbe Hierarchie normalisiert.
- Die sichtbare und technische Versionsführung wurde vollständig auf 2.4.0.0
  umgestellt; der Laufzeitkanal ist stable.

Erhaltene Funktionen und Gestaltung
- Alle fünf fachlichen Wissensbeiträge einschließlich des bereinigten
  Endress+Hauser-Promass-Beitrags und ihrer Sicherheits-/Gültigkeitshinweise.
- Mobile Wissensdatenbank mit vier Herstellergruppen und standardmäßig aktiver
  Kompaktansicht.
- Eigenständige Werkstoffdatenbank mit Suche, Gruppenfiltern und Direktvergleich.
- Bestätigte volle Rechnerbreite ab 761 CSS-Pixeln auf PC und Tablet.
- Bestätigtes PLT-Logo und alle App-/Iconvarianten.
- 11 Werkzeug-/Dienstkarten, Suche, Filterung, Sortierung, Favoriten und Navigation.
- Sechs Rechner, Einheitendatenbank und Messstellen-Dokumentation.
- Alte Werkstoffroute als kompatible Weiterleitung.
- Das verworfene VDE-0100-600-Modul bleibt entfernt.

Technischer Wissensbeitragsstandard
- WISSENSBEITRAGS-STANDARD.md bleibt als technischer und redaktioneller Standard
  erhalten.
- Alle fünf Beiträge tragen unsichtbar data-knowledge-standard="2.4.0.0".
- Die gemeinsame Darstellung erfolgt über assets/knowledge-article.css.
- Die zweitseitige PDF-Beitragsvorlage mit 14 editierbaren Feldern ist auf
  Version 2.4.0.0 aktualisiert.

PWA und Offline-Funktion
- Öffentliche und technische Version: 2.4.0.0.
- Cache-Buster: 2.4.0.0.
- Laufzeitkanal: stable.
- Kerncache: sk-plt-tools-core-v2.4.0.0 mit 48 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.4.0.0 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.
- Nach dem ersten vollständigen Online-Aufruf stehen 17 HTML-Routen
  einschließlich der kompatiblen Werkstoff-Weiterleitung offline bereit.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar
  bleiben.
- SHA256SUMS.txt enthält einen SHA-256-Eintrag für jede weitere Projektdatei.
- Die ZIP-Prüfsumme, der Testbericht und die Übergabedatei werden separat neben
  dem Deployment-ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
