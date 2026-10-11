SK PLT Tools 2.4.0.1-Beta

Beta-Testversion der vollständigen statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.4.0.0.zip vom 11.10.2026.
- SHA-256 des Ausgangsarchivs: c9406ceb3ff2cc9e8a7f98f49cfff0e11e7b5a95228229160df7c817fafd3135
- ZIP-CRC, Pfadsicherheit und interne Prüfsummen der Basis wurden vor der
  Änderung erfolgreich verifiziert.

Änderung in V2.4.0.1-Beta
- Das Hauptlogo und alle sechs benötigten App-/Iconvarianten wurden neu erzeugt.
- Alle sieben PNG-Dateien besitzen echte Alphatransparenz ohne deckende
  Hintergrundfläche.
- Die einzige Wortmarke im Logo lautet exakt „S.K. PCT TOOL“.
- Die bisherige Zeile „by Simon Kiesler“ und die frühere PLT-Wortmarke wurden
  aus den Bilddateien entfernt.
- Hauptseite, Kopfzeilen, PWA-Manifest und PDF-Beitragsvorlage verwenden die
  aktualisierten Logo-Dateien.
- Die sichtbare Betaversion lautet 2.4.0.1-Beta; technische Versionskennung,
  Cache-Buster und Datenmetadaten lauten 2.4.0.1.
- Laufzeitkanal: beta.

Erhaltene Funktionen und Gestaltung
- Alle fünf fachlichen Wissensbeiträge und ihre Sicherheits-/Gültigkeitshinweise.
- Mobile Wissensdatenbank mit vier Herstellergruppen und Kompaktansicht.
- Eigenständige Werkstoffdatenbank mit Suche, Gruppenfiltern und Direktvergleich.
- Sechs Rechner, Einheitendatenbank, Messstellen-Dokumentation, Suche, Filter,
  Sortierung, Favoriten und Seitennavigation.
- Siemens- und Endress+Hauser-Hierarchien sowie alle stabilen internen URLs.
- PDF-Beitragsvorlage mit zwei Seiten und 14 editierbaren Feldern.
- Offline-Funktion mit getrenntem Kern- und Dokumentcache.
- Das verworfene VDE-0100-600-Modul bleibt vollständig entfernt.

PWA und Offline-Funktion
- Öffentliche Betaversion: 2.4.0.1-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.0.1.
- Laufzeitkanal: beta.
- Kerncache: sk-plt-tools-core-v2.4.0.1 mit 48 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.4.0.1 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar
  bleiben.
- SHA256SUMS.txt enthält einen SHA-256-Eintrag für jede weitere Projektdatei.
- Die ZIP-Prüfsumme wird separat als SK-PLT-Tools-V2.4.0.1-Beta.zip.sha256
  bereitgestellt.
