# Automatische Plausibilitätsprüfung VDE 0100-600

Stand: **2.1.0.2-Beta** · verbindliche Formularbasis: Prüfbericht Lfd. Nr. 12782

## Zweck und Grenze

Das Modul kontrolliert die dokumentierte Vollständigkeit und rechnerische Plausibilität. Es führt keine Messung durch, bestätigt keine normgerechte Errichtung und erteilt keine Inbetriebnahmefreigabe. Unsichere Erkennung wird als offener Punkt angezeigt und niemals stillschweigend ergänzt.

## Mustervorlage und Datenschutz

- Die hochgeladene leere Datei `VDEProtokoll.pdf` diente ausschließlich zur Ableitung von Seitengeometrie, Linienankern, Feldzonen und Checkbox-Koordinaten.
- Die PDF-Mustervorlage ist **nicht** Bestandteil der Webanwendung, wird nicht angezeigt, nicht vorab geladen und nicht zum Download angeboten.
- In Vorschau und Klärungsdialog erscheinen ausschließlich Seiten beziehungsweise Ausschnitte des vom Nutzer hochgeladenen Protokolls.
- PDF, JPEG, PNG und WebP werden lokal verarbeitet; PDF.js ist im Projekt enthalten.
- SHA-256, Textextraktion, Layoutanalyse, Korrekturen und Ergebnis verbleiben im Browser. Externe OCR-, Cloud- oder Analysedienste werden nicht verwendet.

## Erkennungspipeline

1. PDF-/Bilddatei lokal einlesen und SHA-256 bilden.
2. PDF-Seiten lokal rendern beziehungsweise Bilddateien in eine Canvas-Fläche übernehmen.
3. Hoch- oder Querformat automatisch ausrichten.
4. A4-Seitenverhältnis, Außenkanten und 33 horizontale Linienanker mit dem Formularprofil abgleichen.
5. 93 Feldzuordnungen auswerten: Stammdaten, drei Messgeräteblöcke, Objekt-/Stromkreisdaten, Prüfpunkte 3.1–3.20, Messungen 4.1–4.4, Isolation, Abschaltung 6.1/6.2, Erproben 7.1–7.6 und Abschluss.
6. Checkboxen anhand innerer Markierungsdichte auslesen. Eingebetteter PDF-Text und eine optionale lokale Browser-`TextDetector`-Schnittstelle liefern zusätzliche Werte.
7. Visuell vorhandene, aber nicht sicher gelesene Einträge als Bestätigungspunkt mit markiertem Originalausschnitt ausgeben.
8. Nach jeder manuellen Klärung die vollständige Regelmenge neu ausführen.

## Vollständigkeitsprüfung

Geprüft werden insbesondere:

- Formularidentität und Prüfgrund
- ausreichende Bezeichnung des technischen Platzes
- Netzsystem und Anlagenart
- Messgerät 1 mit Fabrikat, Typ/Nummer und Kalibrierdatum
- Leitung, Querschnitt, Aderzahl, Länge, Schutzorgan und Nennwerte
- jede Bewertung der Prüfpunkte 3.1–3.20
- Bewertungen und gegebenenfalls Werte der Prüfpunkte 4.1–4.4
- Isolationswerte
- mindestens ein nachvollziehbarer Messweg aus Abschnitt 6.1 oder 6.2
- jede Bewertung der Prüfpunkte 7.1–7.6
- Prüfpunkte 2–6, Prüfername, Datum und Unterschrift

## Messwert-Plausibilität

- numerische Wertebereiche je Formularfeld
- Durchgängigkeit/Niederohmwerte gegen einen internen Hinweiswert; dieser ist ausdrücklich kein allgemeiner Normgrenzwert
- Isolationswiderstände gegen den konfigurierten Mindestprüfwert
- Schleifenimpedanz mit `Zs ≤ U0 / (Kennlinienfaktor × In)` für B/C/D
- Verbraucherstrom `Ib ≤ In`
- Spannungsfall gegen das Prüfziel sowie Konsistenz von ΔU, Un und Prozentwert
- RCD-Auslösestrom gegen `IΔn`
- RCD-Auslösezeit gegen den konfigurierten Standard-Prüfwert
- n.i.O.-Markierungen und fehlende Prüferunterschrift als nicht plausible Abweichung

Die Werte in `assets/vde0100-600-template.json` sind Prüfeinstellungen und müssen bei abweichenden Anlagen-, Schutz- oder Prüfbedingungen fachlich bewertet werden.

## Geführte Klärung und Ergebnis

Jeder offene Punkt wird einzeln mit einem markierten Ausschnitt des hochgeladenen Originals angezeigt. Mögliche Aktionen:

- erkannte Auswahl bestätigen oder ändern,
- Text, Datum oder Messwert korrigieren,
- Punkt als „nicht relevant“ kennzeichnen,
- erkannte Abweichung als „n.i.O.“ bestätigen.

Erst nach vollständiger Klärung wird das Abschlussurteil erzeugt. Bestätigte Abweichungen oder verletzte Messwertregeln führen zum roten X „Nicht plausibel“; andernfalls erscheint der grüne Haken „Plausibel“.
