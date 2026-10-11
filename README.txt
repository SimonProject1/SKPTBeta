SK PLT Tools 2.4.1.1-Beta

Vollständige Beta-Testversion der statischen Web-App für Rechner,
Wissensdatenbank, Einheitendatenbank, Werkstoffdatenbank und Dokumentation.

Direkte Ausgangsbasis
- SK-PLT-Tools-V2.4.1.0-Beta.zip vom 11.10.2026.
- Die vorhandenen Funktionen und Inhalte wurden übernommen.
- Designreferenz: PCT-Controls-Designprobe.zip.

PCT-Design in V2.4.1.1-Beta
- Die neuen Designs sind jetzt sichtbar in die vollständige Webapp integriert.
- Originale Designfarben: Graphit/Schwarz für Flächen, Signalorange für Aktion
  und Fokus sowie Mint für sichere, aktive und bestätigte Zustände.
- Abgeschrägte 45-Grad-Kanten, technische Rasterflächen, Statuslicht,
  mechanische Druckzustände und eingelassene Bedienfelder werden durchgängig
  verwendet.
- Alle Grafiken und Designkomponenten sind lokal und offlinefähig.

Direkt testbare Designkomponenten
- Auf der Startseite befindet sich die neue Karte „PCT Controls“.
- Die Route designsystem/ enthält den interaktiven Vorzeichenumschalter,
  den interaktiven Klappschalter mit Schutzklappe sowie die Referenz für
  Geometrie, Farben und Typografie.

Integrierte Bedienelemente
- Vorzeichenwechsel, Bereiche und Kategorien auf-/zuklappen.
- Werkzeug- und Einheitenfavoriten sowie Favoriten-Drawer.
- Navigation/Baumansicht, separate Zurück- und Startseitentaster.
- Suchfelder, Reset, Dropdowns, Tabs und Toggle-Schalter.
- Kopieren-Taster an Rechenergebnissen mit sichtbarer Erfolgsrückmeldung.
- Info-, Quellen-, Warn- und Sicherheitshinweise.
- Druck-, Neu-/Reset- und Löschaktionen der Messstellen-Dokumentation.

Erhaltene Funktionen und Inhalte
- Alle bestehenden Rechner und Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Fünf fachliche Wissensbeiträge mit Sicherheits- und Gültigkeitshinweisen.
- Suche, Filter, Sortierung, Favoriten, Navigation und stabile URLs.
- Responsive Darstellung für Desktop, Tablet, Smartphone und Standalone-PWA.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- PDF-Beitragsvorlage mit editierbaren AcroForm-Feldern.

Version und PWA
- Öffentliche Betaversion: 2.4.1.1-Beta.
- Technische Versionskennung und Cache-Buster: 2.4.1.1.
- Laufzeitkanal: beta.
- Die neue Designseite und ihre Assets gehören zum Offline-Kerncache.

Deployment
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver
  kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
- SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.
- Die externe ZIP-Prüfsumme wird separat als
  SK-PLT-Tools-V2.4.1.1-Beta.zip.sha256 bereitgestellt.
