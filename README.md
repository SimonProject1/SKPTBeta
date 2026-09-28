# SK PLT Tools 2.0.2.0

Vollständiges Release auf Basis von Version 2.0.1.2 und des Clean-Design-Safepoints 2.0.0.0.

## Änderung in 2.0.2.0

- Neuer Wissensbeitrag `Vacon · Frequenzumrichter · Ist-/Sollwert-Abweichung im PLS`.
- Der Beitrag dokumentiert den Prüfhinweis zu Parameter `2.2.3.7` und zur Einstellung auf die maximale Frequenz.
- Vollständige Einbindung in Wissensdatenbank, Wissenssuche, Startseitensuche, Favoriten, Navigationsbaum und Offline-Precache.
- Nicht passende Wissenskacheln werden bei der Suche zuverlässig ausgeblendet.
- Service-Worker-Release und Cache heißen jetzt `2.0.2.0` und `sk-plt-tools-v2.0.2.0-clean`.

## Inhalt

- vollständige statische Website mit 14 HTML-Seiten
- bestehende Rechner, Dokumentation und Gerätewissen
- vier favoritenfähige Wissenskacheln: Werkstoffe, Air Torque, Siemens und Vacon
- hersteller- und geräteunabhängiges Werkstoff-Nachschlagewerk
- zentrale, erweiterbare Werkstoffdatei `assets/materials.json`
- Startseitensuche, Wissensdatenbank, Favoriten und Navigationsbaum
- PWA-Manifest, Icons und versionierter Offline-Cache
- unveränderte Wissensdatenbank-Vorlagen
- statische Release-Prüfung und funktionale Smoke-Tests

## Vacon-Wissensbeitrag

Die Seite `wissensdatenbank/vacon-frequenzumrichter-ist-sollwert-abweichung/` enthält:

- Hersteller: Vacon
- Gerät: Frequenzumrichter
- Thema: Ist-/Sollwert-Abweichung im PLS
- zu prüfender Parameter: `2.2.3.7`
- Hinweis: Der Parameter sollte im Regelfall auf die maximale Frequenz eingestellt sein.

Der Beitrag ist ein praktischer Prüfhinweis. Vor Parameteränderungen sind die gültige Herstellerdokumentation, der konkrete Gerätestand sowie die Motor-, Anlagen- und Inbetriebnahmevorgaben zu prüfen.

## Unverändert übernommen

- Favoritensystem mit dem Local-Storage-Schlüssel `skPltToolsFavoritesV2`
- Clean Design, Header, Footer, Kachelgestaltung und eingefrorene Infrastruktur
- Rechner, Dokumentationsfunktionen, bestehendes Gerätewissen, Filter, Sortierung und Navigation
- Werkstoff-Nachschlagewerk mit zehn Datensätzen, Filtern, Vergleichen und Quellen
- Service Worker ohne Response-Rewriting
- No-op-Kompatibilitätsdateien
- Wissensdatenbank-Vorlagen einschließlich editierbarer PDF bytegenau

## Installation

1. Vorhandenen Webroot vollständig sichern.
2. Das Paket `SK-PLT-Tools-V2.0.2.0.zip` vollständig entpacken.
3. Den **gesamten Inhalt des Ordners `SK-PLT-Tools-V2.0.2.0`** in den Webroot hochladen und vorhandene Dateien ersetzen.
4. `service-worker.js` im gleichen Webroot wie `index.html` belassen.
5. Website einmal online öffnen und neu laden, damit Cache `sk-plt-tools-v2.0.2.0-clean` aktiviert wird.
6. `TESTBERICHT-UND-ABNAHME.md` durchführen.

## Lokaler Test

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 8080
```

Danach `http://localhost:8080/` öffnen und die Browser-Abnahme aus `TESTBERICHT-UND-ABNAHME.md` durchführen.

Version 2.0.2.0 · Entwickelt von Simon Kiesler
