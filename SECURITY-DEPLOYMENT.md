# Sicherheitsheader für das Deployment

SK PCT Tools setzt auf jeder HTML-Seite `Referrer-Policy: no-referrer` über ein Meta-Element um. Die folgenden Schutzmaßnahmen müssen vom HTTPS-Webserver gesetzt werden, weil sie aus einer statischen PWA heraus nicht zuverlässig erzwungen werden können:

```text
Content-Security-Policy: default-src 'self'; img-src 'self' data:; style-src 'self'; script-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cross-Origin-Opener-Policy: same-origin
```

Hinweis: GitHub Pages verwaltet HTTP-Sicherheitsheader selbst und unterstützt keine projektbezogene Headerdatei. Bei einem eigenen Webserver, Netlify, Cloudflare Pages oder vergleichbarem Hosting ist diese Konfiguration serverseitig zu übernehmen und nach dem Deployment zu prüfen.
