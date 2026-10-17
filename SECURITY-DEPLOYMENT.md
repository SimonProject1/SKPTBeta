# Security- und Deployment-Hinweise – V2.6.5.2-Beta

Stand: 17.10.2026

## Sicherheitsmodell

- Statische, clientseitige PWA ohne serverseitige Datenspeicherung.
- `referrer=no-referrer` auf allen HTML-Seiten.
- Externe Ziele werden nur mit `noopener noreferrer` geöffnet.
- Favoriten und App-Reihenfolge verbleiben lokal im Browser (`localStorage`).
- Der Analogsignal-Rechner speichert weder Messwerte noch physikalische Einheiten.
- MA, ME, Signalart und Eingabewert werden ausschließlich im aktuellen DOM-Zustand
  verarbeitet.
- Keine Änderung am zentralen Einheitensystem anderer Rechner oder Datenbanken.
- Service Worker verarbeitet nur GET-Anfragen derselben Origin.
- Alte `sk-pct-tools-`-Caches werden bei Aktivierung entfernt.

## Releasebestand

- Version: `2.6.5.2-Beta`
- Manifest: `manifest-v2-6-5-2.webmanifest`
- CSS: `assets/app-v2-6-5-2.css`
- Laufzeit: `assets/app-v2-6-5-2.js`
- Suchindex: `assets/search-index-v2-6-5-2.json`
- Cache-Epoch: `v2-6-5-2-core-r1`
- Navigationsassets: `assets/navigation-icons/v2-6-5-2-*.png`
- Release-Modul: `assets/release-module-v2-6-5-2.png`

## Deployment

1. Zielverzeichnis leeren oder den vollständigen Inhalt von
   `SK-PCT-Tools-V2.6.5.2-Beta` gemeinsam veröffentlichen.
2. Keine CSS-, JS-, Manifest-, Suchindex- oder Icon-Dateien aus V2.6.5.1 beimischen.
3. MIME-Typen für `.webmanifest`, `.js`, `.css`, `.json`, `.svg` und `.png` korrekt
   ausliefern.
4. HTTPS verwenden; localhost ist nur für lokale Tests vorgesehen.
5. Startseite einmal online öffnen und auf Aktivierung des neuen Service Workers warten.
6. Manifest, alle internen Routen und den vollständigen Precache online prüfen.
7. Netzwerk deaktivieren und mindestens Startseite, Analogsignal-Rechner,
   Einheitendatenbank und einen Wissensbeitrag offline aufrufen.
8. Bei bestehender iOS-PWA die App nach dem Online-Update vollständig schließen und
   erneut öffnen, damit der neue Worker die Kontrolle übernimmt.

## Integritätsprüfung

```bash
python3 tests/validate_project.py
sha256sum -c SHA256SUMS.txt
```

`SHA256SUMS.txt` umfasst jede Projektdatei außer sich selbst. Das ZIP wird nach der
Erstellung separat gehasht, erneut entpackt und in der entpackten Kopie validiert.

## Content Security Policy

Die App ist statisch und vermeidet Inline-Skripte. Für produktives Hosting kann eine
CSP auf Basis von `default-src 'self'` eingesetzt werden. Vor einer Erzwingung sind
PWA-Manifest, Bilder, Service Worker und der bewusst externe E+H-Link in der Zielumgebung
zu testen.
