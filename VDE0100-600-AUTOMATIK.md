# Automatische Plausibilitätsprüfung VDE 0100-600

Stand: 2.1.0.1-Beta · Musterformular: `228_SR4_K06_E07.1.pdf`

## Zweck und Grenze

Das Modul kontrolliert die dokumentierte Vollständigkeit und rechnerische Plausibilität. Es führt keine Messung durch, bestätigt keine normgerechte Errichtung und erteilt keine Inbetriebnahmefreigabe. Unsichere Erkennung wird als offener Punkt angezeigt, niemals stillschweigend ergänzt.

## Eingabe und Datenschutz

- PDF, JPEG, PNG und WebP; bis zu acht Dateien in einem Prüflauf
- PDF-Seiten werden durch die mitgelieferte PDF.js-Laufzeit lokal in Canvas-Flächen gerendert.
- SHA-256, Textextraktion, Layoutanalyse, Korrekturen und Ergebnis verbleiben im Browser.
- Es wird kein externer OCR-, Cloud- oder Analysedienst aufgerufen.

## Erkennungsstufen

1. **Kalibriertes Muster:** Exakter SHA-256-Treffer des bereitgestellten Musterprotokolls übernimmt die verifizierten Referenzwerte und zugehörigen Konfidenzen.
2. **Digitale PDF:** Eingebetteter Text wird automatisch extrahiert und feldbezogen ausgewertet.
3. **Lokale Browsererkennung:** Falls der Browser `TextDetector` bereitstellt, wird dessen lokale Erkennung verwendet.
4. **Visuelles Formularschema:** Layoutzonen und handschriftliche/markierte Bereiche werden bildbasiert erkannt. Werte, die nicht sicher gelesen werden können, werden zur Klärung vorgelegt.

## Hinterlegte Prüfungen

- Pflichtangaben und erkennbare Wertebereiche
- negative Einzelbewertungen und fehlende Bemerkung
- Isolationswiderstand gegen konfigurierten Mindestprüfwert
- Schleifenimpedanz mit `Zs ≤ U0 / (Kennlinienfaktor × In)` für B/C/D
- Belastungsstrom `Ib ≤ In`
- Spannungsfall gegen konfiguriertes Prüfziel
- RCD-Auslösestrom gegen `IΔn`
- RCD-Auslösezeit gegen konfigurierten Standard-Prüfwert
- Prüferbestätigung und Kalibrierstatus

Die Werte in `assets/vde0100-600-template.json` sind Prüfeinstellungen und müssen für abweichende Anlagen-, Schutz- oder Prüfbedingungen fachlich geprüft werden.

## Geführte Klärung

Jeder offene Punkt wird einzeln angezeigt. Zulässige Bearbeitungen:

- erkannte Auswahl bestätigen oder ändern,
- Text, Datum oder Messwert korrigieren,
- Punkt als „nicht relevant“ kennzeichnen,
- erkannte Abweichung als „n.i.O.“ bestätigen.

Nach jeder Bearbeitung wird die vollständige Regelmenge erneut ausgeführt. Erst wenn keine offenen Punkte mehr bestehen, wird das Abschlussurteil erzeugt. Bestätigte Abweichungen oder weiterhin verletzte Messwertregeln führen zu einem roten X; andernfalls erscheint ein grüner Haken.

## Musterwerte im Testfall

Das Muster enthält unter anderem C25, 25 A, 400 V, 0,18 Ω Niederohmwert, >300 MΩ Isolationswerte, 0,27 Ω Schleifenimpedanz, 0,39 % Spannungsfall sowie RCD-Werte 30 mA / 17,7 mA / 17 ms. Der Kalibrierstatus ist im Scan nicht sicher feststellbar und wird bewusst als offener Punkt behandelt.
