# Testbericht und Abnahme – 2.1.0.3-Beta

**Prüfdatum:** 06.10.2026  
**Direkte Basis:** 2.1.0.2-Beta  
**Stabile Referenz:** 2.1.0.0  
**Gesamturteil:** Release-fähige Beta für die dokumentierte Zweitkontrolle; keine elektrotechnische Zertifizierung oder Inbetriebnahmefreigabe.

## Prüfumfang

- vollständiger Projektbestand mit 16 Direktseiten,
- VDE-Domänenengine und sequentielle Klärungsoberfläche,
- autorisierte leere Referenz als PDF sowie daraus erzeugte PNG-/JPEG-Fotopfade,
- reale ausgefüllte historische PDF ausschließlich als externe Testeingabe,
- Formularabgleich, Feldmapping, Konfidenz, Checkboxen und Unterschriften,
- Pflicht-/Sicherheits-Governance und Ortsangaben-Mehrfeldklärung,
- Messwert-Plausibilität einschließlich Positiv-, Grenz- und Negativfällen,
- Desktop, Tablet, Mobil, Manifest, Service Worker, Offline-Aufrufe,
- Release-Struktur, Datenschutz-Gate, lokale Referenzen, Syntax und SHA-256.

## Fehler aus 2.1.0.2-Beta

| Fehler | Korrektur | Retest |
|---|---|---:|
| Klärungs-Deadlock Ortsangabe | `MASTER-IDENT` enthält alle zwölf Ortsfelder; gemeinsamer Dialog verlangt mindestens zwei Angaben und ist nicht überspringbar. | PASS |
| Personenbezogene Testdatei im Release | Reale ausgefüllte PDF, Precache-Eintrag und alte VDE-Vorschau entfernt; Builder und Validator besitzen ein Inhalts-/Dateinamen-Gate. | PASS |
| Falsche Formularerkennung | Struktur-Ensemble mit harter Ablehnung unter 84 %; abgelehnte Formulare erhalten kein Feldmapping. | PASS |
| Falsche Unterschriften im leeren Formular | Referenzbereinigte Schreibzonen mit Tinten-, Dichte- und Strichwechsel-Evidenz. Beide leeren Signaturfelder werden als „Fehlt“ erkannt. | PASS |
| Instabile Fotoerkennung / falsche Checkboxen | Kontrastnormalisierung, Vierfach-Orientierung, Feinausrichtung, Innenmasken und Blank-Baselines. PDF/PNG/JPEG liefern null falsche Checkboxwerte. | PASS |
| Falscher Referenz-Hash | Autorisierter SHA-256 auf `019b2918bbfa0b7bef71c6b95f1a48136305053995473b625693217383af05f2` korrigiert und validiert. | PASS |
| Überspringbare Pflichtabweichungen | Feldbezogene Auflösungsrichtlinie; Pflicht-, Formular-, Signatur-, n.i.O.- und Messwertfehler sind nicht als „nicht relevant“ auflösbar. | PASS |
| Veralteter PWA-Sollwert | Browser-Test leitet App-ID und Cache aus `VERSION` ab; Sollwert 2.1.0.3-Beta. | PASS |

## Automatisierte Ergebnisse

| ID | Prüfung | Ergebnis |
|---|---|---:|
| T01 | JavaScript-Funktions-Smoke einschließlich VDE-Regeln | PASS · 90 Assertions |
| T02 | VDE-End-to-End: leere Referenz-PDF | PASS · Struktur 99,12 % |
| T03 | VDE-End-to-End: Referenz als PNG | PASS · Struktur 97,96 % |
| T04 | VDE-End-to-End: komprimiertes JPEG | PASS · Struktur 95,67 % |
| T05 | VDE-End-to-End: historisches Fremdformular | PASS · 81,97 %, hart abgelehnt, 0 positionsgebundene Felder |
| T06 | Leere Signaturfelder | PASS · beide „Fehlt“, keine Falsch-Positiven |
| T07 | Leere Checkboxen | PASS · 0 Falsch-Positive in 3.x/4.x/7.x |
| T08 | Pflicht-/Sicherheitsabweichungen nicht überspringbar | PASS |
| T09 | Grüner Positivfall / roter Negativfall in der Engine | PASS |
| T10 | Vollständiger Browser-Smoke | PASS · 16 Direktseiten, Desktop/Tablet/Mobil, PWA und Offline |
| T11 | Statische Release-Validierung | PASS · 16 Seiten, 93 Feldzonen, Referenzprofil, Datenschutz und lokale Assets |
| T12 | Interne SHA-256-Liste | PASS · 78 Einträge |

