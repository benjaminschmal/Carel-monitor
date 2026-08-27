# Weishaupt WEM / Dimplex Modbus Mapping

This document records mappings found in the uploaded **Weishaupt WEM** configuration file. The addresses below are documentation addresses and must not be assumed to be identical to the CAREL `Rxxx` addresses exposed by the currently tested controller. fileciteturn163file0

## Documented read mappings

| Documentation address | Name | Function | Factor |
|---:|---|---:|---:|
| 30001 | Außentemperatur 1 | FC4 | 0.1 |
| 30002 | Außentemperatur 2 | FC4 | 0.1 |
| 30003 | Fehler | FC4 | 1 |
| 30004 | Warnung | FC4 | 1 |
| 30005 | Fehlerfrei | FC4 | 1 |
| 30006 | Betriebsstatusanzeige Code | FC4 | 1 |
| 33103 | Leistungsanforderung | FC4 | 1 |
| 33104 | Vorlauftemperatur | FC4 | 0.1 |
| 33105 | Rücklauftemperatur | FC4 | 0.1 |
| 31201 | HK2 - Raumsolltemperatur | FC4 | 0.1 |
| 31202 | HK2 - Raumtemperatur | FC4 | 0.1 |
| 31204 | HK2 - Vorlaufsolltemperatur | FC4 | 0.1 |
| 31205 | HK2 - Rücklaufsolltemperatur | FC4 | 0.1 |
| 41203 | HK2 - Betriebsart | FC3 | 1 |
| 31301 | HK3 - Raumsolltemperatur | FC4 | 0.1 |
| 41303 | HK3 - Betriebsart | FC3 | 1 |
| 36104 | Gesamt Energie Jahr | FC4 | 1 |
| 36204 | Heizen Energie Jahr | FC4 | 1 |
| 36304 | Warmwasser Energie Jahr | FC4 | 1 |
| 36404 | Kühlen Energie Jahr | FC4 | 1 |
| 34101 | Heizstab-Status | FC4 | 1 |
| 34102 | Heizstab-Betriebsstunden | FC4 | 1 |
| 34103 | Heizstab-Schaltspiele | FC4 | 1 |
| 34104 | Heizstab-Status 1 | FC4 | 1 |
| 34105 | Heizstab-Status 2 | FC4 | 1 |
| 34106 | Heizstab-Betriebsstunden 1 | FC4 | 1 |
| 34107 | Heizstab-Betriebsstunden 2 | FC4 | 1 |
| 44102 | Grenztemperatur | FC3 | 1 |
| 44103 | Bivalenztemperatur | FC3 | 1 |

## Text mappings

### Betriebsstatusanzeige

| Wert | Text |
|---:|---|
| 0 | undefiniert |
| 16 | Standby |
| 19 | Heizbetrieb |
| 23 | Kühlbetrieb |

### Systembetriebsart

| Wert | Text |
|---:|---|
| 0 | Automatik |
| 1 | Heizen |
| 2 | Kühlen |
| 3 | Sommer |
| 4 | StandBy |
| 5 | Heizstab |

### Betriebsart HK2 / HK3

| Wert | Text |
|---:|---|
| 0 | Automatik |
| 1 | Komfort |
| 2 | Normal |
| 3 | Absenkbetrieb |
| 4 | StandBy |

### Fehler

| Wert | Text |
|---:|---|
| 0 | Fehler aktiv / Fehler %d |
| 65535 | Kein Fehler |

### Fehlerfrei

| Wert | Text |
|---:|---|
| 0 | Fehler aktiv |
| 1 | Störungsfreier Betrieb |

## Important distinction for CAREL Monitor

The uploaded configuration is a Weishaupt WEM/Dimplex reference mapping. Live testing of the current CAREL endpoint showed that FC4 address `5` returns the same raw value as CAREL `R005`, while FC4 address `30006` is rejected. Therefore these documentation addresses are stored as reference data and are **not automatically converted into CAREL Rxxx mappings**.

The CAREL Monitor should continue scanning the verified FC4 range `R001...R209` and promote a documentation mapping to an active `Rxxx` mapping only after live verification. Write-capable registers are also kept documentation-only until their address and semantics have been verified on the installed system.
