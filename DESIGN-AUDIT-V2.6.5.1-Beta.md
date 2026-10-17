# Design-Audit-Abnahme – SK PCT Tools V2.6.5.1-Beta

Stand: 17.10.2026  
Basis: vollständige V2.6.5.0-Beta  
Status: vollständig umgesetzt und geprüft

## 1. Hersteller-Hub

Die fünf Herstellerbereiche verwenden dieselbe responsive Rasterfamilie wie die
App-Kacheln auf der Startseite:

- Desktop: gleichmäßige Verteilung über fünf Spalten
- Tablet: vier Spalten
- Smartphone bis 430 px: drei Spalten statt abweichender Zweispalten-Sonderlösung
- breitere Smartphones: vier Spalten
- Smartphone-Querformat: sechs kompakte Spalten entsprechend der Startseite

Sichtbare PNG-Grenzen werden aus derselben unveränderten 512-px-Icongeometrie
abgeleitet. Titel besitzen dasselbe 12-px-Kartenmaß und denselben Zeilenabstand wie
auf Home. Kachel, Icon und Text bleiben bei Hover, Fokus, Touch und Aktivzustand
geometrisch unverändert.

Der Hub nutzt den freien Inhaltsraum zwischen Suche und Footer ausgewogen. Die
Kacheln selbst bleiben kompakt; historische große horizontale und vertikale
Zwischenräume der Zweispalten-Anordnung sind entfernt.

## 2. Favoriten-Unteransicht

Die Favoritenübersicht ist kein body-weites Overlay mehr. Sie wird als direktes Kind
in `.pct-home-screen` oder `.sk-app-frame` eingesetzt.

Verbindlicher Zustand:

1. Der vorhandene große abgerundete App-Rahmen bleibt die einzige Außenbegrenzung.
2. Bestehender Header und Footer bleiben sichtbar und behalten ihre Geometrie.
3. Der reguläre mittlere Seiteninhalt wird während der Favoritenansicht aus dem
   Flexfluss genommen und anschließend vollständig wiederhergestellt.
4. Favoritenkopf, Liste, leerer Zustand und Navigation liegen zwischen Header und Footer.
5. Lange Listen scrollen ausschließlich in `.sk-favorites-list`.
6. Es existiert kein Backdrop, kein Vollbilddrawer und keine zweite Außenkontur.
7. Escape schließt die Ansicht und stellt den Fokus auf den Auslöser zurück.

## 3. Funktionsschutz

Erhalten und geprüft:

- Favoritenzähler und Local-Storage-Key `skPctToolsFavoritesV2`
- vorhandene gespeicherte Favoriten
- Öffnen interner und externer Ziele
- Einzellöschen und Alle leeren
- leerer Zustand und Live-Status
- Fokusfalle, Tastaturbedienung und 44-px-Touchziele
- passendes App-/Wissensicon pro Zeile
- Migration veralteter V2.6.5.0-Icon-URLs auf V2.6.5.1-Assets
- Offlinebetrieb

## 4. Audit-Matrix

| Bereich | Abnahmekriterium | Nachweis |
|---|---|---|
| Rastergleichheit | Startseite und Hersteller-Hub haben je Profil dieselbe Spaltenzahl | `design_regression.py` |
| Icongleichheit | sichtbare Breite/Höhe weicht höchstens 1 px ab | `design_regression.py` |
| Zustände | keine Bewegung bei Hover, Fokus, Drücken, Aktiv | Design-/Browserregression |
| Wissenssuche | Filter, Zähler und Navigation bleiben funktionsfähig | Design-/Auditregression |
| App-Rahmen | Favoriten sind direktes Kind des vorhandenen Rahmens | `design_regression.py` |
| Außenbegrenzung | Drawer liegt vollständig innerhalb des Rahmenrechtecks | `design_regression.py` |
| Header/Footer | vor und nach Öffnen pixelgleich; sichtbar | Design-/Browserregression |
| Kurz/Lang/Leer | alle drei Zustände geprüft | `design_regression.py` |
| Scroll | lange Liste scrollt innen; Außenrahmen bleibt fest | `design_regression.py` |
| Accessibility | ARIA, Fokusfalle, Escape und Fokusrückgabe | Design-/Auditregression |
| Touch/Safe Area | 44-px-Ziele, Hoch-/Querformat, iOS-PWA-Profil | alle Browserprogramme |
| Offline | Precache, Cache-Upgrade und interne Offline-Navigation | `browser_regression.py` |
| Integrität | Referenzen, geschützte Hashes und SHA256SUMS | `validate_project.py` |

## 5. Unterstützte Profile

- iPhone/iOS-PWA-Hochformat: 390 × 844
- Smartphone-Hochformat: 412 × 915
- Smartphone-Querformat: 844 × 390
- Tablet-Touch: 820 × 1180
- Desktop: 1440 × 1000
- zusätzlicher Reflow: 320 px Breite

## 6. Prüfergebnis

- Zielregression: PASS · 103 Prüfungen
- Design-Audit: PASS · 162 Prüfungen
- vollständige Browser-/Funktionsregression: PASS · 1.347 Prüfungen
- offene Fehler im geprüften Umfang: keine

## 7. Freigaberegel

Der Build ist nur freigabefähig, wenn Strukturprüfung, alle drei Browserprogramme,
vollständige SHA256SUMS-Prüfung, ZIP-Rückentpackung und separate ZIP-SHA-256-
Verifikation erfolgreich sind.
