SK PLT Tools 2.4.0.2-Beta

Beta-Testversion der vollständigen statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank und Werkstoffdatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis: SK-PLT-Tools-V2.4.0.1-Beta.zip vom 11.10.2026.
- SHA-256 des Ausgangsarchivs: e06aaedb00f8e859efd67fe69e616f619db4e93d1c53f72f2a5ed5c1b99c5266
- ZIP-CRC, Pfadsicherheit und interne Prüfsummen der Basis wurden vor der
  Änderung erfolgreich verifiziert.

Änderung in V2.4.0.2-Beta
- Das bestätigte PCT-Zahnradlogo wurde in alle sieben produktiv verwendeten
  Web-App-Formate übernommen.
- Die Bildmarke zeigt „PCT“ groß am Zahnrad.
- Der einzige Schriftzug unterhalb der Bildmarke lautet exakt
  „Tool’s by S.K.“.
- Bereitgestellt sind assets/logo.png, favicon.png, apple-touch-icon.png,
  icon-192.png, icon-512.png, icon-maskable-192.png und
  icon-maskable-512.png.
- Alle Varianten besitzen echte Alphatransparenz. Die beiden Maskable-Icons
  liegen innerhalb der vorgesehenen Sicherheitszone.
- Hauptseite, Kopfzeilen, PWA-Manifest, Service Worker und PDF-Beitragsvorlage
  verwenden die aktualisierten Logo-Dateien.
- Die sichtbare Betaversion lautet 2.4.0.2-Beta; technische Versionskennung,
  Cache-Buster und Datenmetadaten lauten 2.4.0.2.
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
- Öffentliche Betaversion: 2.4.0.2-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.0.2.
- Laufzeitkanal: beta.
- Kerncache: sk-plt-tools-core-v2.4.0.2 mit 48 Zielen.
- Dokumentcache: sk-plt-tools-documents-v2.4.0.2 mit drei Dokumenten.
- Manifest-ID, start_url und scope bleiben versionsunabhängig auf ./ gesetzt.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar
  bleiben.
- SHA256SUMS.txt enthält einen SHA-256-Eintrag für jede weitere Projektdatei.
- Die ZIP-Prüfsumme wird separat als SK-PLT-Tools-V2.4.0.2-Beta.zip.sha256
  bereitgestellt.
