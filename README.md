# SK PLT Tools Beta 2.0.3.2-Beta.2

Vollständige Beta auf Basis der vollständigen Version 2.0.3.2-Beta.1; die stabile Basis 2.0.2.0 bleibt unverändert.

## Neu in 2.0.3.2-Beta.2

- Startseitenkachel des Siemens-Rechners in `Siemens Rohwert` umbenannt.
- Schieberegler mit flüssigem, stufenlos interpoliertem Farbverlauf statt harter Farbblöcke; die Reglerfarbe folgt dem aktuellen Rohwert kontinuierlich.

- Überarbeiteter `Siemens-SPS-Analogwert-Rechner` ausschließlich für 4–20 mA, 0–20 mA, 0–10 V und 2–10 V.
- Direkte Umrechnung `Siemens-Rohwert → mA/V` und `mA/V → Siemens-Rohwert`.
- Vollständige Entfernung der frei definierbaren Messbereichs- und Einheitenkonfiguration aus diesem Rechner.
- Stufenlos bedienbarer, live gekoppelter Schieberegler über den INT16-Bereich −32.768…32.767.
- Deutlich getrennte Zustände: Unterlauf, Unterbereich, Nennbereich, Überbereich und Überlauf.
- Schnellwerte für alle Bereichsgrenzen sowie 0 %, 50 % und 100 % des Nennbereichs.
- Siemens-Nennskalierung 0…27.648 = 0…100 %; lineare Fortführung außerhalb des Nennbereichs.
- Responsive Bedienung für PC und Mobilgeräte sowie Tastaturbedienung des Reglers.

## Beta-Isolation

- Sichtbarer App-Name `SK PLT Tools Beta` und BETA-Kennzeichnung auf jeder Seite.
- Eigene PWA-ID und `start_url`: `./?app=sk-plt-tools-beta-2.0.3.2-beta.2`.
- Getrennter Service-Worker-Cache: `sk-plt-tools-beta-v2.0.3.2-Beta.2`.
- Die Aktivierung entfernt ausschließlich ältere Caches mit dem Präfix `sk-plt-tools-beta-`.
- Das stabile Paket `SK-PLT-Tools-V2.0.2.0.zip` bleibt unverändert.

## Erhalten

Design, Header, Footer, Startseite, Navigation, Favoriten, Suche, Sortierung, Wissensdatenbank, Mobilansicht, Offline-Betrieb, bestehende Rechner und Dokumentationsfunktionen wurden aus der vorhandenen Beta-Linie übernommen.

## Installation und Test

1. Das Paket in einen **eigenen Beta-Webroot bzw. Unterordner** entpacken; die stabile Installation 2.0.2.0 nicht überschreiben.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.2-Beta.2` bereitstellen.
3. Automatische Prüfungen im Projektordner starten:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 8080
```

4. Danach die Browser-Abnahme aus `TESTBERICHT-UND-ABNAHME.md` durchführen.

## Fachlicher Hinweis

Die Bereichsgrenzen bilden die im Rechner dokumentierte Siemens-Skalierung ab. Je nach Baugruppe, Kanalparametrierung und Diagnosekonfiguration können Diagnosegrenzen abweichen; für den Einsatz ist die jeweilige Siemens-Moduldokumentation maßgeblich.

2.0.3.2-Beta.2 · Beta · Entwickelt von Simon Kiesler
