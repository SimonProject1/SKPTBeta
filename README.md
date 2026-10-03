# SK PLT Tools Beta 2.0.4.1-Beta.1

Vollständiger Beta-Patchstand auf Basis von 2.0.4.0-Beta.1. Die stabile Referenz 2.0.2.0 bleibt unverändert.

## Ziel dieses Stands

2.0.4.1-Beta.1 behebt zwei klar abgegrenzte Darstellungs- und Navigationsfehler, ohne die vorhandenen Rechner- oder Wissensinhalte funktional zu verändern.

## Änderungen gegenüber 2.0.4.0-Beta.1

- Im Baummenü enthält **Wissen → Siemens → SPS** ausschließlich den Wissensbeitrag **Rohwert Grundlagen**. Der dort irrtümlich zusätzlich aufgeführte **Rohwert-Rechner** wurde entfernt.
- Auf **Wissensdatenbank → Siemens SPS Rohwert Grundlagen** verwenden die Breadcrumb-Links **Startseite** und **Wissensdatenbank** nun dieselbe cyanfarbene Darstellung wie auf den übrigen Wissensdatenbankseiten; der lila Browser-Standardstil wird nicht mehr wirksam.
- Sichtbare und technische Versionsangaben, Cache-Buster, Manifest-ID, PWA-Start-URL und Beta-Cache wurden konsistent auf `2.0.4.1-Beta.1` angehoben.
- Release-, Funktions- und Browserprüfungen wurden um explizite Regressionstests für beide Fehler ergänzt.
- `SHA256SUMS.txt` enthält die Prüfsummen des vollständigen Projektstands.

## Vollständig enthalten

- Alle 16 HTML-Seiten und alle Werkzeuge aus 2.0.4.0-Beta.1.
- Der Wissensbeitrag „Siemens SPS Rohwert Grundlagen“ und der separate Siemens-Rohwert-Rechner.
- Suche, Filter, Sortierung, Favoriten, Baumnavigation und Offline-Cache.
- Werkstoffdaten, Vorlagen, Projektdokumentation, Testskripte und visuelle Testnachweise.
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
