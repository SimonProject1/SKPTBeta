### SK PLT Tools Beta 2.0.3.7-Beta.1

Vollstaendige Beta auf Basis von 2.0.3.6-Beta.1. Die stabile Referenz 2.0.2.0 bleibt unveraendert.

#### Neu in 2.0.3.7-Beta.1
- Sichtbare Versionsanzeigen im gesamten Projekt vereinheitlicht.
- Die Versionsnummer wird nur noch einmal gross im Hero-Bereich der Startseite angezeigt.
- Die kleine Versionsnummer unter dem Logo wurde entfernt.
- Die Versionsnummern in den Footern wurden entfernt.
- Einheitlicher Footer: „SK PLT Tools Beta · Entwickelt von Simon Kiesler“.
- Technische Versionsangaben fuer Release, Cache und PWA bleiben erhalten.

#### Aus 2.0.3.6-Beta.1 uebernommen
- Neuer Wissensbeitrag „Siemens SPS Rohwert Grundlagen“.
- Erklaerung von Rohwerten, Analogwerten und A/D-Wandlern.
- Erlaeuterung des Siemens-Standardbereichs 0 ... 27648.
- Getrennte Darstellung der Skalierungsmodelle fuer 4 ... 20 mA und 0 ... 20 mA.
- Uebersicht der Diagnosebereiche: Unterlauf, Untersteuerung, Nennbereich, Uebersteuerung und Ueberlauf.
- Vergleich von S7-300, S7-400, S7-1200 und S7-1500.
- Kartenuebersicht fuer ET 200SP, ET 200SP HA und F-AI.
- Praxisbeispiel zur Rohwertskalierung.
- Suchindex-Eintrag fuer den Wissensbeitrag.
- Verknuepfung zwischen Wissensdatenbank und Siemens-Rohwert-Rechner.

### Fachlicher Hinweis

Fuer ET 200SP HA AI 16xI HART sind die Parametrierungen „NE43 aus“ und „NE43 ein“ getrennt. Bei aktivierter Ausfallueberwachung beginnt der ungueltige Bereich laut der bestehenden Projektdokumentation bei 3,6 mA / Rohwert -691 und 21,0 mA / Rohwert 29376; die Hysteresegrenzen liegen bei 3,8 mA und 20,5 mA. Das S7-1500/ET 200MP F-AI-8xI-Profil bewertet bewusst keine unbestaetigten Diagnosegrenzen. Details und Quellen stehen in SIEMENS-QUELLEN-UND-GRENZWERTE.md.

### Unveraendert uebernommen

E+H Device Viewer, Rechner, Messstellen-Dokumentation, VDE-Plausibilitaetspruefung, Wissensdatenbank, Suche, Sortierung, Favoriten, Navigation und Offline-Betrieb wurden aus dem vorherigen Beta-Stand uebernommen.

### Installation und Test
- Das Paket in einen eigenen Beta-Webroot beziehungsweise Unterordner bereitstellen; die stabile Installation 2.0.2.0 nicht ueberschreiben.
- Den vollstaendigen Projektinhalt bereitstellen.
- Automatische Pruefungen im Projektordner starten:

```text
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 4173
python tools/browser-smoke-test.py
```

- Danach die manuelle Abnahme aus TESTBERICHT-UND-ABNAHME.md auf PC, iPhone und iPad durchfuehren.

2.0.3.7-Beta.1 · Beta · Entwickelt von Simon Kiesler
