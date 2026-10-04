# Testbericht und Abnahme – 2.1.0.1-Beta

Prüfdatum: 04.10.2026  
Stabile Basis: 2.1.0.0

## Prüfumfang

- vollständiger Bestand mit 16 HTML-Seiten und allen direkten Seitenrouten
- sechs Rechner, Messstellen-Dokumentation und überarbeitete VDE-0100-600-Prüfung
- Foto-/PDF-Eingabe, lokales PDF.js-Rendering und Musterfingerabdruck
- Formularprofil `228_SR4_K06_E07.1.pdf` mit erkanntem offenem Kalibrierstatus
- geführte Korrektur des offenen Punkts bis zum grünen Abschlussurteil
- Engine-Regeln für Pflichtangaben, Wertebereiche, Isolationswiderstand, Zs, Ib/In, Spannungsfall und RCD
- fünf Wissensbeiträge und Werkstoff-Nachschlagewerk
- Suche, Filter, Sortierung, Favoriten, Navigationsbaum und mobile Darstellung
- Desktop 1440 × 1050, Tablet 820 × 1180 und Mobil 390 × 844
- Manifest, Service Worker, Cache-Name, Precache und Offline-Aufrufe
- lokale Referenzen, JavaScript-/Python-/JSON-Syntax, Vorlagen und SHA-256-Integrität

## Automatisierte Prüfungen

| Prüfung | Befehl | Ergebnis |
|---|---|---|
| Fachliche Funktions-Smoke-Tests | `node tools/functional-smoke-test.js` | Bestanden; bestehende Rechner und neue VDE-Engine einschließlich Positiv-/Negativfällen |
| Statische Release-Validierung | `python tools/validate_release.py` | Bestanden; 16 Seiten, VDE-Schema, Musterhash, lokale Referenzen, Manifest, Precache, Syntax und Integrität |
| Browser-/Responsive-/PWA-/Offline-Test | `python tools/browser-smoke-test.py` bei lokalem Server | Bestanden; Desktop, Tablet, Mobil, Muster-PDF, Klärungsablauf, PWA und Offline-Aufrufe |
| Prüfsummen | `sha256sum -c SHA256SUMS.txt` | Bestanden |
| ZIP-Struktur und Dekompression | `unzip -t` sowie Dateibestandsvergleich | Bestanden nach finalem Paketbau |

## VDE-Musterfall

1. Die unveränderte PDF wird lokal geladen und mit PDF.js gerendert.
2. SHA-256 `744f24436071c5c9f36d91fc82fa2a6a16f20ec8662bd81f68e3f53321792772` ordnet das kalibrierte Musterprofil eindeutig zu.
3. Mindestens 25 Protokollwerte werden übernommen.
4. Der im Scan nicht sicher feststellbare Kalibrierstatus bleibt als genau ein offener Punkt bestehen.
5. Nach Auswahl „Gültig / im Protokoll nachgewiesen“ werden alle Regeln erneut ausgeführt.
6. Isolationswerte, Niederohmwert, Zs, Ib/In, Spannungsfall sowie RCD-Auslösestrom und -zeit bestehen die hinterlegten Plausibilitätsregeln; das UI zeigt den grünen Haken „Plausibel“.
7. Separate Engine-Tests weisen nach, dass eine zu hohe Zs und ein RCD-Auslösestrom über IΔn zum Fehler führen.

## Abnahmekriterien

1. Kein Bestandsmodul und keine bestehende Direktseite fehlt.
2. PDF und Bildformate sind auswählbar; die Dokumentenverarbeitung erfolgt lokal.
3. Unsichere oder fehlende Angaben werden nicht erfunden, sondern als offene Punkte angeboten.
4. Jeder offene Punkt kann korrigiert, ausgewählt, als nicht relevant oder als n.i.O. bestätigt werden.
5. Ein Abschlussurteil erscheint erst nach vollständiger Klärung.
6. Bestätigte Abweichungen oder verletzte Regeln führen zum roten X; andernfalls erscheint der grüne Haken.
7. Der Service Worker aktiviert `sk-plt-tools-v2.1.0.1-Beta` und enthält Engine, Schema, PDF.js sowie Musterdatei im Offline-Precache.
8. Alle lokalen Referenzen und Navigationsziele existieren.
9. `SHA256SUMS.txt` stimmt vollständig mit dem Paketinhalt überein.
10. Das ZIP enthält den vollständigen Projektordner als einzige oberste Ebene.

## Ergebnis

**Bestanden.** Die automatisierten Prüfungen wurden am 04.10.2026 für 2.1.0.1-Beta erfolgreich ausgeführt. Der vollständige Vorgängerbestand bleibt funktionsfähig. Die neue VDE-Dokumentenprüfung verarbeitet das Musterformular, führt durch offene Punkte und erzeugt das geforderte grüne beziehungsweise rote Abschlussurteil. Die fachliche Sicherheitsgrenze bleibt sichtbar dokumentiert.
