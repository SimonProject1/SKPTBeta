# SK PLT Tools 2.1.0.5-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.0.5-Beta** basiert auf dem vollständigen Stand **2.1.0.4-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Schwerpunkt dieser Beta

Die Plausibilitätsprüfung VDE 0100-600 bewertet ausschließlich eingetragene Messwerte und die für ihre rechnerische Prüfung benötigten Bezugsdaten.

- Formularidentität, Formularaufbau und Strukturpassung sind keine Bewertungskriterien.
- Unterschriften, Namen, Datum, Ortsangaben, Kreuze, Textfelder und sonstige formale Angaben werden von der VDE-Engine nicht verarbeitet.
- Ein internes Referenzprofil enthält nur Mess-/Bezugsfeldzonen. Es unterstützt intern die Orientierung und Lokalisierung, ist kein Bestandteil des Ergebnisses und wird nicht als Datei oder Download ausgeliefert.
- Der Nutzer bestätigt zuerst, welche Messgrößen im Dokument tatsächlich eingetragen sind.
- Fehlende oder unsicher erkannte Mess- beziehungsweise notwendige Bezugswerte werden einzeln am Originalausschnitt abgefragt.
- Fehlende oder unsichere Werte erzeugen kein rotes X. Solange ein benötigter Wert fehlt, bleibt die Ergebnisansicht gesperrt.
- Ein grüner Haken erscheint nur bei vollständigem Messumfang und ausschließlich bestandenen Rechenregeln.
- Ein rotes X erscheint erst, wenn mindestens eine rechnerische Abweichung nach Erkennung oder manueller Eingabe ausdrücklich als tatsächlich eingetragener Wert bestätigt wurde.

## Messgrößen und Rechenregeln

- Schutzpotenzialausgleich und Niederohmmessung gegen den hinterlegten Rechen-/Prüfwert,
- Isolationswiderstand gegen den Mindestprüfwert,
- Schleifenimpedanz `Zs ≤ U0 / (Faktor × In)` mit B = 5, C = 10, D = 20,
- Kurzschlussstrom-Konsistenz `Ik ≈ U0 / Zs`,
- Verbraucherstrom `Ib ≤ In`,
- Spannungsfall gegen Prüfziel sowie Konsistenz von `ΔU / Un × 100` und Prozentwert,
- RCD-Auslösestrom `IΔ ≤ IΔn`,
- RCD-Auslösezeit gegen den hinterlegten Standard-Prüfwert,
- numerische Plausibilitätsbereiche für weitere ausgewählte Messgrößen.

Die hinterlegten Rechen- und Prüfwerte sind dokumentierte Softwareparameter. Die Anwendung führt keine Messung durch und ersetzt keine fachliche Bewertung oder Inbetriebnahmefreigabe.

## Erkennung und Datenschutz

- PDF wird lokal mit PDF.js gerendert; eingebetteter PDF-Text wird lokal ausgewertet.
- Fotos werden lokal ausgerichtet und über die browserseitige `TextDetector`-Schnittstelle ausgewertet, sofern diese Laufzeitfunktion verfügbar ist.
- Steht keine lokale Bildtexterkennung zur Verfügung oder ist ein Wert unsicher, führt die Anwendung den Nutzer zur manuellen Eingabe am markierten Messwertausschnitt.
- Es findet kein Dokumentupload statt.
- Die leere Mustervorlage und reale ausgefüllte Protokolle sind nicht Bestandteil des Releases oder PWA-Caches.

## Projektstruktur

- `index.html` und 15 Direktseiten,
- `assets/`: zentrale Laufzeitdateien, Datenkataloge, VDE-Messwertengine, Regeln und internes Lokalisierungsprofil,
- `plausibilitaetspruefung-vde0100-600/`: Upload-, Analyse-, Einzelklärungs- und Ergebnisoberfläche,
- `vendor/pdfjs/`: lokale PDF.js-Laufzeit,
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente,
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Datenschutz-Gate, Prüfsummen und ZIP,
- `tools/validate_release.py`: statische Vollständigkeits-, Ausschluss-, Datenschutz- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner-, Inhalts- und VDE-Rechenregressionen,
- `tools/browser-smoke-test.py`: Browser-, Responsive-, PWA- und Offline-Test,
- `tools/vde-protocol-e2e-test.py`: reproduzierbare PDF-, Fehlwert-, Negativ- und Smartphone-Foto-Szenarien,
- `TESTBERICHT-UND-ABNAHME.md`: geprüfter Release-Nachweis,
- `SHA256SUMS.txt`: vollständige interne SHA-256-Prüfsummen.

## Testen

```bash
node tools/functional-smoke-test.js
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
# in einem zweiten Terminal
python3 tools/browser-smoke-test.py
python3 tools/vde-protocol-e2e-test.py
```

## Release bauen

```bash
python3 tools/release.py --all
```

Der Build synchronisiert Version, Manifest, App-ID, Cache-Namen, Precache und Dokumentationsreferenzen, prüft das Datenschutz-Gate, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
