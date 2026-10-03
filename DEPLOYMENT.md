# Deployment – SK PLT Tools Beta 2.0.4.1-Beta.1

> Diese Beta parallel zur stabilen Version 2.0.2.0 in einem eigenen Webroot oder Unterordner bereitstellen. Den stabilen Webroot nicht ersetzen. PWA-ID, Start-URL und Cache sind separat.

## Upload

1. `SK-PLT-Tools-V2.0.4.1-Beta.1.zip` vollständig entpacken.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.4.1-Beta.1` in einen eigenen Beta-Webroot kopieren.
3. `service-worker.js` muss neben `index.html` liegen.
4. Die Anwendung einmal online öffnen und neu laden. Dadurch wird `sk-plt-tools-beta-v2.0.4.1-Beta.1` aktiviert; ausschließlich ältere Beta-Caches werden entfernt.
5. Prüfen, dass jede Seite `SK PLT Tools Beta` und `BETA` zeigt; `Version 2.0.4.1-Beta.1` darf sichtbar ausschließlich einmal im Hero der Startseite stehen.
6. Im Baummenü prüfen, dass unter **Wissen → Siemens → SPS** nur **Rohwert Grundlagen** erscheint.
7. Im Rohwert-Grundlagenartikel prüfen, dass die Breadcrumb-Links **Startseite** und **Wissensdatenbank** cyan und nicht lila dargestellt werden.
8. Auf der Startseite die Kachel **E+H Device Viewer**, die sichtbare Externkennzeichnung und das Öffnen in einem neuen Tab prüfen.
9. Sicherstellen, dass die Kachel keine Seriennummern- oder sonstigen Eingabefelder in SK PLT Tools anbietet.
10. Startseitensuche, Filter **Externe Dienste**, Favoriten und Navigationsbaum prüfen.
11. Regressionstest für Rechner, Wissensdatenbank und mobile Ansicht gemäß `TESTBERICHT-UND-ABNAHME.md` durchführen.
12. Paketintegrität mit `SHA256SUMS.txt` prüfen.

## Automatische Prüfung

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

## Externe Abhängigkeit

Der E+H Device Viewer benötigt eine Netzwerkverbindung und wird nicht in den Offline-Cache aufgenommen. Ausfall, Änderungen und Inhalte des externen Dienstes liegen außerhalb von SK PLT Tools. Alle übrigen bereits lokal geladenen Kernfunktionen bleiben offlinefähig.

## Stabile Version schützen

- `SK-PLT-Tools-V2.0.2.0.zip` nicht ändern oder überschreiben.
- Kein Deployment in den produktiven 2.0.2.0-Webroot.
- Beta und Stable verwenden getrennte PWA-IDs und Cache-Präfixe.

## Rückfall

Bei einem Abbruch der Abnahme nur den separaten Beta-Webroot zurücksetzen. Die stabile Installation 2.0.2.0 bleibt davon unberührt.
