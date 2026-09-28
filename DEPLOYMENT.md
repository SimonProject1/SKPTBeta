# Deployment – SK PLT Tools Beta 2.0.3.3-Beta.1

> Diese Beta parallel zur stabilen Version 2.0.2.0 in einem eigenen Webroot oder Unterordner bereitstellen. Den stabilen Webroot nicht ersetzen. PWA-ID, Start-URL und Cache sind separat.

## Upload

1. Das Downloadpaket `SK-PLT-Tools-V2.0.3.3-Beta.1.zip` vollständig entpacken.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.3-Beta.1` in einen eigenen Beta-Webroot kopieren.
3. `service-worker.js` muss im gleichen Webroot wie `index.html` liegen.
4. Die Anwendung einmal mit Netzwerkverbindung öffnen und neu laden. Dadurch wird der Cache `sk-plt-tools-beta-v2.0.3.3-Beta.1` aktiviert; ausschließlich ältere Beta-Caches werden entfernt.
5. Im Browser prüfen, dass auf jeder Seite `SK PLT Tools Beta`, `BETA` und `Version 2.0.3.3-Beta.1` sichtbar sind.
6. Den Siemens-SPS-Analogwert-Rechner für alle vier Signalbereiche, beide Eingaberichtungen, den Schieberegler und alle fünf Bereichszustände prüfen.
7. Startseitensuche, Favoriten, Navigationsbaum, Wissensdatenbank und mobile Ansicht gemäß `TESTBERICHT-UND-ABNAHME.md` prüfen.
8. Paketintegrität mit `SHA256SUMS.txt` prüfen.

## Automatische Prüfung

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
```

## Stabile Version schützen

- Das Originalpaket `SK-PLT-Tools-V2.0.2.0.zip` nicht ändern oder überschreiben.
- Kein Deployment in den produktiven 2.0.2.0-Webroot.
- Beta und Stable verwenden getrennte PWA-IDs und getrennte Cache-Präfixe.

## Wissensdatenbank-Vorlagen

Die drei Dateien unter `wissensdatenbank/vorlagen/` wurden nicht inhaltlich verändert. Die statische Release-Prüfung kontrolliert ihre bekannten SHA-256-Hashes.

## Rückfall

Bei einem Abbruch der Abnahme nur den separaten Beta-Webroot zurücksetzen. Die stabile Installation 2.0.2.0 bleibt davon unberührt.
