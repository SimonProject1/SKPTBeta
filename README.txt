SK PCT Tools 2.6.1.3-Beta

Vollständige kontrollierte Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte und vollständig erhaltene Ausgangsbasis ist SK-PCT-Tools-V2.6.1.2-Beta.

Icon-Standard V2.6.1.3
- Genau 17 aktive vollständige Navigations-PNGs, 512 × 512 px, RGBA.
- Alle Dateinamen beginnen mit v2-6-1-3-; die ersetzte V2.6.1.2-Serie und sämtliche Altvarianten wurden entfernt.
- Außenform, Schatten und flächiger Verlauf der V2.6.1.2 bleiben unverändert: links Grün, über Türkis nach oben rechts Blau.
- Nur die weißen Hauptsymbole wurden neu aufgebaut.
- Verbindliches Raster: 288 × 280 px, optischer Mittelpunkt (256, 246), maximal 3 px Mittelpunkttoleranz.
- Einheitliche äußere schwarze Comic-Kontur: 16 px; geschlossene Innendetails: 10 px.
- Geschlossene reine Weißflächen, keine versetzten Drop-Shadows, Doppelkonturen oder uneinheitlichen schwarzen Flächen.
- Rechner: symmetrischer Körper, klares Display, sechs gleich große Tasten.
- Buch: zwei spiegelgleiche geschlossene Seiten und eine klare Mittelfalte.
- WWW: symmetrischer Globus mit wenigen Linien und geschlossenem lesbarem Mittelband.
- Hersteller: identische weiße Namensfelder; Home und Zurück nutzen dasselbe Raster- und Konturprinzip.
- Favoritenstern bleibt unabhängig vom PNG exakt oben rechts: 44 × 44 px Touchfläche, 22-px-Kreis, inaktiv hell und aktiv grün.

Cache- und PWA-Kontrolle
- Eindeutige V2.6.1.3-Dateinamen für Navigationsicons, Manifest, Suchindex und geänderte Kern-CSS-/JavaScript-Ressourcen.
- Service-Worker-Cache-Epoch: v2-6-1-3-icons-r1.
- Alte sk-pct-tools-Caches werden bei Aktivierung vollständig gelöscht.
- Versionskritische Ressourcen werden network-first geladen und offline aus dem exakt benannten Cache bedient.
- Manifest-Shortcuts und Offline-Kerncache verwenden nur die neue Icon-Serie.

Erhaltene Inhalte und Funktionen
- 10 Startseiten-Apps, Hersteller-Hub, fünf Wissensbeiträge und alle internen/externen Navigationsziele.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Suche, Filter, Sortierung, Favoriten und eigene App-Reihenfolge.
- Smartphone-, Tablet-, Desktop- und 320-px-Reflow-Unterstützung.

Wichtige Dateien
- Manifest: manifest-v2-6-1-3.webmanifest
- Service Worker: service-worker.js
- Navigationsicons: assets/navigation-icons/v2-6-1-3-*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Interne Prüfsummen: SHA256SUMS.txt

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. Alle Dateien einschließlich service-worker.js und manifest-v2-6-1-3.webmanifest im gelieferten Pfad belassen.
3. Nach dem ersten Online-Aufruf die einmalige Service-Worker-Aktualisierung/Neuladung abwarten.
4. Für eine vollständige Neuinstallation die alte PWA entfernen und anschließend V2.6.1.3-Beta neu installieren.
5. SECURITY-DEPLOYMENT.md für serverseitige Sicherheitsheader beachten.

Tests
- Statisch: python3 tests/validate_project.py
- Browser/Offline: python3 tests/browser_regression.py
- Manuelle Geräte- und Sichtprüfung: TESTPLAN.md
