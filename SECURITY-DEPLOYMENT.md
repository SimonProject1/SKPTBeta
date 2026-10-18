# Security & Deployment – SK PCT Tools V2.6.6.0-Beta

Stand: 18.10.2026

## Sicherheitsprinzipien

- Lokale PWA ohne serverseitige Konten oder Telemetrie.
- Favoriten, Anordnung und Darstellungszustände verbleiben im Browser-LocalStorage.
- Externe Links öffnen mit `noopener noreferrer`; Referrer-Policy ist `no-referrer`.
- Fachinformationen sind Orientierung. Herstellerdokumentation, Gerätestand, Werkstoffzeugnis sowie betriebliche Freigaben bleiben maßgeblich.
- Keine sicherheitskritischen Parameter oder Werkstofffreigaben automatisiert übernehmen.
- PIN 2457 und Parameter 2.2.3.7 sind nur im vorhandenen fachlichen Warn- und Gültigkeitskontext dargestellt.

## Deployment

1. ZIP-Prüfsumme gegen die veröffentlichte SHA-256 vergleichen.
2. Paket vollständig entpacken; keine Mischinstallation mit älteren Versionen.
3. Projektwurzel unverändert über HTTPS bereitstellen.
4. MIME-Typen für `.webmanifest`, `.json`, `.svg`, `.js`, `.css` und `.png` korrekt ausliefern.
5. `manifest-v2-6-6-0.webmanifest` und `service-worker.js` nicht durch aggressive Zwischen-Caches veralten lassen.
6. Nach Deployment PWA schließen und neu öffnen; bei Bedarf alte Site-Daten entfernen.
7. `python3 tests/validate_project.py` in der Zielkopie ausführen.

## Service Worker

- Cache: `sk-pct-tools-v2-6-6-0-core-r1`.
- Alte Caches mit Präfix `sk-pct-tools-` werden bei Aktivierung entfernt.
- Navigation nutzt Network-first mit Offline-Fallback.
- Assets nutzen Cache-first und werden bei Bedarf ergänzt.
- Query-URLs für Wissens- und Werkstoffdetails werden auf den gecachten Dokumentpfad kanonisiert; Inhalte werden aus den gecachten Daten/JS aufgebaut.

## Offline-Core

Enthält alle Laufzeitseiten, fünf Wissensbeiträge, Werkstoffdaten, Einheiten, Suchindex, zentrale CSS-/JS-Dateien, Manifest, Markenassets und alle 39 aktiven Icons. Dokumentation, Tests und Generatoren sind bewusst nicht Teil des Browser-Precaches, bleiben aber im vollständigen ZIP enthalten.

## Integrität und Rollback

- `SHA256SUMS.txt` prüft alle Projektdateien außer sich selbst.
- Die ZIP-Datei erhält eine separat verifizierte SHA-256.
- Rollback nur als vollständiger Austausch gegen ein zuvor verifiziertes Komplettpaket; keine Patch-Mischung.
