# Testcheckliste und Abnahme – SK PLT Tools 2.0.3.3-Beta.1

## Automatisierte Prüfung

Aus dem Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
```

Die Prüfungen kontrollieren 15 HTML-Seiten, statische Header/Footer, Versionierung, Beta-Cache-Isolation, lokale Referenzen, JavaScript-Syntax, neun Startseitenkacheln, Suche, Navigation, Favoriten, vier Wissenskacheln, zehn Werkstoffdatensätze, Vorlagen-Hashes, die richtungsabhängige Siemens-Reglerskala und bestehende Rechner-Sollwerte.

## Siemens-Rechner-Sollwerte

| Signalbereich | Eingabe | Erwartetes Ergebnis |
|---|---:|---:|
| 4–20 mA | Rohwert 13.824 | 12,000 mA · Nennbereich |
| 0–20 mA | 20 mA | Rohwert 27.648 · Nennbereich |
| 0–10 V | 2,5 V | Rohwert 6.912 · Nennbereich |
| 2–10 V | Rohwert 20.736 | 8,000 V · Nennbereich |

## Bereichszustände

| Rohwert | Erwarteter Zustand |
|---:|---|
| −4.865 | Unterlauf |
| −4.864 | Unterbereich |
| −1 | Unterbereich |
| 0 | Nennbereich |
| 27.648 | Nennbereich |
| 27.649 | Überbereich |
| 32.511 | Überbereich |
| 32.512 | Überlauf |

## Browser-Abnahme

| Nr. | Prüfung | Soll | PC | Mobil |
|---:|---|---|:---:|:---:|
| 1 | Startseite direkt öffnen | Clean Design; Version 2.0.3.3-Beta.1 unter Logo und im Footer; Kachel heißt „Siemens Rohwert“ | ☐ | ☐ |
| 2 | Siemens-Rechner öffnen | Große Seitenüberschrift heißt exakt „Siemens Rohwert“; kein transparentes INT/TNT-Hintergrundelement sichtbar | ☐ | ☐ |
| 3 | „Signal → Siemens-Rohwert“ und alle vier Signalbereiche wählen | Reglergrenzen und Skalenwerte wechseln passend auf 4–20 mA, 0–20 mA, 0–10 V oder 2–10 V; jeder Skalenwert zeigt die Einheit | ☐ | ☐ |
| 4 | Auf „Siemens-Rohwert → Signal“ wechseln | Rohwertskala −32.768, −4.864, 0, 27.648, 32.511 und 32.767 ist sichtbar; aktueller Wert bleibt rechnerisch erhalten | ☐ | ☐ |
| 5 | Regler in beiden Eingaberichtungen ziehen | Rohwert, Signal und Status aktualisieren sich live; Track und Reglerfarbe gehen flüssig und ohne harte Farbblöcke über | ☐ | ☐ |
| 6 | Regler per Pfeiltasten bedienen | Feinverstellung funktioniert | ☐ | ☐ |
| 7 | Schnellwerte wählen | Alle fünf Zustände werden korrekt und deutlich markiert | ☐ | ☐ |
| 8 | Werte außerhalb INT16 manuell eingeben | Unterlauf bzw. Überlauf bleiben eindeutig | ☐ | ☐ |
| 9 | Siemens-Rechner als Favorit setzen | Eintrag erscheint im Favoritenmenü und bleibt nach Neuladen erhalten | ☐ | ☐ |
| 10 | Startseitensuche `Siemens`, `4–20`, `Rohwert` | Rechnerkachel wird gefunden | ☐ | ☐ |
| 11 | Navigationsbaum öffnen | Siemens-Rechner ist unter Rechner erreichbar | ☐ | ☐ |
| 12 | Offline-Test nach Online-Aufruf | Rechner, CSS und JavaScript laden aus dem Beta-Cache | ☐ | ☐ |
| 13 | Wissensdatenbank öffnen und durchsuchen | Bestehende Wissensfunktionen unverändert | ☐ | ☐ |
| 14 | Bestehende Favoriten prüfen | Bestehender Local-Storage-Schlüssel und Inhalte bleiben erhalten | ☐ | ☐ |
| 15 | Schmale Ansicht 320–390 px | Keine horizontale Überlagerung; Statusliste und Eingaben lesbar | ☐ | ☐ |
| 16 | Stabile Installation 2.0.2.0 öffnen | Unverändert und unabhängig von der Beta | ☐ | ☐ |

## Bestehende Rechner-Sollwerte

- Analogsignal: 0…100 auf 4…20 mA, Eingabe 50 → **12,000 mA / 50,0 %**.
- P+F: X1=0, Y1=4, X2=100, Y2=20 → **K=0,160000; Nullpunkt=4,000000**.
- Pt100: 0 °C → **100,000 Ω**.
- Einheiten: 1 bar → **1.000,000 mbar**.
- Spannungsfall: Drehstrom, 400 V, 16 A, 35 m, 2,5 mm² Cu, cos φ 1,00, Grenzwert 6 % → **6,93 V; 1,73 %; Lastspannung 393,07 V; Reserve +17,07 V**.

Prüfer: ____________________  Datum: ____________________  Ergebnis: ☐ bestanden ☐ nicht bestanden
