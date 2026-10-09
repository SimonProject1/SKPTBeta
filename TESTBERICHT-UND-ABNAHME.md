# Testbericht und Abnahme – SK PLT Tools 2.1.5.1-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.5.0-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** Reiterwechsel auf iPhone und PC, Fokus-/Tastaturverhalten, Wechsel bei ungültiger Zwischeneingabe, Gesamtregression, PWA/Offline und Releaseintegrität

## Gesamtergebnis

**PASS – der Drei-Reiter-Wechsel funktioniert auf Desktop und Mobil ohne automatischen Fokus des Eingabefelds. Die sichtbare Reiterauswahl bleibt auch bei einer vorübergehend ungültigen Messbereichseingabe bedienbar.**

## Korrekturen

- Reiterklicks fokussieren `#inputValue` nicht mehr.
- Beim Reiterklick wird ein aktiver Eingabe-, Auswahl- oder Textfokus beendet, damit die iPhone-Bildschirmtastatur geschlossen bleibt.
- `aria-selected`, `tabindex` und `aria-labelledby` werden vor der Neuberechnung aktualisiert.
- Pfeiltasten-, Pos1- und Ende-Steuerung behalten den Fokus auf dem ausgewählten Reiter.
- Berechnungslogik, sichtbare Ergebniswerte und Diagnosefarben bleiben unverändert.

## Automatisierte Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.5.1-Beta in VERSION, 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | Desktop-Reiterklick | PASS · Signal, Rohwert und Phys. Wert wechseln per Mausklick; `aria-selected` folgt dem aktiven Modus |
| T03 | Desktop ohne Eingabefokus | PASS · ein Reiterklick setzt den Fokus nicht auf `#inputValue` |
| T04 | Ungültige Zwischeneingabe | PASS · Reiterauswahl wechselt sichtbar, obwohl das leere Minimum die Neuberechnung vorübergehend blockiert |
| T05 | Mobiler Reiterklick | PASS · Rohwert und Phys. Wert wechseln im mobilen Browser |
| T06 | Mobile Fokusbeendigung | PASS · das gemeinsame Eingabefeld ist nach dem Reiterklick nicht aktiv |
| T07 | Tastaturbedienung | PASS · Pfeil links/rechts, Pos1 und Ende bleiben implementiert; Fokus liegt auf dem gewählten Reiter |
| T08 | Rechenlogik | PASS · Rohwert-, Signal- und physikalische Vorgabe einschließlich negativem Messbereich wechselseitig geprüft |
| T09 | Diagnosegrenzen und Farben | PASS · Standard-S7- und NE43-Grenzfälle sowie Grün, Gelb/Orange, Rot und Cyan geprüft |
| T10 | iPhone-Hochformat | PASS · 390 × 844 px, kein horizontales Überlaufen, sticky Header und feste Schnellzugriffe |
| T11 | Smartphone-Querformat | PASS · 844 × 390 px, Safe-Area-/Viewport-Shell und feste untere Bedienzone |
| T12 | Tablet/Desktop | PASS · 820 × 1180 px und 1440 × 1050 px ohne Layoutregression |
| T13 | Alle Direktseiten | PASS · 15 Seiten auf Version, Header, Touchflächen und Überlauf geprüft |
| T14 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T15 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.5.1-beta`, Cache `sk-plt-tools-v2.1.5.1-Beta`, Precache und Offline-Direktaufrufe |
| T16 | Releaseintegrität | PASS · statische Validierung, vollständige interne SHA-256-Prüfsummen und ZIP-Integrität |

## Ausgeführte Befehle

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.5.1-Beta.zip
```

## Abnahme

- Die beiden gemeldeten Bedienprobleme sind im Reiter-Controller korrigiert und durch statische, funktionale und echte Browserprüfungen abgedeckt.
- Sämtliche unterstützten Module, Wissensinhalte, Navigation, Suche, Favoriten sowie PWA- und Offline-Funktionen bleiben erhalten.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
