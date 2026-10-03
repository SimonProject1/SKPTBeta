# SK PLT Tools Beta 2.0.4.0-Beta.1

Vollständiger, konsolidierter Beta-Safepoint. Die stabile Referenz 2.0.2.0 bleibt unverändert.

## Ziel dieses Stands

2.0.4.0-Beta.1 führt die zuletzt vorhandenen Teilstände wieder zu einem vollständigen, prüfbaren Projektpaket zusammen. Es wird bewusst keine neue Großfunktion begonnen.

## Enthalten

- Vollständige Funktionsbasis aus 2.0.3.5-Beta.2.
- Wissensbeitrag „Siemens SPS Rohwert Grundlagen“ aus 2.0.3.6-Beta.1.
- Bereinigte sichtbare Versionsanzeige aus 2.0.3.7-Beta.1: nur im Hero der Startseite sichtbar.
- Einheitlicher Footer: „SK PLT Tools Beta · Entwickelt von Simon Kiesler“.
- Getrennte und fachlich konsistente Darstellung der Skalierungsmodelle 4–20 mA und 0–20 mA.
- Vollständige Integration des Grundlagenartikels in Wissensdatenbank, Suche, Navigation und Offline-Cache.
- Einheitliche technische Version in `VERSION`, HTML, App, Manifest und Service Worker.

## Installation und Test

1. Das Paket in einen eigenen Beta-Webroot entpacken; die stabile Version 2.0.2.0 nicht überschreiben.
2. Im Projektordner ausführen:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

3. Danach die manuelle Geräteabnahme gemäß `TESTBERICHT-UND-ABNAHME.md` durchführen.
