SK PLT Tools 2.4.1.0-Beta

Beta-Testversion der vollständigen statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.4.0.2-Beta.zip vom 11.10.2026.
- SHA-256 des Ausgangsarchivs: 6913fe54c65b7e8a17dc1f5cfd2be94673f75b67610d80da54ad1e7f12febb10
- Funktions-, Inhalts-, Navigations-, PWA- und Logostand der Basis bleibt erhalten.

Änderung in V2.4.1.0-Beta
- Vollständiges Fachgrafikpaket für alle fünf Wissensbeiträge ergänzt.
- 11 responsive SVG-Grafiken zu Air Torque, Endress+Hauser Promass,
  Siemens SITRANS P320, Siemens SPS-Rohwert und Vacon integriert.
- Alle Grafiken besitzen Alternativtexte, sichtbare Bildunterschriften und
  skalieren ohne horizontalen Überlauf auf Desktop, Tablet und Smartphone.
- Sämtliche Grafikdateien sind lokal im Deployment enthalten und Bestandteil
  des strikten Offline-Caches; es bestehen keine externen Bildabhängigkeiten.
- Öffentliche Betaversion: 2.4.1.0-Beta.
- Technische Versionskennung, Cache-Buster und Datenmetadaten: 2.4.1.0.
- Laufzeitkanal: beta.

Grafikbestand
- assets/graphics/air-torque-drehrichtung.svg
- assets/graphics/promass-steigleitung.svg
- assets/graphics/promass-vermeiden.svg
- assets/graphics/promass-sensorlagen.svg
- assets/graphics/promass-druckhaltung.svg
- assets/graphics/sitrans-p320-sil-aktivierung.svg
- assets/graphics/sps-rohwert-signalweg.svg
- assets/graphics/sps-rohwert-skalen.svg
- assets/graphics/sps-rohwert-beispiel.svg
- assets/graphics/vacon-parameter-2-2-3-7.svg
- assets/graphics/vacon-pruefkette.svg

Erhaltene Funktionen und Gestaltung
- Alle fünf fachlichen Wissensbeiträge und ihre Sicherheits-/Gültigkeitshinweise.
- Mobile Wissensdatenbank, Werkstoffdatenbank, sechs Rechner,
  Einheitendatenbank, Messstellen-Dokumentation, Suche, Filter, Sortierung,
  Favoriten und Seitennavigation.
- Sieben bestätigte Logo- und Iconvarianten.
- PDF-Beitragsvorlage mit zwei Seiten und 14 editierbaren Feldern.
- Das verworfene VDE-0100-600-Modul bleibt vollständig entfernt.

PWA und Offline-Funktion
- Kerncache: sk-plt-tools-core-v2.4.1.0 mit 59 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.4.1.0 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- SHA256SUMS.txt enthält einen SHA-256-Eintrag für jede weitere Projektdatei.
