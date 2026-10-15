SK PCT Tools 2.6.1.2-Beta

Vollständige kontrollierte Beta der statischen PWA für Rechner, Wissensdatenbank,
Einheitendatenbank und Werkstoffdatenbank.
Direkte Ausgangsbasis ist die vollständige SK-PCT-Tools-V2.6.1.1-Beta.

Icon-Standard V2.6.1.2
- 17 aktive vollständige Navigations-PNGs, 512 × 512 px, RGBA.
- Alle Dateinamen beginnen mit v2-6-1-2-; die ersetzte v2-6-1-1-Serie wurde vollständig entfernt.
- Jedes PNG enthält die identische abgerundete Iconform, kräftige schwarze Comic-Außenkontur, dezente Tiefe und einen weichen flächigen Verlauf: links Grün, über Türkis nach oben rechts Blau.
- Die bisherigen kurzen blau-grünen inneren Linien beziehungsweise Rahmenbögen entfallen vollständig; CSS erzeugt keine zweite Rahmenebene.
- Innenmotive bleiben einfach weiß/hellgrau und erhalten eine deutlich sichtbare schwarze Comic-Umrandung: Rechner, Buch/Nachschlagewerk, WWW, Herstellernamen, Home und Zurück.
- Keine Kategoriefelder, Kleinstbeschriftungen, alten Farbmotive oder dynamischen Dateinamen-Fallbacks.
- Favoriten: 44 × 44 px Touchfläche, sichtbarer 22-px-Kreis oben rechts; inaktiv hell/ruhig, aktiv grün mit dezentem Leuchtring.

Cache- und PWA-Kontrolle
- Eindeutige Dateinamen für Manifest, Suchindex und geänderte CSS-/JavaScript-Ressourcen.
- Service-Worker-Cache-Epoch: v2-6-1-2-icons-r1.
- Alte sk-pct-tools-Caches werden bei Aktivierung vollständig gelöscht.
- Versionskritische Ressourcen werden network-first geladen und offline aus dem exakt benannten Cache bedient.
- Der Service Worker wird mit releasebezogener URL und updateViaCache:none registriert.
- Manifest-Shortcuts und Offline-Kerncache verwenden nur die neue Icon-Serie.

Erhaltene Inhalte und Funktionen
- 10 Startseiten-Apps, Hersteller-Hub, fünf Wissensbeiträge und alle internen/externen Navigationsziele.
- Alle sechs Rechner und ihre Berechnungslogik.
- Einheiten- und Werkstoffdatenbank, Suche, Filter, Sortierung, Favoriten und eigene App-Reihenfolge.
- Smartphone-, Tablet-, Desktop- und 320-px-Reflow-Unterstützung.

Wichtige Dateien
- Manifest: manifest-v2-6-1-2.webmanifest
- Service Worker: service-worker.js
- Navigationsicons: assets/navigation-icons/v2-6-1-2-*.png
- Reproduzierbarer Generator: tools/generate_png_icons.py
- Verbindliche Vorgaben: ICON-DESIGNRICHTLINIE.txt
- Interne Prüfsummen: SHA256SUMS.txt

Deployment
1. Den vollständigen Ordnerinhalt unverändert auf einen HTTPS-Webserver kopieren.
2. Alle Dateien einschließlich service-worker.js und manifest-v2-6-1-2.webmanifest im gelieferten Pfad belassen.
3. Nach dem ersten Online-Aufruf die einmalige Service-Worker-Aktualisierung/Neuladung abwarten.
4. Für eine vollständige Neuinstallation die alte PWA entfernen und anschließend V2.6.1.2-Beta neu installieren.
5. SECURITY-DEPLOYMENT.md für serverseitige Sicherheitsheader beachten.

Tests
- Statisch: python3 tests/validate_project.py
- Browser/Offline: python3 tests/browser_regression.py
- Manuelle Geräteabnahme: TESTPLAN.md
