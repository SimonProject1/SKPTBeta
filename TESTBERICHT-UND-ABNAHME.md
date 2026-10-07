# Testbericht und Abnahme – 2.1.0.4-Beta

**Prüfdatum:** 07.10.2026  
**Direkte Basis:** 2.1.0.3-Beta  
**Stabile Referenz:** 2.1.0.0  
**Gesamturteil:** Release-fähige Beta für die dokumentierte Zweitkontrolle; keine elektrotechnische Zertifizierung oder Inbetriebnahmefreigabe.

## Prüfumfang

- vollständiger Projektbestand mit 16 Direktseiten,
- VDE-Domänenengine und sequentielle Klärungsoberfläche,
- technische Formularidentität ohne automatische fachliche Negativbewertung,
- autorisierte leere Referenz als PDF sowie daraus erzeugte PNG-/JPEG-Fotopfade,
- reale ausgefüllte historische PDF ausschließlich als externe Testeingabe,
- daraus ausschließlich temporär erzeugtes Smartphone-Foto,
- Formularabgleich, Feldmapping, Konfidenz, Checkboxen und Unterschriften,
- Genau-ein-Kreuz-Regel und sequenzielle Klärung fehlender, mehrfacher, ungültiger oder unsicherer Kreuze,
- Pflicht-/Sicherheits-Governance und Ortsangaben-Mehrfeldklärung,
- Messwert-Plausibilität einschließlich Positiv-, Grenz- und Negativfällen,
- Desktop, Tablet, Mobil, Manifest, Service Worker und Offline-Aufrufe,
- Release-Struktur, Datenschutz-Gate, lokale Referenzen, Syntax und SHA-256.

## Fehlerbild aus 2.1.0.3-Beta und Korrektur

| Fehler | Korrektur | Retest |
|---|---|---:|
| Strukturpassung unter 84 % führte automatisch zu `FORM-LAYOUT = fail`. | Formularidentität liefert nur noch `FORM-IDENTITY = open` mit `technicalOnly`; kein automatisches n.i.O. | PASS |
| Abweichendes Formular blockierte das Feldmapping vollständig. | Technisches Mapping ab 68 %; darunter manuelle Pflichtfeldzuordnung ohne Negativurteil. | PASS |
| Für ein unsicheres Formular war nur die Bestätigung als n.i.O. vorgesehen. | Drei eindeutige Optionen: „Formular trotzdem verwenden“, „Zuordnung manuell prüfen“, „Andere Datei hochladen“. | PASS |
| Mehrere oder unsichere Kreuze waren nicht als eigener Regeltyp dokumentiert. | `CHOICE-MULTIPLE-*`, `CHOICE-INVALID-*`, Kandidatenkonfidenz und Genau-ein-Kreuz-Regel. | PASS |
| Ein Endergebnis durfte logisch nicht von einer offenen Formularfrage abhängen. | Ergebnisansicht bleibt bei jeder offenen Pflicht-, Kreuz-, Messwert- oder Formularentscheidung gesperrt. | PASS |
| Formularabweichung konnte ein rotes X verursachen. | Rot nur bei bestätigtem Mangel, bestätigter fehlender Pflichtangabe oder rechnerischem Messwertfehler. | PASS |
| Schrittanzeige markierte im Offenpunktdialog bereits „Ergebnis“. | Übersicht und Offenpunktdialog bleiben im Schritt „Klärung“; „Ergebnis“ wird erst am Ende aktiv. | PASS |

## Automatisierte Ergebnisse

| ID | Prüfung | Ergebnis |
|---|---|---:|
| T01 | JavaScript-Funktions-Smoke einschließlich VDE-Regeln | PASS · 98 Assertions |
| T02 | Referenz-PDF, exakter Hash | PASS · Struktur 99,12 % |
| T03 | Referenz als PNG | PASS · Struktur 97,96 % |
| T04 | Referenz als komprimiertes JPEG | PASS · Struktur 95,67 % |
| T05 | Ausgefüllte externe Test-PDF | PASS · Struktur 81,97 % · Formularhinweis, kein automatischer Fehler |
| T06 | Smartphone-Foto aus externer Testeingabe | PASS · Struktur 82,75 % · Formularhinweis, kein automatischer Fehler |
| T07 | Drei Optionen für unsichere Formularidentität | PASS · exakte Beschriftung und Funktion geprüft |
| T08 | 78-%-Regressionsfall in der Domänenengine | PASS · technisch offen, kein `fail` |
| T09 | Kein Endergebnis bei offenen Punkten | PASS · PDF und Smartphone |
| T10 | Genau-ein-Kreuz-Regel | PASS · fehlend, mehrfach, ungültig und unsicher offen |
| T11 | Pflicht-/Sicherheitsabweichungen nicht überspringbar | PASS |
| T12 | Grüner Positivfall | PASS |
| T13 | Roter Fall durch bestätigte fehlende Pflichtangabe | PASS |
| T14 | Messwertregeln für Zs, RCD, Isolation, Ib/In und Spannungsfall | PASS |
| T15 | Vollständiger Browser-Smoke | PASS · 16 Direktseiten, Desktop/Tablet/Mobil, PWA und Offline |
| T16 | Statische Release-Validierung | PASS · Struktur, Versionen, Datenschutz, lokale Assets und Syntax |
| T17 | Interne SHA-256-Liste | PASS · vollständige Dateiliste |

