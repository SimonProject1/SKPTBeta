# Messwert-Plausibilitätsprüfung VDE 0100-600

Stand: **2.1.0.5-Beta** · direkte Basis: **2.1.0.4-Beta**

## Verbindlicher Bewertungsumfang

Das Modul bewertet ausschließlich:

1. die im Nutzer-Dokument tatsächlich eingetragenen Messwerte und
2. die Bezugsdaten, die für die jeweils anwendbare Rechenregel erforderlich sind.

Nicht ausgewertet werden Formularidentität, Strukturpassung, Unterschriften, Namen, Datum, Ortsangaben, gesetzte Kreuze, Freitext, Prüfgrund, Messgeräte-Stammdaten oder sonstige formale Angaben.

## Interne Lokalisierungshilfe

Das interne Profil `assets/vde0100-600-template.json` enthält nur noch 18 Zonen für Messwerte und rechnerisch notwendige Bezugsdaten. Der Struktur-Fingerabdruck wird ausschließlich verwendet, um die wahrscheinlich richtige Seitenausrichtung und mögliche Messwertfelder zu finden.

- Der interne Lokalisierungswert wird nicht angezeigt.
- Er wird nicht an die Rechenengine übergeben.
- Er kann weder grün noch rot auslösen.
- Die Mustervorlage selbst ist nicht eingebettet, nicht im Precache und nicht downloadbar.

## Entscheidungsablauf

### 1. Messumfang bestätigen

Nach der lokalen Erkennung schlägt die Anwendung Messgrößen vor. Der Nutzer bestätigt nur die Größen, zu denen im Dokument tatsächlich ein Messwert eingetragen ist. Diese Auswahl ist keine formale Protokollbewertung.

### 2. Werte einzeln klären

Für jede ausgewählte Messgröße gilt:

- fehlt der Messwert, wird genau dieser Messwert abgefragt;
- ist der Messwert unsicher erkannt, wird er am Originalausschnitt bestätigt oder korrigiert;
- fehlt eine notwendige Bezugsgröße, wird genau diese Bezugsgröße abgefragt;
- ein fehlender oder unsicherer Wert ist ein offener Punkt, niemals automatisch n. i. O.;
- es gibt keine Aktion, mit der ein fehlender Wert als Mangel und damit rot bestätigt werden kann.

### 3. Endergebnis sperren

Solange der Messumfang nicht bestätigt ist oder ein notwendiger Mess-/Bezugswert fehlt beziehungsweise unsicher ist, bleibt die Ergebnisansicht gesperrt.

### 4. Rechenabweichung bestätigen

Ergibt eine vollständig berechenbare Regel eine Abweichung, zeigt die Anwendung die Rechnung und bietet zwei Wege:

- Messwert korrigieren oder
- den erkannten beziehungsweise manuell eingegebenen Wert als tatsächlich eingetragen bestätigen.

Erst die zweite Variante übernimmt die Rechenabweichung als bestätigten n.-i.-O.-Befund.

### 5. Ergebnis

- **Grüner Haken:** Messumfang bestätigt, alle erforderlichen Mess-/Bezugswerte vorhanden, keine Rechenregel fehlgeschlagen.
- **Rotes X:** mindestens eine Rechenabweichung wurde als tatsächlich eingetragener Wert bestätigt.
- **Kein Endergebnis:** mindestens ein notwendiger Wert oder der Messumfang ist offen.

## Erkennungspipeline

1. Nutzerdatei lokal einlesen und für PDF.js beziehungsweise Bild-Canvas vorbereiten.
2. Seiten in vier Orientierungen vergleichen; internes Profil nur als Ausrichtungshilfe verwenden.
3. Eingebetteten PDF-Text auswerten.
4. Browserseitige lokale Bildtexterkennung verwenden, sofern `TextDetector` verfügbar ist.
5. Nur die 19 in der Engine definierten Mess-/Bezugsfelder übernehmen.
6. Erkannten Messumfang vorschlagen.
7. Unsichere und fehlende Werte einzeln klären.
8. Nach jeder Eingabe alle anwendbaren Rechenregeln erneut ausführen.
9. Ergebnis erst bei vollständig geschlossener Klärung freigeben.

## Rechenregeln und Standardparameter

| Regel | Rechnung / Grenzwert |
|---|---|
| Durchgängigkeit | ausgewählter Wert ≤ `continuityMaxOhm` (Standard 1 Ω) |
| Isolation | kleinster Isolationswert ≥ `insulationMinMOhm` (Standard 1 MΩ) |
| Schleifenimpedanz | `Zs ≤ U0 / (Faktor × In)`, B = 5, C = 10, D = 20 |
| Kurzschlussstrom | `Ik` gegen `U0 / Zs`, Standardtoleranz 30 % |
| Stromrelation | `Ib ≤ In` |
| Spannungsfall | Prozentwert ≤ 5 %; Konsistenz `ΔU / Un × 100` mit 0,3 Prozentpunkten Toleranz |
| RCD-Auslösestrom | `IΔ ≤ IΔn` |
| RCD-Auslösezeit | `tA ≤ 300 ms` als hinterlegter Standard-Prüfwert |

Abweichende Schutzgeräte, Prüfbedingungen, Anlagenarten oder normative Sonderfälle müssen von der verantwortlichen Elektrofachkraft fachlich bewertet werden.
