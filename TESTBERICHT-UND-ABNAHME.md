# Testbericht und Abnahme – 2.1.1.0-Beta

**Prüfdatum:** 08.10.2026  
**Direkte Basis:** 2.1.0.5-Beta  
**Stabile Referenz:** 2.1.0.0  
**Gesamturteil:** **PASS – release-fähige Beta für die dokumentierte manuelle Messwert-Zweitkontrolle.** Keine elektrotechnische Zertifizierung oder Inbetriebnahmefreigabe.

## 1. Abnahmekriterien

| ID | Kriterium | Ergebnis |
|---|---|---:|
| A01 | Die automatische Foto-, PDF-, OCR- und Protokollanalyse ist aus der VDE-Laufzeit entfernt. | PASS |
| A02 | Formularidentität, Protokollaufbau, Unterschriften, Namen, Datum, Orte, Kreuze und sonstige formale Angaben beeinflussen die Bewertung nicht. | PASS |
| A03 | Sechs manuelle Masken decken Spannungsfall, Isolation, Schleifenimpedanz/Kurzschlussstrom, RCD, Niederohmigkeit und Schutzpotentialausgleich ab. | PASS |
| A04 | Bedingte Masken zeigen nur Eingaben, die für den gewählten Rechenweg erforderlich sind. | PASS |
| A05 | Keine Messgröße enthält einen numerisch vorbelegten Grenzwert. | PASS |
| A06 | Kontextabhängige Grenzwerte werden über Zusatzangaben oder einen freigegebenen Sollwert bereitgestellt. | PASS |
| A07 | Fehlende Angaben werden feldgenau benannt. | PASS |
| A08 | Ungültige Zahlen, negative Messwerte und mathematisch ungültige Grundlagen werden gezielt abgewiesen. | PASS |
| A09 | Bei fehlender oder ungültiger Berechnungsgrundlage bleibt die Ergebnisansicht gesperrt. | PASS |
| A10 | Vollständige Ergebnisse zeigen Grenzwert, Formel, eingesetzte Zahlen und `i. O.`/`nicht i. O.`. | PASS |
| A11 | Die Sicherheitsgrenze „digitale Zweitkontrolle, keine Inbetriebnahmefreigabe, kein Ersatz für die verantwortliche Elektrofachkraft“ bleibt sichtbar. | PASS |
| A12 | Alle übrigen Module, Projektstruktur, PWA, Navigation, Suche, Favoriten und Offline-Funktion bleiben erhalten. | PASS |

## 2. Implementierter Prüfbereich

Die manuelle Engine stellt genau sechs Messgrößengruppen bereit:

1. Spannungsfall – direkter Prozentvergleich oder Berechnung aus `ΔU / Un × 100`.
2. Isolationsmessung – kleinster Messwert gegen freigegebenen Mindestwert.
3. Schleifenimpedanz/Kurzschlussstrom – direkter `Zs,max`, Berechnung `Zs,max = U0 / Ia` oder `Ik ≥ Ia`.
4. RCD-Prüfung – Auslösezeit, Auslösestrom oder beide Größen gegen freigegebene Grenzen.
5. Niederohmigkeit – Messwert gegen freigegebenen Maximalwert.
6. Schutzpotentialausgleich – Messwert gegen freigegebenen Maximalwert.

Das Eingabeschema enthält keine Defaultwerte. Die Engine besitzt keine Texterkennung, Dokumentklassifikation, Bildverarbeitung, Feldlokalisierung oder formale Protokollfelder.

## 3. Automatisierte Testergebnisse

| ID | Prüfung | Ergebnis |
|---|---|---:|
| T01 | JavaScript-Funktions-Smoke aller bestehenden Rechner/Inhalte und der manuellen VDE-Engine | PASS · 94 Assertions |
| T02 | VDE-Regelmenge und sechs Messgrößen vollständig vorhanden | PASS |
| T03 | Automatische Eingänge Foto/PDF/OCR/Protokoll in Regeln und Laufzeit deaktiviert | PASS |
| T04 | Fehlende Eingabe erzeugt Zustand `incomplete`, gezielte Feldmeldung und kein Ergebnis | PASS |
| T05 | Ungültige Eingabe erzeugt Zustand `error` und kein Ergebnis | PASS |
| T06 | Grenzgleichheit aller Vergleiche wird inklusiv als `i. O.` bewertet | PASS |
| T07 | Über- beziehungsweise Unterschreitung aller Grenztypen wird als `nicht i. O.` bewertet | PASS |
| T08 | RCD-Kombiprüfung zeigt zwei Einzelrechnungen und korrekten Gesamtstatus | PASS |
| T09 | Formale Stördaten ändern ein identisches Messwertergebnis nicht | PASS |
| T10 | Manueller Browser-E2E: Fehlwertsperre, Positiv-, Negativ- und Kombifall | PASS |
| T11 | Browser-Smoke auf 16 Direktseiten | PASS |
| T12 | Responsive Desktop 1440 × 1050, Tablet 820 × 1180, Mobil 390 × 844 | PASS · kein horizontales Überlaufen |
| T13 | Manifest, App-ID, Service Worker, versionsisolierter Cache und Offline-Aufruf | PASS |
| T14 | Statische Release-Validierung: Struktur, lokale Referenzen, Syntax, Ausschlüsse und Governance | PASS |
| T15 | Vollständige interne SHA-256-Dateiliste | PASS |