## Kernergebnisse der Protokolltests

### Leere verbindliche Referenz

- Exakter Referenz-Hash wird erkannt.
- Strukturpassung: 99,12 %.
- Keine leere Checkbox wird als i.O., n.i.O. oder n.rel. klassifiziert.
- Prüfer- und Inbetriebnehmer-Unterschrift werden nicht als vorhanden gemeldet.
- Fehlende Pflichtwerte erscheinen einzeln als offene Punkte.

### Foto-/Rasterpfad

- PNG: 97,96 %, JPEG: 95,67 %.
- Beide Varianten bleiben sicher oberhalb der Annahmeschwelle von 90 %.
- Trotz Skalierung und JPEG-Kompression entstehen keine falschen Checkbox- oder Signatur-Positiven.

### Externes ausgefülltes historisches Formular

- Strukturpassung: 81,97 % und damit unter der harten Ablehnungsschwelle von 84 %.
- Das Dokument wird als „NICHT UNTERSTÜTZT“ geführt.
- Es werden keine positionsgebundenen Formularwerte extrahiert.
- Die Formularabweichung kann weder als „nicht relevant“ markiert noch manuell auf „unterstützt“ umgestellt werden.
- Nach Bestätigung der Abweichung erscheint das rote X „Nicht plausibel“.

## Messwert- und Governance-Nachweise

Bestanden wurden unter anderem Zs-Grenzen für B/C/D, `Ib ≤ In`, Spannungsfallgrenze und Konsistenz, Isolation, Durchgängigkeitshinweis, RCD-Auslösestrom/-zeit, ungültige Datums-/Bereichswerte, fehlende Prüferunterschrift, n.i.O.-Einzelbewertungen, harter Fremdformularschutz sowie manipulierte `_notRelevant`-Zustände. Ein vollständiger positiver Datensatz ergibt weiterhin den grünen Haken.

## Datenschutz- und Release-Nachweis

- Keine reale ausgefüllte Protokoll-PDF im Projekt.
- Kein bekannter Dateiinhalt und kein Precache-Eintrag der externen Testdatei.
- Die leere Referenz-PDF ist ebenfalls nicht eingebettet; ausgeliefert werden nur ihr korrekter Hash und abgeleitete, nicht personenbezogene Struktur-/Blank-Merkmale.
- Externe Protokolle werden den Tests ausschließlich per Umgebungsvariable übergeben.

## Restrisiken

- Die Erkennung ist ein lokales heuristisches Ensemble und kein trainiertes, selbstlernendes KI-Modell.
- Stark perspektivische, abgeschnittene, beschädigte oder fachlich abweichende Aufnahmen können eine manuelle Formular- oder Feldklärung erfordern.
- Lokale Browser-Texterkennung ist nicht in jeder Laufzeit verfügbar; dann werden visuell vorhandene Einträge zur manuellen Bestätigung angeboten.
- Grenzwerte und Ergebnisse bleiben durch eine verantwortliche Elektrofachkraft zu bewerten.

## Abnahme

Die im Testbericht der Vorgängerversion festgestellten kritischen, hohen und mittleren Fehler sind im geprüften Stand behoben. Die Beta ist für weitere kontrollierte Anwender- und Feldtests freigabefähig. Eine produktive elektrotechnische Freigabe wird ausdrücklich nicht erteilt.
