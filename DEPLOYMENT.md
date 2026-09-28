# Upload-Anleitung – SK PLT Tools 2.0.1.2

## Vorbereitungen

- Aktuell veröffentlichten Webroot vollständig sichern.
- Prüfen, dass das Zielsystem statische HTML-, CSS-, JavaScript-, JSON-, PNG-, PDF-, DOCX- und Webmanifest-Dateien unverändert ausliefert.
- Nicht nur Einzel- oder Patchdateien ersetzen: Version 2.0.1.2 ist ein vollständig gemeinsam geprüfter Projektstand.

## Upload und Rollout

1. Das Downloadpaket `SK-PLT-Tools-V2.0.1.2.zip` vollständig entpacken.
2. Alle Dateien und Ordner **aus dem Ordner `SK-PLT-Tools-V2.0.1.2`** in den Webroot kopieren und vorhandene Dateien ersetzen.
3. Prüfen, dass insbesondere `wissensdatenbank/werkstoff-nachschlagewerk/index.html`, `assets/materials.css`, `assets/favorites.js`, `assets/favorites.css`, `service-worker.js` und die vorhandenen Werkstoffdateien übertragen wurden.
4. Sonstige `assets/version-*.js` aus älteren Releases löschen. Die mitgelieferte `assets/version-1.9.8.5.js` ist ein absichtlicher No-op für die Migration und bleibt Bestandteil dieses Pakets.
5. `service-worker.js` muss im gleichen Webroot wie `index.html` liegen.
6. Die Anwendung einmal mit Netzwerkverbindung öffnen und anschließend neu laden. Dadurch wird der Cache `sk-plt-tools-v2.0.1.2-clean` aktiviert; ältere Cache-Namen werden entfernt.
7. Im Browser kontrollieren, dass unter dem Logo und im Footer „Version 2.0.1.2“ angezeigt wird.
8. Das Werkstoff-Nachschlagewerk öffnen und die Brotkrümelnavigation prüfen: „Startseite“ muss zum Webroot, „Wissensdatenbank“ zur Wissensübersicht führen; der letzte Eintrag lautet „Werkstoff-Nachschlagewerk“.
9. Wissensdatenbank öffnen und bei Werkstoff-Nachschlagewerk, Air Torque Antrieb sowie Siemens Sitrans P320 jeweils Favorit setzen und entfernen. Jeder Eintrag muss im linken Favoritenmenü erscheinen; Seitenwechsel und Neuladen dürfen den Status nicht löschen.
10. Bei jeder Wissenskachel zusätzlich außerhalb des Sterns klicken und prüfen, dass die zugehörige Wissensseite weiterhin öffnet.
11. Die vollständige Checkliste in `TESTBERICHT-UND-ABNAHME.md` durchführen.
12. Die Paketintegrität mit `SHA256SUMS.txt` prüfen.

## Wichtiger Hinweis zur Wissensdatenbank-PDF

Die Dateien unter `wissensdatenbank/vorlagen/` wurden nicht inhaltlich verändert. Insbesondere die editierbare PDF bleibt bytegenau unverändert, weil ihre Vorlage in diesem Release nicht geändert wird.

## Rückfall

Bei einem Abbruch der Abnahme den zuvor gesicherten Webroot vollständig wiederherstellen. Anschließend Website-Daten beziehungsweise Service Worker der Site löschen oder eine harte Aktualisierung durchführen.

## Architekturhinweis

Die Clean-Design-Infrastruktur bleibt unverändert: finale Header-, Footer- und Kachelstrukturen stehen direkt im HTML; der Service Worker schreibt keine Antworten um. Version 2.0.1.2 ergänzt ausschließlich die fehlende statische Brotkrümelnavigation im Werkstoff-Nachschlagewerk, die erforderlichen Versions-/Cacheangaben, die Freigabeprüfung und die Release-Dokumentation.
