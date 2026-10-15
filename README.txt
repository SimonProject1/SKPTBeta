SK PCT Tools 2.6.1.4-Beta

Vollständige optimierte statische PWA für Rechner, Wissensdatenbank,
Hersteller-Hub, Einheitendatenbank und Werkstoffdatenbank.
Ausgangsbasis: SK-PCT-Tools-V2.6.1.3-Beta.

Zentrale Architektur
- assets/app-v2-6-1-4.css ist der einzige operative CSS-Bestand.
- assets/app-v2-6-1-4.js bündelt App-Rahmen, Versionsanzeige, Header, Footer,
  Navigation, Buttons, Icons, Favoriten, Startseitensuche, Sortierung und PWA-Registrierung.
- Wiederkehrende Header- und Footer-Inhalte werden aus leeren, semantischen
  Platzhaltern erzeugt. Der Seiteninhalt bleibt statisch und offline verfügbar.
- Seitenspezifische Rechner- und Datenbanklogik bleibt getrennt, damit Fachlogik
  übersichtlich testbar ist.
- Gemeinsame JSON-, Such-, Sortier- und Escape-Hilfen werden zentral wiederverwendet.

Icon-Standard V2.6.1.4
- 10 aktive vollständige Navigations-PNGs, jeweils 512 × 512 px mit Transparenz.
- Der unveränderte Grün-Türkis-Blau-Hintergrund, weiße Symbole und schwarze
  Comic-Konturen der V2.6.1.3-Beta bleiben erhalten.
- Sechs pixelidentische Rechnerbilder verwenden einen gemeinsamen Rechner-Master.
- Drei pixelidentische Datenbankbilder verwenden einen gemeinsamen Buch-Master.
- E+H, fünf Herstellermarken, Home und Zurück bleiben eigenständige Motive.
- Favoritensterne liegen weiterhin unabhängig vom PNG oben rechts; sichtbarer
  Kreis rund 22 px, Touchziel mindestens 44 × 44 px.

PWA und Offline
- Manifest: manifest-v2-6-1-4.webmanifest
- Suchindex: assets/search-index-v2-6-1-4.json
- Service Worker: service-worker.js
- Ein einzelner Release-Cache: sk-pct-tools-v2-6-1-4-core-r1
- Der Cache enthält nur aktive Laufzeitressourcen und alle internen Seiten.
- Alte sk-pct-tools-Caches werden beim Aktivieren entfernt.
- Navigation arbeitet online network-first und offline aus dem Release-Cache.

Erhaltene Funktionen
- 10 Startseiten-Apps und eigene App-Reihenfolge
- sechs Rechner einschließlich Vorzeichen-Taster, Kopieren und Einheitenfavoriten
- Wissensdatenbank, Hersteller-Hub, Suche und fünf Wissensbeiträge
- Werkstoff- und Einheitendatenbank mit Suche, Filter, Vergleich und Favoriten
- internes Scrollen, iOS-Safe-Areas, Smartphone, Tablet, Desktop und 320-px-Reflow
- installierbare PWA und vollständiger Offline-Start

Prüfung
- Statisch: python3 tests/validate_project.py
- Browser, Responsive und Offline: python3 tests/browser_regression.py
- Manueller Abnahmeumfang: TESTPLAN.md
- Ergebnisse: TEST-RESULTS.txt

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. service-worker.js im Projektstamm und alle relativen Pfade beibehalten.
3. Nach dem ersten Online-Aufruf die Service-Worker-Aktualisierung abwarten.
4. SECURITY-DEPLOYMENT.md für serverseitige Sicherheitsheader beachten.