## Kernergebnisse der Protokolltests

### Leere verbindliche Referenz

- SHA-256: `019b2918bbfa0b7bef71c6b95f1a48136305053995473b625693217383af05f2`.
- PDF-Strukturpassung: 99,12 %.
- PNG-Strukturpassung: 97,96 %.
- JPEG-Strukturpassung: 95,67 %.
- Keine leere Checkbox wird als i.O., n.i.O. oder n.rel. klassifiziert.
- Prüfer- und Inbetriebnehmer-Unterschrift werden als fehlend erkannt.
- Fehlende Pflichtwerte erscheinen einzeln als offene Punkte.

### Externe ausgefüllte Test-PDF

- Strukturpassung: 81,97 %.
- Status: abweichende/unsichere Formularidentität, nicht n.i.O.
- `FORM-IDENTITY` ist offen und technisch; `FORM-LAYOUT` existiert nicht mehr als Fehlerpfad.
- Die drei geforderten Formularoptionen sind sichtbar.
- Nach „Formular trotzdem verwenden“ bleibt die fachliche Offenpunktliste erhalten.
- Vor Klärung aller Punkte ist die Ergebnisansicht nicht erreichbar.

### Smartphone-Foto

- Temporär aus der externen Test-PDF erzeugte JPEG-Aufnahme mit 1170 Pixel Breite, JPEG-Qualität 68 und angepasstem Kontrast.
- Strukturpassung: 82,75 %.
- Dieselbe nicht blockierende Formularlogik wie im PDF-Pfad.
- Mobile Darstellung bei 390 × 844 Pixel geprüft.
- „Zuordnung manuell prüfen“ aktiviert die feldweise Klärung; kein Endergebnis erscheint vor Abschluss.

### 78-%-Fehlbewertung

Ein synthetischer Engine-Regressionsfall mit exakt 78 % Strukturpassung erzeugt ausschließlich den technischen offenen Punkt `FORM-IDENTITY`. Es entsteht kein `fail`, kein automatisches n.i.O. und kein rotes X. Nach „Formular trotzdem verwenden“ wird die fachliche Prüfung fortgesetzt.

## Ergebnis-Governance

- Offene Punkte werden in der Ergebnislogik nicht als abgeschlossen behandelt.
- Automatisch erkannte n.i.O.-Kreuze und rechnerische Grenzwertverletzungen werden vor dem roten Ergebnis bestätigt.
- Fehlende Pflichtangaben können als Mangel bestätigt werden; dadurch wird das Endergebnis rot.
- Nicht sicher erkannte Werte werden bestätigt oder korrigiert.
- Der grüne Positivfall verlangt vollständige Pflichtdaten, eindeutige zulässige Kreuze und plausible Messwerte.
- Pflichtfelder und sicherheitsrelevante Abweichungen können nicht als „nicht relevant“ übersprungen werden.

## Datenschutz- und Release-Nachweis

- Die ausgefüllte Test-PDF ist nicht im Projekt, ZIP oder Precache enthalten.
- Ihr bekannter Dateiname und SHA-256 werden vom Release-Builder und Validator als Release-Inhalt blockiert.
- Das Smartphone-Testfoto und der mobile Test-Screenshot werden nur außerhalb des Projektstamms erzeugt.
- Die leere Referenz-PDF ist ebenfalls nicht eingebettet; ausgeliefert werden nur Hash, Strukturmerkmale und Blank-Baselines.
- Externe Protokolle werden Tests ausschließlich über Umgebungsvariablen übergeben.

## Restrisiken

- Die Erkennung ist ein lokales heuristisches Ensemble und kein trainiertes, selbstlernendes KI-Modell.
- Stark perspektivische, abgeschnittene, beschädigte oder fachlich anders strukturierte Aufnahmen können eine vollständige manuelle Zuordnung erfordern.
- Lokale Browser-Texterkennung ist nicht in jeder Laufzeit verfügbar; visuell vorhandene Einträge bleiben dann zur manuellen Bestätigung offen.
- Grenzwerte und Ergebnisse müssen durch eine verantwortliche Elektrofachkraft bewertet werden.

## Abnahme

Die beschriebene Fehlbewertung ist im geprüften Stand behoben. Die Version 2.1.0.4-Beta ist für kontrollierte Anwender- und Feldtests freigabefähig. Eine produktive elektrotechnische Freigabe wird ausdrücklich nicht erteilt.
