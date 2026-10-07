# Automatische Plausibilitätsprüfung VDE 0100-600

Stand: **2.1.0.4-Beta** · direkte Basis: **2.1.0.3-Beta** · verbindliche Formularbasis: Prüfbericht Lfd. Nr. 12782

## Zweck und Grenze

Das Modul kontrolliert lokal die dokumentierte Vollständigkeit und rechnerische Plausibilität. Es führt keine Messung durch, bestätigt keine normgerechte Errichtung und erteilt keine Inbetriebnahmefreigabe. Unsichere Erkennung bleibt ein offener Punkt und wird niemals stillschweigend als i.O. oder n.i.O. gewertet.

## Referenz und Testeingaben

- `VDEProtokoll.pdf` ist die verbindliche leere Referenz.
- Im Release werden ausschließlich Referenz-Hash, normalisierte Strukturmerkmale, Linienanker, Feldzonen und Blank-Baselines gespeichert.
- Die Referenz-PDF selbst ist nicht eingebettet oder downloadbar.
- Ausgefüllte reale Protokolle sind ausschließlich externe Testeingaben und werden weder gepackt noch vorgecacht.
- PDF, JPEG, PNG und WebP werden lokal im Browser verarbeitet.

## Entscheidungsmodell

### 1. Formularidentität

Die Strukturpassung ist ein technischer Qualitätsindikator, kein fachliches Prüfergebnis.

- Ab 90 % oder bei exaktem Referenz-Hash: eindeutige Referenzidentität.
- Von 68 % bis unter 90 %: abweichende/unsichere Identität; Referenzmapping ist technisch möglich.
- Unter 68 %: stark unsichere Identität; kein automatisches positionsgebundenes Mapping, aber manuelle Zuordnung bleibt möglich.
- In keinem Fall erzeugt die Formularidentität allein n.i.O. oder ein rotes X.

Bei unsicherer Identität werden angeboten:

1. **Formular trotzdem verwenden** – erkannte Zuordnungen übernehmen; alle unsicheren oder fehlenden Angaben bleiben offen.
2. **Zuordnung manuell prüfen** – erkannte Werte einzeln am Original bestätigen oder korrigieren; fehlende Werte danach ergänzen.
3. **Andere Datei hochladen** – aktuelle Auswahl verwerfen und zum Upload zurückkehren.

### 2. Kreuze

Für jeden erforderlichen Auswahlpunkt gilt:

- genau ein zulässiger Wert wird akzeptiert;
- kein Kreuz, mehrere Kreuze, ein nicht zulässiger Wert oder ein unsicherer Kandidat erzeugt einen offenen Einzelpunkt;
- der Originalausschnitt und die zulässigen Werte werden zur Bestätigung angezeigt;
- eine bestätigte n.i.O.-Markierung bleibt ein sicherheitsrelevanter Mangel;
- der Formularwert „nicht relevant“ ist nur dort zulässig, wo das Feldschema ihn fachlich vorsieht.

### 3. Pflichtangaben und Messwerte

- Pflichtangaben ohne sicheren Wert werden nacheinander geklärt.
- Für 4.1 bis 4.4 ist bei bestätigtem i.O. der zugehörige Messwert erforderlich.
- Für die automatische Abschaltung muss mindestens ein vollständiger Messweg aus 6.1 oder 6.2 vorliegen.
- Isolationswerte, Schleifenimpedanz, RCD-Werte, Stromrelation und Spannungsfall werden auf Wertebereich und rechnerische Plausibilität geprüft.
- Pflichtfelder und sicherheitsrelevante Abweichungen sind nicht über „nicht relevant“ überspringbar.

### 4. Ergebnis

- Offene Punkte sperren die Ergebnisansicht.
- **Grüner Haken:** alle erforderlichen Kreuze sind eindeutig, alle Pflichtangaben und Messwerte liegen vor und keine Plausibilitätsregel schlägt fehl.
- **Rotes X:** mindestens ein Mangel, eine fehlende Pflichtangabe oder ein rechnerisch unplausibler Messwert wurde bestätigt.
- Ein unsicheres oder abweichendes Formular allein kann nie ein rotes Ergebnis erzeugen.

## Erkennungspipeline

1. Datei lokal einlesen und SHA-256 bilden.
2. PDF mit lokalem PDF.js rendern oder Foto skalieren.
3. Kontrast normalisieren und vier Orientierungen sowie ±1°/±2° Feinausrichtung vergleichen.
4. Struktur-Ensemble aus 18 × 24 Raster, 96 horizontalen und 64 vertikalen Projektionen, Linienankern und A4-Seitenverhältnis bilden.
5. Sofern technisch möglich, 93 Referenzfeldzonen auswerten.
6. Checkboxen über Blank-Differenz, Blauanteil, Dunkeldichte und Strichwechsel klassifizieren; sichere und unsichere Kandidaten getrennt protokollieren.
7. Handschrift, Zahlen, Datumswerte und Unterschriften mit feldbezogener Konfidenz übernehmen.
8. Vollständigkeits- und Plausibilitätsregeln berechnen.
9. Offene Punkte einzeln klären und nach jeder Entscheidung alle Regeln erneut ausführen.

## Fachliche Plausibilitätsregeln

- numerische Feldbereiche,
- Durchgängigkeit/Niederohmwerte gegen einen dokumentierten internen Hinweiswert,
- Isolationswiderstand gegen den konfigurierten Mindestprüfwert,
- Schleifenimpedanz mit `Zs ≤ U0 / (Kennlinienfaktor × In)` für B/C/D,
- Verbraucherstrom `Ib ≤ In`,
- Spannungsfall gegen Prüfziel und rechnerische Konsistenz von ΔU, Un und Prozent,
- RCD-Auslösestrom gegen `IΔn`,
- RCD-Auslösezeit gegen den konfigurierten Standard-Prüfwert,
- bestätigte n.i.O.-Markierungen und fehlende Prüferunterschrift.
