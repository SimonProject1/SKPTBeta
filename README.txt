SK PLT Tools 2.3.1.0-Beta

Beta-Testversion der kompakten statischen Web-App für Rechner,
Wissensdatenbank und Einheitendatenbank.

Basis dieser Beta
- Verbindliche Ausgangsbasis ist die öffentliche stabile Version 2.3.0.0 vom 10.10.2026.
- Bestätigte SHA-256 der Basis: 91ff22671dbdf2b0103c2c884daab3523bd5d476cddee6e881dcb78a0bd6747a.
- Die bestätigten Funktionen und das Design wurden erhalten; geändert wurde gezielt die mobile Übersicht der Wissensdatenbank.

Neue mobile Wissensdatenbank
- Wissensbeiträge werden auf Smartphones nach Hersteller zusammengefasst.
- Gruppen: Herstellerunabhängig, Air Torque, Siemens und Vacon.
- Jede Herstellergruppe ist einzeln ein- und ausklappbar und zeigt sichtbare Treffer sowie Gesamtzahl.
- Die Gruppenzustände werden lokal unter skKnowledgeManufacturerStateV1 gespeichert.
- Die kompakte Beitragsansicht ist mobil standardmäßig aktiv, blendet Beschreibungen aus und bleibt unter skKnowledgeCompactCardsV1 gespeichert.
- Bei einer Suche werden passende Herstellergruppen automatisch geöffnet; Gruppen ohne Treffer werden ausgeblendet.
- Desktop und reguläre Tablet-Ansicht bleiben als flache zweispaltige Beitragsübersicht erhalten.

Bewahrte Funktionen
- Mobile Startseite mit einklappbaren Werkzeugkategorien und optionaler Kompaktansicht.
- Alle 10 Werkzeug-/Dienstkarten, Suche, Kategorienfilter, Sortierung und Wissensbeitragssuche.
- Favoriten, Seitennavigation, alle sechs Rechner, Einheitendatenbank und fünf Wissensbeiträge.
- Werkstoff-Nachschlagewerk, Messstellen-Dokumentation und externer E+H Device Viewer.
- Das verworfene VDE-0100-600-Funktionsmodul ist nicht Bestandteil dieser Anwendung.

Bedienung der mobilen Wissensdatenbank
- Herstellerzeile antippen, um die enthaltenen Wissensbeiträge ein- oder auszuklappen.
- Unter „Beitragsansicht“ die Option „Kompakte Beiträge“ ein- oder ausschalten.
- Über das Suchfeld nach Hersteller, Gerät, Werkstoff oder Thema filtern.
- Einstellungen werden ausschließlich lokal in localStorage gespeichert.

Deployment zum Testen
- Den vollständigen Inhalt dieses Ordners unverändert auf einen HTTPS-Webserver kopieren.
- manifest.webmanifest und service-worker.js müssen im Projektstamm erreichbar bleiben.
- Nach dem ersten vollständigen Online-Aufruf stehen alle produktiven Seiten offline bereit.
- Für einen lokalen Funktionstest kann ein statischer HTTP-Server verwendet werden; Service Worker und Installation anschließend unter HTTPS prüfen.

PWA
- Start-URL, Scope und App-ID bleiben versionsunabhängig auf ./ gesetzt.
- Der Service Worker verwendet die Beta-Caches core-v2.3.1.0 und documents-v2.3.1.0.
- Laufzeitkanal: beta.

Integrität
- SHA256SUMS.txt enthält einen SHA-256-Eintrag je weiterer Datei im Projektordner.
- Die Prüfsumme des ZIP-Archivs wird separat neben dem ZIP bereitgestellt.

Release Notes
- Siehe RELEASE-NOTES.txt.
