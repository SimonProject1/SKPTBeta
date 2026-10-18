# Analogsignal-Rechner – Praxishinweis V2.6.5.4-Beta

## Zweck

Der Rechner bildet einen einheitenlosen Messbereich linear auf einen der
unterstützten Standardsignalbereiche ab oder führt die Umkehrrechnung aus.

## Eingaben

- Messbereichsanfang MA
- Messbereichsende ME
- Signalart: 4–20 mA, 0–20 mA, 0–10 V oder 2–10 V
- Umrechnungsrichtung
- Skalierungs- beziehungsweise Signalwert

MA, ME und der berechnete Skalierungswert sind bewusst einheitenlos. Die fachliche
Einheit ergibt sich aus dem Messbereich des jeweiligen Geräts oder Prüfmittels.

## Berechnung

Skalierungswert → Signal:

`Signal = Signal_min + (Wert - MA) / (ME - MA) × (Signal_max - Signal_min)`

Signal → Skalierungswert:

`Wert = MA + (Signal - Signal_min) / (Signal_max - Signal_min) × (ME - MA)`

Der Messbereichsanteil wird in Prozent ausgegeben. Werte außerhalb des Messbereichs
werden entsprechend der bisherigen fachlichen Logik linear extrapoliert. MA und ME
müssen unterschiedlich sein; unvollständige oder ungültige Zahlen werden gemeldet.

## Bedienung ab V2.6.5.4-Beta

- Jede Änderung an Eingaben oder Auswahlen aktualisiert das Ergebnis unmittelbar.
- Ein separater Berechnen-Schritt ist nicht erforderlich.
- Es gibt im Analogsignal-Rechner keinen sichtbaren Zurücksetzen-Button.
- Ergebniswerte besitzen bewusst keine Kopierbuttons oder versteckten Kopierflächen.
- Die ±-Taster wechseln das Vorzeichen touch- und tastaturfreundlich.
- Fehlermeldungen und Ergebnisse werden über Live-Regionen ausgegeben.
- Die App funktioniert nach erfolgreichem Precache auch offline.
