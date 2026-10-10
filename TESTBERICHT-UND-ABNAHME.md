# Testbericht und Abnahme – SK PLT Tools 2.1.7.2-Beta

**Prüfdatum:** 10.10.2026  
**Ausgangsbasis:** vollständige 2.1.7.1-Beta  
**Ergebnis:** automatisierte Freigabekriterien erfüllt

## 1. Testumgebung

- Linux-Container, statischer HTTP-Server auf `127.0.0.1:4173`.
- Chromium über Playwright.
- Desktop: 1440 × 1050, Device Scale 1.
- Tabletprofil: 820 × 1180, Device Scale 2, Mobilemodus.
- iPhone-Touchprofil: 390 × 844, Device Scale 2, Touchmodus.
- Smartphone-Querformat: 844 × 390, Device Scale 2, Touchmodus.

Die iPhone-Prüfung ist eine reproduzierbare Browser-/Touch-Emulation. Eine zusätzliche Prüfung auf physischer iOS-/Safari-Hardware ist nicht Bestandteil dieses automatisierten Containerlaufs.

## 2. Änderungsprüfung 2.1.7.2-Beta

- Auf allen sechs Rechnerseiten ist genau ein Bereich `.sk-unit-database-cta` vorhanden.
- Desktop: reale Breite höchstens 720 px; Tablet: höchstens 640 px; beide jeweils weniger als 92 % der Hauptinhaltsbreite.
- Smartphone: vollständig innerhalb des Viewports; Button bleibt innerhalb des Bereichs und touchfreundlich.
- Neuer Herstellerlink exakt `https://www.de.endress.com/de/onlinetools?store_locale=de`.
- Externer Link mit `target="_blank"` und `rel="noopener noreferrer"`.
- Navigationsbaum enthält dasselbe neue externe Ziel.

## 3. Datenmodell und Umrechnungen

- 19 Kategorien und 115 Einheiten geladen und validiert.
- Eindeutigkeit von Kategorien und Einheiten geprüft.
- Gültige feste Standardeinheit je Kategorie geprüft.
- Standards bar, °C, m³/h, m, V, A und Ω bestätigt.
- 575 Roundtrip-Fälle: fünf Testwerte je Einheit über die Kategoriestandardeinheit und zurück.
- Referenzfälle bestätigt: bar/mbar, °C/K, °F/°C, m³/h/l/min, kWh/MJ und cP/mPa·s.
- Offset-Sonderfälle bestätigt: 32 °F = 0 °C und −40 °C = −40 °F.

## 4. Favoriten, Suche und Dropdowns

- Einheitensuche, Kategorienfilter und Zurücksetzen geprüft.
- Sternmarkierung, `localStorage`-Schlüssel `skPltUnitFavoritesV1` und Reload-Persistenz geprüft.
- Favorisierte Einheit erscheint in der Dropdown-Gruppe „Favoriten“.
- Feste Standardeinheit bleibt in der Gruppe „Standardeinheit“ sichtbar.
- Weitere Einheiten bleiben vollständig auswählbar.

## 5. Rechnerregressionen

- Analogsignal: 0…100 → 4…20 mA ergibt 12,000 mA bei 50 %; Wechsel bar/psi und mA/A werttreu.
- Einheitenrechner: 1 bar = 1.000,000 mbar; 32 °F = 273,150 K und 0,000 °C.
- P+F: K-Faktor 0,160000 und Nullpunkt 4,000000; X- und Y-Wertepaare werden bei Einheitenwechsel gemeinsam umgerechnet.
- Pt100/Pt1000: 0 °C = 100,000 Ω für Pt100; °C/°F und Ω-basierte Rückrichtung geprüft.
- Siemens Rohwert: 12 mA = 13.824 und 50,000 °C; Messbereich −50…150 °C wechselt korrekt zu −58…302 °F; ± bleibt funktionsfähig.
- Spannungsfall: 16 A, 35 m, 2,5 mm², 400 V ergibt 6,93 V beziehungsweise 1,73 %; A/mA, m/ft und V/mV werttreu.

## 6. Responsive Design und Bedienung

Alle 16 Seiten wurden in Desktop-, Tablet- und iPhone-Touchprofil geladen. Geprüft wurden:

- kein horizontaler Überlauf,
- Versionsstand 2.1.7.2-Beta,
- gemeinsamer Header und Footer,
- Headerlinie und Startseiten-Button,
- Favoriten- und Navigationsschalter,
- feste mobile untere Bedienzone,
- dunkle Safe-Area-Grundfläche,
- mobile Zahlentastaturattribute aller Rechner-Zahlenfelder,
- alle sechs Rechner in allen drei Haupt-Viewports,
- kompakter responsiver Einheitendatenbank-Bereich.

Für die sechs Rechner wurden 18 aktuelle Screenshots erzeugt; für die Einheitendatenbank zusätzlich Desktop-, Tablet- und Mobile-Nachweise.

## 7. PWA und Offline

- Manifest-Version, App-ID und Shortcuts geprüft.
- Service-Worker-Cache `sk-plt-tools-v2.1.7.2-Beta` installiert.
- `units.json`, Einheitensystem, Datenbankseite und Rechnerintegrationen im Precache bestätigt.
- Einheitendatenbank offline vollständig aus dem Cache geöffnet; 115 Einheiten verfügbar.
- Keine JavaScript-Konsolenfehler in den Desktop-, Tablet- und Mobile-Prüfläufen.

## 8. Ausgeführte Prüfkommandos

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1208/chrome-linux64/chrome python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
```

## 9. Abnahme

Die automatisierten Freigabekriterien für den kompakten responsiven Einheitendatenbank-Bereich, den neuen abgesicherten Herstellerlink, Datenmodell, Favoriten, Dropdowns, automatische Faktor-/Offset-Umrechnung, Rechnerregression, Responsive Design und Offline-PWA sind erfüllt. Der Release bleibt wegen der zentralen Einheitenarchitektur als **Beta** gekennzeichnet.
