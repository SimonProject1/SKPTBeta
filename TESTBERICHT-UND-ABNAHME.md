# Testbericht und Abnahme – SK PLT Tools 2.1.2.1-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.2.0-Beta  
**Stabile Referenz:** 2.1.0.0  
**Prüfumfang:** vollständiges Projekt, Schwerpunkt Siemens-Rohwert-Rechner

## Gesamtergebnis

**PASS – die Beta erfüllt den dokumentierten Funktionsumfang und ist als vollständiges ZIP auslieferbar.**

## Fachliche Umrechnung

Die physikalische Skalierung verwendet den Siemens-Nennbereich 0…27.648 als 0…100 %:

- `Prozent = Rohwert / 27.648 × 100`
- `Signal = Signal-Minimum + Prozent / 100 × (Signal-Maximum − Signal-Minimum)`
- `Istwert = Messbereich-Minimum + Prozent / 100 × (Messbereich-Maximum − Messbereich-Minimum)`
- die Rückrechnungen aus Signalwert und Istwert verwenden dieselbe lineare Beziehung; der ausgegebene Siemens-Rohwert wird auf eine ganze Zahl gerundet.

## Geprüfte Referenzfälle

| ID | Eingabe und Konfiguration | Erwartetes Ergebnis | Ergebnis |
|---|---|---|---|
| R01 | Rohwert 13.824; 4–20 mA; −50…150 °C | 12,000 mA; 50,0 %; 50,000 °C | PASS |
| R02 | Signal 8,000 mA; 4–20 mA; −50…150 °C | Rohwert 6.912; 25,0 %; 0,000 °C | PASS |
| R03 | Istwert 0,000 °C; 4–20 mA; −50…150 °C | Rohwert 6.912; 8,000 mA; 25,0 % | PASS |
| R04 | Rohwert 27.648; −1…9 bar | 100,0 %; 9,000 bar; freie Einheit übernommen | PASS |
| R05 | Rohwert −4.864; 4–20 mA; −50…150 °C | Unterbereich; ca. 1,185 mA; −17,5926 %; −85,185 °C | PASS |
| R06 | Rohwert 27.649; 4–20 mA; −50…150 °C | Überbereich; ca. 20,001 mA; 100,0036 %; 150,007 °C | PASS |
| R07 | Minimum = Maximum | verständliche Validierungsfehlermeldung | PASS |
| R08 | leere Einheit | verständliche Validierungsfehlermeldung | PASS |
| R09 | 0–20 mA sowie 2–10 V | bestehende Hin- und Rückrechnung unverändert | PASS |
| R10 | ET-200SP- und ET-200SP-HA-Grenzen | Unterlauf, Unterbereich, Nennbereich, Überbereich und Überlauf unverändert | PASS |

## Technische Prüfungen

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | Versionskonsistenz | PASS · 2.1.2.1-Beta in VERSION, allen 15 HTML-Seiten, Manifest, Navigation, App-Laufzeit, Service Worker und Release-Konfiguration |
| T02 | PWA/Cache/Manifest | PASS · eindeutige App-ID `sk-plt-tools-2.1.2.1-beta`, isolierter Cache `sk-plt-tools-v2.1.2.1-Beta`, vollständiger Precache |
| T03 | Statische Release-Validierung | PASS · 15 Direktseiten, lokale Referenzen, JavaScript-Syntax, Modulbestand und SHA-256-Liste fehlerfrei |
| T04 | Funktions-Smoke-Test | PASS · alle Rechnerregressionen, drei Siemens-Eingaberichtungen, negative Grenzen, freie Einheiten, Unter- und Überbereich |
| T05 | Browser-Smoke-Test | PASS · Desktop 1440 px, Tablet 820 px, Mobil 390 px, kein horizontales Überlaufen |
| T06 | PWA-/Offline-Test | PASS · Service Worker aktiv, Release-Cache vorhanden, Siemens-Rechner und Werkstoffmodul offline direkt aufrufbar |
| T07 | Navigation und übrige Module | PASS · neun Startseitenkacheln, fünf Wissenskacheln, Suche, Filter, Sortierung, Favoriten und Navigation |
| T08 | ZIP-Integrität | PASS · vollständiger Projektstamm, fehlerfrei prüf- und entpackbar |

## Verwendete automatisierte Prüfungen

```bash
node tools/functional-smoke-test.js
python3 tools/release.py --checksums
python3 tools/validate_release.py
PLAYWRIGHT_CHROMIUM_EXECUTABLE=/opt/pw-browsers/chromium-1208/chrome-linux64/chrome python3 tools/browser-smoke-test.py
unzip -t SK-PLT-Tools-V2.1.2.1-Beta.zip
sha256sum -c SHA256SUMS.txt
```

## Abnahme

- Die vollständige Projektstruktur der V2.1.2.0-Beta ist erhalten.
- Die Erweiterung ist auf den Siemens-Rohwert-Rechner, dessen Tests und die erforderlichen Release-/Dokumentationseinträge begrenzt.
- Physikalische Werte werden im bestätigten Unter- und Überbereich linear extrapoliert; kartenspezifische Diagnosegrenzen bleiben maßgeblich.
- Die Einheit ist frei wählbarer Anzeigetext und führt keine Einheitenumrechnung aus.

**Abnahmestatus: PASS.**
