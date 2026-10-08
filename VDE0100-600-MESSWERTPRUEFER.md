# Manueller VDE-Messwertprüfer

Stand: **2.1.1.0-Beta** · direkte Basis: **2.1.0.5-Beta**

## Verbindlicher Umfang

Der VDE-Messwertprüfer ist eine manuelle, rechnerische Zweitkontrolle. Er verarbeitet ausschließlich vom Nutzer eingegebene Messwerte und die für den gewählten Rechenweg notwendigen Bezugs- oder Grenzwerte.

Nicht Bestandteil der Laufzeit oder Bewertungslogik sind Foto-, PDF-, OCR- oder Protokollanalyse, Formularidentität, Formularstruktur, Kreuze, Unterschriften, Namen, Datum, Orte oder sonstige formale Angaben.

## Ergebnis-Governance

1. Der Nutzer wählt genau eine Messgröße und gegebenenfalls den Bewertungsweg.
2. Die Maske zeigt nur die dafür benötigten Eingaben.
3. Kontextabhängige Grenzwerte werden niemals vorbelegt.
4. Ein Grenzwert muss als freigegebener Sollwert eingegeben oder aus den ausdrücklich abgefragten Bezugsgrößen berechnet werden.
5. Fehlende oder ungültige Angaben werden einzeln benannt.
6. Solange die Berechnungsgrundlage unvollständig oder fehlerhaft ist, wird kein Ergebnis ausgegeben.
7. Grenzwerte werden inklusiv bewertet: Gleichheit mit dem zulässigen Grenzwert ist i. O.
8. Nach vollständiger Eingabe zeigt die Anwendung verwendeten Grenzwert, Formel, eingesetzte Werte und Ergebnis `i. O.` oder `nicht i. O.`.

## Dokumentierte Rechenregeln

| Messgröße | Erforderliche Eingaben | Regel |
|---|---|---|
| Spannungsfall, Prozentwert | gemessener Prozentwert, freigegebener Maximalwert | `ΔU%gemessen ≤ ΔU%max` |
| Spannungsfall, Voltwert | `ΔU`, `Un`, freigegebener Maximalwert in % | `ΔU% = ΔU / Un × 100`; danach `ΔU% ≤ ΔU%max` |
| Isolationsmessung | kleinster gemessener Wert, freigegebener Mindestwert | `RISO,min gemessen ≥ RISO,min freigegeben` |
| Schleifenimpedanz, direkter Sollwert | `Zs`, freigegebenes `Zs,max` | `Zs ≤ Zs,max` |
| Schleifenimpedanz, Rechenweg | `Zs`, `U0`, freigegebener Auslösestrom `Ia` | `Zs,max = U0 / Ia`; danach `Zs ≤ Zs,max` |
| Kurzschlussstrom | `Ik`, freigegebener erforderlicher Auslösestrom `Ia` | `Ik ≥ Ia` |
| RCD-Auslösezeit | gemessene Zeit, freigegebene Maximalzeit | `tA ≤ tA,max` |
| RCD-Auslösestrom | gemessener Strom, freigegebene Unter- und Obergrenze | `IΔ,min ≤ IΔ ≤ IΔ,max` |
| Niederohmigkeit | gemessener Widerstand, freigegebener Maximalwert | `RPE ≤ RPE,max` |
| Schutzpotentialausgleich | gemessener Widerstand, freigegebener Maximalwert | `RPA ≤ RPA,max` |

## Bewusst nicht angenommene Grenzwerte

Es gibt keine Software-Defaults für Spannungsfall, Isolationswiderstand, RCD-Zeit oder -Strom, Niederohmigkeit, Schutzpotentialausgleich oder Schleifenimpedanz. Auch Kennlinienfaktoren wie B/C/D werden nicht pauschal abgeleitet. Der erforderliche Auslösestrom `Ia` ist aus der freigegebenen Schutzgeräte- beziehungsweise Projektgrundlage zu übernehmen.

Damit werden Netzform, Abschaltzeit, RCD-Typ, Prüfstromfaktor, Prüfspannung, Stromkreisart, Schutzmaßnahme und projektspezifische Vorgaben nicht durch ungesicherte Annahmen ersetzt.

## Technische Dateien

- `assets/vde0100-600-engine.js` – deterministische, manuelle Rechenengine.
- `assets/vde0100-600-input-schema.json` – dynamische Eingabemasken ohne Zahlenvorgaben.
- `assets/vde0100-600-rules.json` – freigegebener Regelumfang und Governance.
- `plausibilitaetspruefung-vde0100-600/checker.js` – reine Eingabe-, Fehler- und Ergebnissteuerung.
- `tools/functional-smoke-test.js` – Rechenregressionen aller Regeln und Grenzfälle.
- `tools/vde-protocol-e2e-test.py` – Browser-E2E der manuellen Bedienung; der Dateiname bleibt zur Strukturkompatibilität erhalten.

## Sicherheitsgrenze

Das Tool führt keine Messung durch, bewertet keine vollständige Anlage, erteilt keine Inbetriebnahmefreigabe und ersetzt nicht die verantwortliche Elektrofachkraft. Die Verantwortung für Messdurchführung, Auswahl der anwendbaren Regel, Freigabe des Sollwerts und Gesamtbewertung verbleibt bei der verantwortlichen Elektrofachkraft.
