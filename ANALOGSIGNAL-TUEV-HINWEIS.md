# Analogsignal-Rechner – TÜV-Praxishinweis V2.6.5.2-Beta

## Zweck

Der Analogsignal-Rechner unterstützt die schnelle lineare Skalierungsprüfung bei
TÜV-Abnahmen und Funktionskontrollen.

## Benötigte Angaben

1. **Messbereichsanfang (MA)**
2. **Messbereichsende (ME)**
3. **Signalart / Signalbereich**: 4–20 mA, 0–20 mA, 0–10 V oder 2–10 V
4. **Umrechnungsrichtung** und der zu prüfende Eingabewert

MA, ME und der daraus berechnete Skalierungswert werden im Rechner bewusst
**einheitenlos** behandelt. Die fachliche Einheit – zum Beispiel bar, °C, l/h oder % –
ergibt sich ausschließlich aus dem am Gerät, Prüfmittel oder Prüfprotokoll festgelegten
Messbereich und wird nicht im Rechner ausgewählt oder gespeichert.

## Berechnung

Für Skalierungswert → Signal gilt unverändert die lineare Abbildung:

`Signal = Signalmin + (Wert − MA) / (ME − MA) × (Signalmax − Signalmin)`

Für Signal → Skalierungswert wird dieselbe Beziehung umgekehrt:

`Wert = MA + (Signal − Signalmin) / (Signalmax − Signalmin) × (ME − MA)`

Der Messbereichsanteil wird in Prozent ausgegeben. Werte außerhalb des Nennbereichs
werden weiterhin linear extrapoliert; der Rechner begrenzt sie nicht künstlich.

## Bedienhinweise

- MA und ME müssen unterschiedlich sein.
- Negative und über null liegende Messbereiche sind zulässig.
- Dezimalwerte können über die Zahleneingabe erfasst werden; der ±-Taster wechselt
  das Vorzeichen touchfreundlich.
- „Zurücksetzen“ stellt 0…100 und 4–20 mA wieder her.
- Ergebnis und Messbereichsanteil können über die Kopierbuttons übernommen werden.
- Die App funktioniert nach erfolgreichem Precache auch offline.

## Abgrenzung

Der Rechner ersetzt nicht die Festlegung oder Prüfung der fachlichen Einheit, der
Geräteparametrierung, der zulässigen Toleranz, der Messunsicherheit oder der
Anlagenfreigabe. Diese Angaben bleiben Bestandteil der jeweiligen TÜV-Unterlage,
Messstellenbeschreibung und Arbeitsanweisung.
