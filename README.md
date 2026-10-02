## SK PLT Tools Beta 2.0.3.6-Beta.1

Vollständige Beta auf Basis des vollständigen Projektpakets 2.0.3.5-Beta.1. Die stabile Referenz 2.0.2.0 bleibt unverändert.

### Neu in 2.0.3.6-Beta.1
 
- Neuer Wissensbeitrag „Siemens SPS Rohwert Grundlagen“
- Erklärung von Rohwerten, Analogwerten und A/D-Wandlern
- Erläuterung des Siemens-Standardbereichs 0…27648
- Erklärung der Rohwerte bei 4…20 mA
- Übersicht der Diagnosebereiche (Unterlauf, Untersteuerung, Übersteuerung, Überlauf)
- Vergleich S7-300, S7-400, S7-1200 und S7-1500
- Kartenübersicht ET200SP, ET200SP HA und F-AI
- Praxisbeispiel zur Rohwertskalierung
- Neuer Suchindex-Eintrag für den Wissensbeitrag
- Neue Verknüpfung zwischen Wissensdatenbank und Rohwert-Rechner

## Fachlicher Hinweis

Für **ET 200SP HA AI 16xI HART** sind die Parametrierungen „NE43 aus“ und „NE43 ein“ getrennt. Bei aktivierter Ausfallüberwachung beginnt der ungültige Bereich laut Siemens bei **3,6 mA / Rohwert −691** und **21,0 mA / Rohwert 29.376**; die Hysteresegrenzen liegen bei 3,8 mA und 20,5 mA. Das **S7-1500/ET 200MP F-AI-8xI-Profil** bewertet bewusst keine unbestätigten Diagnosegrenzen. Details und offizielle Quellen stehen in `SIEMENS-QUELLEN-UND-GRENZWERTE.md`.

## Unverändert übernommen

E+H Device Viewer, alle weiteren Rechner, Messstellen-Dokumentation, VDE-Plausibilitätsprüfung, Wissensdatenbank, Suche, Sortierung, Favoriten, Navigation und Offline-Betrieb wurden aus 2.0.3.5-Beta.1 übernommen.

## Installation und Test

1. Das Paket in einen eigenen Beta-Webroot bzw. Unterordner entpacken; die stabile Installation 2.0.2.0 nicht überschreiben.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.5-Beta.2` bereitstellen.
3. Automatische Prüfungen im Projektordner starten:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

4. Danach die manuelle Abnahme aus `TESTBERICHT-UND-ABNAHME.md` auf PC und iPhone/iPad durchführen.

2.0.3.5-Beta.2 · Beta · Entwickelt von Simon Kiesler
