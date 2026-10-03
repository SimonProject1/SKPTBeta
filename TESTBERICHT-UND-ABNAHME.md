# Testbericht und Abnahme – SK PLT Tools 2.0.4.2-Beta.1

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
python tools/validate_release.py
```

Geprüft werden 16 HTML-Seiten, lokale Referenzen, JavaScript- und JSON-Syntax, technische Versionierung, genau eine sichtbare Versionsanzeige im Startseiten-Hero, einheitliche Footer, Suche, Filterung, Sortierung, Favoriten, Navigation, Offline-Cache, Werkstoffdaten, bestehende Rechner-Sollwerte sowie die getrennten Rohwert-Skalierungsmodelle.

Zusätzliche Regressionstests für 2.0.4.2-Beta.1:

- Der Knoten **Wissen → Wissensdatenbank** wird als gemeinsame `.sk-tree-node-row` aus Pfeilschaltfläche und Link erzeugt.
- Kein Link ist innerhalb einer `.sk-tree-node-toggle`-Schaltfläche verschachtelt.
- Knoten-Kachel und übrige Navigationskacheln verwenden den dunkelblauen Hintergrund `rgb(10, 38, 57)` beziehungsweise `#0a2639`.
- Der Auf-/Zuklapp-Pfeil verwendet `rgb(137, 211, 41)` beziehungsweise `#89d329`.
- Pfeilschaltfläche und Link liegen vollständig innerhalb der Kachel; die Pfeilschaltfläche ist vertikal auf die Kachelmitte ausgerichtet.
- `aria-controls`, `aria-expanded` und die dynamische Auf-/Zuklapp-Beschriftung bleiben vorhanden.
- Der Knoten **Wissen → Siemens → SPS** besitzt weiterhin exakt den Eintrag **Rohwert Grundlagen**.
- `SHA256SUMS.txt` enthält jede Paketdatei außer der Prüfsummendatei selbst und stimmt bytegenau mit dem ausgelieferten Stand überein.

## Automatisches Ergebnis

**Bestanden am 03.10.2026:**

- Statische Release-Prüfung: 16 Seiten, lokale Referenzen, Versionskonsistenz, Manifest, Service Worker, semantisch gültiger Wissen-Knoten, Kachel-/Pfeilregeln, Wissensdatenbank und vollständige SHA-256-Dateiliste bestanden.
- Funktionaler Regressionstest: Analogsignal-, P+F-, Pt-, Einheiten-, Spannungsfall- und Siemens-Rohwert-Rechner bestanden; Werkstoffsuche, Favoritenlogik und beide getrennten Rohwert-Skalierungsmodelle bestanden.
- Browser-Smoke-Test mit Chromium: Desktop 1440 × 1050 px, Tablet 820 × 1180 px und Mobil 390 × 844 px bestanden; der Wissen-Knoten liegt auf Desktop und Mobil vollständig innerhalb der Kachel, der Pfeil ist zentriert, und alle 16 Seiten bleiben ohne horizontales Überlaufen oder Browser-Konsolenfehler.
- Aktualisierte visuelle Nachweise liegen in `test-artifacts/`; der geöffnete Wissen-Knoten ist als `navigation-wissen-desktop.png` und `navigation-wissen-mobile.png` dokumentiert.

Die manuelle Abnahme auf realem PC und iPhone/iPad bleibt offen.

## Manuelle Geräteabnahme

| Nr. | Prüfung | PC | iPhone/iPad | Bemerkung |
|---:|---|:---:|:---:|---|
| 1 | Startseite und alle Kacheln öffnen | ☐ | ☐ | |
| 2 | Suche, Sortierung, Favoriten und Navigation prüfen | ☐ | ☐ | |
| 3 | Wissen öffnen: „Wissensdatenbank“ vollständig innerhalb der dunkelblauen Kachel | ☐ | ☐ | |
| 4 | Grünen Pfeil auf mittige Ausrichtung sowie Auf-/Zuklappen prüfen | ☐ | ☐ | |
| 5 | Unter Wissen → Siemens → SPS nur „Rohwert Grundlagen“ prüfen | ☐ | ☐ | |
| 6 | Breadcrumb-Links im Rohwert-Grundlagenartikel auf Cyan prüfen | ☐ | ☐ | |
| 7 | Siemens-Kartenprofile und beide Skalierungsmodelle prüfen | ☐ | ☐ | |
| 8 | Offline-Start bereits geladener Kernseiten prüfen | ☐ | ☐ | |
| 9 | Keine horizontale Überlagerung bei 320–390 px | ☐ | ☐ | |
| 10 | Versionsanzeige nur einmal im Startseiten-Hero | ☐ | ☐ | |

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
