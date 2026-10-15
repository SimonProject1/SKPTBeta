# Testplan · SK PCT Tools 2.6.0.4-Beta

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
3. Prüfen, dass nur Caches der Version 2.6.0.4-Beta aktiv sind.

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

## 8. Entschlackte PNG-Navigationsgrafiken
1. Alle 17 Navigations-PNGs prüfen: 512 × 512 px, RGBA, echte transparente und deckende Pixel, keine defekte Grafik.
2. Verbindliche Leitregel prüfen: ein gemeinsamer Rahmen, ein klares Hauptmotiv, ein kleiner Favoritenstern; die Erklärung steht ausschließlich im Titel darunter.
3. Sicherstellen, dass RECHNER, WISSEN, MATERIAL, EXTERN und PCT nicht als integrierte Kategoriefelder in den PNGs erscheinen.
4. Sicherstellen, dass HTML, CSS und JavaScript kein sichtbares Kategoriefeld über dem Icon erzeugen.
5. Motive prüfen: sechs Taschenrechner mit Display, sechs großen Tasten und ±; drei Bücher mit zwei Farbseiten und schwarzer Mittelfalte; eine Weltkugel mit klaren Längen-/Breitengraden und kleinem WWW.
6. Hersteller-Hub prüfen: fünf ruhige Kurzmarken ohne PCT-Plakette; Home und Zurück als klare Einzelmotive.
7. Die sechs Rechner-PNGs und die drei Buch-PNGs müssen je Gruppe pixelidentisch sein.
8. Außenrahmen prüfen: kräftige schwarze Kontur, genau ein Blau-Cyan-Grün-Bogen, keine zweite Leuchtkontur und kein doppelter Schatten.
9. Favoriten prüfen: 44 × 44 px Touchfläche, sichtbarer Kreis 22 px, vollständig innerhalb des Außenrahmens.
10. Favorit inaktiv ohne grünes Leuchten; nach Aktivierung mit kleinem kontrollierten grünen Leuchten.
11. Titel prüfen: Umrechnen, Siemens RAW, Werkstoffe und Wissen; andere eindeutige Titel unverändert.
12. Titelkontur fein und ohne horizontales Überlaufen prüfen.
13. Drei Spalten bei 390 × 844 und 320 × 900 prüfen; zusätzlich Tablet 820 × 1180 und Desktop 1440 × 1000.
14. Grafiken bei 24, 56, 64, 94, 192 und 512 px auf klare Silhouette und reduzierte Details prüfen.
15. Manifest-Shortcuts auf image/png und sizes 512x512 prüfen.
16. Offline erneut laden; alle 17 PNG-Navigationsgrafiken müssen aus dem Version-2.6.0.4-Beta-Cache erscheinen.
17. Prüfen, dass assets/navigation-icons/ keine SVG-Datei enthält und als einzige technische SVG-Ausnahme assets/pct-controls.svg verbleibt.
18. ICON-DESIGNRICHTLINIE.txt als verbindliche Übergabegrundlage auf Vollständigkeit prüfen.
