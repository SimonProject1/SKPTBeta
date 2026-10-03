# Testbericht und Abnahme – SK PLT Tools 2.0.4.0-Beta.1

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

Geprüft werden 16 HTML-Seiten, lokale Referenzen, JavaScript- und JSON-Syntax, technische Versionierung, genau eine sichtbare Versionsanzeige im Startseiten-Hero, einheitliche Footer, Suche, Filterung, Sortierung, Favoriten, Navigation, Offline-Cache, Werkstoffdaten, bestehende Rechner-Sollwerte sowie die getrennten Rohwert-Skalierungsmodelle.

## Automatisches Ergebnis

**Bestanden am 03.10.2026:**

- Statische Release-Prüfung: 16 Seiten, lokale Referenzen, Versionskonsistenz, Manifest, Service Worker, Suche, Navigation, Wissensdatenbank und JavaScript-Syntax bestanden.
- Funktionaler Regressionstest: Analogsignal-, P+F-, Pt-, Einheiten-, Spannungsfall- und Siemens-Rohwert-Rechner bestanden; Werkstoffsuche, Favoritenlogik und beide getrennten Rohwert-Skalierungsmodelle bestanden.
- Browser-Smoke-Test mit Microsoft Edge/Chromium: Desktop 1440 × 1050 px, Tablet 820 × 1180 px und Mobil 390 × 844 px bestanden; alle 16 Seiten ohne horizontales Überlaufen und ohne Browser-Konsolenfehler.
- Visuelle Nachweise liegen in `test-artifacts/`.

Die manuelle Abnahme auf realem PC und iPhone/iPad bleibt offen.

## Manuelle Geräteabnahme

| Nr. | Prüfung | PC | iPhone/iPad | Bemerkung |
|---:|---|:---:|:---:|---|
| 1 | Startseite und alle Kacheln öffnen | ☐ | ☐ | |
| 2 | Suche, Sortierung, Favoriten und Navigation prüfen | ☐ | ☐ | |
| 3 | Rohwert-Grundlagenartikel und Übergang zum Rechner prüfen | ☐ | ☐ | |
| 4 | Siemens-Kartenprofile und beide Skalierungsmodelle prüfen | ☐ | ☐ | |
| 5 | Offline-Start bereits geladener Kernseiten prüfen | ☐ | ☐ | |
| 6 | Keine horizontale Überlagerung bei 320–390 px | ☐ | ☐ | |
| 7 | Versionsanzeige nur einmal im Startseiten-Hero | ☐ | ☐ | |

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
