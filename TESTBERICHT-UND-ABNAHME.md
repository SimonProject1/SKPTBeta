# Testbericht und Abnahme – 2.1.2.0-Beta

**Prüfdatum:** 09.10.2026  
**Direkte Basis:** 2.1.1.0-Beta  
**Stabile Referenz:** 2.1.0.0

## Ergebnis

**PASS – release-fähige Beta für den dokumentierten Funktionsumfang.**

## Prüfergebnisse

| ID | Prüfung | Ergebnis |
|---|---|---|
| T01 | ZIP-Integrität | PASS · Archiv vollständig und fehlerfrei entpackbar |
| T02 | Versionskonsistenz | PASS · Version in HTML, Manifest, App-Laufzeit, Service Worker und Release-Konfiguration identisch |
| T03 | Statische Release-Validierung | PASS · 15 Direktseiten, lokale Referenzen, JavaScript-Syntax und Prüfsummen fehlerfrei |
| T04 | Funktions-Smoke-Test | PASS · Rechner, Werkstoffsuche, Wissensseiten, Favoriten und externe Verknüpfung fehlerfrei |
| T05 | Browser-Smoke-Test | PASS · Desktop, Tablet, Mobil, Navigation, Suche, Filter, Favoriten, PWA und Offline-Aufrufe fehlerfrei |
| T06 | Paketbereinigung | PASS · Keine veralteten Modulpfade, Modultexte oder dedizierten Laufzeit-/Testdateien im Paket |

## Abnahmekriterien

- neun sichtbare Startseitenkacheln,
- 15 direkt aufrufbare Seiten einschließlich Startseite,
- sechs Rechnerkacheln,
- fünf Wissenskacheln,
- zehn Werkstoffdatensätze,
- eindeutige Release-ID und isolierter Offline-Cache,
- vollständige SHA-256-Liste,
- keine fehlenden lokalen Referenzen oder JavaScript-Syntaxfehler.

Die Prüfergebnisse werden durch die mitgelieferten automatisierten Tests und `SHA256SUMS.txt` reproduzierbar nachgewiesen.
