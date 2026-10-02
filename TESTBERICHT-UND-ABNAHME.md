# Testbericht und Abnahme – SK PLT Tools 2.0.3.4-Beta.1

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

Die Prüfungen kontrollieren 15 HTML-Seiten, statische Header/Footer, Versionierung, Beta-Cache-Isolation, lokale Referenzen, JavaScript-Syntax, zehn Startseitenkacheln, Suche, Filterung, Navigation, Favoriten, den sicheren E+H-Externlink, vier Wissenskacheln, zehn Werkstoffdatensätze, Vorlagen-Hashes, die Siemens-Reglerskala und bestehende Rechner-Sollwerte.

**Build-Verifikation vom 02.10.2026:** statische Release-Prüfung bestanden; funktionale Regression bestanden; Browser-Smoke-Test bei 1440 × 1050 px und mobiler Ansicht 390 × 844 px bestanden; keine Browser-Konsolenfehler. Die manuelle Abnahme auf realem PC und iPhone/iPad bleibt offen.

## E+H Device Viewer – Abnahmekriterien

| Nr. | Prüfung | Soll | PC | iPhone/iPad |
|---:|---|---|:---:|:---:|
| 1 | Startseite öffnen | Kachel `E+H Device Viewer` sichtbar; Kategorie `EXTERN`; Version 2.0.3.4-Beta.1 | ☐ | ☐ |
| 2 | Kachel prüfen | Hinweis auf externen Herstellerdienst und Nicht-Speicherung sichtbar | ☐ | ☐ |
| 3 | Kachel öffnen | `https://netilion.endress.com/app/library/device_viewer` öffnet in neuem Tab | ☐ | ☐ |
| 4 | Datenschutz | Kein Seriennummern-, Such- oder anderes Eingabefeld für E+H in SK PLT Tools | ☐ | ☐ |
| 5 | Filter `Externe Dienste` | Nur die E+H-Kachel bleibt sichtbar | ☐ | ☐ |
| 6 | Suche `E+H`, `Device Viewer`, `Endress`, `Seriennummer` | E+H-Kachel wird gefunden | ☐ | ☐ |
| 7 | Favorit setzen und öffnen | Favorit bleibt erhalten; externer Link öffnet weiterhin in neuem Tab | ☐ | ☐ |
| 8 | Navigationsbaum | Gruppe `Externe Dienste` enthält `E+H Device Viewer ↗` | ☐ | ☐ |
| 9 | Offline-Modus | E+H wird nicht als offline verfügbar dargestellt; bestehende Kernfunktionen bleiben erreichbar | ☐ | ☐ |
| 10 | Schmale Ansicht 320–390 px | Keine horizontale Überlagerung; Kachel und Hinweis vollständig lesbar | ☐ | ☐ |

## Regression – Siemens Rohwert

| Signalbereich | Eingabe | Erwartetes Ergebnis |
|---|---:|---:|
| 4–20 mA | Rohwert 13.824 | 12,000 mA · Nennbereich |
| 0–20 mA | 20 mA | Rohwert 27.648 · Nennbereich |
| 0–10 V | 2,5 V | Rohwert 6.912 · Nennbereich |
| 2–10 V | Rohwert 20.736 | 8,000 V · Nennbereich |

## Regression – bestehende Rechner

- Analogsignal: 0…100 auf 4…20 mA, Eingabe 50 → **12,000 mA / 50,0 %**.
- P+F: X1=0, Y1=4, X2=100, Y2=20 → **K-Faktor=0,160000; Nullpunkt=4,000000**.
- Pt100: 0 °C → **100,000 Ω**.
- Einheiten: 1 bar → **1.000,000 mbar**.
- Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1,00, Grenzwert 6 % → **6,93 V; 1,73 %; Lastspannung 393,07 V; Reserve +17,07 V**.

## Paket- und Freigabeprüfung

| Prüfung | Soll | Ergebnis |
|---|---|---|
| Vollständige Struktur | Alle bisherigen Seiten, Assets, Vorlagen und Werkzeuge enthalten | ☐ |
| Versionskonsistenz | Überall 2.0.3.4-Beta.1 | ☐ |
| Paketintegrität | `sha256sum -c SHA256SUMS.txt` ohne Fehler | ☐ |
| Stable-Schutz | 2.0.2.0 unverändert und getrennt | ☐ |
| Manuelle Geräteabnahme | PC und iPhone/iPad ohne kritischen Fehler | ☐ |

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
