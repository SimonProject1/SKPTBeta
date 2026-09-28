# SK PLT Tools 2.0.1.2

Vollständiges Release auf Basis von Version 2.0.1.1 und des Clean-Design-Safepoints 2.0.0.0.

## Änderung in 2.0.1.2

- Das Werkstoff-Nachschlagewerk enthält jetzt die fehlende Brotkrümelnavigation `Startseite › Wissensdatenbank › Werkstoff-Nachschlagewerk`.
- Die beiden Navigationslinks führen korrekt zum Webroot und zur Wissensdatenbank-Übersicht.
- Gestaltung und Verhalten entsprechen den vorhandenen Wissensbeiträgen Air Torque und Siemens Sitrans P320.
- Service-Worker-Release und Cache heißen jetzt `2.0.1.2` und `sk-plt-tools-v2.0.1.2-clean`.

## Inhalt

- vollständige statische Website mit 13 HTML-Seiten
- bestehende Rechner, Dokumentation und Gerätewissen
- hersteller- und geräteunabhängiges Werkstoff-Nachschlagewerk
- zentrale, erweiterbare Werkstoffdatei `assets/materials.json`
- Startseitensuche, Wissensdatenbank, Favoriten und Navigationsbaum
- PWA-Manifest, Icons und versionierter Offline-Cache
- unveränderte editierbare PDF-Vorlage der Wissensdatenbank
- statische Release-Prüfung und funktionale Smoke-Tests

## Werkstoff-Nachschlagewerk

Die Seite `wissensdatenbank/werkstoff-nachschlagewerk/` unterstützt:

- Brotkrümelnavigation zurück zur Startseite und zur Wissensdatenbank
- Suche nach Werkstoffnummer mit und ohne Punkt
- Suche nach Kurzname, AISI/ASTM-Bezeichnung, UNS und gebräuchlichen Namen
- Filter nach Werkstoffgruppen
- bewusste Mehrfachtreffer bei mehrdeutigen Angaben wie `316L`
- klare Abgrenzung zwischen Walz-/Knetwerkstoffen und Stahlguss
- Vergleiche `316 gegen 316L` und `1.4404 gegen 1.4408`
- Quellenlinks und identischen Sicherheitshinweis pro Datensatz

Die Inhalte dienen nur der Orientierung. Es erfolgt keine automatische Werkstofffreigabe, keine pauschale Medienbeständigkeitsbewertung und keine Zusage vollständiger Austauschbarkeit.

## Unverändert übernommen

- Favoriten-Fix aus Version 2.0.1.1 mit dem vorhandenen Local-Storage-Schlüssel `skPltToolsFavoritesV2`
- Clean Design, Header, Footer, Kachelgestaltung und eingefrorene Infrastruktur
- Rechner, Dokumentationsfunktionen, Gerätewissen, Filter, Sortierung und Navigation
- Service Worker ohne Response-Rewriting
- No-op-Kompatibilitätsdateien
- Wissensdatenbank-Vorlagen einschließlich der editierbaren PDF bytegenau

## Installation

1. Vorhandenen Webroot vollständig sichern.
2. Das Paket `SK-PLT-Tools-V2.0.1.2.zip` vollständig entpacken.
3. Den **gesamten Inhalt des Ordners `SK-PLT-Tools-V2.0.1.2`** in den Webroot hochladen und vorhandene Dateien ersetzen.
4. `service-worker.js` im gleichen Webroot wie `index.html` belassen.
5. Website einmal online öffnen und neu laden, damit Cache `sk-plt-tools-v2.0.1.2-clean` aktiviert wird.
6. `TESTBERICHT-UND-ABNAHME.md` durchführen.

## Clean Design und Infrastruktur

- Finale Header-, Footer-, Versions-, Kachel- und Integrationsstruktur liegt direkt in HTML/CSS.
- JavaScript wird nur für echte Interaktionen, Suche, Vergleiche, Rechner, Favoriten und Navigation verwendet.
- Der Service Worker übernimmt ausschließlich versionierten Cache, Network-first-Navigation und Offline-Fallback; kein Response-Rewriting.
- Bestehende No-op-Kompatibilitätsdateien bleiben unverändert im Paket.

## Lokaler Test

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 8080
```

Danach `http://localhost:8080/` öffnen und die Browser-Abnahme aus `TESTBERICHT-UND-ABNAHME.md` durchführen.

Version 2.0.1.2 · Entwickelt von Simon Kiesler
