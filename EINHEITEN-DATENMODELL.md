# Einheitendatenmodell – SK PLT Tools 2.1.7.2-Beta

## Zweck

`assets/units.json` ist die verbindliche Single Source of Truth für alle Einheiten. Rechner dürfen Umrechnungsfaktoren und Temperatur-Offsets nicht parallel pflegen.

## Schema

- `schemaVersion`: Version des JSON-Schemas.
- `release`: technischer Release-Stand.
- `conversionModel`: gemeinsame Formeln, Roundtrip-Toleranz und Favoritenschlüssel.
- `categories[]`: 19 physikalische Kategorien.
  - `id`: stabiler technischer Kategoriename.
  - `name`: deutsche Anzeige.
  - `defaultUnit`: unveränderliche Standardeinheit der Kategorie.
  - `calculatorTargetUnit`: sinnvolle zweite Einheit im Einheitenrechner.
  - `description`: fachliche Einordnung.
  - `units[]`: Einheiten der Kategorie.
- `units[]`:
  - `id`: stabiler technischer Einheitenname.
  - `name`, `symbol`, `aliases`: Anzeige und Suche.
  - `toBase.factor`, `toBase.offset`: Umrechnung in die Kategorie-Basiseinheit.
  - `precision`: empfohlene Anzeigegenauigkeit.
  - `note`: optionale Formel- oder Konventionsangabe.
- `validationCases[]`: verbindliche Referenzumrechnungen.

## Umrechnungsmodell

```text
Basiswert = Eingabewert × Faktor + Offset
Ausgabewert = (Basiswert − Offset) ÷ Faktor
```

Dieses affine Modell deckt lineare Einheiten und Einheiten mit Offset ab. Beispiele:

- °C → K: zunächst °C als Basis; K verwendet Faktor 1 und Offset −273,15.
- °F → °C: Faktor 5/9 und Offset −160/9.
- bar → mbar: 1 bar = 1.000 mbar.

## Standardeinheiten

Verbindliche Standards sind unter anderem Druck `bar`, Temperatur `°C`, Volumenstrom `m³/h`, Länge `m`, Spannung `V`, Strom `A` und Widerstand `Ω`. Rechner dürfen für einen konkreten Anwendungsfall eine bevorzugte Anfangseinheit wie `mA` oder `mm²` wählen; die feste Kategoriestandardeinheit bleibt im Dropdown immer sichtbar.

## Favoriten

Einheitenfavoriten werden ausschließlich lokal im Browser gespeichert:

```text
Schlüssel: skPltUnitFavoritesV1
Wert: JSON-Array aus "categoryId:unitId"
```

Die Daten verlassen den Browser nicht. Dropdowns werden bei Änderungen aktualisiert und behalten ihre gültige Auswahl.

## Erweiterungsregeln

1. Keine doppelte Kategorie-ID oder doppelte Einheiten-ID innerhalb einer Kategorie.
2. Genau eine gültige `defaultUnit` je Kategorie.
3. Faktor ungleich null; Faktor und Offset müssen endlich sein.
4. Physikalisch unterschiedliche Dimensionen nicht in einer Kategorie mischen. Deshalb enthält „Viskosität“ ausschließlich dynamische Viskosität; kinematische Viskosität wäre eine eigene Kategorie.
5. Neue Faktoren mit Referenzfall ergänzen.
6. Roundtrip-Test, Browsertest, Precache, Suchindex und Dokumentation aktualisieren.
