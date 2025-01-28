# Versandpreise

Dieses Python-Skript berechnet die günstigsten Versandkosten für Pakete basierend auf Gewicht, Abmessungen und Zielort. Es unterstützt mehrere Versanddienste und -Provider und hilft, die besten Optionen zu finden. Es funktioniert für Sendungen ins Inland und Ausland, Versandort ist jedoch immer Deutschland.

Es gibt für diese Software keinen Support.

## Unterstützte Paketdienste / Provider
- Pakajo (Pakajo und Finale Label > Warenpost, DHL, DPD, usw.)
- Jumingo Express
- Sendcloud (nur Warenpost)
- Hermes
- GLS
- Deutsche Post

In Zukunft sollen noch DHL (Privatkunden via DHL.de) und DPD implementiert werden. Es werden nur Optionen angezeigt, die Warenversand erlauben.

## Lizenz
Dieses Skript steht unter der [Creative Commons BY-SA 4.0 Lizenz](https://creativecommons.org/licenses/by-sa/4.0/).

## Für Einsteiger

### Was macht dieses Skript?
Stell dir vor, du möchtest ein Paket verschicken, bist dir aber unsicher, welcher Versanddienstleister der günstigste ist. Dieses Skript vergleicht automatisch verschiedene Anbieter und gibt dir die besten Optionen.

### Wie benutzt man das Skript?
1. **Eingaben bereitstellen**: Gib oben im Code Details zu deinem Paket an, z. B. Gewicht, Maße und Zielort.
2. **Ergebnisse ansehen**: Das Skript liefert die günstigsten Versandmöglichkeiten und alle wichtigen Details.

## Für Fortgeschrittene

### Funktionsüberblick
Das Skript nutzt APIs verschiedener Versanddienstleister (z. B. Deutsche Post, Hermes, GLS) und berechnet die günstigsten Preise für nationale und internationale Sendungen. Es berücksichtigt:
- Paketgewicht
- Abmessungen
- Prioritätsoptionen (bei manchen Dienstleistern)

### Features
- **Mehrsprachige Unterstützung**: Automatische Anpassung des Ländercodes (Alpha-2/Alpha-3).
- **Anpassbarkeit**: Über Konfigurationen und Eingabeparameter steuerbar.
- **Flexible Ausgabe**: Ergebnisse als Liste oder JSON, basierend auf den Benutzereinstellungen.

### Technische Details
- Programmiert in Python
- Voll konfigurierbar über die Optionen oben im Code
- Zur Eigennutzung geschrieben, daher potentiell ineffizienter oder redundanter Code. Ich habe dieses Projekt schnell zusammengeflickt und nur teilweise debuggt, entsprechend ist mit einigen Fehlern zu rechnen.

## Kontakt und Mitwirken
Entwickelt von Jan-Ole Michael @ [postonaut.de](https://postonaut.de)  

Erstelle für Vorschläge oder Fehlerberichte eine Issue hier auf GitHub.