## 4. Rechenweg- und Grenzfallmatrix

| Messgröße / Weg | Grenzfall i. O. | Abweichung erkannt | Fehler-/Fehlwertfall |
|---|---|---|---|
| Spannungsfall direkt | `3,00 % ≤ 3,00 %` | `3,01 % > 3,00 %` | fehlender Messwert → kein Ergebnis |
| Spannungsfall aus Volt | `8 V / 400 V × 100 = 2 %` bei Limit `2 %` | rechnerischer Prozentwert oberhalb Limit | `Un = 0 V` → Fehler, kein Ergebnis |
| Isolation | `1 MΩ ≥ 1 MΩ` | `0,99 MΩ < 1 MΩ` | fehlender Wert → kein Ergebnis |
| Zs gegen Sollwert | `2,5 Ω ≤ 2,5 Ω` | `2,51 Ω > 2,5 Ω` | fehlendes `Zs,max` → kein Ergebnis |
| Zs aus `U0 / Ia` | `230 V / 80 A = 2,875 Ω`; Messwert `2,875 Ω` | Messwert `2,876 Ω` | fehlendes/ungültiges `Ia` → kein Ergebnis |
| Kurzschlussstrom | `80 A ≥ 80 A` | `79,9 A < 80 A` | fehlendes `Ia` → kein Ergebnis |
| RCD-Auslösezeit | `300 ms ≤ 300 ms` | `301 ms > 300 ms` | fehlende Maximalzeit → kein Ergebnis |
| RCD-Auslösestrom | `15 mA` und `30 mA` liegen inklusiv in `15…30 mA` | `14,9 mA` bzw. `31 mA` außerhalb | Untergrenze größer Obergrenze → Fehler |
| Niederohmigkeit | `0,5 Ω ≤ 0,5 Ω` | `0,51 Ω > 0,5 Ω` | negativer Messwert → Fehler |
| Schutzpotentialausgleich | `0,2 Ω ≤ 0,2 Ω` | `0,21 Ω > 0,2 Ω` | nichtnumerische Eingabe → Fehler |

## 5. Browser-E2E-Nachweis

Der manuelle E2E-Test verwendet keine Dateien. Er prüft ausschließlich sichtbare Bedienelemente und Eingaben:

- exakt sechs Messgrößen im Prüfstand,
- kein `input[type=file]`, kein Upload-, Analyse- oder Vorschaupanel,
- feldgenaue Meldung bei fehlendem Spannungsfall,
- gesperrtes Ergebnis vor Vervollständigung,
- sichtbarer Grenzwert, Formel und Rechenweg im bestandenen Grenzfall,
- sichtbarer `nicht i. O.`-Status bei vollständiger Isolationsabweichung,
- gezielte `Ia`-Abfrage und danach berechnetes `Zs,max = 2,875 Ω`,
- RCD-Kombiprüfung mit einem bestandenen und einem nicht bestandenen Einzelcheck,
- mobile Bedienung und kein horizontales Überlaufen.

Die finalen Ansichten sind in `test-artifacts/vde-messwertpruefer-desktop.png` und `test-artifacts/vde-messwertpruefer-mobile.png` dokumentiert.

## 6. Vollständigkeit und Release-Integrität

- 16 HTML-Direktseiten wurden geprüft.
- Alle bestehenden Rechner, Wissensseiten, Navigation, Suche, Favoriten und externen Integrationen blieben erhalten.
- Version `2.1.1.0-Beta` ist in `VERSION`, HTML-Attributen, App-Laufzeit, Manifest, Navigation, Service Worker, VDE-Modulen, Tests, Dokumentation und Release-Konfiguration konsistent.
- PWA-App-ID und Start-URL lauten `./?app=sk-plt-tools-2.1.1.0-beta`.
- Der Cache lautet `sk-plt-tools-v2.1.1.0-Beta`; ältere SK-PLT-Tools-Caches werden bei Aktivierung entfernt.
- Das neue Eingabeschema und die VDE-Regeln sind im Offline-Precache enthalten.
- Das entfernte VDE-Lokalisierungsprofil und die alte Automatikdokumentation sind nicht mehr Bestandteil des Releases.
- Die vollständige Prüfsummenliste wird unmittelbar vor dem finalen ZIP-Build neu erzeugt und danach erneut validiert.

## 7. Restrisiken und fachliche Grenzen

- Die Anwendung kann nicht prüfen, ob ein manuell eingegebener Sollwert fachlich korrekt freigegeben wurde.
- Netzform, Abschaltzeit, RCD-Typ, Prüfstromfaktor, Prüfspannung, Stromkreisart und Schutzmaßnahme werden nicht automatisch interpretiert.
- Ein rechnerisch bestandenes Einzelergebnis bestätigt weder die vollständige Prüfung noch den ordnungsgemäßen Zustand der Anlage.
- Messdurchführung, Auswahl des anwendbaren Grenzwerts, Gesamtbewertung und Freigabe verbleiben bei der verantwortlichen Elektrofachkraft.

## 8. Abnahme

Die geforderten Änderungen sind im geprüften Stand umgesetzt. **SK PLT Tools 2.1.1.0-Beta** ist als release-fähige Beta für kontrollierte Anwender- und Feldtests des manuellen VDE-Messwertprüfers freigegeben. Eine produktive elektrotechnische Freigabe wird ausdrücklich nicht erteilt.
