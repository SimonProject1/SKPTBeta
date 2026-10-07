# Automatische Plausibilitätsprüfung VDE 0100-600

Stand: **2.1.0.3-Beta** · direkte Basis: **2.1.0.2-Beta** · verbindliche Formularbasis: Prüfbericht Lfd. Nr. 12782

## Zweck und Grenze

Das Modul kontrolliert lokal die dokumentierte Vollständigkeit und rechnerische Plausibilität. Es führt keine Messung durch, bestätigt keine normgerechte Errichtung und erteilt keine Inbetriebnahmefreigabe. Unsichere Erkennung wird als offener Punkt angezeigt und niemals stillschweigend ergänzt.

## Referenz und Datenschutz

- `VDEProtokoll.pdf` ist die autorisierte leere Referenz.
- Im Projekt werden nur der korrekte SHA-256, normalisierte Strukturmerkmale, Linienanker, Feldzonen und Blank-Baselines gespeichert.
- Die Referenz-PDF selbst wird nicht eingebettet oder zum Download angeboten.
- Die reale ausgefüllte Test-PDF ist kein Release-Bestandteil und wird nicht offline gecacht.
- PDF, JPEG, PNG und WebP werden lokal im Browser verarbeitet.

## Erkennungspipeline

1. Datei lokal einlesen und SHA-256 bilden.
2. PDFs mit lokalem PDF.js bis zu einer stabilen Analyseauflösung rendern; Fotos hochwertig skalieren.
3. Helligkeitsverteilung robust normalisieren.
4. Alle vier Seitenorientierungen vergleichen; anschließend ±1°/±2° Feinausrichtung bewerten.
5. Formularidentität als Ensemble bestimmen:
   - 18 × 24 Zellraster,
   - 96 horizontale und 64 vertikale Dichteprojektionen,
   - 33 horizontale und zwei vertikale Linienanker,
   - A4-Seitenverhältnis,
   - bei der unveränderten Referenz zusätzlich exakter SHA-256.
6. Formulare ab 90 % Strukturpassung akzeptieren, 84–90 % manuell klären und unter 84 % hart ablehnen.
7. Positionsgebundene Felder nur bei akzeptierter oder klärbarer Formularidentität auslesen. Hart abgelehnte Fremdformulare erzeugen keine falschen Feldwerte.
8. 93 Feldzuordnungen mit der leeren Referenz baseline-bereinigen.
9. Checkboxen anhand von Blauanteil, zusätzlicher Dunkeldichte und Strichwechseln im Boxeninneren bewerten.
10. Handschriftliche Einträge als visuelle Evidenz kennzeichnen und – sofern lokale Texterkennung verfügbar ist – mit dem gelesenen Wert zusammenführen.
11. Unterschriften in der eigentlichen Schreibzone gegen den Blank-Zustand bewerten; Drucklinien und Beschriftungen gelten nicht als Unterschrift.
12. Typabhängige Konfidenz anwenden und unsichere Werte in die Klärungswarteschlange stellen.
13. Nach jeder manuellen Entscheidung die vollständige Regelmenge erneut berechnen.

## Konfidenz und Klärung

- Choice-, Checkbox-, Zahlen- und Datumswerte benötigen grundsätzlich mindestens 80 %.
- Freitext benötigt mindestens 74 %.
- Niedrigere Werte bleiben offen, auch wenn ein Kandidat erkannt wurde.
- Jeder offene Punkt erscheint einzeln mit Originalausschnitt.
- Der technische Platz ist ein gemeinsamer Mehrfeld-Punkt; mindestens zwei Ortsfelder müssen bestätigt werden.
- Pflichtfelder, harte Formularabweichungen, fehlende Prüferunterschrift und sicherheitsrelevante Messwert-/Statusabweichungen können nicht als „nicht relevant“ entfernt werden.
- Fachlich bedingte Statusfelder können den expliziten Formularwert „nicht relevant“ erhalten; optionale Metadaten können als optional nicht relevant dokumentiert werden.

## Vollständigkeitsprüfung

Geprüft werden insbesondere Formularidentität, Prüfgrund, mindestens zwei Ortsangaben, Netzsystem, Anlagenart, Messgerät 1 einschließlich Kalibrierdatum, Leitungs- und Schutzdaten, Prüfpunkte 3.1–3.20, Bewertungen 4.1–4.4, Isolationswerte, mindestens ein Messweg aus 6.1/6.2, Prüfpunkte 7.1–7.6 sowie Prüferangaben einschließlich Unterschrift.

## Messwert-Plausibilität

- numerische Feldbereiche,
- Durchgängigkeit/Niederohmwerte gegen einen dokumentierten internen Hinweiswert,
- Isolationswiderstand gegen den konfigurierten Mindestprüfwert,
- Schleifenimpedanz mit `Zs ≤ U0 / (Kennlinienfaktor × In)` für B/C/D,
- Verbraucherstrom `Ib ≤ In`,
- Spannungsfall gegen Prüfziel und rechnerische Konsistenz von ΔU, Un und Prozent,
- RCD-Auslösestrom gegen `IΔn`,
- RCD-Auslösezeit gegen den konfigurierten Standard-Prüfwert,
- bestätigte n.i.O.-Markierungen und fehlende Prüferunterschrift als rotes Ergebnis.

## Abschluss

Nach vollständiger Klärung erscheint unverändert:

- **grüner Haken – Plausibel**, wenn keine offene oder bestätigte Abweichung verbleibt;
- **rotes X – Nicht plausibel**, wenn mindestens eine Sicherheits-, Vollständigkeits- oder Messwertregel fehlschlägt.
