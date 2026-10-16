SK PCT Tools 2.6.2.0-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.2.0-Beta basiert vollständig auf V2.6.1.9-Beta.

ÄNDERUNG DIESER VERSION
- Das bisherige SK-PCT-Tools-Logo wurde vollständig durch eine neue Markenfamilie
  im freigegebenen technisch-industriellen Icon-Design ersetzt.
- Die neue Bildmarke verbindet große PCT-Schrift, SK-Typenschild, Zahnradform und
  "TOOL'S BY S.K." mit kräftigen schwarzen Konturen, Cyan-/Blau-/Grün-Akzenten,
  Tiefenstaffelung und dem identischen Außenmaster der App-Icons.
- Das Logo bleibt bei 64 px als PCT-Marke erkennbar und besitzt für 180/192/512 px
  zusätzliche Marken- und Herkunftsdetails.
- Das sichtbare Startseiten- und Headerlogo verwendet assets/logo-sk-pct-tools.png.
- favicon.png, apple-touch-icon.png, icon-192.png, icon-512.png,
  icon-maskable-192.png und icon-maskable-512.png wurden aus derselben Quelle neu
  erzeugt.
- Maskable- und Apple-Varianten sind vollflächig und opak. Die komplette zentrale
  Bild-/Wortmarke liegt in der normierten Maskable-Safe-Zone; nur dekorative Rails
  dürfen durch Gerätemasken beschnitten werden.
- Alle 16 HTML-Dokumente enthalten Manifest-, Favicon- und Apple-Touch-Verweise.
- Manifest, Offline-Kerncache und sichtbare Laufzeitverweise verwenden ausschließlich
  die neue Markenfamilie.

GESCHÜTZTER APP-ICON- UND FAVORITENSTAND
- Die 22 freigegebenen App-, Wissens-, Hersteller- und Navigationsicons wurden nicht
  grafisch verändert oder neu gerendert.
- Ihre Bilddaten sind bitidentisch zur vollständigen V2.6.1.9-Beta; nur der
  Dateipräfix wurde versionsgerecht auf v2-6-2-0- umgestellt.
- Die zehn Startseiten- und fünf Wissens-Favoritenbuttons bleiben direkte Kinder des
  jeweiligen festen `.sk-app-icon-wrapper`.
- Touchfläche, 22-px-Kreis, Mittelpunkt auf der oberen rechten tatsächlichen
  Iconkante sowie stabile Hover-/Fokus-/Press-/Aktivzustände bleiben unverändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-2-0.css
- Zentrale Laufzeit: assets/app-v2-6-2-0.js
- Manifest: manifest-v2-6-2-0.webmanifest
- Suchindex: assets/search-index-v2-6-2-0.json
- Service-Worker-Cache: sk-pct-tools-v2-6-2-0-core-r1
- Control-Sprite: assets/pct-controls.svg
- App-Icon-Generator: tools/generate_png_icons.py
- Markenlogo-Generator: tools/generate_brand_assets.py
- Markenmaster: assets/logo-sk-pct-tools.png

MARKEN-/PWA-DATEIEN
- assets/logo-sk-pct-tools.png: 512 × 512, RGBA, transparente Außenkanten
- assets/favicon.png: 64 × 64, RGBA, für Browser-Tabs optimiert
- assets/apple-touch-icon.png: 180 × 180, RGBA/opak, iPhone/iPad
- assets/icon-192.png und icon-512.png: transparente Standard-PWA-Icons
- assets/icon-maskable-192.png und icon-maskable-512.png: opake Full-Bleed-Icons

PRÜFUNG
1. python3 tools/generate_brand_assets.py
2. python3 tests/validate_project.py
3. python3 tests/browser_regression.py

Die real ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Projektdateien außer
SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
