# Testbericht und Abnahme – SK PLT Tools 2.1.5.0-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.4.2-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** kompletter Drei-Reiter-Umbau des Siemens-Rohwert-Rechners, Ausschluss der alten Oberfläche, Diagnosefarben, Responsive-Regression, PWA/Offline, Releaseintegrität

## Gesamtergebnis

**PASS – der Drei-Reiter-Aufbau ist funktional, die alte Rechneroberfläche ist entfernt, iPhone-, Tablet- und Desktop-Darstellung sind automatisiert geprüft und das vollständige Release ist versions- und prüfsummenkonsistent.**

## Abgenommene Oberfläche

- Reiter exakt in der Reihenfolge **Signal**, **Rohwert**, **Phys. Wert**.
- Ein einziges gemeinsames sichtbares Vorgabefeld; bei jedem Reiterwechsel bleiben genau zwei abgeleitete Wertkarten sichtbar.
- Physikalischer Messbereich vor Einheitssignal und SPS-Karte; 4–20 mA ist Standard.
- Alte Auswahl „Eingaberichtung“, altes Ergebnisraster, Bereichsregler und alte Statusleiste sind weder im HTML noch in CSS/JavaScript vorhanden.
- Rohwertfarben: Grün `#89d329`, Gelb/Orange `#f5b942`, Rot `#ff7b83`, Cyan `#00b7e8`.
- Mobile untere Bedienzone, iPhone-Safe-Area, Header-Trennlinie und Startseiten-Link-Ausrichtung bleiben erhalten.

## Automatisierte Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.5.0-Beta in VERSION, 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | Drei Reiter | PASS · Beschriftung, Reihenfolge, ARIA-Auswahl und echte Klick-/Tastaturumschaltung vorhanden |
| T03 | Sichtbare Eingabe/Ausgabe | PASS · genau ein Vorgabefeld; je Reiter zwei und nur zwei Ergebniswerte sichtbar |
| T04 | Rechenlogik | PASS · Rohwert-, Signal- und physikalische Vorgabe einschließlich negativem Messbereich wechselseitig geprüft |
| T05 | Diagnosegrenzen | PASS · Standard-S7- und NE43-Grenzfälle für Nennbereich, Unter-/Übersteuerung und Unter-/Überlauf geprüft |
| T06 | Rohwertfarben | PASS · berechnete Browserfarben Grün, Gelb/Orange, Rot und Cyan an den zugehörigen Zuständen geprüft |
| T07 | Altoberfläche | PASS · `#inputKind`, altes Ergebnis-/Steuerraster, Regler und Statusleiste statisch und im Browser ausgeschlossen |
| T08 | iPhone-Hochformat | PASS · 390 × 844 px, kein horizontales Überlaufen, sticky Header, bündige Linie, feste 50 × 50-px-Schnellzugriffe |
| T09 | Smartphone-Querformat | PASS · 844 × 390 px, Safe-Area-/Viewport-Shell, feste untere Bedienzone und vollbreiter Header |
| T10 | Tablet | PASS · 820 × 1180 px, Reiter und zwei Ergebniswerte ohne Layoutüberlauf |
| T11 | Desktop | PASS · 1440 × 1050 px, vollständige Reihenfolge und Reiterinteraktion |
| T12 | Alle Direktseiten | PASS · 15 Seiten auf Mobil/Tablet auf Versionsstand, Header, Touchflächen und Überlauf geprüft |
| T13 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T14 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.5.0-beta`, Cache `sk-plt-tools-v2.1.5.0-Beta`, Precache und Offline-Direktaufrufe |
| T15 | Statische Validierung | PASS · lokale Referenzen, JavaScript-Syntax, Ausschlussregeln, Safe-Area-Metadaten und interne SHA-256-Liste fehlerfrei |
| T16 | Releaseintegrität | PASS · vollständige interne SHA-256-Prüfsummen und ZIP-Integrität geprüft |

## Ausgeführte Befehle

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.5.0-Beta.zip
```

## Testartefakte

- `test-artifacts/siemens-desktop.png`
- `test-artifacts/siemens-tablet.png`
- `test-artifacts/siemens-mobile.png`
- zusätzliche Startseiten-, Navigations- und Querformat-Screenshots im selben Ordner

## Abnahme

- Der technisch zuverlässige Drei-Reiter-Aufbau wurde vollständig umgesetzt; die vorgesehene Unterseiten-Ausweichlösung ist nicht erforderlich.
- Sämtliche unterstützten Module, Wissensinhalte, Navigation, Suche, Favoriten sowie PWA- und Offline-Funktionen bleiben erhalten.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
