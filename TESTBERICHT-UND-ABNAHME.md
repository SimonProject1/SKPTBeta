# Testbericht und Abnahme – 2.0.5.1-Beta.1

Prüfdatum: 03.10.2026

## Prüfumfang

- 16 HTML-Seiten und alle direkten Seitenrouten
- sechs Rechner, Messstellen-Dokumentation und VDE-0100-600-Prüfung
- fünf Wissensbeiträge und Werkstoff-Nachschlagewerk
- Startseitensuche, Kategorienfilter, Sortierung und Suchübergabe an das Werkstoffmodul
- Favoriten hinzufügen, persistieren, öffnen und entfernen
- Navigationsbaum aus `assets/navigation-tree.json`, Auf-/Zuklappen, aktive Links und mobile Darstellung
- Desktop 1440 × 1050, Tablet 820 × 1180 und Mobil 390 × 844
- PWA-Manifest, Service-Worker-Registrierung, Cache-Name, Precache und Offline-Aufrufe
- lokale Referenzen, JavaScript-Syntax, Vorlagendateien und SHA-256-Integrität

## Automatisierte Prüfungen

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Fachliche Funktions-Smoke-Tests | `node tools/functional-smoke-test.js` | Bestanden |
| Statische Release-Validierung | `python tools/validate_release.py` | Bestanden: 16 Seiten, lokale Referenzen, Modulstruktur, Manifest, Precache, Syntax und Integrität |
| Browser-/Responsive-/PWA-/Offline-Test | `python tools/browser-smoke-test.py` bei lokalem Server | Bestanden: Desktop, Tablet, Mobil, Suche, Filter, Sortierung, Favoriten, Navigation und Offline-Aufrufe |
| Prüfsummen | `sha256sum -c SHA256SUMS.txt` | Bestanden |

## Abnahmekriterien

1. Kein Rechnerergebnis weicht von der validierten Ausgangsbasis ab.
2. Jede HTML-Seite ist direkt erreichbar und besitzt genau einen Header, Footer, Favoriten- und Navigationstrigger.
3. Keine Seite erzeugt horizontales Überlaufen auf Tablet oder Mobilgerät.
4. Suche, Favoriten, Sortierung und Navigationsbaum bleiben bedienbar.
5. Der Service Worker aktiviert den Cache `sk-plt-tools-beta-v2.0.5.1-Beta.1` und liefert ausgewählte Seiten und Daten nach Offline-Schaltung aus.
6. Alle lokalen Referenzen und alle in `navigation-tree.json` enthaltenen lokalen Ziele existieren.
7. `SHA256SUMS.txt` stimmt vollständig mit dem Paketinhalt überein.

## Ergebnis

**Bestanden.** Die automatisierten Prüfungen wurden am 03.10.2026 nach der finalen Konsolidierung erfolgreich ausgeführt. Rechnerergebnisse und fachliche Inhalte entsprechen der validierten Ausgangsbasis; gemeinsame Funktionen, Direktseiten, Responsive-Verhalten sowie PWA- und Offline-Aufrufe sind funktionsfähig. Manuelle fachliche Freigaben und gerätespezifische Praxistests bleiben zusätzlich empfohlen.
