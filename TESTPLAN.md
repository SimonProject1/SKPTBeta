# Testplan · SK PCT Tools 2.6.0.3-Beta

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
3. Prüfen, dass nur Caches der Version 2.6.0.3-Beta aktiv sind.

## 6. Manuelle Plattformprüfung
1. iPhone/iPad/Android: Installation, Safe Areas, Hoch-/Querformat und echter Touch.
2. Safari/Firefox/Edge: Smoke-Test.
3. VoiceOver/NVDA: Fokusreihenfolge, Zustände und Live-Regionen.
4. Hosting: Sicherheitsheader gemäß SECURITY-DEPLOYMENT.md prüfen.

## 7. Verbindlicher Plus/Minus-Standard
1. Analogsignal, P+F, Pt100/Pt1000, Einheitenrechner und Siemens-Rohwert öffnen.
2. Jeden sichtbaren ±-Taster auf 44 × 44 px, 13-px-Radius, schwarze Kontur, Cyan-Fokus und grünen Druckzustand prüfen.
3. Ausrichtung in jedem Eingabefeld sowie unveränderte Feldhöhe bei Smartphone, Tablet und Desktop kontrollieren.
4. Positive, negative und Nullwerte umschalten; Eingabewert und Ergebnis müssen unmittelbar aktualisiert werden.
5. Auf Smartphone und Tablet jeden Taster per Tap auslösen.

## 8. Alternative PNG-Navigationsgrafiken
1. Alle zehn Startseitenziele prüfen: zehn geladene PNG-Dateien ohne defekte Grafik; jede Datei 512 × 512 px, RGBA und transparent.
2. Dreistufige Bedeutung prüfen: Hauptmotiv = Funktion, integriertes Textfeld = Kategorie, HTML-Titel unter dem Icon = konkretes Ziel.
3. Motivklassen prüfen: sechs Taschenrechner, drei Bücher und eine WWW-Weltkugel mit Auswärtspfeil.
4. Kategorien prüfen: sechs Rechner = RECHNER; Einheitendatenbank und Wissensdatenbank/Wissensbeiträge = WISSEN; Werkstoffdatenbank = MATERIAL; externer E+H-Dienst = EXTERN.
5. Die sechs Rechner-PNGs müssen pixelidentisch sein und denselben SHA-256-Wert besitzen.
6. Rechnergeometrie prüfen: Frontkörper x=108…392 px/y=42…346 px, sichtbare Tiefe bis x=407 px/y=362 px, Kategoriefeld ab y=382 px.
7. Auf Smartphone, Tablet und Desktop Außenmaß, Rahmenstärke, Eckenradius, Perspektive, CSS-Schatten, PNG-Innenmaß und Favoritensternposition aller zehn App-Kacheln vergleichen.
8. Jedes fachlich gekennzeichnete Icon darf genau ein Kategoriefeld zeigen. Das sichtbare Feld muss Bestandteil der PNG-Pixel sein.
9. HTML, CSS und JavaScript dürfen kein zusätzliches RECHNER-, WISSEN-, EXTERN-, MATERIAL-, PCT- oder PIPING-Overlay erzeugen.
10. Im Browser ::before-/::after-Inhalte der Icon-Container auf verbotenen Kategorietext prüfen.
11. Wissens-Hub prüfen: fünf weiße Hersteller-/Kurzmarken ohne zusätzliche Motivgrafik, jeweils mit genau einem integrierten PCT-Feld.
12. Beitragskarten prüfen: alle fünf Wissensbeiträge verwenden das Buch mit integriertem WISSEN-Feld.
13. Grafiken bei 24, 56, 64, 94, 192 und 512 px auf Kontur, Transparenz, Plastizität und Lesbarkeit prüfen.
14. Smartphone 390 × 844, Tablet 820 × 1180, Desktop 1440 × 1000 und Reflow 320 × 900 prüfen.
15. Manifest-Shortcuts auf image/png und sizes 512x512 prüfen.
16. Offline erneut laden; alle 17 PNG-Navigationsgrafiken müssen aus dem Version-2.6.0.3-Beta-Cache erscheinen.
17. Prüfen, dass assets/navigation-icons/ keine SVG-Datei enthält und als einzige technische SVG-Ausnahme assets/pct-controls.svg verbleibt.
18. ICON-DESIGNRICHTLINIE.txt als verbindliche Übergabegrundlage auf Vollständigkeit prüfen.
