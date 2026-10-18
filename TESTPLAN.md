# Testplan – SK PCT Tools V2.6.5.4-Beta

Stand: 18.10.2026  
Basis: vollständige V2.6.5.3-Beta

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
node --check assets/app-v2-6-5-4.js
node --check assets/analogsignal-rechner.js
python3 -m py_compile tests/*.py tools/*.py
python3 tests/validate_project.py
```

Prüfumfang: VERSION, 16 HTML-Dokumente, 14 aktive interne Unterseiten, zentrale
CSS-/JS-Referenzen, Manifest, Suchindex, Cache-Epoch, lokale Ziele, H1,
Header/Footer, 10 Apps, 24 versionierte Navigationsicons, geschützte PNG-Inhalte,
Offline-Precache, gezielte Analogsignal-Bereinigung und SHA256SUMS.txt.

## 2. Analogsignal-Struktur und entfernte Oberflächenelemente

- Kickertext und Kickerknoten fehlen vollständig.
- `#calculate`, `#reset` und `.analog-signal-actions` fehlen vollständig.
- keine verwaisten Analogsignal-Aktionsregeln im CSS.
- keine `.pct-copy-button`, `.pct-copy-host`, Kopier-Tooltips oder Kopier-Touchflächen.
- Ergebniswerte bleiben sichtbar und ohne horizontalen Überlauf.
- Kopierfunktionen anderer Rechner bleiben unverändert vorhanden.

## 3. Analogsignal-Berechnung

Automatisiert in `browser_regression.py`:

- alle vier Signalarten: 4–20 mA, 0–20 mA, 0–10 V und 2–10 V
- beide Richtungen: Skalierungswert → Signal und Signal → Skalierungswert
- Änderungen von MA, ME, Signalart, Richtung und Eingabewert
- vollständig negativer Bereich −200…−100
- über null verlaufender Bereich −50…150
- positiver Bereich 10…110
- ungültig/leere Eingabe und MA = ME
- direkte Folgeeingaben 25, 75, 0, 100, −25 und 125 ohne Berechnen-Button
- lineare Grenz-/Extrapolationswerte 0 mA und 24 mA bei −25 % / 125 %
- Enter, ±-Touchbedienung, aria-live und sichtbare Ergebniswerte

## 4. Layout und visuelle Regression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2654.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/visual_shell_regression_v2654.py
```

- 16 Routen × 5 Profile
- iPhone/iOS-PWA 390 × 844
- Smartphone 412 × 915
- Smartphone-Querformat 844 × 390
- Tablet 820 × 1180
- Desktop 1440 × 1000
- Rahmenlage, Headerhöhe, Footer, Safe Area, Reflow, Überlauf, Bilder und
  Interaktionsstabilität
- zusätzliche Analogsignal-Screenshots auf iPhone und Desktop

## 5. Browser, Touch, Accessibility und Offline

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2654.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Geprüft werden Favoriten kurz/lang/leer, Suche und Filter, Hersteller-Hub,
Breadcrumbs, Tastaturfokus, Fokusfalle, Escape, Fokusrückgabe, 44-px-Touchziele,
unveränderter Header im Sortiermodus, Drag-and-Drop mit Pointer-/Touch-Abbruch,
320-px-Reflow, sechs Rechner, Service-Worker-Upgrade und Offlineaufruf.

## 6. Regression gegen V2.6.5.3

Operative Textdateien werden nach Normalisierung der Versionsnummern verglichen.
Zulässige Abweichungen: Analogsignal-HTML/-JS, gezielte Kopierunterdrückung in der
zentralen Laufzeit, Entfernung ausschließlich Analogsignal-spezifischer Aktions-CSS-
Regeln sowie Manifest-/Suchindexbeschreibung. Versionierte PNG-Dateien müssen
inhaltlich SHA-256-identisch zur V2.6.5.3-Basis bleiben.

## 7. Abschluss

1. TEST-RESULTS.txt finalisieren.
2. Temporäre QA-Dateien und `__pycache__` aus dem Projekt entfernen.
3. SHA256SUMS.txt über alle Projektdateien außer sich selbst erzeugen.
4. Struktur- und Prüfsummenprüfung erneut ausführen.
5. vollständiges ZIP erzeugen und separat per SHA-256 prüfen.
6. ZIP erneut entpacken und die Strukturprüfung in der Kopie wiederholen.
