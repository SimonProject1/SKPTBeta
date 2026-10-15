SK PCT Tools 2.6.1.1-Beta

Vollständige kontrollierte Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige SK-PCT-Tools-V2.6.1.0-Beta.

Behobene Ursache
- In V2.6.1.0-Beta zeigten die HTML-Verweise zwar auf die erwarteten Dateien, die zehn ausgelieferten App-PNGs enthielten jedoch selbst weiterhin die farbigen Taschenrechner-, Buch- und Weltkugelmotive.
- Zusätzlich verwendete der Service Worker cache-first mit ignoreSearch:true. Dadurch konnten gleichnamige Dateien trotz neuer ?v=-Parameter aus einem älteren PWA-Cache geliefert werden.
- V2.6.1.1-Beta beseitigt beide Ursachen: neu erzeugte Quelldateien und eindeutige Dateinamen sowie ein neuer Cache-Epoch ohne ignoreSearch-Fallback.

Icon-Standard V2.6.1.1
- 17 aktive Navigations-PNGs, 512 × 512 px, RGBA, transparente Hintergründe.
- Alle Dateinamen beginnen mit v2-6-1-1-; alte app-*.png-, manufacturer-*.png- und nav-*.png-Dateien wurden entfernt.
- Gemeinsamer dunkler Cartoon-Tech-Rahmen mit schwarzer Außenkontur und einem Blau-Cyan-Grün-Rahmenbogen wird zentral in CSS erzeugt.
- Innen ausschließlich einfache weiße beziehungsweise hellgraue Funktionssymbole mit schwarzer Kontur: Rechner, Buch/Nachschlagewerk und WWW-Weltkugel.
- Hersteller-Hub, Home und Zurück verwenden ruhige weiße Einzelmotive.
- Keine Kategoriefelder, Kleinstbeschriftungen, alten Farbmotive oder dynamischen Dateinamen-Fallbacks.
- Favoriten: 44 × 44 px Touchfläche, sichtbarer 22-px-Kreis oben rechts; inaktiv hell/ruhig, aktiv grün mit dezentem Leuchtring.

Cache- und PWA-Kontrolle
- Eindeutige Dateinamen für Manifest, Suchindex und geänderte CSS-/JavaScript-Ressourcen.
- Service-Worker-Cache-Epoch: v2-6-1-1-icons-r1.
- Alte sk-pct-tools-Caches werden bei Aktivierung vollständig gelöscht.
- Versionskritische Ressourcen werden network-first geladen und offline aus dem exakt benannten Cache bedient.
- Der Service Worker wird mit releasebezogener URL und updateViaCache:none registriert.
- Manifest-Shortcuts und Offline-Kerncache verwenden nur die neue Icon-Serie.

Erhaltene Inhalte und Funktionen
- 10 Startseiten-Apps, Hersteller-Hub, fünf Wissensbeiträge und alle internen/externalen Navigationsziele.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Suche, Filter, Sortierung, Favoriten und eigene App-Reihenfolge.
- Smartphone-, Tablet-, Desktop- und 320-px-Reflow-Unterstützung.

Wichtige Dateien
- Manifest: manifest-v2-6-1-1.webmanifest
- Service Worker: service-worker.js
- Navigationsicons: assets/navigation-icons/v2-6-1-1-*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Interne Prüfsummen: SHA256SUMS.txt

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. Alle Dateien einschließlich service-worker.js und manifest-v2-6-1-1.webmanifest im gelieferten Pfad belassen.
3. Nach dem ersten Online-Aufruf die einmalige Service-Worker-Aktualisierung/Neuladung abwarten.
4. Für eine vollständige Neuinstallation die alte PWA entfernen und anschließend V2.6.1.1-Beta neu installieren.
5. SECURITY-DEPLOYMENT.md für serverseitige Sicherheitsheader beachten.

Tests
- Statisch: python3 tests/validate_project.py
- Browser/Offline: python3 tests/browser_regression.py
- Manuelle Geräteabnahme: TESTPLAN.md
