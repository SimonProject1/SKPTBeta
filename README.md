# SK PLT Tools Beta 2.0.3.0-Beta.1

Vollständige Beta auf Basis der unveränderten stabilen Version 2.0.2.0.

## Neu in 2.0.3.0-Beta.1

- Neuer `Siemens-SPS-Analogwert-Rechner` für 4–20 mA, 0–20 mA, 0–10 V und 2–10 V.
- Wechselseitige Umrechnung aus Siemens-Rohwert, Signalwert, Prozentwert oder physikalischem Wert.
- Frei definierbarer physikalischer Minimal-/Maximalwert und frei definierbare Einheit.
- Siemens-Nennskalierung 0…27.648 = 0…100 % mit linearer Kennzeichnung von Unter- und Überbereich.
- Eigener sichtbarer App-Name `SK PLT Tools Beta`, statische BETA-Kennzeichnung und Version `2.0.3.0-Beta.1`.
- Eindeutige PWA-ID und eigene `start_url` im Manifest.
- Getrennter Cache `sk-plt-tools-beta-v2.0.3.0-Beta.1`; die Aktivierung löscht ausschließlich ältere Beta-Caches und keine stabilen Caches.
- Vollständige Integration in Startseite, Suche, Favoriten, Seitennavigation und Offline-Precache.

## Erhalten

Design, Header, Footer, mobile Darstellung, bestehende Rechner, Messstellen-Dokumentation, Plausibilitätsprüfung, Wissensdatenbank, Werkstoffsuche, Sortierung, Navigation und Favoritenlogik wurden aus 2.0.2.0 übernommen.

## Installation und Test

1. Das Paket in einen **eigenen Beta-Webroot bzw. Unterordner** entpacken; die stabile Installation 2.0.2.0 nicht überschreiben.
2. Den vollständigen Inhalt des Ordners `SK-PLT-Tools-V2.0.3.0-Beta.1` bereitstellen.
3. Automatische Prüfungen im Projektordner starten:

```bash
python tools/validate_release.py
node tools/functional-smoke-test.js
python -m http.server 8080
```

4. Danach die Browser-Abnahme aus `TESTBERICHT-UND-ABNAHME.md` durchführen.

2.0.3.0-Beta.1 · Beta · Entwickelt von Simon Kiesler
