# Testbericht und Abnahme – SK PLT Tools 2.1.5.2-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.5.1-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** ±-Vorzeichenwechsel am aktiven Siemens-Eingabefeld und an beiden physikalischen Messbereichsgrenzen, sofortige Berechnung, iPhone-Fokus-/Tastaturverhalten, Gesamtregression, PWA/Offline und Releaseintegrität

## Gesamtergebnis

**PASS – der ±-Vorzeichenwechsel ist an Signal, Rohwert, Phys. Wert, Minimum und Maximum verfügbar. Gültige Zahlen wechseln zuverlässig das Vorzeichen, die Berechnung wird sofort aktualisiert und der ±-Touch fokussiert auf dem iPhone-Profil kein Zahlenfeld.**

## Umsetzung

- Das gemeinsame Feld `#inputValue` besitzt eine feste ±-Schaltfläche, deren zugängliche Beschriftung dem aktiven Reiter folgt.
- `#physicalMin` und `#physicalMax` besitzen jeweils eine eigene ±-Schaltfläche.
- Die reine Funktion `toggleSignValue` akzeptiert positive, negative, Null- und Dezimalkommawerte und weist leere oder ungültige Werte ab.
- Nach einem erfolgreichen Wechsel werden `input` und `change` ausgelöst; damit laufen dieselben validierten Berechnungswege wie bei einer manuellen Eingabe.
- Alle ±-Schaltflächen sind `type="button"`, liegen außerhalb von Labels und verhindern bei `pointerdown` den Eingabefokus. Ein vorhandener Formularfokus wird beendet.
- Die Reiter-Fokuskorrektur aus V2.1.5.1-Beta bleibt unverändert aktiv.

## Automatisierte Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.5.2-Beta in VERSION, 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker, Tests und Release-Konfiguration |
| T02 | Vorzeichen Signal | PASS · 12 mA → −12 mA → 12 mA; Rohwert und physikalischer Wert werden sofort neu berechnet |
| T03 | Vorzeichen Rohwert/Phys. Wert | PASS · derselbe gemeinsame ±-Button bleibt in allen drei aktiven Reitern wirksam und korrekt beschriftet |
| T04 | Vorzeichen Minimum | PASS · −50 → 50 → −50; der physikalische Istwert folgt sofort |
| T05 | Vorzeichen Maximum | PASS · 150 → −150 erzeugt unmittelbar die Messbereichsvalidierung; Rückwechsel auf 150 stellt die Berechnung wieder her |
| T06 | Positive/negative Werte | PASS · 12 → −12 und −12 → 12 funktional geprüft |
| T07 | Dezimalkomma/Null | PASS · 12,5 → −12,5; 0 bleibt 0 |
| T08 | Ungültige Eingabe | PASS · leere Eingabe wird mit gültiger Fehlermeldung abgewiesen und nicht ersetzt |
| T09 | Desktop ohne Eingabefokus | PASS · kein Zahlenfeld erhält durch einen ±-Klick Fokus |
| T10 | iPhone-Touch ohne Eingabefokus | PASS · Touchprofil 390 × 844; ± per `tap`, Fokuszähler bleibt 0 und das Zahlenfeld inaktiv |
| T11 | Reiterregression | PASS · Signal, Rohwert und Phys. Wert wechseln weiterhin ohne automatischen Fokus |
| T12 | Rechenlogik | PASS · Rohwert-, Signal- und physikalische Vorgabe einschließlich negativem Messbereich wechselseitig geprüft |
| T13 | Diagnosegrenzen und Farben | PASS · Standard-S7- und NE43-Grenzfälle sowie Grün, Gelb/Orange, Rot und Cyan geprüft |
| T14 | Responsive Layouts | PASS · 1440 × 1050, 820 × 1180, 390 × 844 und 844 × 390 ohne horizontale Layoutregression |
| T15 | Alle Direktseiten | PASS · 15 Seiten auf Version, Header, Touchflächen und Überlauf geprüft |
| T16 | Navigation/Favoriten | PASS · Öffnen, Schließen, Persistenz, Entfernen und Baummenüstruktur funktionieren |
| T17 | PWA/Offline | PASS · App-ID `sk-plt-tools-2.1.5.2-beta`, Cache `sk-plt-tools-v2.1.5.2-Beta`, Precache und Offline-Direktaufrufe |
| T18 | Releaseintegrität | PASS · statische Validierung, vollständige interne SHA-256-Prüfsummen und ZIP-Integrität |

## Ausgeführte Befehle

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
python3 -m http.server 4173 --bind 127.0.0.1
PLAYWRIGHT_CHROMIUM_EXECUTABLE=<chromium> python3 tools/browser-smoke-test.py
sha256sum -c SHA256SUMS.txt
unzip -t SK-PLT-Tools-V2.1.5.2-Beta.zip
```

## Abnahme

- Die geforderten fünf Anwendungsfälle (aktives Signal-/Rohwert-/Phys.-Feld sowie Minimum und Maximum) sind umgesetzt.
- Unmittelbare Berechnung und iPhone-sichere Fokusbehandlung sind funktional, statisch und im echten Browserprofil abgesichert.
- Sämtliche unterstützten Module, Wissensinhalte, Navigation, Suche, Favoriten sowie PWA- und Offline-Funktionen bleiben erhalten.
- Das Release enthält keine personenbezogenen Testdaten.

**Abnahmestatus: PASS.**
