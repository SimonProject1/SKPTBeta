# Testbericht und Abnahme – 2.1.0.5-Beta

**Prüfdatum:** 07.10.2026  
**Direkte Basis:** 2.1.0.4-Beta  
**Stabile Referenz:** 2.1.0.0  
**Gesamturteil:** **PASS – release-fähige Beta für die dokumentierte rechnerische Messwert-Zweitkontrolle.** Keine elektrotechnische Zertifizierung oder Inbetriebnahmefreigabe.

## 1. Abnahmekriterien

| ID | Kriterium | Ergebnis |
|---|---|---:|
| A01 | Nur eingetragene Messwerte und rechnerisch notwendige Bezugsdaten beeinflussen die Bewertung. | PASS |
| A02 | Formularidentität, Strukturpassung, Unterschriften, Namen, Datum, Orte, Kreuze, Textfelder und formale Angaben sind irrelevant. | PASS |
| A03 | Fehlende oder unsichere Mess-/Bezugswerte werden einzeln abgefragt und erzeugen kein rotes X. | PASS |
| A04 | Solange ein notwendiger Wert fehlt, bleibt das Endergebnis gesperrt. | PASS |
| A05 | Vollständige plausible Werte erzeugen einen grünen Haken. | PASS |
| A06 | Ein bestätigter rechnerisch unplausibler Messwert erzeugt ein rotes X. | PASS |
| A07 | Das interne Vorlagenprofil dient nur zur Messfeldlokalisierung und ist kein sichtbarer Download oder Bewertungsparameter. | PASS |
| A08 | Vollständige Projektstruktur, Versionierung, PWA, Cache, Manifest, Release, Dokumentation, Tests und Prüfsummen sind konsistent. | PASS |

## 2. Implementierte Prüfgrenze

Die VDE-Engine enthält **19 zugelassene Felder**: 13 Messwertfelder und 6 rechnerisch notwendige Bezugsfelder. Sie enthält keine Felder für Formularidentität, Prüfgrund, Stammdaten, Namen, Datum, Orte, Unterschriften, Kreuze oder Freitext.

Der Nutzer bestätigt aus **12 Messgrößengruppen** nur die im Dokument tatsächlich eingetragenen Größen. Daraus ermittelt die Engine die jeweils erforderlichen Bezugswerte. Fehlende und unsichere Werte bleiben neutral offen. Rechenabweichungen bleiben ebenfalls offen, bis der Nutzer entweder korrigiert oder den Wert als tatsächlich eingetragen bestätigt.

Das interne Profil wurde auf **18 Mess-/Bezugsfeldzonen** reduziert. Sein Struktur-Fingerabdruck wird ausschließlich für Seitenausrichtung und Lokalisierung verwendet. Der interne Lokalisierungswert wird weder angezeigt noch an die Ergebnislogik übergeben. Die Mustervorlage selbst ist nicht eingebettet, nicht im PWA-Cache und nicht downloadbar.

## 3. Automatisierte Testergebnisse

| ID | Prüfung | Ergebnis |
|---|---|---:|
| T01 | JavaScript-Funktions-Smoke aller bestehenden Rechner/Inhalte und VDE-Messwertregeln | PASS · 97 Assertions |
| T02 | VDE-Engine: formale Felder vollständig ausgeschlossen | PASS |
| T03 | VDE-Engine: unbestätigter Messumfang ist neutral offen | PASS |
| T04 | VDE-Engine: fehlende Bezugsgröße ist offen, niemals automatisch rot | PASS |
| T05 | VDE-Engine: vollständiger positiver Messwertsatz | PASS · grüner Zustand |
| T06 | VDE-Engine: Zs-Überschreitung und Bestätigungs-Governance | PASS · roter Zustand nach Bestätigung |
| T07 | VDE-Engine: formale Stördaten ändern ein identisches Messwertergebnis nicht | PASS |
| T08 | E2E-PDF mit vollständigen plausiblen Messwerten | PASS · grüner Haken |
| T09 | E2E-PDF ohne U0 | PASS · Einzelabfrage, kein Endergebnis, kein rotes X |
| T10 | E2E-PDF mit Zs = 4,00 Ω bei B16/U0 = 230 V | PASS · rotes X erst nach Wertbestätigung |
| T11 | E2E-Smartphone-Foto 1170 × 1650, JPEG 68, 1,4° Drehung | PASS · lokale Bildtextschnittstelle, Einzelbestätigung, grüner Haken |
| T12 | Browser-Smoke auf 16 Direktseiten | PASS |
| T13 | Responsive Desktop 1440 × 1050, Tablet 820 × 1180, Mobil 390 × 844 | PASS · kein horizontales Überlaufen |
| T14 | Manifest, App-ID, Service Worker, versionsisolierter Cache und Offline-Aufruf | PASS |
| T15 | Statische Release-Validierung: Struktur, lokale Referenzen, Syntax, Datenschutz und Ausschlusslogik | PASS |
| T16 | Vollständige interne SHA-256-Dateiliste | PASS |

## 4. Nachweis der Ergebnis-Governance

### 4.1 Fehlende Bezugsgröße

