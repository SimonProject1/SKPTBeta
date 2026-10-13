SK PCT Tools 2.5.1.4-Beta

Vollständige Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
Direkte Ausgangsbasis ist die vollständige 2.5.1.3-Beta.

Änderungen dieser Beta
- Kritischer Navigationsfix für die Wissensdatenbank: Herstelleransichten und alle
  fünf Wissensbeiträge werden nun über eine normalisierte Projektwurzel geöffnet.
- Die frühere Grid-Regel kann den mit `hidden` markierten Hersteller-Hub nicht mehr
  sichtbar halten; die gewählte Hersteller-Unteransicht erscheint sofort.
- Beitragsziele funktionieren unabhängig davon, ob die aktuelle Adresse mit /,
  index.html oder einem Hersteller-Parameter endet.
- Die gesamte Wissenskarte ist eine eindeutige Tap-Zone; der Favoritenstern bleibt
  davon getrennt bedienbar.
- Die sechs Rechnerseiten sind kompakter: flachere Seitentitel, kleinere Abstände,
  mehr Eingabefelder nebeneinander und Ergebnisse neben der Eingabe auf Desktop.
- Auf Smartphones werden Eingabefelder in der Regel zweispaltig dargestellt;
  Touch-Ziele bleiben mindestens 42 bis 44 px hoch.
- Der Siemens-Rohwert-Rechner verwendet auf Desktop eine kompakte Rasterfläche
  für Eingabe, Ergebnisse, Messbereich, Konfiguration und Diagnose.
- Der Spannungsfall-Rechner zeigt Eingabe- und Ergebnisfelder dichter an, ohne
  Berechnungslogik oder fachliche Hinweise zu entfernen.
- Der Hinweis zur Einheitendatenbank ist auf Rechnerseiten jetzt eine flache Leiste.

Erhaltene Funktionen und Inhalte
- Alle 11 Startseiten-Apps und ihre eindeutigen App-Icons.
- Alle sechs Rechner und sämtliche vorhandenen Berechnungslogiken.
- Einheitendatenbank, Werkstoffdatenbank und Messstellen-Dokumentation.
- Alle fünf fachlichen Wissensbeiträge und die PDF-Beitragsvorlage.
- Startseitensuche, Kategorienfilter, Sortierung, Zurücksetzen und Favoriten.
- Long-Press-Bearbeitungsmodus mit lokaler Speicherung der App-Reihenfolge.
- Vollständig lokale Offline-Funktion mit Kern- und Dokumentcache.
- Gemeinsame Rechteckbasis, fester Header/Footer und interne Scrollbereiche.
- Runde Formensprache für Panels, Felder und Schalter.

Version und PWA
- Öffentliche Version: 2.5.1.4-Beta.
- Technische Versionskennung und Cache-Buster: 2.5.1.4-Beta.
- Laufzeitkanal: beta.
- Einstellungen: localStorage; App-Reihenfolgen, Wissensansicht und Favoriten werden nicht übertragen.

Deployment
1. Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
2. manifest.webmanifest und service-worker.js müssen im Projektstamm verbleiben.
3. Für lokale Tests einen HTTP-Server verwenden, z. B.:
   python3 -m http.server 8080
4. Anschließend http://localhost:8080/ öffnen.
5. SHA256SUMS.txt enthält für jede weitere Projektdatei einen SHA-256-Eintrag.

Tests
- Automatische Struktur- und Integritätsprüfung:
  python3 tests/validate_project.py
- Manueller Testplan: TESTPLAN.md
