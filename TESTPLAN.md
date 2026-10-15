# Testplan – SK PCT Tools 2.6.1.4-Beta

## Automatisierte Strukturprüfung

```bash
python3 tests/validate_project.py
```

Prüft Version, Manifest, Suchindex, alle lokalen Verweise, zentrale CSS-/JS-Dateien,
Header-/Footer-Platzhalter, 10 App-Ziele, 10 Navigations-PNGs, Icon-Geometrie,
Service-Worker-Cache, Generator, Dokumentation und interne SHA-256-Prüfsummen.

## Automatisierte Browserprüfung

Lokalen Server im Projektstamm starten:

```bash
python3 -m http.server 8080
SK_BASE_URL=http://127.0.0.1:8080/ python3 tests/browser_regression.py
```

Abdeckung:
- 15 aktive Seiten
- Smartphone 390 × 844
- Tablet 820 × 1180
- Desktop 1440 × 1000
- Reflow bei 320 CSS-Pixeln
- Header, Footer, App-Rahmen und horizontale Überläufe
- Home-/Zurück-Navigation und Favoriten
- Suche, Hersteller-Hub, Einheiten- und Werkstoffdatenbank
- sechs Rechnerreferenzen und ±-Touchbedienung
- internes Scrollen des Siemens-Rechners
- PWA-Installation, Cache-Upgrade und Offline-Navigation

## Visueller Vorher-/Nachher-Vergleich

Für dieselben 15 Seiten je einen Screenshot in drei Viewports erzeugen.
Dynamische Fokuszustände vor der Aufnahme neutralisieren und den internen
Scrollbereich auf Position 0 setzen. Zusätzlich die berechneten Rechtecke und
Kernstile von Body, Rahmen, Header, Inhalt und Footer vergleichen.

Abnahmekriterien:
- keine DOM-Geometrieabweichung
- kein horizontaler Überlauf
- identischer App-Rahmen und internes Scrollverhalten
- unveränderte Icon-Außenform, Farben, Symbolmasse und Favoritenposition
- Pixelabweichungen nur durch die neue Versionszeichenfolge oder technisch
  unvermeidbare Antialiasing-/Zustandsrasterung

## Manuelle PWA-Kontrolle

1. Online öffnen und Installation prüfen.
2. Anwendung vollständig schließen.
3. Netzwerk deaktivieren.
4. Startseite, einen Rechner, Hersteller-Hub und Wissensbeitrag öffnen.
5. Netzwerk aktivieren und Upgrade von einem alten sk-pct-tools-Cache prüfen.
6. Sicherstellen, dass nur sk-pct-tools-v2-6-1-4-core-r1 bestehen bleibt.
