# Sicherheit und Deployment – SK PCT Tools V2.6.5.0-Beta

Stand: 17.10.2026

## 1. Deploymentvoraussetzungen

- ausschließlich über HTTPS veröffentlichen;
- Projektwurzel vollständig und unverändert deployen;
- keine alte V2.6.x-Datei parallel in derselben PWA-Scope belassen;
- MIME-Typen für `.webmanifest`, `.js`, `.css`, `.json`, `.svg` und `.png` korrekt setzen;
- `service-worker.js` ohne langfristigen HTTP-Cache beziehungsweise mit sofortiger
  Revalidierung ausliefern;
- `assets/app-v2-6-5-0.css`, `assets/app-v2-6-5-0.js` und versionierte Assets dürfen
  langfristig gecacht werden, da ihre Dateinamen releasegebunden sind.

## 2. Empfohlene HTTP-Sicherheitsheader

Jede HTML-Seite enthält bereits `Referrer-Policy: no-referrer` als Meta-Element.
Die folgenden Header müssen serverseitig gesetzt werden:

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cross-Origin-Opener-Policy: same-origin
```

Hinweis: GitHub Pages verwaltet Header selbst und unterstützt keine
projektbezogene Headerdatei. Bei eigenem Webserver, Netlify, Cloudflare Pages oder
vergleichbarem Hosting ist die Konfiguration serverseitig zu übernehmen.

## 3. PWA-/Service-Worker-Strategie

- Release: `2.6.5.0-Beta`
- Cache-Epoch: `v2-6-5-0-core-r1`
- Scope und Start-URL: `./`
- Precache enthält alle aktiven Seiten, Daten, Laufzeitdateien, SVG-Controls und
  freigegebenen PNG-Assets.
- Aktivierung entfernt ältere `sk-pct-tools-*`-Caches.
- Navigation verwendet Network-first mit Cachefallback.
- statische Assets verwenden Cache-first und werden bei Bedarf ergänzt.
- Suchparameter und Hash werden für Cachekeys normalisiert.

## 4. Update-/Rollback-Ablauf

Deployment:

1. ZIP-SHA-256 gegen die separat gelieferte Prüfsumme prüfen.
2. ZIP in eine leere Zielwurzel entpacken.
3. `VERSION`, Manifest, zentrale CSS-/JS-Dateien und Service Worker stichprobenartig prüfen.
4. vollständige Zielwurzel atomar veröffentlichen.
5. online Startseite, interne Unterseite und Offlineaufruf testen.
6. installierte PWA einmal vollständig schließen und neu öffnen.

Rollback:

1. vollständiges vorheriges Release wiederherstellen;
2. dessen Service Worker und Cache-Epoch mit veröffentlichen;
3. Browser/PWA online öffnen, damit der vorherige Worker übernehmen kann;
4. Funktions- und Offlineprüfung wiederholen.

## 5. Integrität

- `SHA256SUMS.txt` enthält jede Projektdatei außer sich selbst.
- geschützte PNGs werden zusätzlich gegen feste Referenz-Hashes geprüft.
- das vollständige ZIP erhält eine separate SHA-256-Datei.
- geänderte oder fehlende Dateien führen in `tests/validate_project.py` zu FAIL.

## 6. Daten- und Datenschutz

- Favoriten, Appreihenfolge und Einheitenfavoriten bleiben lokal im Browser.
- der E+H Device Viewer ist als externer Dienst gekennzeichnet und wird mit
  `noopener`, `noreferrer` und `no-referrer` geöffnet.
- SK PCT Tools überträgt keine lokalen Eingaben an einen eigenen Server.
- vertrauliche Anlagendaten dürfen nicht in statische Projektdateien aufgenommen werden.
