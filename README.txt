SK PCT Tools · V2.6.6.0-Beta
================================
Stand: 18.10.2026

ZWECK
-----
Mobile-first PWA für PCT-/PLT-Praxiswissen, Rechner, Einheiten- und Werkstoffdaten.
Die vollständige V2.6.5.5-Beta ist die unveränderte fachliche Basis dieser Version.

VERBINDLICHE NAVIGATION
-----------------------
Wissensdatenbank:
Startseite → Wissensdatenbank → Hersteller → Gerät/Familie/Themenbereich → Wissensbeitrag

Vorhandene Pfade:
- Air Torque → Pneumatischer Antrieb → Drehrichtung SCO/SCC
- Endress+Hauser → Promass → Einbaulage und Einbausituation
- Siemens → SITRANS P320 → SIL-Verriegelung
- Siemens → SPS / Analogkarte → Rohwert und Skalierung
- Vacon → Frequenzumrichter → Ist-/Sollwert-Abweichung im PLS
- Sonstiges bleibt sichtbar, enthält aber keine erfundenen Beiträge.

Werkstoffdatenbank:
Startseite → Werkstoffdatenbank → Werkstoff/Werkstoffdetails
- keine Werkstoffgruppen-Zwischenebene;
- zehn vorhandene Werkstoffe direkt als App-Kacheln;
- Suche, Direktfilter und Direktvergleich bleiben parallel erreichbar.

DESIGN
------
- Kompakte responsive App-Kacheln auf jeder Navigationsebene.
- Herstellericons sind bytegenau aus der freigegebenen Familie übernommen.
- Fünf Geräte-/Familienicons, fünf funktionsbezogene Beitragsicons und zehn variable Werkstofficons sind neu.
- Werkstoffnummer ist das primäre Erkennungsmerkmal jedes Werkstofficons.
- Hover, Fokus, Touch und Aktivzustand verändern weder Position noch Größe.
- Smartphone: kontextueller Zurück-Chip; Tablet/Desktop: vollständige Breadcrumbs.
- Wissensbeiträge nutzen ein ruhiges flaches Layout; Inhalte, Fachgrafiken, Warnungen, Quellen und Merkpunkte bleiben erhalten.

WICHTIGE DATEIEN
----------------
- assets/app-v2-6-6-0.css / assets/app-v2-6-6-0.js
- assets/knowledge-overview.js
- assets/materials.js / assets/materials.json
- assets/search-index-v2-6-6-0.json
- assets/navigation-icons/v2-6-6-0-*.png
- tools/generate_png_icons.py
- manifest-v2-6-6-0.webmanifest
- service-worker.js
- WISSENSBEITRAGS-STANDARD.md
- ICON-DESIGNRICHTLINIE.txt
- TESTPLAN.md / TEST-RESULTS.txt

START UND DEPLOYMENT
--------------------
Die Projektwurzel über HTTPS oder lokal über einen Webserver ausliefern, z. B.:
  python3 -m http.server 8080
Direkter Dateiaufruf über file:// wird wegen Fetch-, Manifest- und Service-Worker-Regeln nicht unterstützt.
Nach Deployment alten Browser-/PWA-Cache schließen oder die PWA neu öffnen. Der Cache-Epoch lautet v2-6-6-0-core-r1.

PRÜFUNG
-------
  python3 tests/validate_project.py
  python3 tests/design_regression.py
  python3 tests/design_audit_v2660.py
  python3 tests/correction_block_v2660.py
  python3 tests/layout_regression_v2660.py
  python3 tests/visual_shell_regression_v2660.py
  python3 tests/browser_regression.py

Integrität: SHA256SUMS.txt enthält jede Projektdatei außer sich selbst. Die ZIP-Prüfsumme wird zusätzlich neben dem Downloadpaket veröffentlicht.
