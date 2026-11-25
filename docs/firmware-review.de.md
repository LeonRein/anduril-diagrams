# Andúril 2: Prüfung der Diagramme (Stand 2023‑10‑03) gegen die aktuelle Firmware

**Firmware-Stand:** ToyKeeper/anduril, Release 2026‑10‑26 (Commit 71fe301)
**Lampe:** Fireflies E12 Eclipse → Build `fireflies-lume10`, Modellnummer **0453** (AVR32DD20, AW2016‑RGB‑Aux‑Chip)
**Methode:** Handbuch (`docs/anduril-manual.md`) und ChangeLog gelesen, Event-Handler in `ui/anduril/*.c` geprüft und den Lume10-Build mit dem Präprozessor aufgelöst, um die tatsächlich aktiven Funktionen zu ermitteln.

## Fehler (ein Diagramm sagt etwas, das die Firmware heute nicht mehr tut)

| # | Diagramm | Alt | Aktuell |
|---|----------|-----|---------|
| 1 | Advanced | Tactical Mode → **3C** → Next Channel Mode | 3C wird im Tactical Mode absichtlich ignoriert (Bugfix 2024‑04‑20). Pfeil entfernt; Tactical-Box zeigt jetzt „6C: back to Off · 3C: ignored“. |
| 2 | Advanced | Voltage Config 1: 1C = −0.30 V … 7C = 0 V … 13C = +0.30 V (0,05‑V‑Schritte) | 0,01‑V‑Schritte: **20C = ±0**, 1C = −0.19 V, 40C = +0.20 V (seit 2026‑09). |
| 3 | Beide | Version: `BBPP-YYYY-MM-DD` | `MODEL-YYYY-MM-DD(-SINCE-DIRTY)` (seit 2023‑12) |
| 4 | Advanced | Ramp Extras: verwaiste Zeile „1C = Ramp → 2C goes to full power“ unter der Liste | entfernt (Duplikat) |

## Fehlende Funktionen (vor allem die neue Aux-Steuerung)

| # | Wo | Neu | Auf der E12? |
|---|----|-----|--------------|
| 5 | Off / Lockout → 7C | Aux-Muster: Off → Low → High → **Breathing → Fast Breathing → Heavy Breathing** → Blinking → **2× Blink → 1× Blink** | ja (Breathing nur mit AW2016-Chip) |
| 6 | Off → **8H** | Helligkeit des Standby-Musters: bei „Low“ die Low-Stufe, bei High/Breathing/Blinking die High-Stufe (14 Stufen) | ja |
| 7 | Ramp → **8H** (auf Aux-Kanal) | Aux-Helligkeit im eingeschalteten Zustand (9 Stufen). Feste Aux-Farben: das *ist* ihre Helligkeit (die Rampe wirkt dort nicht); HSV-Kanal: Maximum, die Rampe dimmt darunter | ja |
| 8 | Batt Check → **1H** | Batt Color: Spannung als Farbe statt Ziffern | ja |
| 9 | Batt Color → **8H** | POVD-/Batt-Color-Helligkeit | ja |
| 10 | Batt Check → **2H** | Powerbank-Host-Modus (USB‑C laden anderer Geräte) | ja |
| 11 | Voltage Config 3–5 | Aux low ramp level, aux high ramp level, aux while on (0/1/2/3) | ja |
| 12 | Simple UI | Extended Simple UI (Fireflies): Ramp 3C/6C Rampenstil, Ramp 5H Sunset-Timer, Off/Lockout 7C/7H Aux | ja |
| 13 | Simple UI | Batt Check 1H / 2H funktionieren auch im Simple UI | ja |
| 14 | Kanalliste | Kanal „HSV color“ (RGB-Aux als Farbrad, 3H = Farbton) | ja (ab Werk deaktiviert) |
| 15 | Zellspannungs-Legende | Schwellen 3.0 / 3.3 / 3.5 / 3.7 / 3.9 / 4.1 V, Smooth POVD | ja |
| 16 | Tactical-Slots | 153+ = Police, Lightning, Candle, Bike (in dieser Reihenfolge) | ja |

## Geprüft und korrekt
Pfeile zwischen ON/OFF/Ramp/Lockout, Strobe-Reihenfolge (Party → Tactical → Police → Lightning → Candle → Bike), Ramp Config, Ramp Extras (5 Punkte), Channel Mode Config (9H), Misc Config (9H), Momentary Mode, Auto-Lock (Lockout 10H), Lockout 1H/2H/3C/3H/4C/4H/5C, Simple-UI-Konfiguration (Off 10H, 4 Punkte), Factory Reset 13H, Thermal Config (n + 30 °C, max. 70 °C), Beacon-Timing, SOS im Blinky-Kreis.

## Werkseinstellungen der E12 (zur Info)
Simple UI aktiv · gestufte Rampe (Simple UI: 10–130, 5 Stufen) · 2C geht im Advanced UI auf volle Leistung · nur Hauptkanal aktiv · Aux Off: Breathing + Rainbow · Aux Lockout: Fast Breathing + Voltage · POVD 4 s · Temperaturlimit 50 °C · Level 150 = reine FET‑Turbostufe.

## Darstellung
- 3H / 4H / 8H werden im Ramp-Modus gedrückt; ihre Wirkung hängt nur vom aktiven Kanal ab. Deshalb gehen sie im Diagramm direkt von ON aus (Kasten „Hold in Ramp“), nicht vom Kasten „Next Channel Mode“. 3C schaltet nur den Kanal um, die Lampe bleibt im Ramp-Modus.
- Ovale und das Schloss sind Modi, Kästen sind Aktionen oder Menüs.
- ON und der Ramp-Balken sind derselbe Modus (`steady_state`). Das ON-Oval trägt die Aktionen, der Balken zeigt die Helligkeitsstufen und auf welcher Stufe man von OFF/Lockout aus landet. Beide tragen deshalb denselben gelben Rahmen, und ON ist mit „Ramp mode“ beschriftet.

## Varianten der Diagramme
- `anduril2-e12-*`: zugeschnitten auf die Fireflies E12 Eclipse (Lume10, 0453): echte Kanalliste (Main, HSV, 7 Aux-Farben), 3H = Momentary Turbo bzw. Farbton im HSV-Kanal, Werkseinstellungen, Tactical-Slots 153–156 ausgeschrieben, keine Hinweise auf Mehrkanal-/200%-Funktionen.
- `anduril2-generic-*`: allgemeine Multi-Channel-Fassung wie das Original; ★ markiert Funktionen, die nur manche Lampen haben.
- Neu erzeugen: `make` im Repo-Root (siehe README).
