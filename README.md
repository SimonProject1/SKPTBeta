# SK PLT Tools Beta 2.0.4.2-Beta.1

Vollständiger Beta-Patchstand auf Basis von 2.0.4.1-Beta.1. Die stabile Referenz 2.0.2.0 bleibt unverändert.

## Ziel dieses Stands

2.0.4.2-Beta.1 korrigiert die Darstellung des geöffneten Eintrags **Wissen → Wissensdatenbank** im seitlichen Navigationsbaum. Rechner-, Wissens- und Prüfinhalte bleiben funktional unverändert.

## Änderungen gegenüber 2.0.4.1-Beta.1

- **Wissensdatenbank** wird innerhalb einer dunkelblauen, abgerundeten Knoten-Kachel dargestellt.
- Der Auf-/Zuklapp-Pfeil sitzt in einer festen, vertikal und horizontal zentrierten Schaltfläche und verwendet das grüne Navigations-Akzentfarbschema.
- Die vorher ungültige Verschachtelung eines Links in einer Schaltfläche wurde durch eine semantisch gültige Knoten-Zeile aus separater Schaltfläche und Link ersetzt. Dadurch verschiebt der Browser den Link nicht mehr aus der Kachel.
- Hover-, Fokus- und Aktivzustände wirken auf die vollständige Knoten-Kachel; Tastaturbedienung und ARIA-Zuordnung zum Unterbaum bleiben erhalten.
- Sichtbare und technische Versionsangaben, Cache-Buster, Manifest-ID, PWA-Start-URL und Beta-Cache wurden konsistent auf `2.0.4.2-Beta.1` angehoben.
- Release-, statische und browserbasierte Prüfungen enthalten explizite Regressionstests für Knotenstruktur, Kachelhintergrund, Pfeilfarbe, Ausrichtung und Elementgrenzen.
- `SHA256SUMS.txt` enthält die Prüfsummen des vollständigen Projektstands.

## Vollständig enthalten

- Alle 16 HTML-Seiten und alle Werkzeuge aus 2.0.4.1-Beta.1.
- Analogsignal-, Siemens-Rohwert-, P+F-, Pt-, Einheiten- und Spannungsfall-Rechner.
- Messstellen-Dokumentation und VDE-0100-600-Plausibilitätsprüfung.
- Suche, Filter, Sortierung, Favoriten, Baumnavigation und Offline-Cache.
- Wissensdatenbank, Werkstoffdaten, Vorlagen, Projektdokumentation, Testskripte und visuelle Testnachweise.
- Sichtbare Versionsanzeige ausschließlich im Hero der Startseite.
- Einheitlicher Footer: „SK PLT Tools Beta · Entwickelt von Simon Kiesler“.

## Installation und Test

1. Das Paket in einen eigenen Beta-Webroot entpacken; die stabile Version 2.0.2.0 nicht überschreiben.
2. Im Projektordner ausführen:

```bash
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
python tools/validate_release.py
```

3. Danach die manuelle Geräteabnahme gemäß `TESTBERICHT-UND-ABNAHME.md` durchführen.
4. Die vollständige Paketintegrität mit `SHA256SUMS.txt` prüfen.