Im PDF-Test wurde `U0` entfernt, während `Zs`, Kennlinie und Nennstrom vorhanden blieben.

- Die Anwendung öffnete `REQ-phaseVoltage` als einzelne Rückfrage.
- Die Schaltfläche zur Bestätigung eines n.-i.-O.-Befunds war nicht verfügbar.
- Die Ergebnisansicht blieb verborgen.
- Nach manueller Eingabe von `230 V` wurde neu gerechnet und der grüne Haken ausgegeben.

### 4.2 Bestätigte Rechenabweichung

Im Negativtest wurden `Zs = 4,00 Ω`, `B16` und `U0 = 230 V` verwendet. Der Rechenwert beträgt `230 / (5 × 16) = 2,875 Ω`.

- Vor Bestätigung blieb die Ergebnisansicht gesperrt.
- Der Nutzer konnte den Wert korrigieren oder als tatsächlich eingetragen bestätigen.
- Erst nach Bestätigung erschien das rote X.

### 4.3 Smartphone-Foto

Das Foto wurde reproduzierbar als 1170 × 1650 Pixel großes JPEG mit Qualität 68, Kontrastanpassung und 1,4° Drehung erzeugt.

- Der echte Bilddateipfad, Canvas-Rendering, lokale Ausrichtung, interner Messfeld-Lokator und die browserseitige `TextDetector`-Schnittstelle wurden durchlaufen.
- Da `TextDetector` nicht in jeder Chromium-Laufzeit nativ verfügbar ist, verwendete der Test einen deterministischen Browseradapter für genau die im Testfoto sichtbaren Textzeilen.
- Bildtextwerte wurden absichtlich mit 78 % Konfidenz übernommen und deshalb einzeln bestätigt.
- Vor Abschluss aller Wertbestätigungen blieb das Endergebnis gesperrt und es gab kein rotes X.
- Nach Abschluss erschien der grüne Haken; die mobile Ansicht blieb ohne horizontales Überlaufen.

## 5. Rechenregeln im Positivtest

| Messgröße | Eingabe | Auswertung |
|---|---:|---|
| Niederohmmessung | 0,20 Ω | ≤ 1 Ω · PASS |
| Isolation | >300; >300; >300 MΩ | kleinster Wert ≥ 1 MΩ · PASS |
| Schleifenimpedanz | 0,50 Ω, B16, U0 230 V | Grenzwert 2,875 Ω · PASS |
| Kurzschlussstrom | 460 A | U0/Zs = 460 A · 0 % Abweichung · PASS |
| Stromrelation | Ib 10 A, In 16 A | 10 ≤ 16 · PASS |
| Spannungsfall | ΔU 4 V, Un 400 V, 1,0 % | 1,0 % ≤ 5 % und rechnerisch konsistent · PASS |
| RCD-Auslösestrom | IΔ 18 mA, IΔn 30 mA | 18 ≤ 30 · PASS |
| RCD-Auslösezeit | 17 ms | ≤ 300 ms · PASS |

## 6. Vollständigkeit und Release-Integrität

- 16 HTML-Direktseiten wurden geprüft.
- Alle bestehenden Rechner, Wissensseiten, Navigation, Suche, Favoriten und externen Integrationen blieben erhalten.
- Version `2.1.0.5-Beta` ist in `VERSION`, HTML-Attributen, App-Laufzeit, Manifest, Navigation, Service Worker, VDE-Modulen, Tests, Dokumentation und Release-Konfiguration konsistent.
- PWA-App-ID und Start-URL lauten versionsspezifisch `sk-plt-tools-2.1.0.5-beta`.
- Der Cache lautet `sk-plt-tools-v2.1.0.5-Beta`; ältere SK-PLT-Tools-Caches werden bei Aktivierung entfernt.
- Die vollständige Prüfsummenliste wird unmittelbar vor dem finalen ZIP-Build neu erzeugt und danach erneut validiert.
- Die Mustervorlage und reale personenbezogene Prüfprotokolle sind nicht im Projekt, ZIP oder Precache enthalten.

## 7. Restrisiken und Grenzen

- Die Bildtexterkennung hängt von der lokalen Browserunterstützung für `TextDetector` ab. Ohne diese Funktion oder bei schlechter Aufnahme führt die Anwendung konsequent in die manuelle Messwertauswahl und Einzelergänzung.
- Stark abgeschnittene oder verzerrte Fotos können keinen verlässlichen automatischen Messumfang liefern.
- Die hinterlegten Standardparameter bilden keine vollständige Abdeckung aller normativen Sonderfälle, RCD-Typen, Netzformen oder Prüfbedingungen.
- Numerisch plausible Werte sind keine Bestätigung einer normgerechten Anlage.
- Prüfung, fachliche Bewertung und Freigabe verbleiben bei der verantwortlichen Elektrofachkraft.

## 8. Abnahme

Die geforderten Änderungen sind im geprüften Stand umgesetzt. **SK PLT Tools 2.1.0.5-Beta** ist als release-fähige Beta für kontrollierte Anwender- und Feldtests der dokumentierten rechnerischen Messwert-Zweitkontrolle freigegeben. Eine produktive elektrotechnische Freigabe wird ausdrücklich nicht erteilt.
