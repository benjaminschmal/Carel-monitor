# Weishaupt WWP S 8 ID – zusätzliche Modbus-Erkenntnisse

## Ausgangslage

Die angeschlossene Wärmepumpe ist eine **Weishaupt WWP S 8 ID**. Die Zuordnung des Modells stammt aus den vorliegenden Weishaupt-Unterlagen.

Die WWP S 8 ID ist SG-Ready-fähig. Die SG-Ready-Funktion arbeitet über zwei digitale Eingänge (SGR1/ID1 und SGR2/ID2). Die vier Betriebszustände sind:

| SGR1 / ID1 | SGR2 / ID2 | Zustand | Bedeutung |
|---|---|---|---|
| geschlossen | offen | 1 | Sperre / EVU-Sperre |
| offen | offen | 2 | Normalbetrieb |
| offen | geschlossen | 3 | Erhöhter Betrieb |
| geschlossen | geschlossen | 4 | Zwangsbetrieb |

Im Zustand 3 wird die konfigurierte SG-Ready-Anhebung auf die Sollwerte für Heizen und Warmwasser aufgeschlagen.

## Weishaupt-Modbus-Referenzregister

Die aktuelle Weishaupt-Datenpunktliste `83807301` (Version 1/2025-11) dokumentiert unter anderem folgende Datenpunkte. Diese Adressen sind **Weishaupt-Modbus-Adressen und nicht automatisch CAREL-Rxxx-Adressen**.

| Modbus-Adresse | Datenpunkt | Zugriff | Status |
|---:|---|---|---|
| 30006 | Betriebsstatusanzeige | R | dokumentiert |
| 35101 | SG-Ready 1 | R | dokumentiert |
| 35102 | SG-Ready 2 | R | dokumentiert |
| 40001 | Systembetriebsart | R/W | dokumentiert |
| 40002 | SollwertPV | R/W | dokumentiert |
| 42102 | Warmwasser Push | R/W | dokumentiert |
| 42103 | Warmwasser Normal | R/W | dokumentiert |
| 42104 | Warmwasser Absenk | R/W | dokumentiert |
| 42105 | SG-Ready Anhebung | R/W | dokumentiert, Verfügbarkeit an der Anlage noch zu prüfen |

### Betriebsstatus 30006

Für `30006` sind unter anderem folgende Statuscodes dokumentiert:

| Wert | Status |
|---:|---|
| 10 | EVU-Sperre |
| 11 | SG-Tarif |
| 12 | SG-Maximal |
| 14 | Erhöhter Betrieb |
| 19 | Heizbetrieb |
| 20 | Warmwasserbetrieb |
| 37 | SGR3 Heizen |
| 39 | SGR3 Warmwasser |
| 40 | SGR4 Heizen |
| 42 | SGR4 Warmwasser |

## Wichtige Abgrenzung zum CAREL Monitor

Der CAREL Monitor liest aktuell den CAREL-Registerbereich und verwendet dafür die bekannten CAREL-Zuordnungen:

| CAREL-Register | Bedeutung |
|---:|---|
| R002 | Vorlauf |
| R003 | Rücklauf |
| R006 | Außentemperatur |

Die oben aufgeführten Weishaupt-Adressen `30006`, `35101`, `35102`, `40001`, `40002` und `42102–42105` werden **noch nicht als CAREL-Rxxx-Register gemappt**. Sie sind zunächst als zusätzliche Referenz für die weitere Untersuchung dokumentiert.

Insbesondere `35101` und `35102` sollen zunächst read-only getestet werden. Ein Modbus-Schreibzugriff auf diese Eingänge ist nicht vorgesehen.

## Quellen

- Weishaupt, Datenpunktliste **Modbus TCP (WWP)**, Dokument 83807301, Version 1/2025-11.
- Weishaupt, Montage- und Betriebsanleitung **WWP S 6 ID – WWP S 18 ID**.
- Vorliegende Anlagenunterlagen zur installierten **WWP S 8 ID**.

## Nächster Test

Vor einer Erweiterung des CAREL-Monitors soll geprüft werden, welche der dokumentierten Weishaupt-Datenpunkte über die vorhandene Schnittstelle tatsächlich erreichbar sind. Priorität haben:

```text
35101  SG-Ready 1
35102  SG-Ready 2
30006  Betriebsstatusanzeige
```

Erst nach diesem Read-only-Test werden weitere Register in das aktive CAREL-Mapping übernommen.
