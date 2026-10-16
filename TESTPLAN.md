# Testplan – SK PCT Tools V2.6.3.0-Beta

Stand: 16.10.2026  
Basis: vollständige V2.6.2.1-Beta

## 1. Statische Struktur- und Integritätsprüfung

```bash
python3 tests/validate_project.py
```

Prüfumfang:
- 16 HTML-Dokumente, davon 14 gerahmte interne Seiten
- genau eine zentrale CSS- und eine zentrale App-JS-Datei
- Version 2.6.3.0-Beta in HTML, Manifest, Suchindex und Laufzeit
- keine operativen Altversionsreferenzen
- lokale Ziele, H1, Referrer-Schutz, Header und Footer
- Manifest-, Favicon- und Apple-Touch-Verweis in allen HTML-Dokumenten
- Service-Worker-Kerncache `v2-6-3-0-core-r1`
- vollständige und korrekte `SHA256SUMS.txt`

## 2. Geschützte Bildbestände

- SHA-256-Vergleich aller 7 Logo-/Browser-/Apple-/PWA-PNGs mit V2.6.2.1-Beta
- SHA-256-Vergleich aller 22 App-/Wissens-/Hersteller-/Navigations-PNGs
- genau 22 aktive Navigationsdateien mit Präfix `v2-6-3-0-`
- PNG-Signatur, 512 × 512 px, RGBA und Transparenz der Navigationsicons
- sichtbare Alpha-Grenze `(13, 9, 489, 491)`
- vollständige Aufnahme der aktiven Bilddateien in den Offline-Kerncache

## 3. Versionsschild

Auf Startseite und allen internen Seiten:
- sichtbarer Versionswert `V2.6.3.0-Beta`
- exakter Text `Tool by S.K.`
- 3-px-Schwarzrahmen und Verlaufshintergrund
- Cyan-, Blau- und Grün-Akzentkanten
- keine Transformation oder Verschiebung
- keine horizontale oder vertikale Übersteuerung
- lesbare responsive Darstellung bis 320 CSS-Pixel und im Querformat

## 4. Header- und Navigationsbuttons

Für Suche, Favoritenübersicht, Home und Zurück:
- Smartphone/Tablet mindestens 44 × 44 px
- Desktop 48 × 48 px
- schwarze Kontur, Stahlfläche, räumliche Tiefe und dreifarbige Akzentkante
- `touch-action: manipulation`
- sichtbarer Fokuszustand
- identische Geometrie in Ruhe, Hover, Fokus, Press und Aktivzustand
- Navigation, aria-expanded, Favoritenzähler und Schließen-Funktion wirksam

## 5. Strukturelle Favoritenkopplung

Für zehn Startseiten- und fünf Wissens-App-Icons:
- `.sk-favorite-button` bleibt direktes Kind von `.sk-app-icon-wrapper`
- sichtbarer Favoritenkreis 21 bis 23 px, Sollmaß 22 px
- Touchfläche mindestens 44 × 44 px
- Kreismittelpunkt auf der oberen rechten sichtbaren PNG-/Wrapperkante
- aktive und inaktive Zustände geometrisch identisch
- App-Kachel, Wrapper und PNG in allen Interaktionszuständen pixelstabil

## 6. Browser-Regression

```bash
python3 tests/browser_regression.py
```

Prüfumfang:
- 15 aktive Routen × Smartphone 390 × 844, Tablet 820 × 1180 und Desktop 1440 × 1000
- Header, Footer, Rahmen, Scrollverhalten und horizontaler Überlauf
- 320-px-Reflow-Sanity und Safe-Area-kompatible Geometrie
- Startseitensuche öffnen/schließen ohne Buttonverschiebung
- Favoritenübersicht öffnen/schließen, Zähler und Eintragsdarstellung
- reale Touch-Auslösung auf Smartphone und Tablet
- sechs Rechnerreferenzen einschließlich Grenzwerte und Reset
- Wissensnavigation, Kompaktansicht und Quellenbündel
- Offline-Start, Offline-Unterseiten und Upgrade auf `v2-6-3-0-core-r1`

## 7. Visuelle Abnahme

- Startseite bei 320 × 900, 390 × 844, 820 × 1180 und 1440 × 1000
- Unterseiten auf Smartphone, Tablet und Desktop
- geöffnete Favoritenübersicht auf dem Smartphone
- kein Beschnitt, keine defekten Bilder und kein horizontaler Überlauf
- optisch geschlossene Familie aus Logo, Versionsschild, App-Icons und Navigation
- App-Icon-Bilddaten und feste Favoritenanker optisch unverändert

Die ausgeführten Ergebnisse werden in `TEST-RESULTS.txt` dokumentiert. Danach werden
`SHA256SUMS.txt` und das vollständige ZIP-Paket erzeugt und erneut geprüft.
