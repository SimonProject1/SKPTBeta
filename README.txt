SK PCT Tools 2.6.2.1-Beta
Stand: 16.10.2026
Projektinhaber: Simon Kiesler

ÜBERBLICK
SK PCT Tools ist eine offlinefähige PWA für technische Rechner, Einheiten-,
Werkstoff- und Wissensdaten sowie Praxishinweise der Prozessleittechnik.
V2.6.2.1-Beta basiert vollständig auf V2.6.2.0-Beta.

ÄNDERUNG DIESER VERSION
- Der redundante kleine Textblock „SK“ oberhalb des Zahnrads wurde aus der gesamten
  Marken-/PWA-Familie entfernt. Die Herkunft bleibt eindeutig im unteren Feld
  „TOOL'S BY S.K.“ enthalten.
- Zahnrad, PCT-Schriftzug und das untere weiße Herkunftsfeld wurden proportional
  vergrößert und neu zentriert. Der freigegebene technisch-industrielle Stil mit
  schwarzen Konturen sowie Cyan-/Blau-/Grün-Akzenten bleibt erhalten.
- Die zusätzliche schwarze/dunkle CSS-Logokachel um das sichtbare Startseiten- und
  Headerlogo wurde entfernt. Der transparente Host zeigt nur noch das eigentliche
  Logo; Bild und Host besitzen dasselbe Außenmaß.
- assets/logo-sk-pct-tools.png, favicon.png, apple-touch-icon.png, icon-192.png,
  icon-512.png, icon-maskable-192.png und icon-maskable-512.png wurden aus derselben
  reproduzierbaren Quelle neu erzeugt.
- Maskable- und Apple-Varianten sind vollflächig und opak. Die komplette zentrale
  PCT-/Zahnrad-/Herkunftsmarke liegt in der normierten Maskable-Safe-Zone; nur
  dekorative Rails dürfen durch Gerätemasken beschnitten werden.
- Alle 16 HTML-Dokumente enthalten Manifest-, Favicon- und Apple-Touch-Verweise.
  Manifest, Metadaten, Suchindex, Offline-Kerncache und Laufzeitverweise verwenden
  ausschließlich V2.6.2.1-Beta.

GESCHÜTZTER APP-ICON- UND FAVORITENSTAND
- Die 22 freigegebenen App-, Wissens-, Hersteller- und Navigationsicons wurden nicht
  grafisch verändert oder neu gerendert; nur ihr Dateipräfix wurde versionsgerecht
  auf v2-6-2-1- umgestellt.
- Die zehn Startseiten- und fünf Wissens-Favoritenbuttons bleiben direkte Kinder des
  jeweiligen festen `.sk-app-icon-wrapper`.
- Touchfläche, 22-px-Kreis, Mittelpunkt auf der oberen rechten tatsächlichen
  Iconkante sowie stabile Hover-/Fokus-/Press-/Aktivzustände bleiben unverändert.

ZENTRALE ARCHITEKTUR
- Zentraler Stil: assets/app-v2-6-2-1.css
- Zentrale Laufzeit: assets/app-v2-6-2-1.js
- Manifest: manifest-v2-6-2-1.webmanifest
- Suchindex: assets/search-index-v2-6-2-1.json
- Service-Worker-Cache: sk-pct-tools-v2-6-2-1-core-r1
- Control-Sprite: assets/pct-controls.svg
- App-Icon-Generator: tools/generate_png_icons.py
- Markenlogo-Generator: tools/generate_brand_assets.py
- Markenmaster: assets/logo-sk-pct-tools.png

MARKEN-/PWA-DATEIEN
- assets/logo-sk-pct-tools.png: 512 × 512, RGBA, transparente Außenkanten
- assets/favicon.png: 64 × 64, RGBA, Browser-Tab
- assets/apple-touch-icon.png: 180 × 180, RGBA/opak, iPhone/iPad
- assets/icon-192.png und icon-512.png: transparente Standard-PWA-Icons
- assets/icon-maskable-192.png und icon-maskable-512.png: opake Full-Bleed-Icons

PRÜFUNG
1. python3 tools/generate_brand_assets.py
2. python3 tests/validate_project.py
3. python3 tests/browser_regression.py

Die real ausgeführten Ergebnisse stehen in TEST-RESULTS.txt. Alle Projektdateien außer
SHA256SUMS.txt selbst sind in SHA256SUMS.txt mit SHA-256 erfasst.
