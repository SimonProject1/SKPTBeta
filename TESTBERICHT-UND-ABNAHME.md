# Testbericht und Abnahme – SK PLT Tools 2.0.3.5-Beta.2

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/pfad/zu/chromium python tools/browser-smoke-test.py
```

Die Prüfungen kontrollieren 15 HTML-Seiten, statische Header/Footer, Versionierung, Beta-Cache-Isolation, lokale Referenzen, JavaScript-Syntax, zehn Startseitenkacheln, Suche, Filterung, Navigation, Favoriten, den sicheren E+H-Externlink, fünf Wissenskacheln, zehn Werkstoffdatensätze, Vorlagen-Hashes, Siemens-Kartenprofile, bestätigte Grenzwerte, Regler-/Eingabesynchronisierung, kompakte Bedienelemente, einklappbare Karteninformationen und bestehende Rechner-Sollwerte.

**Build-Verifikation vom 02.10.2026:** statische Release-Prüfung bestanden; funktionale Regression bestanden; alle 15 Seiten im Browser auf iPad-Breite 820 × 1180 px und iPhone-Breite 390 × 844 px ohne horizontales Überlaufen geprüft; Desktop-Ansicht 1440 × 1050 px bestanden; Größen der kompakten Schaltflächen geprüft; keine Browser-Konsolenfehler. Die manuelle Abnahme auf realem PC und iPhone/iPad bleibt offen.

## Siemens Rohwert – automatisiert geprüfte Grenzen

| Profil / Parametrierung | Prüfung | Erwartung |
|---|---:|---|
| ET 200SP AI 4xI ST · 4–20 mA | −4.865 | Unterlauf |
| ET 200SP AI 4xI ST · 4–20 mA | −4.864 | Untersteuerung |
| ET 200SP AI 4xI ST · 4–20 mA | 27.648 | Nennbereich |
| ET 200SP AI 4xI ST · 4–20 mA | 27.649 | Übersteuerung |
| ET 200SP AI 4xI ST · 4–20 mA | 32.512 | Überlauf |
| ET 200SP HA AI 16xI · NE43 ein | −691 | Unterlauf / ungültig ab 3,6 mA |
| ET 200SP HA AI 16xI · NE43 ein | −690…−346 | untere Hysterese |
| ET 200SP HA AI 16xI · NE43 ein | 28.512…29.375 | obere Hysterese |
| ET 200SP HA AI 16xI · NE43 ein | 29.376 | Überlauf / ungültig ab 21,0 mA |
| S7-1500/ET 200MP F-AI 8xI | 0…27.648 | nur Nennskalierung; keine Diagnosebewertung |

## Synchronisierung und Bedienung

- Profil-, Signalbereichs- und Eingaberichtungswechsel erhalten den aktuellen Rohwert, soweit er im bestätigten Bereich des Zielprofils liegt.
- Wechsel Rohwert → Signal rechnet das Eingabefeld um; Reglerbewegungen aktualisieren Eingabe und Ergebnis sofort.
- Nicht unterstützte Signalbereiche werden im jeweiligen Kartenprofil deaktiviert.
- Bei Profilen ohne bestätigte Diagnosegrenzen werden Farbbereiche und Zustandsstreifen ausgeblendet.
- Wissensdatenbank-Kachel `Siemens · SPS · Rohwert` öffnet den Rohwert-Rechner.

## Regression – bestehende Rechner

- Analogsignal: 0…100 auf 4…20 mA, Eingabe 50 → **12,000 mA / 50,0 %**.
- P+F: X1=0, Y1=4, X2=100, Y2=20 → **K-Faktor=0,160000; Nullpunkt=4,000000**.
- Pt100: 0 °C → **100,000 Ω**.
- Einheiten: 1 bar → **1.000,000 mbar**.
- Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1,00, Grenzwert 6 % → **6,93 V; 1,73 %; Lastspannung 393,07 V; Reserve +17,07 V**.

## Manuelle Geräteabnahme

| Nr. | Prüfung | PC | iPhone/iPad | Bemerkung |
|---:|---|:---:|:---:|---|
| 1 | Startseite und alle Kacheln öffnen | ☐ | ☐ | |
| 2 | Siemens-Kartenprofile und deaktivierte Signalbereiche prüfen | ☐ | ☐ | |
| 3 | Rohwert-/Signaleingabe und Regler synchron prüfen | ☐ | ☐ | |
| 4 | Feste Rot-/Gelb-/Grün-Bereiche gegen Profildokumentation prüfen | ☐ | ☐ | |
| 5 | Wissenskachel Siemens · SPS · Rohwert öffnen | ☐ | ☐ | |
| 6 | Offline-Start bereits geladener Kernseiten prüfen | ☐ | ☐ | |
| 7 | Keine horizontale Seitenüberlagerung bei 320–390 px | ☐ | ☐ | |
| 8 | Quellen- und Grenzwertdokument öffnen | ☐ | ☐ | |
| 9 | Karteninformationen auf- und zuklappen | ☐ | ☐ | |
| 10 | Kompakte Header-, Favoriten-, Navigations- und Vorzeichen-Schaltflächen prüfen | ☐ | ☐ | |

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
