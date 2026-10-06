# Testbericht und Abnahme – 2.1.0.2-Beta

Prüfdatum: 06.10.2026  
Direkte Basis: 2.1.0.1-Beta  
Stabile Basis: 2.1.0.0

## Prüfumfang

- vollständiger Bestand mit 16 HTML-Seiten und allen direkten Seitenrouten
- sechs Rechner, Messstellen-Dokumentation und formulargebundene VDE-0100-600-Prüfung
- Foto-/PDF-Eingabe und lokales PDF.js-Rendering
- abgeleitetes Profil der leeren Vorlage `VDEProtokoll.pdf` mit SHA-256-Herkunftsnachweis, ohne Auslieferung der PDF
- A4-/Ausrichtungskontrolle, 33 Linienanker, 93 Feldzuordnungen und Checkbox-Raster
- Vollständigkeit der Prüfpunkte 3.1–3.20, 4.1–4.4, Abschnitte 6.1/6.2 und 7.1–7.6
- geführte Auswahl/Korrektur, „nicht relevant“, Bestätigung n.i.O. und grünes/rotes Abschlussurteil
- Regeln für Wertebereiche, Isolationswiderstand, Durchgängigkeit, Zs, Ib/In, Spannungsfall und RCD
- fünf Wissensbeiträge, Werkstoff-Nachschlagewerk, Suche, Filter, Sortierung, Favoriten und Navigationsbaum
- Manifest, Service Worker, Cache-Name, Precache, lokale Referenzen, JavaScript-/Python-/JSON-Syntax und SHA-256-Integrität

## Ausgeführte automatisierte Prüfungen

| Prüfung | Befehl / Verfahren | Ergebnis |
|---|---|---|
| Fachliche Funktions-Smoke-Tests | `node tools/functional-smoke-test.js` | Bestanden; Bestandsrechner, 93 VDE-Feldzuordnungen, positiver Abschlussfall sowie Zs-, RCD- und n.i.O.-Negativfälle |
| Statische Release-Validierung | `python tools/validate_release.py` | Bestanden; 16 Seiten, lokale Referenzen, Formulargeometrie, UI-Pflichtelemente, Vorlagenschutz, Manifest, Precache und Syntax |
| Referenzgeometrie | deterministischer Bildvergleich der externen `VDEProtokoll.pdf` gegen die ausgelieferten Linienanker | Bestanden; Layoutscore 100 %, keine falsch erkannten Markierungen im leeren Checkbox-Raster |
| Prüfsummen | `sha256sum -c SHA256SUMS.txt` | Bestanden |
| ZIP-Struktur und Dekompression | `unzip -t` und Bestandsvergleich | Bestanden; 79 Dateien unter genau einem Projektstamm, keine Referenz-PDF enthalten |

## Browser-Teststatus

`tools/browser-smoke-test.py` wurde auf die neue Oberfläche, den reinen Nutzerupload, das Fehlen einer Musterladefunktion, Formularpassung, Originalvorschau und Originalausschnitt im Klärungsdialog aktualisiert. Die Ausführung war im Build-Container nicht möglich, weil kein Chromium-Binary vorhanden war, der Browser-Download durch die Sandbox mit HTTP 403 blockiert wurde und keine DesktopBrowser-CDP-Adresse bereitgestellt war. Die statische DOM-Prüfung, die JavaScript-Syntaxprüfung, die fachliche Engine-Prüfung und der deterministische Referenzbildtest wurden davon unabhängig erfolgreich ausgeführt.

## Sicherheits- und Sichtbarkeitsprüfung

1. `VDEProtokoll.pdf` ist nicht im Projektbestand vorhanden.
2. Es gibt weder `#loadSample` noch einen Link oder Download auf die Mustervorlage.
3. `referenceForm.embedded` und `referenceForm.downloadable` sind `false`.
4. Vorschau und Feldkontext werden ausschließlich aus `state.pages` des aktuellen Nutzeruploads erzeugt.
5. Die frühere Regressionstest-Fixture bleibt ohne UI-Verknüpfung ausschließlich im Testbereich erhalten.

## Abnahmekriterien

1. Kein Bestandsmodul und keine bestehende Direktseite fehlt.
2. PDF und Bildformate sind auswählbar; die Dokumentenverarbeitung erfolgt lokal.
3. Unsichere oder fehlende Angaben werden nicht erfunden, sondern als offene Punkte angeboten.
4. Jeder offene Punkt kann korrigiert, ausgewählt oder als nicht relevant behandelt werden; bestätigte Abweichungen bleiben n.i.O.
5. Ein Abschlussurteil erscheint erst nach vollständiger Klärung.
6. Bestätigte Abweichungen oder verletzte Regeln führen zum roten X; andernfalls erscheint der grüne Haken.
7. Der Service Worker aktiviert `sk-plt-tools-v2.1.0.2-Beta` und enthält Engine, Schema, Regeln und PDF.js im Offline-Precache.
8. Alle lokalen Referenzen und Navigationsziele existieren.
9. `SHA256SUMS.txt` stimmt vollständig mit dem Paketinhalt überein.
10. Das ZIP enthält den vollständigen Projektordner als einzige oberste Ebene.

## Ergebnis

**Freigabefähig mit dokumentiertem Browser-Infrastrukturhinweis.** Statische, fachliche, geometrische und Integritätsprüfungen sind bestanden. Der vollständige Browser-Smoke-Test ist im Zielsystem mit installiertem Chromium nachzuholen; das entsprechende Testskript ist Bestandteil des Pakets.
