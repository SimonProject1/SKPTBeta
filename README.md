# SK PLT Tools 2.1.1.0-Beta

Vollständiges statisches und offline-fähiges Webprojekt für PLT-/MSR-Aufgaben. **2.1.1.0-Beta** basiert auf dem vollständigen Stand **2.1.0.5-Beta**; die stabile Referenz bleibt **2.1.0.0**.

## Schwerpunkt dieser Beta

Die bisherige automatische Foto-/PDF- und Protokollanalyse der VDE-0100-600-Funktion wurde vollständig durch einen manuellen **VDE-Messwertprüfer** ersetzt.

- kein Datei-Upload, keine PDF-Auswertung, keine Fotoanalyse und keine OCR,
- keine Formularidentität, Kreuze, Unterschriften oder formale Protokollprüfung in der Bewertungslogik,
- sechs klar getrennte Messgrößen: Spannungsfall, Isolation, Schleifenimpedanz/Kurzschlussstrom, RCD, Niederohmigkeit und Schutzpotentialausgleich,
- dynamische Eingabemasken zeigen nur die für den gewählten Rechenweg notwendigen Angaben,
- kein numerischer Grenzwert wird vorbelegt,
- kontextabhängige Grenzen werden als freigegebener Sollwert eingegeben oder aus `U0` und freigegebenem `Ia` berechnet,
- fehlende und ungültige Angaben werden gezielt benannt,
- kein Endergebnis bei unvollständiger Berechnungsgrundlage,
- jedes vollständige Ergebnis zeigt Grenzwert, Formel, eingesetzte Zahlen und `i. O.` beziehungsweise `nicht i. O.`.

## Messgrößen und Rechenwege

- Spannungsfall: Direktvergleich in Prozent oder Berechnung `ΔU / Un × 100`.
- Isolationsmessung: kleinster Messwert gegen freigegebenen Mindestwert.
- Schleifenimpedanz: gegen freigegebenes `Zs,max` oder `Zs,max = U0 / Ia`.
- Kurzschlussstrom: `Ik ≥ Ia`.
- RCD-Auslösezeit: gegen freigegebene Maximalzeit.
- RCD-Auslösestrom: innerhalb eines freigegebenen Grenzbereichs.
- Niederohmigkeit und Schutzpotentialausgleich: gegen freigegebene Maximalwerte.

Die Anwendung führt keine Messung durch und ersetzt weder fachliche Bewertung noch Inbetriebnahmefreigabe durch die verantwortliche Elektrofachkraft.

## Projektstruktur

- `index.html` und 15 Direktseiten,
- `assets/`: zentrale Laufzeitdateien, Datenkataloge, manuelle VDE-Rechenengine, Eingabeschema und Regeln,
- `plausibilitaetspruefung-vde0100-600/`: manueller VDE-Prüfstand,
- `shared/`: zentrale Header-, Footer- und Bedienelement-Fragmente,
- `vendor/`: aus der vollständigen Basis übernommene Drittanbieterstruktur; nicht vom VDE-Messwertprüfer geladen,
- `tools/release.py`: Versionssynchronisierung, PWA-Precache, Datenschutz-Gate, Prüfsummen und ZIP,
- `tools/validate_release.py`: statische Vollständigkeits-, Ausschluss- und Integritätsprüfung,
- `tools/functional-smoke-test.js`: Rechner-, Inhalts- und VDE-Rechenregressionen,
- `tools/browser-smoke-test.py`: Browser-, Responsive-, PWA- und Offline-Test,
- `tools/vde-protocol-e2e-test.py`: manueller VDE-E2E-Test; Dateiname aus Strukturkompatibilität,
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

Der Build synchronisiert Version, Manifest, App-ID, Cache, Precache und Dokumentationsreferenzen, erzeugt `SHA256SUMS.txt` und baut das vollständige ZIP.
