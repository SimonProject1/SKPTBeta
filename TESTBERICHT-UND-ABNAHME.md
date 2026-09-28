# Testcheckliste und Abnahme – SK PLT Tools 2.0.1.2

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
```

Die automatisierte Prüfung kontrolliert unter anderem:

- 13 erwartete HTML-Seiten
- genau einen statischen Header und Footer je Seite
- Version 2.0.1.2 in HTML, Skripten, Manifest und Service Worker
- Cache-Namen `sk-plt-tools-v2.0.1.2-clean`
- vollständige Brotkrümelnavigation auf der Werkstoffseite mit `Startseite`, `Wissensdatenbank` und `Werkstoff-Nachschlagewerk`
- korrekte lokale Ziele der Breadcrumb-Links (`../../` und `../`)
- acht unveränderte Startseiten-Werkzeugkacheln
- genau drei erwartete Wissenskacheln
- Favoritenintegration (`tool-card`) bei Werkstoff-Nachschlagewerk, Air Torque Antrieb und Siemens Sitrans P320
- vorhandenen Local-Storage-Schlüssel sowie Klickschutz- und Renderlogik des bestehenden Favoritensystems
- vollständige lokale Referenzen und JavaScript-Syntax
- zehn Werkstoffdatensätze mit Pflichtfeldern, Quellen und gültigen Gruppen
- Suchtreffer `14404` → `1.4404`
- Mehrfachtreffer `316L` → `1.4404`, `1.4409` und `1.4435`
- Gruppenfilter `316L` + Stahlguss → `1.4409`
- Vergleiche `316 gegen 316L` und `1.4404 gegen 1.4408`
- Offline-Precache der Werkstoffseite und zentralen Datendatei
- unveränderte Hashes der drei Vorlagendateien unter `wissensdatenbank/vorlagen/`
- bestehende Rechner-Sollwerte

## Browser-Abnahme

| Nr. | Prüfung | Soll | PC | iPhone |
|---:|---|---|:---:|:---:|
| 1 | Startseite direkt öffnen | Finales Clean Design ohne sichtbaren Umbau | ☐ | ☐ |
| 2 | Unterseite öffnen und „Startseite“ wählen | Kein altes Layout, Logo oder Versionsplatzhalter | ☐ | ☐ |
| 3 | Seite hart neu laden | Version 2.0.1.2 unter Logo und im Footer | ☐ | ☐ |
| 4 | Werkstoff-Nachschlagewerk öffnen | Brotkrümel `Startseite › Wissensdatenbank › Werkstoff-Nachschlagewerk` vollständig sichtbar | ☐ | ☐ |
| 5 | Im Werkstoff-Breadcrumb „Startseite“ wählen | Startseite öffnet korrekt | ☐ | ☐ |
| 6 | Im Werkstoff-Breadcrumb „Wissensdatenbank“ wählen | Übersicht der Wissensbeiträge öffnet korrekt | ☐ | ☐ |
| 7 | Breadcrumb auf schmalem Display prüfen | Vollständig lesbar, sauberer Umbruch, keine Überlagerung | ☐ | ☐ |
| 8 | Wissensdatenbank öffnen | Drei Wissenskacheln sichtbar; jede zeigt einen Favoritenstern | ☐ | ☐ |
| 9 | Werkstoff-Nachschlagewerk als Favorit setzen | Stern aktiv; Eintrag im linken Favoritenmenü | ☐ | ☐ |
| 10 | Air Torque Antrieb als Favorit setzen | Stern aktiv; Eintrag im linken Favoritenmenü | ☐ | ☐ |
| 11 | Siemens Sitrans P320 als Favorit setzen | Stern aktiv; Eintrag im linken Favoritenmenü | ☐ | ☐ |
| 12 | Mit gesetzten Favoriten Seite wechseln und neu laden | Alle Favoriten und Zähler bleiben erhalten | ☐ | ☐ |
| 13 | Favorit im linken Menü öffnen | Richtiger Wissensbeitrag öffnet | ☐ | ☐ |
| 14 | Stern bei jeder Wissenskachel erneut wählen | Nur Favorit wird entfernt; keine Seitennavigation | ☐ | ☐ |
| 15 | Jede Wissenskachel außerhalb des Sterns wählen | Zugehörige Wissensseite öffnet unverändert | ☐ | ☐ |
| 16 | Wissenssuche verwenden | Filterung blendet Kacheln ein/aus; Sterne bleiben an den sichtbaren Kacheln korrekt | ☐ | ☐ |
| 17 | Navigationsbaum öffnen | Alle Wissensseiten vorhanden und erreichbar | ☐ | ☐ |
| 18 | Startseitensuche `316L` | Wissensbeitrag erscheint; Öffnen übernimmt `316L` in die Werkstoffsuche | ☐ | ☐ |
| 19 | Werkstoffsuche `1.4404` und `14404` | Beide Schreibweisen liefern 1.4404 | ☐ | ☐ |
| 20 | Werkstoffsuche `316L` | Mehrere Treffer: 1.4404, 1.4409/CF3M und 1.4435 | ☐ | ☐ |
| 21 | Werkstoffsuche `CF8M` | 1.4408/GX5CrNiMo19-11-2; Stahlguss klar markiert | ☐ | ☐ |
| 22 | Werkstoffsuche `Alloy 59` | 2.4605/N06059 | ☐ | ☐ |
| 23 | Gruppenfilter und Vergleiche | Filter sowie beide Direktvergleiche funktionieren | ☐ | ☐ |
| 24 | Externe Quellenlinks | Öffnen in neuem Tab; Anwendungsnavigation bleibt erhalten | ☐ | ☐ |
| 25 | Offline-Test nach Online-Aufruf | Startseite, Wissensseiten, CSS/JS/JSON und bestehende Kernseiten laden aus Cache | ☐ | ☐ |
| 26 | PDF-Vorlage herunterladen | Datei funktioniert und ist gegenüber 2.0.1.1 bytegenau unverändert | ☐ | ☐ |
| 27 | Responsive Darstellung | Breadcrumb, Suche, Filter, Karten, Sterne, Favoritenmenü und Vergleiche vollständig bedienbar | ☐ | ☐ |
| 28 | Bestehende Rechner | Alle bisherigen Sollwerte unverändert | ☐ | ☐ |

## Rechner-Sollwerte

- Analogsignal: 0…100 auf 4…20 mA, Eingabe 50 → **12,000 mA / 50,0 %**.
- P+F: X1=0, Y1=4, X2=100, Y2=20 → **K=0,160000; Nullpunkt=4,000000**.
- Pt100: 0 °C → **100,000 Ω**.
- Einheiten: 1 bar → **1.000,000 mbar**.
- Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1,00, Grenzwert 6 % → **6,93 V; 1,73 %; Lastspannung 393,07 V; Reserve +17,07 V**.

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
