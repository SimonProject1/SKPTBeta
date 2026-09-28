# Testcheckliste und Abnahme – SK PLT Tools 2.0.2.0

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
```

Die automatisierte Prüfung kontrolliert unter anderem:

- 14 erwartete HTML-Seiten
- genau einen statischen Header und Footer je Seite
- Version 2.0.2.0 in HTML, Skripten, Manifest und Service Worker
- Cache-Namen `sk-plt-tools-v2.0.2.0-clean`
- genau vier erwartete, favoritenfähige Wissenskacheln
- Vacon-Seite mit Hersteller, Gerät, Thema, Parameter `2.2.3.7`, maximaler Frequenz und Stylesheet
- Vacon-Einträge im Suchindex, Navigationsbaum und Offline-Precache
- vollständige Brotkrümelnavigation auf der Werkstoffseite
- acht unveränderte Startseiten-Werkzeugkacheln
- vorhandenen Local-Storage-Schlüssel sowie Klickschutz- und Renderlogik des Favoritensystems
- vollständige lokale Referenzen und JavaScript-Syntax
- zehn Werkstoffdatensätze mit Pflichtfeldern, Quellen und gültigen Gruppen
- Suchtreffer `14404` → `1.4404`
- Mehrfachtreffer `316L` → `1.4404`, `1.4409` und `1.4435`
- Gruppenfilter `316L` + Stahlguss → `1.4409`
- Vergleiche `316 gegen 316L` und `1.4404 gegen 1.4408`
- unveränderte Hashes der drei Vorlagendateien unter `wissensdatenbank/vorlagen/`
- bestehende Rechner-Sollwerte

## Browser-Abnahme

| Nr. | Prüfung | Soll | PC | iPhone |
|---:|---|---|:---:|:---:|
| 1 | Startseite direkt öffnen | Finales Clean Design; Version 2.0.2.0 unter Logo und im Footer | ☐ | ☐ |
| 2 | Wissensdatenbank öffnen | Vier Wissenskacheln sichtbar; jede zeigt einen Favoritenstern | ☐ | ☐ |
| 3 | Vacon-Kachel öffnen | Seite „Ist-/Sollwert-Abweichung im PLS“ öffnet | ☐ | ☐ |
| 4 | Vacon-Breadcrumb „Startseite“ wählen | Startseite öffnet korrekt | ☐ | ☐ |
| 5 | Vacon-Breadcrumb „Wissensdatenbank“ wählen | Wissensübersicht öffnet korrekt | ☐ | ☐ |
| 6 | Vacon-Inhalt prüfen | Vacon, Frequenzumrichter, Parameter 2.2.3.7 und maximale Frequenz korrekt sichtbar | ☐ | ☐ |
| 7 | Vacon-Seite auf schmalem Display prüfen | Überschrift, Parameterkarte und Hinweis vollständig lesbar | ☐ | ☐ |
| 8 | Vacon als Favorit setzen | Stern aktiv; Eintrag im linken Favoritenmenü | ☐ | ☐ |
| 9 | Werkstoff, Air Torque und Siemens als Favoriten setzen | Alle vier Wissensfavoriten vorhanden | ☐ | ☐ |
| 10 | Mit gesetzten Favoriten Seite wechseln und neu laden | Favoriten und Zähler bleiben erhalten | ☐ | ☐ |
| 11 | Stern erneut wählen | Nur Favorit wird entfernt; keine Seitennavigation | ☐ | ☐ |
| 12 | Kachel außerhalb des Sterns wählen | Zugehörige Wissensseite öffnet | ☐ | ☐ |
| 13 | Wissenssuche `Vacon`, `PLS`, `2.2.3.7` | Vacon-Kachel bleibt jeweils sichtbar | ☐ | ☐ |
| 14 | Startseitensuche `Vacon`, `2.2.3.7`, `maximale Frequenz` | Vacon-Wissensbeitrag wird jeweils angeboten | ☐ | ☐ |
| 15 | Navigationsbaum öffnen | Vacon unter Wissensdatenbank erreichbar | ☐ | ☐ |
| 16 | Werkstoff-Nachschlagewerk öffnen | Breadcrumb vollständig sichtbar | ☐ | ☐ |
| 17 | Werkstoffsuche `1.4404`, `14404`, `316L`, `CF8M`, `Alloy 59` | Erwartete Einzel- und Mehrfachtreffer | ☐ | ☐ |
| 18 | Gruppenfilter und Vergleiche | Filter sowie beide Direktvergleiche funktionieren | ☐ | ☐ |
| 19 | Externe Quellenlinks | Öffnen in neuem Tab; Anwendungsnavigation bleibt erhalten | ☐ | ☐ |
| 20 | Offline-Test nach Online-Aufruf | Startseite, Wissensseiten einschließlich Vacon, CSS/JS/JSON und Kernseiten laden aus Cache | ☐ | ☐ |
| 21 | PDF-Vorlage herunterladen | Datei funktioniert und ist bytegenau unverändert | ☐ | ☐ |
| 22 | Bestehende Rechner | Alle bisherigen Sollwerte unverändert | ☐ | ☐ |

## Rechner-Sollwerte

- Analogsignal: 0…100 auf 4…20 mA, Eingabe 50 → **12,000 mA / 50,0 %**.
- P+F: X1=0, Y1=4, X2=100, Y2=20 → **K=0,160000; Nullpunkt=4,000000**.
- Pt100: 0 °C → **100,000 Ω**.
- Einheiten: 1 bar → **1.000,000 mbar**.
- Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1,00, Grenzwert 6 % → **6,93 V; 1,73 %; Lastspannung 393,07 V; Reserve +17,07 V**.

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
