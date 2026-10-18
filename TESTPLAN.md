# Testplan SK PCT Tools V2.6.6.0-Beta

Stand: 18.10.2026

## 1. Testziele

Nachweis von Struktur, Integrität, Navigation, Suche, Favoriten, Direktvergleich, Touch, Accessibility-Basis, Offlinefähigkeit, visueller Konsistenz und Regression gegenüber der vollständigen V2.6.5.5-Beta.

## 2. Zielgrößen

- 320 × 740 px
- 390 × 844 px (iPhone-nahe Touch-/PWA-Emulation)
- 768 × 1024 px (Tablet)
- 1280/1440 px Desktop
- Chromium mit Mobile-/Touchprofil und Safari-iPhone-User-Agent für iOS-nahe Prüfung

Ein physisches iPhone/iOS-Safari ist nicht Bestandteil der automatisierten Containerprüfung; Safe-Area, Touch, Standalone-Metadaten, Service Worker und Offlinepfade werden automatisiert geprüft.

## 3. Struktur und Integrität

- exakt 16 HTML-Seiten, ein H1 je Seite;
- zentrale versionierte CSS-/JS-/Manifest-Referenzen;
- alle lokalen Links/Assets vorhanden;
- 39 aktive PNG-Icons, 512 × 512 px, Transparenz;
- fünf Herstellericons byteidentisch;
- zehn Werkstoffdatensätze und zehn Werkstofficons;
- 19 Suchindexeinträge;
- keine operative Altversion;
- vollständige SHA256SUMS.txt.

## 4. Wissensnavigation

Für jeden Pfad vollständig testen:

1. Startseite → Wissensdatenbank
2. Hersteller öffnen
3. Gerät/Familie/Themenbereich öffnen
4. Wissensbeitrag öffnen
5. auf Tablet/Desktop über Breadcrumb zurück
6. mobil über kontextuellen Zurück-Chip zurück
7. Browser-Zurück/-Vorwärts prüfen

Pfade: Air Torque, Endress+Hauser, Siemens/SITRANS P320, Siemens/SPS-Analogkarte, Vacon. Sonstiges muss leer bleiben und darf keinen erfundenen Beitrag zeigen.

## 5. Werkstoffdatenbank

- zehn Werkstoffe direkt als Kacheln;
- kein Gruppen-Zwischenschritt;
- Kachel öffnet unmittelbare Detailansicht;
- Werkstoffnummernsuche mit und ohne Punkt;
- Mehrfachtreffer 316L;
- Filterzustände;
- Zurücknavigation;
- Direktvergleich 1.4404 gegen 1.4408;
- Quellen, Warnungen und Fachdaten vorhanden.

## 6. Suche und Favoriten

- Wissenssuche findet Hersteller, Familie und Beitrag;
- Startseitensuche nutzt den erweiterten Suchindex;
- leerer Favoritenzustand;
- Favorit für Wissenskachel;
- Favorit für direkte Werkstoffdetail-URL;
- Iconkopplung und Entfernen;
- lokale Speicherung unter skPctToolsFavoritesV2.

## 7. Interaktion und Accessibility-Basis

- Touchziele mindestens 44 px, testtolerant 39 px für native Rendering-Abweichungen;
- sichtbarer Fokus;
- keine Kachelbewegung bei Hover/Fokus/Aktiv;
- keine horizontale Überbreite;
- reduzierte Bewegung respektiert;
- genau ein H1;
- Breadcrumb/Zurück-Chip passend zum Viewport.

## 8. Offline/PWA

- Service Worker installiert und übernimmt die Seite;
- Cache-Epoch v2-6-6-0-core-r1;
- Wissenshub, direkter Promass-Beitrag und direkte Werkstoffdetail-URL offline;
- alle 39 Icons, Daten, Suchindex, CSS und JS im Core;
- Manifest und PWA-Logos unverändert erreichbar.

## 9. Regression

- zehn Startseiten-Apps;
- Header/Versionsmodul/Home/Zurück/Favoriten erhalten;
- Header bleibt im Sortiermodus geometrisch unverändert;
- fünf Fachbeiträge enthalten SCO/SCC, Promass-Grafiken, PIN 2457, Rohwertdaten und Parameter 2.2.3.7;
- Rechner-, Einheiten- und externe App-Pfade laden ohne Konsolenfehler.

## 10. Programme

- `tests/validate_project.py`
- `tests/correction_block_v2660.py`
- `tests/design_regression.py`
- `tests/design_audit_v2660.py`
- `tests/layout_regression_v2660.py`
- `tests/visual_shell_regression_v2660.py`
- `tests/browser_regression.py`
