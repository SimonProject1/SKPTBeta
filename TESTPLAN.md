# Testplan – SK PCT Tools V2.6.5.2-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.5.1-Beta

## 1. Struktur, Syntax, Referenzen und Integrität

```bash
node --check assets/app-v2-6-5-2.js
node --check assets/analogsignal-rechner.js
python3 -m py_compile tests/*.py tools/*.py
python3 tests/validate_project.py
```

Prüfumfang: VERSION, 16 HTML-Dokumente, 14 aktive interne Unterseiten, zentrale
CSS-/JS-Referenzen, Manifest, Suchindex, Cache-Epoch, lokale Ziele, H1, Header/Footer,
10 Apps, 24 versionierte Navigationsicons, geschützte PNG-Hashes, Offline-Precache,
Analogsignal-Einheitenbereinigung und SHA256SUMS.txt.

## 2. Analogsignal-Rechner

Automatisiert im `browser_regression.py`:

- sichtbare und operative Entfernung von Prozesskategorie, Prozesseinheit,
  Signaleinheit, s0/s1 und `unit-system.js`
- Signalarten 4–20 mA, 0–20 mA, 0–10 V und 2–10 V
- Vorwärtsrechnung bei 50 %: 12 mA, 10 mA, 5 V und 6 V
- Umkehrrechnung aller vier Signalarten auf den einheitenlosen Skalierungswert
- MA kleiner ME
- negativer Messbereich −50…150
- vollständig positiver Messbereich 10…110
- leere/ungültige Eingabe und MA = ME
- Zurücksetzen auf 0…100 / 4–20 mA / Vorwärts / 50
- direkte Folgeeingabe nach Reset
- Ergebnisprozent, Kopierstatus, Enter, ±-Touchziel und Liveberechnung
- Hilfeaussage: Nur MA, ME und Signalart; Skalierungswerte einheitenlos

## 3. Vollständiger Positionsabgleich

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/layout_regression_v2652.py
```

1.440 Prüfungen über 16 Routen und fünf Profile:

- iPhone/iOS-PWA 390 × 844
- Smartphone 412 × 915
- Smartphone-Querformat 844 × 390
- Tablet 820 × 1180
- Desktop 1440 × 1000

Geprüft werden Rahmenlage, identische Headerhöhe je Profil, Logo-/Versions-/Button-
Mittellinien, Interaktionsstabilität, Inhaltsbeginn, Footerabschluss, Safe Area,
horizontaler Überlauf, defekte Bilder und die vollständige Einbettung von Header,
Inhalt und Footer in denselben App-Rahmen.

## 4. Design-, Touch-, Accessibility- und Offline-Audit

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_audit_v2652.py
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/design_regression.py
```

- 162 Auditprüfungen über alle 16 Seiten
- 103 Raster-/Favoritenprüfungen in fünf Profilen
- Suche, Filter, Hersteller-Hub, Breadcrumbs, Chevron, Favoriten Kurz/Lang/Leer
- Tastaturfokus, Fokusfalle, Escape, Fokusrückgabe und 44-px-Touchziele
- unveränderter Header im Sortiermodus
- Offlineaufruf einer Unterseite aus dem Precache

## 5. Vollständige Browser-/Funktionsregression

```bash
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

1.366 Prüfungen:

- 15 aktive Seiten × Smartphone, Tablet und Desktop
- zusätzliche 320-px-Reflow- und 844 × 390-Profile
- pixelidentische Headerzustände und identische Außenrahmen
- Favoriten, Suche, Sortierung und Drag-and-Drop mit Pointer-/Touch-Abbruch
- sechs Rechner mit Referenz-, Grenz-, Reset-, Kopier- und Vorzeichentests
- Einheiten- und Werkstoffdatenbank
- Wissens-Hub, Herstelleransichten und sämtliche Wissensbeiträge
- Service-Worker-Installation, Upgrade und Offlinebetrieb

## 6. Visuelle QA

Repräsentative Screenshots werden auf 390 × 844 und 1440 × 1000 kontrolliert:
Startseite, Analogsignal-Rechner, Favoriten, Suche, Wissens-Hub, Wissensbeitrag,
Einheitendatenbank und Werkstoffdatenbank. Kriterien: keine Überlagerung, keine
abgeschnittenen Header-/Footer-Inhalte, keine Layoutsprünge, keine horizontalen
Überläufe und konsistente Rahmen-/Achsenlage.

## 7. Abschluss

1. TEST-RESULTS.txt finalisieren.
2. `__pycache__` und temporäre QA-Dateien aus dem Projekt entfernen.
3. SHA256SUMS.txt über alle Projektdateien außer sich selbst erzeugen.
4. Strukturprüfung erneut ausführen.
5. vollständiges ZIP erzeugen.
6. ZIP separat hashen, erneut entpacken und Strukturprüfung in der Kopie ausführen.
