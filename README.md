# SK PLT Tools Beta 2.0.3.3-Beta.1

Vollständige Beta auf Basis der zuletzt erstellten vollständigen Version 2.0.3.2-Beta.2; die stabile Basis 2.0.2.0 bleibt unverändert.

## Neu in 2.0.3.3-Beta.1

- Große Seitenüberschrift des Siemens-Rechners exakt auf `Siemens Rohwert` geändert.
- Richtungsabhängige Reglerskala: Bei `Signal → Siemens-Rohwert` zeigt der Regler den gewählten Bereich 4–20 mA, 0–20 mA, 0–10 V oder 2–10 V einschließlich Einheit.
- Bei `Siemens-Rohwert → Signal` bleibt die vollständige Rohwertskala −32.768…32.767 sichtbar.
- Das große transparente INT/TNT-Hintergrundelement im Konfigurationsbereich wurde vollständig entfernt.
- Die bisherige bidirektionale Umrechnung, Diagnosezustände, Schnellwerte und kontinuierliche Reglerfarbe bleiben erhalten.
- Responsive Bedienung für PC und Mobilgeräte sowie Tastaturbedienung des Reglers bleiben erhalten.

## Beta-Isolation

- Sichtbarer App-Name `SK PLT Tools Beta` und BETA-Kennzeichnung auf jeder Seite.
- Eigene PWA-ID und `start_url`: `./?app=sk-plt-tools-beta-2.0.3.3-beta.1`.
- Getrennter Service-Worker-Cache: `sk-plt-tools-beta-v2.0.3.3-Beta.1`.
- Die Aktivierung entfernt ausschließlich ältere Caches mit dem Präfix `sk-plt-tools-beta-`.
- Das stabile Paket `SK-PLT-Tools-V2.0.2.0.zip` bleibt unverändert.

## Erhalten

Design, Header, Footer, Startseite, Navigation, Favoriten, Suche, Sortierung, Wissensdatenbank, Mobilansicht, Offline-Betrieb, bestehende Rechner und Dokumentationsfunktionen wurden aus der vorhandenen Beta-Linie übernommen.

## Installation und Test

1. Das Paket in einen **eigenen Beta-Webroot bzw. Unterordner** entpacken; die stabile Installation 2.0.2.0 nicht überschreiben.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.3-Beta.1` bereitstellen.
3. Automatische Prüfungen im Projektordner starten:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 8080
```

4. Danach die Browser-Abnahme aus `TESTBERICHT-UND-ABNAHME.md` durchführen.

## Fachlicher Hinweis

Die Bereichsgrenzen bilden die im Rechner dokumentierte Siemens-Skalierung ab. Je nach Baugruppe, Kanalparametrierung und Diagnosekonfiguration können Diagnosegrenzen abweichen; für den Einsatz ist die jeweilige Siemens-Moduldokumentation maßgeblich.

2.0.3.3-Beta.1 · Beta · Entwickelt von Simon Kiesler
