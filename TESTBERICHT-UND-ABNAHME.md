# Testbericht und Abnahme – SK PLT Tools 2.0.4.1-Beta.1

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
python tools/validate_release.py
```

Geprüft werden 16 HTML-Seiten, lokale Referenzen, JavaScript- und JSON-Syntax, technische Versionierung, genau eine sichtbare Versionsanzeige im Startseiten-Hero, einheitliche Footer, Suche, Filterung, Sortierung, Favoriten, Navigation, Offline-Cache, Werkstoffdaten, bestehende Rechner-Sollwerte sowie die getrennten Rohwert-Skalierungsmodelle.

Zusätzliche Regressionstests für 2.0.4.1-Beta.1:

- Der Knoten **Wissen → Siemens → SPS** besitzt exakt einen Eintrag: **Rohwert Grundlagen**.
- Ein exakter Eintrag **Rohwert-Rechner** ist in diesem Wissenszweig nicht vorhanden.
- Die Breadcrumb-Links **Startseite** und **Wissensdatenbank** haben die korrekten Ziele `../../` und `../`.
- Beide Links werden im Browser als `rgb(0, 183, 232)` beziehungsweise `#00b7e8` dargestellt.
- `SHA256SUMS.txt` enthält jede Paketdatei außer der Prüfsummendatei selbst und stimmt bytegenau mit dem ausgelieferten Stand überein.

## Automatisches Ergebnis

**Bestanden am 03.10.2026:**

- Statische Release-Prüfung: 16 Seiten, lokale Referenzen, Versionskonsistenz, Manifest, Service Worker, Suche, bereinigter Wissensbaum, Breadcrumb-Darstellung, Wissensdatenbank, vollständige SHA-256-Prüfsummen und JavaScript-Syntax bestanden.
- Funktionaler Regressionstest: Analogsignal-, P+F-, Pt-, Einheiten-, Spannungsfall- und Siemens-Rohwert-Rechner bestanden; Werkstoffsuche, Favoritenlogik und beide getrennten Rohwert-Skalierungsmodelle bestanden.
- Browser-Smoke-Test mit Microsoft Edge/Chromium: Desktop 1440 × 1050 px, Tablet 820 × 1180 px und Mobil 390 × 844 px bestanden; Breadcrumb-Farben und bereinigter Wissensbaum bestanden; alle 16 Seiten ohne horizontales Überlaufen und ohne Browser-Konsolenfehler.
- Visuelle Nachweise liegen in `test-artifacts/`.

Die manuelle Abnahme auf realem PC und iPhone/iPad bleibt offen.

## Manuelle Geräteabnahme

| Nr. | Prüfung | PC | iPhone/iPad | Bemerkung |
|---:|---|:---:|:---:|---|
| 1 | Startseite und alle Kacheln öffnen | ☐ | ☐ | |
| 2 | Suche, Sortierung, Favoriten und Navigation prüfen | ☐ | ☐ | |
| 3 | Unter Wissen → Siemens → SPS nur „Rohwert Grundlagen“ prüfen | ☐ | ☐ | |
| 4 | Breadcrumb-Links im Rohwert-Grundlagenartikel auf einheitliche cyanfarbene Darstellung prüfen | ☐ | ☐ | |
| 5 | Rohwert-Grundlagenartikel und Übergang zum Rechner prüfen | ☐ | ☐ | |
| 6 | Siemens-Kartenprofile und beide Skalierungsmodelle prüfen | ☐ | ☐ | |
| 7 | Offline-Start bereits geladener Kernseiten prüfen | ☐ | ☐ | |
| 8 | Keine horizontale Überlagerung bei 320–390 px | ☐ | ☐ | |
| 9 | Versionsanzeige nur einmal im Startseiten-Hero | ☐ | ☐ | |

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
