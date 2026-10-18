SK PCT TOOLS – V2.6.5.5-Beta
Stand: 18.10.2026
Basis: vollständige V2.6.5.4-Beta

1. ZWECK DIESER VERSION

V2.6.5.5-Beta setzt ausschließlich Punkt 1 des abgestimmten Fahrplans als
kleinen, sicheren Korrekturblock um. Schwerpunkt sind kontrollierte
Textumbrüche, vollständige Auswahlwerte bei schmalen Viewports, behutsam
angehobene Mikro- und Hilfstexte sowie kompakte leere Favoritenzustände.

2. UMGESETZTER KORREKTURBLOCK

- Automatische Silbentrennung ist für App-Bezeichnungen,
  Herstellerbezeichnungen, Seitentitel und Wissensbeitragstitel deaktiviert.
- Fachlich kontrollierte Umbruchstellen sind unter anderem für
  Analogsignal-Rechner, Wissensdatenbank, Einbausituation, E+H Device Viewer,
  Endress+Hauser, Siemens Rohwert sowie weitere lange Datenbank-/Rechnertitel
  hinterlegt.
- Das mobile Dreispaltenraster und alle vorhandenen Icongrößen bleiben erhalten.
- Im Analogsignal-Rechner belegt die Umrechnungsrichtung bis 430 px selektiv die
  volle Feldbreite; beide vollständigen Richtungsbezeichnungen bleiben sichtbar.
- Im Spannungsfall-Rechner belegt die Stromart bis 430 px selektiv die volle
  Feldbreite; „Drehstrom, symmetrisch“ und „Wechselstrom, einphasig“ bleiben
  vollständig erhalten.
- Endress+Hauser besitzt im Wissens-Hub eine kontrollierte Umbruchstelle; Abstände
  und Grundaufbau des Hubs wurden nicht neu gestaltet.
- Sichtbare Mikrotexte beginnen regulär bei etwa 10 px; Hilfstexte bei etwa
  13 px. Die aktuelle Versionsanzeige bleibt bei 320 px vollständig im Modul.
- Der mobile zusätzliche „Startseite“-Chip der Werkstoffdatenbank ist verborgen;
  der Desktop-Breadcrumb und der mobile „Wissensdatenbank“-Chip in Beiträgen
  bleiben erhalten.
- Leere Favoritenzustände in Favoritenübersicht und Einheitendatenbank sind als
  kompakte horizontale Hinweiszeilen mit Stern, Kurztext und Anzahl ausgeführt.
  Vorhandene Favoriten werden weiterhin als vollständige Listen dargestellt.

3. AUSDRÜCKLICH UNVERÄNDERT

- visueller Stil und Fachinhalt der fünf Wissensbeiträge
- Fachgrafiken
- große PNG-Icons und Logo-Inhalte
- Headergeometrie und vorhandene Icongrößen
- Ergebnisdarstellungen der Rechner
- Drag-and-Drop-Sortierung einschließlich Undo/Redo und Speicherung
- übrige Funktionen und Datenmodelle

Versionierte PNG-Dateien wurden ausschließlich auf den neuen Dateinamen
V2.6.5.5 fortgeschrieben; ihre Binärinhalte sind SHA-256-identisch zur Basis.

4. START UND INSTALLATION

Die Anwendung ist statisch. Für Entwicklung und Prüfung im Projektordner:

  python3 -m http.server 8080 --bind 127.0.0.1

Danach http://127.0.0.1:8080/ öffnen. Für den produktiven Einsatz den gesamten
Projektordner unverändert auf einen HTTPS-Webserver oder GitHub Pages laden.
Der Service Worker verwendet die Cache-Epoche v2-6-5-5-core-r1 und entfernt
ältere sk-pct-tools-Caches beim Aktivieren.

5. ZENTRALE VERSIONIERTE DATEIEN

- assets/app-v2-6-5-5.css
- assets/app-v2-6-5-5.js
- assets/search-index-v2-6-5-5.json
- manifest-v2-6-5-5.webmanifest
- service-worker.js
- VERSION
- RELEASE-NOTES.txt
- TESTPLAN.md
- TEST-RESULTS.txt
- DESIGN-AUDIT-V2.6.5.5-Beta.md
- UEBERGABE-V2.6.5.5-Beta.txt
- SHA256SUMS.txt

6. QUALITÄTSSICHERUNG

Geprüft wurden 320 px, 390 px, Smartphone, Tablet, Desktop und zusätzlich
Smartphone-Querformat. Der Prüfumfang enthält Reflow, Touch, Tastatur,
Fokusführung, Berechnungen, Suche, Favoriten, Sortierung, Offlinebetrieb,
Service-Worker-Upgrade, Referenzen, Syntax, geschützte PNG-Inhalte und
vollständige Regression. Details stehen in TESTPLAN.md und TEST-RESULTS.txt.
