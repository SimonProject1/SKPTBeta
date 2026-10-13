# Testplan · SK PCT Tools 2.5.2.4-Beta

## 1. Automatische Prüfungen

```bash
python3 tests/validate_project.py
python3 tests/browser_regression.py
```

Browserprofile: Smartphone 390 × 844, Tablet 820 × 1180, Desktop 1440 × 1000 sowie Reflow 320 × 900.

## 2. Navigation und Semantik
1. Startseite sowie alle internen Unterseiten öffnen.
2. Lokale Links, gemeinsamer Header/Footer, genau eine H1 und Referrer-Schutz prüfen.
3. Startseite zeigt 10 Apps; Messstellen-Dokumentation und PDF-Vorlage dürfen nirgends verlinkt sein.

## 3. Rechner-Referenzwerte
1. Analogsignal: 0…100 und 4…20 mA; 50 ergibt 12 mA und 50 %.
2. P+F: (0|4) und (100|20); K-Faktor 0,16, Nullpunkt 4.
3. Pt100: 0 °C ergibt ungefähr 100 Ω.
4. Pt100/Pt1000: Werte unter -200 °C, über 850 °C sowie Widerstände außerhalb des jeweiligen Sensorbereichs werden abgewiesen.
5. Einheiten: 1 bar ergibt 100 kPa.
6. Siemens: 4–20 mA, 12 mA, -50…150 °C; Rohwert 13.824 und 50 °C.
7. Spannungsfall: Ergebnis vor Berechnung und nach Reset verborgen; Referenzfall ergibt ungefähr 6,93 V / 1,73 % / 393,07 V.

## 4. Datenbanken und Wissen
1. Einheitensuche, Favoriten und 19 Kategorien prüfen.
2. Werkstoffsuche, Gruppenfilter, Kartendetails und Quellenlinks prüfen.
3. Jeden der fünf Wissensbeiträge öffnen: Kurzantwort sichtbar, Fachdetails geschlossen.
4. Quellenblock nennt bei Praxiswissen „Erfahrungsberichte aus der Instandhaltungs- und PLT-Praxis (anonymisiert)“ und hält Gültigkeitsgrenzen sichtbar.

## 5. PWA und Offline
1. Online laden und Service Worker aktivieren lassen.
2. Offline Startseite, Rechner, Datenbanken und Wissensbeiträge öffnen.
3. Prüfen, dass nur Caches der Version 2.5.2.4-Beta aktiv sind.

## 6. Manuelle Plattformprüfung (nachgelagert)
1. iPhone/iPad/Android: Installation, Safe Areas, Hoch-/Querformat und echter Touch.
2. Safari/Firefox/Edge: Smoke-Test.
3. VoiceOver/NVDA: Fokusreihenfolge, Zustände und Live-Regionen.
4. Hosting: Sicherheitsheader gemäß SECURITY-DEPLOYMENT.md prüfen.

## 7. Verbindlicher Plus/Minus-Standard
1. Analogsignal, P+F, Pt100/Pt1000, Einheitenrechner und Siemens-Rohwert öffnen.
2. Jeden sichtbaren ±-Taster auf 44 × 44 px, 13-px-Radius, schwarze Kontur, Cyan-Fokus und grünen Druckzustand prüfen.
3. Ausrichtung in jedem Eingabefeld sowie unveränderte Feldhöhe bei Smartphone, Tablet und Desktop kontrollieren.
4. Positive, negative und Nullwerte umschalten; Eingabewert und Ergebnis müssen unmittelbar aktualisiert werden.
5. Auf Smartphone und Tablet jeden Taster per Tap auslösen; Scrollen darf nicht blockiert und Doppeltipp-Zoom nicht provoziert werden.

## 8. Eigenständige Navigationsgrafiken
1. Alle zehn Startseitenziele prüfen: zehn geladene, unterschiedliche SVG-Dateien ohne defekte Grafik.
2. Wissens-Hub und Beitragskarten prüfen: fünf eigenständige Herstellergrafiken konsistent wiederverwendet.
3. Startseite, Zurück-/Home-Navigation, Einheitendatenbank-CTA und externe E+H-Kachel anklicken.
4. Externe Kachel muss den Auswärtspfeil zeigen und weiterhin abgesichert in einem neuen Tab öffnen.
5. Grafiken bei 320, 390, 820 und 1440 px auf Kontur, Transparenz, Innenabstand und Erkennbarkeit prüfen.
6. Offline erneut laden; alle Navigationsgrafiken müssen aus dem Version-2.5.2.4-Beta-Cache erscheinen.
7. ICON-DESIGNRICHTLINIE.txt als verbindliche Übergabegrundlage auf Vollständigkeit prüfen.
