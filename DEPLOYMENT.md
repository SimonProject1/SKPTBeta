# Deployment – SK PLT Tools Beta 2.0.3.0-Beta.1

> Diese Beta parallel zur stabilen Version 2.0.2.0 in einem eigenen Webroot oder Unterordner bereitstellen. Den stabilen Webroot nicht ersetzen. PWA-ID, Start-URL und Cache sind separat.

# Upload-Anleitung – SK PLT Tools 2.0.3.0-Beta.1

## Vorbereitungen

- Aktuell veröffentlichten Webroot vollständig sichern.
- Prüfen, dass das Zielsystem statische HTML-, CSS-, JavaScript-, JSON-, PNG-, PDF-, DOCX- und Webmanifest-Dateien unverändert ausliefert.
- Nicht nur Einzel- oder Patchdateien ersetzen: Version 2.0.3.0-Beta.1 ist ein vollständig gemeinsam geprüfter Projektstand.

## Upload und Rollout

1. Das Downloadpaket `SK-PLT-Tools-V2.0.3.0-Beta.1.zip` vollständig entpacken.
2. Alle Dateien und Ordner **aus dem Ordner `SK-PLT-Tools-V2.0.3.0-Beta.1`** in den Webroot kopieren und vorhandene Dateien ersetzen.
3. Prüfen, dass insbesondere die neue Seite `wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/index.html`, `assets/vacon-wissen.css`, `assets/search-index.json`, `assets/navigation-tree.json` und `service-worker.js` übertragen wurden.
4. Sonstige `assets/version-*.js` aus älteren Releases löschen. Die mitgelieferte `assets/version-1.9.8.5.js` ist ein absichtlicher No-op für die Migration und bleibt Bestandteil dieses Pakets.
5. `service-worker.js` muss im gleichen Webroot wie `index.html` liegen.
6. Die Anwendung einmal mit Netzwerkverbindung öffnen und anschließend neu laden. Dadurch wird der Cache `sk-plt-tools-v2.0.3.0-Beta.1-clean` aktiviert; ältere Cache-Namen werden entfernt.
7. Im Browser kontrollieren, dass unter dem Logo und im Footer „Version 2.0.3.0-Beta.1“ angezeigt wird.
8. Die Wissensdatenbank öffnen. Es müssen vier Wissenskacheln sichtbar sein: Werkstoff-Nachschlagewerk, Air Torque Antrieb, Siemens Sitrans P320 und Vacon Frequenzumrichter.
9. Den Vacon-Beitrag öffnen und Brotkrümelnavigation, Hersteller, Gerät, Thema, Parameter `2.2.3.7` und den Hinweis zur maximalen Frequenz prüfen.
10. Bei allen vier Wissenskacheln Favorit setzen und entfernen. Jeder Eintrag muss im linken Favoritenmenü erscheinen; Seitenwechsel und Neuladen dürfen den Status nicht löschen.
11. In der Startseitensuche nach `Vacon`, `2.2.3.7` und `maximale Frequenz` suchen. Der Vacon-Wissensbeitrag muss jeweils angeboten werden.
12. Die vollständige Checkliste in `TESTBERICHT-UND-ABNAHME.md` durchführen.
13. Die Paketintegrität mit `SHA256SUMS.txt` prüfen.

## Wichtiger Hinweis zu den Wissensdatenbank-Vorlagen

Die drei Dateien unter `wissensdatenbank/vorlagen/` wurden nicht inhaltlich verändert. Die statische Release-Prüfung kontrolliert weiterhin ihre bekannten SHA-256-Hashes.

## Rückfall

Bei einem Abbruch der Abnahme den zuvor gesicherten Webroot vollständig wiederherstellen. Anschließend Website-Daten beziehungsweise Service Worker der Site löschen oder eine harte Aktualisierung durchführen.

## Architekturhinweis

Die Clean-Design-Infrastruktur bleibt unverändert: finale Header-, Footer- und Kachelstrukturen stehen direkt im HTML; der Service Worker schreibt keine Antworten um. Version 2.0.3.0-Beta.1 ergänzt den Vacon-Wissensbeitrag und dessen statische Integrationen.
