# Siemens-Quellen und kartenspezifische Rohwertgrenzen

Stand: 06.10.2026 · Bestandteil von SK PLT Tools 2.1.6.1-Beta

## Grundsatz

Der Rechner verwendet nur Grenzwerte, die in den unten genannten Siemens-Unterlagen eindeutig kartenspezifisch und für die jeweilige Parametrierung beschrieben sind. Die lineare Nennskalierung ist 0…27.648. Diagnose, Wertstatus und Ersatzwertverhalten der realen Baugruppe haben Vorrang vor dieser Rechenhilfe.

## Freigegebene Profile

### 1. ET 200SP · AI 4xI 2-/4-wire ST

- Artikelnummer: **6ES7134-6GD01-0BA1**
- Messbereich **4…20 mA**:
  - Unterlauf: **−32.768…−4.865**; Beginn beim Unterschreiten von **−4.864** beziehungsweise unter **1,185 mA**.
  - Untersteuerungsbereich: **−4.864…−1**.
  - Nennbereich: **0…27.648**.
  - Übersteuerungsbereich: **27.649…32.511**.
  - Überlauf: **32.512…32.767**; Beginn oberhalb von **32.511** beziehungsweise oberhalb von **22,81 mA**.
- Messbereich **0…20 mA**, Parametrierung **2-Draht-Messumformer**: Negative Werte sind laut Siemens nicht möglich; deshalb gibt es hier keinen Untersteuerungs- oder Unterlaufbereich. Oberer Nenn-, Übersteuerungs- und Überlaufbereich entsprechen der Siemens-Tabelle.
- Quelle: Siemens, *Analog Input Module AI 4xI 2-/4-wire ST (6ES7134-6GD01-0BA1)*, Kapitel „Representation of analog values in the current measuring ranges“, Dokument-ID 59768161: https://support.industry.siemens.com/cs/mdm/59768161?c=65190275851&lc=en-US

### 2. ET 200SP HA · AI 16xI 2-wire HART HA

- Artikelnummer: **6DL1134-6TH00-0PH1**
- Messbereiche im Profil: **0…20 mA** und **4…20 mA / 4…20 mA HART**.

#### Parametrierung „Ausfallüberwachung nach NE43“ deaktiviert

Für 4…20 mA gelten die systemischen S7-Grenzen:

- Unterlauf beginnt bei **−4.865** bzw. unter **1,185 mA**.
- Untersteuerungsbereich: **−4.864…−1**.
- Nennbereich: **0…27.648**.
- Übersteuerungsbereich: **27.649…32.511**.
- Überlauf beginnt bei **32.512** bzw. oberhalb **22,81 mA**.

#### Parametrierung „Ausfallüberwachung nach NE43“ aktiviert (Firmware ab V1.1)

Die Modulüberwachung arbeitet mit Hysterese:

- Unterlauf / ungültig ab **3,6 mA**, Tabellenwert **0xFD4D = −691**.
- Wieder gültig erst oberhalb **3,8 mA**, Tabellenwert **0xFEA6 = −346**; der Zwischenbereich wird im Rechner gelb als Hysteresebereich angezeigt.
- Überlauf / ungültig ab **21,0 mA**, Tabellenwert **0x72C0 = 29.376**.
- Wieder gültig erst unterhalb **20,5 mA**, Tabellenwert **0x6F60 = 28.512**; der Zwischenbereich wird im Rechner gelb als Hysteresebereich angezeigt.

Quelle: Siemens, *AI 16xI 2-wire HART HA, 6DL1134-6TH00-0PH1*, Gerätehandbuch 09/2021, A5E39408995-AD, Kapitel 5.4.13 sowie Tabellen C-3 und C-4. Offizielle Dokumentseite: https://support.industry.siemens.com/cs/document/109770922/

### 3. S7-1500 / ET 200MP · F-AI 8xI 0(4)..20mA

- Artikelnummer: **6ES7536-1MF00-0AB0**.
- Das offizielle Gerätehandbuch bestätigt die Messbereiche **0…20 mA** und **4…20 mA**, jeweils 16 Bit inklusive Vorzeichen, und verweist für Überlauf/Unterlauf auf den Anhang „Representation of analog values“.
- In dieser Release-Version ist dieses Profil deshalb bewusst auf die bestätigte Nennskalierung **0…27.648** begrenzt. Es werden **keine** kartenspezifischen Unterlauf-/Überlaufgrenzen behauptet oder farblich bewertet.
- Quelle: Siemens, *Analog Input Module F-AI 8xI 0(4)..20mA (6ES7536-1MF00-0AB0)*, Gerätehandbuch 09/2024, A5E51970360-AC, Dokument-ID 109823702: https://support.industry.siemens.com/cs/document/109823702/

## Wichtige Abweichung: NE 43 (Ausgabe 2021)

Siemens weist darauf hin, dass für die meisten SIMATIC-Komponenten die systemischen Ausfallgrenzen **unter 1,185 mA** und **über 22,81 mA** ohne besondere Einstellung gelten. Bei **ET 200SP HA**, **ET 200SP** und **CFU CIO HART** soll die modulintern als „Ausfallüberwachung nach NE43“ bezeichnete Funktion für die Umsetzung der überarbeiteten NE 43 (2021) deaktiviert werden, weil sie noch auf der alten NE 43 (2003) basiert. Die aktuelle Anlagen- und Bausteinparametrierung ist daher zwingend zu prüfen.

Quelle: Siemens Industry Online Support, *Introduction of a safety margin for signal detection in control systems in accordance with NE43 (2021 edition)*, Beitrags-ID 109971742: https://support.industry.siemens.com/cs/document/109971742/

## Nicht als Kartenfreigabe verwenden

Die Option **„Generische Umrechnung · ohne Kartenfreigabe“** führt ausschließlich die lineare Umrechnung zwischen Signal und 0…27.648 aus. Sie enthält bewusst keine Diagnosegrenzen. Für eine weitere Siemens-Karte darf erst nach Prüfung von Artikelnummer, Firmware, Messart, Messbereich, Geberanschluss und Diagnoseparametrierung ein eigenes Profil ergänzt werden.


## Physikalische Skalierung

Der frei eingebbare physikalische Messbereich ist eine lineare Anwenderskalierung und verändert keine kartenspezifische Diagnosegrenze. Es gelten:

- `Prozent = Rohwert / 27.648 × 100`
- `Istwert = Minimum + Prozent / 100 × (Maximum − Minimum)`
- `Rohwert = (Istwert − Minimum) / (Maximum − Minimum) × 27.648`

Minimum und Maximum dürfen negativ sein; das Maximum muss größer als das Minimum sein. Werte im bestätigten Unter- oder Überbereich werden linear extrapoliert. Die frei eingegebene Einheit dient ausschließlich der Anzeige und wird nicht physikalisch umgerechnet.
