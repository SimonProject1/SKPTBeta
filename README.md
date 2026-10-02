# SK PLT Tools Beta 2.0.3.4-Beta.1

Vollständige Beta auf Basis von 2.0.3.3-Beta.1. Die stabile Referenz 2.0.2.0 bleibt unverändert.

## Neu in 2.0.3.4-Beta.1

- Neue Startseitenkachel **E+H Device Viewer**.
- Ziel: `https://netilion.endress.com/app/library/device_viewer`.
- Der offizielle Endress+Hauser-Dienst wird klar als extern gekennzeichnet und in einem neuen Tab geöffnet.
- `noopener`, `noreferrer`, `external` und `referrerpolicy="no-referrer"` begrenzen die Kopplung zur SK-PLT-Tools-Seite.
- SK PLT Tools enthält kein Seriennummernfeld und speichert keine Seriennummern oder Eingaben für diesen Dienst.
- Neuer Startseitenfilter **Externe Dienste**.
- Der Eintrag ist im Navigationsbaum verfügbar; als Favorit behält er das Öffnen in einem neuen Tab bei.
- Versionsangaben, Ressourcenkennungen, PWA-ID, `start_url` und separater Beta-Cache wurden auf 2.0.3.4-Beta.1 fortgeschrieben.

## Unverändert übernommen

Siemens Rohwert, alle weiteren Rechner, Messstellen-Dokumentation, VDE-Plausibilitätsprüfung, Wissensdatenbank, Suche, Sortierung, Favoriten, Navigation, responsive Darstellung und Offline-Betrieb wurden aus 2.0.3.3-Beta.1 übernommen.

## Installation und Test

1. Das Paket in einen eigenen Beta-Webroot bzw. Unterordner entpacken; die stabile Installation 2.0.2.0 nicht überschreiben.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.4-Beta.1` bereitstellen.
3. Automatische Prüfungen im Projektordner starten:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

4. Danach die manuelle Abnahme aus `TESTBERICHT-UND-ABNAHME.md` auf PC und iPhone/iPad durchführen.

## Datenschutz und externer Dienst

SK PLT Tools übergibt an den E+H Device Viewer keine in SK PLT Tools erfassten Seriennummern oder Formulardaten. Eingaben erfolgen ausschließlich auf der externen Herstellerseite. Für Inhalt, Verfügbarkeit, Datenschutz und Nutzungsbedingungen des externen Dienstes ist dessen Betreiber verantwortlich.

2.0.3.4-Beta.1 · Beta · Entwickelt von Simon Kiesler
