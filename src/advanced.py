import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# usage: python3 advanced.py OUT.svg [generic|e12]
from common import *
import common
E12 = len(sys.argv) > 2 and sys.argv[2] == "e12"
common.SHOW_STAR = not E12


def V(generic, e12):
    return e12 if E12 else generic

S = SVG(2000, 1346)
FS = 13      # body font size
LH = 17.6    # body line height

# =====================================================================
#  TOP ROW
# =====================================================================

# ---- Ramp Extras Config -------------------------------------------------
S.card(12, 27, 312, 616, "Ramp Extras Config", "config")
S.para(24, 82, [
    "1) Release after first flash",
    ">• Disable Manual Memory",
    ">>◦ **1+C** = disable manual memory,",
    ">>   go back to automatic memory",
    "2) Release after second flash",
    ">• Set manual memory timer",
    ">>◦ Click n times for n minutes (0 = off)",
    "3) Release after third flash",
    ">• Ramp up after “Off → 1H”",
    ">>◦ **0C** = Ramp up after moon",
    ">>◦ **1C** = Stay at floor level",
    "4) Release after fourth flash",
] + V([
    ">• Configure turbo style",
    ">>◦ **0C** = No turbo, only ceiling",
    ">>◦ **1C** = Ramp → 2C goes to full power",
    ">>   (200% for dual-channel lights)",
    ">>◦ **2C** = Ramp → 2C goes to ceiling, or",
    ">>   full power (200% for dual-channel",
    ">>   lights) if ramped up to ceiling first",
], [
    ">• Configure turbo style __(E12 default: 1C)__",
    ">>◦ **0C** = No turbo, only ceiling",
    ">>◦ **1C** = Ramp → 2C goes to full power",
    ">>   (level 150 = FET turbo)",
    ">>◦ **2C** = Ramp → 2C goes to ceiling, or",
    ">>   full power if ramped up to the",
    ">>   ceiling first",
]) + [
    "5) Release after fifth flash",
    ">• Configure smooth steps",
    ">>◦ **0C** = Disable",
    ">>◦ **1C** = Enable __(default)__",
], size=FS, lh=LH)
S.add('<line x1="26" y1="514" x2="310" y2="514" stroke="%s"/>' % STROKE)
S.para(26, 538, [
    "**Memory types**",
    "**Automatic:** last ramped brightness",
    "**Manual:** saved brightness (Ramp → 10C)",
    "**Hybrid:** last ramped brightness for",
    "   n minutes, then manual memory",
], size=FS, lh=LH + 2)

# ---- Channel Mode Config -------------------------------------------------
S.card(345, 27, 227, 428, "Channel Mode Config", "config")
y = S.para(357, 80, V([
    "1) Release after first flash",
    ">• Configure channel 1",
    "2) Release after second flash",
    ">• Configure channel 2",
    "3) Release after third flash",
    ">• Configure channel 3",
    "4) Release after fourth flash",
    ">• Configure channel 4",
    "5) Release after fifth flash",
    ">• Configure channel 5",
    "6+) Release after sixth+ flash",
    ">• Configure channels 6 – 12",
    ">   (aux LED channels come last:",
    ">   Red, Yellow, Green, Cyan,",
    ">   Blue, Purple, White)",
], [
    "__Release after the n-th flash:__",
    "1) Main LEDs  __(on)__",
    "2) HSV aux color wheel  __(off)__",
    "3) Aux red  __(off)__",
    "4) Aux yellow  __(off)__",
    "5) Aux green  __(off)__",
    "6) Aux cyan  __(off)__",
    "7) Aux blue  __(off)__",
    "8) Aux purple  __(off)__",
    "9) Aux white  __(off)__",
    None,
    "__(on / off = factory default)__",
]), size=FS, lh=V(LH, 22))
S.text(357, 388, "Channel Config", size=16, weight=650, fill=INK)
S.para(357, 412, [
    "• **0:** Disable channel",
    "• **1:** Enable channel",
], size=FS, lh=LH)

# ---- Sunset timer / manual memory ----------------------------------------
S.card(345, 473, 227, 74, None, "mode")
S.text(436, 506, "Sunset Timer", size=18, weight=650, fill=INK, anchor="middle")
S.text(436, 528, "1 blink = 5 minutes", size=FS, fill=BODY, anchor="middle")
S.stopwatch(531, 514, 16)

S.card(345, 567, 227, 76, None, "mode")
S.text(458, 597, "Manual Memory", size=18, weight=650, fill=INK, anchor="middle")
S.text(458, 617, "Activate manual memory and save", size=12.5, fill=BODY, anchor="middle")
S.text(458, 633, "brightness (+ channel mode)", size=12.5, fill=BODY, anchor="middle")

# ---- Ramp Config ---------------------------------------------------------
S.card(688, 27, 320, 485, "Ramp Config", "config")
S.text(702, 76, "7H in Ramp: current ramp  ·  10H in Off: Simple UI ramp", size=11.5, fill=MUTED)
S.para(700, 96, [
    "1) Release after first flash  __(7H and 10H)__",
    ">• Set floor level",
    ">>◦ Click n times for level n of 150",
    "2) Release after second flash  __(7H and 10H)__",
    ">• Set ceiling level",
    ">>◦ Click n times for level 151 − n",
    "3) Release after third flash",
    ">• Stepped ramp  __(7H and 10H)__",
    ">>◦ Click n times for 1 to 150 steps",
    ">• Smooth ramp speed  __(only 7H)__",
    ">>◦ **1C** = full speed (~2.5 s end-to-end)",
    ">>◦ **2C** = half speed (~5 s)",
    ">>◦ **3C** = third speed (~7.5 s)",
    ">>◦ **4C** = quarter speed (~10 s)",
    "4) Release after fourth flash  __(only 10H)__",
    ">• Configure Simple UI turbo style",
    ">>◦ **0C** = No turbo, only ceiling",
    ">>◦ **1C** = Ramp → 2C goes to full power",
] + V([
    ">>   (200% for dual-channel lights)",
    ">>◦ **2C** = Ramp → 2C goes to ceiling, or",
    ">>   full power (200% for dual-channel",
    ">>   lights) if ramped up to ceiling first",
], [
    ">>◦ **2C** = Ramp → 2C goes to ceiling, or",
    ">>   full power if ramped up to ceiling first",
    None,
    "__E12 defaults: smooth 1–130 · stepped 10–130,__",
    "__7 steps · Simple UI 10–130, 5 steps, no turbo__",
]), size=FS, lh=LH + 0.5)

# ---- Toggle ramp style ---------------------------------------------------
S.card(766, 552, 262, 146, None, "mode")
S.text(897, 582, "Toggle Ramp Style", size=18, weight=650, fill=INK, anchor="middle")
gid = S.nid("rg")
S.add('<defs><linearGradient id="%s" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="#334155"/>'
      '<stop offset="1" stop-color="#FDE68A"/></linearGradient></defs>' % gid)
S.add('<path d="M790,664 L882,602 L882,664 Z" fill="url(#%s)"/>' % gid)
for i, (h, c) in enumerate([(18, "#475569"), (34, "#94A3B8"), (50, "#E2E8F0"), (64, "#FDE68A")]):
    S.add('<rect x="%d" y="%d" width="22" height="%d" rx="2" fill="%s" stroke="#64748B" stroke-width="0.8"/>' % (
        908 + i * 24, 664 - h, h, c))
S.text(836, 686, "Smooth", size=FS, fill=BODY, anchor="middle")
S.text(955, 686, "Stepped", size=FS, fill=BODY, anchor="middle")

# ---- Tactical Mode Config -----------------------------------------------
S.card(1033, 27, 247, 308, "Tactical Mode Config", "config")
S.para(1045, 80, [
    "1) Release after first flash",
    ">• Configure tactical slot 1",
    "2) Release after second flash",
    ">• Configure tactical slot 2",
    "3) Release after third flash",
    ">• Configure tactical slot 3",
], size=FS, lh=LH)
S.text(1045, 205, "Tactical Slot Config", size=16, weight=650, fill=INK)
S.para(1045, 229, [
    "• **0:** Last-used strobe mode",
    "• **1 – 150:** Brightness level",
    "• **151:** Party Strobe",
    "• **152:** Tactical Strobe",
] + V([
    "• **153+:** next strobes in group order",
    "   (Police★, Lightning, Candle, Bike)",
], [
    "• **153:** Police  · **154:** Lightning",
    "• **155:** Candle  · **156:** Bike Flasher",
]) + [
], size=FS, lh=LH)

# ---- Actions -------------------------------------------------------------
S.card(1305, 27, 313, 143, "Actions", "info")
S.para(1319, 78, [
    "**1C:** Click",
    "**1H:** Hold",
    "**2C:** Click, Click",
    "**2H:** Click, Hold",
], size=FS, lh=LH)
S.para(1455, 78, [
    "**nC / nH:** n presses",
    "__Number entry in menus:__",
    "**Click** = +1",
    "**Hold** = +10",
], size=FS, lh=LH)
S.text(1319, 158, "__Ovals & lock = modes · boxes = actions / menus__", size=12)

# ---- Misc Config ---------------------------------------------------------
S.card(1305, 182, 313, 262, "Misc Config", "config", sub=None)
S.text(1319, 230, V("Only available on some lights", "E12: only item 1 exists, and it has no effect"), size=12, fill=MUTED)
S.para(1319, 254, [
    "1) Release after first flash",
    ">• Set tint ramp style",
    ">>◦ **0C** = Smooth (blend channels)",
    ">>◦ **1C** = Middle tint only",
    ">>◦ **2C** = Extreme tints only (toggle)",
    ">>◦ **3+C** = Stepped ramp with 3+ steps",
] + V([
    "2) Release after second flash",
    ">• Set jump start level",
    ">>◦ 1 to 150",
    ">>◦ Usually between 20 and 50",
], [
    None,
    "__The only channel with “tint” is HSV, and its__",
    "__3H always rotates the hue smoothly in a__",
    "__circle. No jump-start setting on the E12.__",
]), size=FS, lh=LH)

# ---- Title ---------------------------------------------------------------
S.card(1642, 27, 346, 327, None, "#0F172A")
S.text(1660, 102, "Andúril 2", size=66, weight=800, fill=INK, ls="-1")
S.text(1661, 145, V("Multi-Channel", "Fireflies E12 Eclipse"), size=V(32, 27), weight=700, fill=INK)
S.text(1661, 180, "Advanced UI", size=28, weight=600, fill="#4F46E5")
S.para(1661, 214, V([
    "**Firmware:** Andúril 2 release 2026-10-26",
    "**Diagram revision:** 2026-11-25",
    "**Source:** github.com/ToyKeeper/anduril",
], [
    "**Firmware:** fireflies-lume10 · model 0453",
    "**Release:** 2026-10-26 · **Diagram:** 2026-11-25",
    "**Source:** github.com/ToyKeeper/anduril",
]), size=13.5, lh=20)
S.add('<rect x="1656" y="278" width="318" height="64" rx="8" fill="#FFFBEB" stroke="#FCD34D"/>')
S.para(1666, 297, V([
    "**NOTE:** Some features are hardware-specific",
    "or may be disabled by manufacturers.",
    "★ = only on some lights (e.g. FF E12 Eclipse)",
], [
    "**Factory defaults:** Simple UI · stepped ramp ·",
    "only Main channel on (Ramp 3C = ramp style) ·",
    "2C = full power · Turbo = level 150 (FET)",
]), size=12.5, lh=16.5)

# ---- Aux LED Color for Cell Voltage -------------------------------------
S.card(1642, 362, 346, 140, None, "aux")
S.text(1815, 391, "Aux LED Color for Cell Voltage", size=18, weight=650, fill=INK, anchor="middle")
S.wheel(1683, 428, 22)
S.battery(1746, 402, 214, 42, size=11)
S.text(1815, 474, V("Single-color aux: fast blink 3.3 – 2.9 V, off below 2.9 V",
                    "Standby (Voltage color): 6 steps as shown"), size=11.5, fill=BODY, anchor="middle")
S.text(1815, 490, V("Smooth POVD★: ~60 shades instead of 6",
                    "Post-off display & Batt Color: smooth, ~60 shades"), size=11.5, fill=MUTED, anchor="middle")

# =====================================================================
#  MIDDLE BAND
# =====================================================================

# ---- Tactical Mode -------------------------------------------------------
S.card(1033, 390, 212, 114, "Tactical Mode", "mode", tsize=18)
S.para(1047, 439, [
    "**1H:** Tactical Slot 1",
    "**2H:** Tactical Slot 2",
    "**3H:** Tactical Slot 3",
    "**6C:** back to Off  __· 3C: ignored__",
], size=FS, lh=16.5)

# ---- Next Channel Mode (lockout 3H) --------------------------------------
S.card(1466, 467, 140, 90, None, "lock")
S.text(1536, 495, "Next Channel", size=17, weight=650, fill=INK, anchor="middle")
S.text(1536, 517, "Mode", size=17, weight=650, fill=INK, anchor="middle")
S.text(1536, 541, "(3H to cycle)", size=12.5, fill=MUTED, anchor="middle")

# ---- Lockout side column -------------------------------------------------
S.card(1642, 508, 346, 72, None, "lock")
S.stopwatch(1681, 548, 15, fillwedge=False)
S.lock(1681, 546, 13)
S.text(1715, 536, "Auto-lock Config", size=18, weight=650, fill=INK)
S.text(1715, 556, "Release after blink", size=12.5, fill=BODY)
S.text(1715, 572, "N clicks for N minutes (0 = off)", size=12.5, fill=BODY)

S.card(1642, 590, 346, 92, None, "lock")
S.auxsun(1681, 624, 17)
S.text(1715, 617, "Aux LED Mode in Lockout", size=18, weight=650, fill=INK)
S.para(1715, 638, [
    "Off → Low → High → Breathing★ →",
    "Fast Breathing★ → Heavy Breathing★ →",
    "Blinking → 2× Blink → 1× Blink",
], size=12.5, lh=16)

S.card(1642, 692, 346, 124, None, "lock")
S.wheel(1681, 748, 19)
S.text(1715, 719, "Aux LED Color in Lockout", size=18, weight=650, fill=INK)
S.para(1715, 740, [
    "Release on selected color:",
    "Red → Yellow → Green → Cyan →",
    "Blue → Purple → White → Disco →",
    "Rainbow → Voltage",
] + V([], ["__E12 default: Fast Breathing + Voltage__"]), size=12.5, lh=15.5)

S.card(1642, 826, 346, 70, None, "lock")
S.moon(1681, 861, 17)
S.text(1715, 855, "Momentary Moon", size=18, weight=650, fill=INK)
S.text(1715, 876, "Lowest floor of smooth vs. stepped", size=12.5, fill=BODY)

S.card(1642, 904, 346, 72, None, "lock")
S.moon(1681, 940, 17)
S.text(1715, 930, "Momentary Low", size=18, weight=650, fill=INK)
S.text(1715, 950, "Highest floor of smooth vs. stepped,", size=12.5, fill=BODY)
S.text(1715, 965, "or manual memory if set", size=12.5, fill=BODY)

# ---- Left: tint / turbo / next channel ------------------------------------
S.card(12, 683, 232, 212, "Hold in Ramp", "mode", tsize=18)
S.para(26, 736, V([
    "**3H:** Momentary Turbo",
    "   __or tint ramp, if the current__",
    "   __channel has a tint to ramp__",
    "**4H:** Momentary Turbo",
    "   __(lights with tint ramping)__",
    "**8H★:** Aux brightness, 9 steps",
    "   __(on an aux channel)__",
    "   __= max. of the aux ramp__",
], [
    "**3H:** Momentary Turbo",
    "   __HSV channel: rotate hue__",
    "**4H:** Momentary Turbo",
    "**8H:** Aux brightness, 9 steps",
    "   __only on an aux / HSV channel__",
    "   __fixed colors: sets brightness__",
    "   __(ramp has no effect there)__",
    "   __HSV: sets max., ramp dims__",
]), size=FS, lh=17.6)

S.card(282, 682, 214, 196, "Next Channel Mode", "mode", tsize=18)
S.text(296, 729, V("(3C to cycle)", "(3C, enabled channels only)"), size=12.5, fill=MUTED)
if not E12:
    S.para(296, 750, [
        "• Channel 1",
        "• Channel 2",
        "• 50/50",
        "• Tint Ramp",
    ], size=FS, lh=17)
    S.para(394, 750, [
        "• Autotint",
        "• HSV color★",
        "• Aux LED",
        "   channels",
    ], size=FS, lh=17)
else:
    S.para(296, 752, [
        "• Main LEDs",
        "• HSV color wheel  __(3H: hue)__",
        "• Aux Red · Yellow · Green ·",
        "   Cyan · Blue · Purple · White",
    ], size=FS, lh=17)
S.add('<line x1="296" y1="826" x2="482" y2="826" stroke="%s"/>' % STROKE)
S.para(296, 845, [
    "__Switches to the next enabled__",
    "__channel and stays in Ramp.__",
], size=12.5, lh=16)

# ---- ON / OFF / ramp / lockout ------------------------------------------
# Switch to Simple UI
S.card(847, 752, 193, 40, None, "info", strip=False)
S.text(943, 778, "Switch to Simple UI", size=18, weight=650, fill=INK, anchor="middle")

# Ramp column
gid = S.nid("rb")
S.add('<defs><linearGradient id="%s" x1="0" x2="0" y1="0" y2="1">'
      '<stop offset="0" stop-color="#FEF9C3"/><stop offset="0.45" stop-color="#FDE68A"/>'
      '<stop offset="1" stop-color="#64748B"/></linearGradient></defs>' % gid)
S.add('<rect class="card" x="1297" y="618" width="95" height="288" rx="10" fill="url(#%s)" stroke="#94A3B8" filter="url(#sh)"/>' % gid)
S.add('<path d="M1297.5,658 V628 Q1297.5,618.5 1307,618.5 H1382 Q1391.5,618.5 1391.5,628 V658 Z" fill="#F97316"/>')
S.add('<line x1="1297" y1="658" x2="1392" y2="658" stroke="#FFFFFF" stroke-width="2"/>')
S.text(1344.5, 644, "Turbo", size=14, weight=700, fill="#FFFFFF", anchor="middle")
S.text(1344.5, 677, "Ceiling", size=13.5, weight=600, fill=INK, anchor="middle")
S.text(1344.5, 898, "Floor", size=13.5, weight=600, fill="#FFFFFF", anchor="middle")
S.text(1338, 772, "Ramp", size=22, weight=700, fill=INK, anchor="middle", rotate=-90)
S.text(1362, 772, "2H Down / 1H Up", size=13, weight=500, fill=INK, anchor="middle", rotate=-90)
S.add('<line x1="1375" y1="690" x2="1375" y2="878" stroke="%s" stroke-width="1.6" marker-start="url(#ah)" marker-end="url(#ah)"/>' % INK)

# Momentary
S.star(858, 881, 72, 32, "Momentary", accent="mode", n=18, size=18)
S.text(858, 934, "Disconnect power to exit", size=13, fill=MUTED, anchor="middle")

# =====================================================================
#  BOTTOM: strobes
# =====================================================================
S.group(12, 913, 535, 410, "", "strobe", tsize=19)
S.text(26, 945, "Strobe", size=19, weight=700, fill=INK)
S.text(26, 968, "Modes", size=19, weight=700, fill=INK)
for (cx, cy, ls) in [(190, 962, ["Lightning"]), (415, 962, ["Candle"]), (70, 1076, ["Police★", "Strobe"]),
                     (70, 1227, ["Tactical", "Strobe"]), (225, 1273, ["Party", "Strobe"]),
                     (392, 1273, ["Bike", "Flasher"])]:
    two = len(ls) > 1
    S.star(cx, cy, 58 if not two else 52, 30 if not two else 40, None, lines=ls, n=16, size=16)

S.card(206, 1016, 222, 72, None, "strobe")
S.text(296, 1050, "Candle Timer", size=18, weight=650, fill=INK, anchor="middle")
S.text(296, 1071, "1 blink = 5 minutes", size=FS, fill=BODY, anchor="middle")
S.stopwatch(390, 1058, 15)

S.card(130, 1102, 360, 120, None, "strobe")
S.text(144, 1126, "Actions", size=16, weight=650, fill=INK)
S.para(144, 1146, [
    "**1H:** Brighter / Faster __(except Police & Lightning)__",
    "**2H:** Dimmer / Slower __(except Police & Lightning)__",
    "**3C:** Next channel mode __(saved per strobe mode)__",
    "**4C:** Previous strobe mode",
    "**5C:** Momentary with selected strobe mode",
], size=12.5, lh=15.8)

S.arrow("M249,962 L353,962", "2C", (301, 962))
S.arrow("M472,966 C525,985 524,1090 524,1150 C524,1235 495,1262 450,1270", "2C", (524, 1128))
S.arrow("M336,1273 L283,1273", "2C", (309, 1273))
S.arrow("M174,1290 C140,1295 118,1280 104,1262", "2C", (138, 1290))
S.arrow("M70,1186 L70,1118", "2C", (70, 1152))
S.arrow("M80,1037 C88,990 108,965 130,962", "2C", (95, 995))
S.arrow("M392,992 C370,1000 345,1004 332,1014", "5H", 0.45)

# ---- standby aux / version / factory reset ------------------------------
S.card(574, 966, 324, 108, None, "aux")
S.auxsun(866, 992, 15)
S.text(588, 992, "Aux LED Mode in Standby", size=18, weight=650, fill=INK)
S.para(588, 1013, [
    "**7C:** Off → Low → High → Breathing★ →",
    "Fast Breathing★ → Heavy Breathing★ →",
    "Blinking → 2× Blink → 1× Blink",
    "**8H★:** brightness of Low / High __(Breathing = High)__",
], size=12.5, lh=15.5)

S.card(574, 1082, 324, 108, None, "aux")
S.wheel(866, 1108, 17)
S.text(588, 1107, "Aux LED Color in Standby", size=18, weight=650, fill=INK)
S.para(588, 1129, [
    "**7H:** release on selected color:",
    "Red → Yellow → Green → Cyan → Blue →",
    "Purple → White → Disco → Rainbow →",
    V("Voltage", "Voltage  ·  __E12 default: Breathing + Rainbow__"),
], size=12.5, lh=15.5)

S.card(574, 1198, 324, 76, None, "info")
S.text(884, 1222, "Version Check", size=18, weight=650, fill=INK, anchor="end")
S.text(884, 1243, "MODEL-YYYY-MM-DD(-SINCE-DIRTY)", size=12.5, weight=600, fill=BODY, anchor="end")
S.text(884, 1262, V("Brand+Product ID · Year · Month · Day", "E12 (Lume10) with this release: 0453-2026-10-26"), size=12.5, fill=MUTED, anchor="end")

S.card(574, 1284, 324, 38, None, "info", strip=False)
S.text(884, 1309, "Factory Reset", size=18, weight=650, fill=INK, anchor="end")

# =====================================================================
#  BOTTOM: blinky / utility
# =====================================================================
S.group(1030, 988, 958, 335, "Blinky / Utility Modes", "blinky", tsize=19, anchor="end")

S.card(1040, 1000, 300, 314, "Voltage Config", "blinky", tsize=18)
S.para(1052, 1048, [
    "1) Release after first flash",
    ">• Voltage correction (0.01 V steps)",
    ">>◦ **20C** = ±0.00 V (default)",
    ">>◦ **19C** = −0.01 V … **1C** = −0.19 V",
    ">>◦ **21C** = +0.01 V … **40C** = +0.20 V",
    "2) Release after second flash",
    ">• Post-off voltage display (RGB aux)",
    ">>◦ **0C** = off, **nC** = n seconds",
    "3) Release after third flash",
    ">• Aux low ramp level: **nC** = lit (low)",
    ">   from ramp level n, **0C** = never",
    "4) Release after fourth flash",
    ">• Aux high ramp level: **nC** = high",
    ">   from ramp level n, **0C** = never",
    "5) Release after fifth flash",
    V(">• Aux while on: **0C** none, **1C** single-color aux,", ">• Aux while on: **0C** none, **1C** button LED"),
    V(">   **2C** RGB aux, **3C** both", ">   __(default)__, **2C** RGB aux, **3C** both"),
], size=12.3, lh=15.2)

# Batt check node
S.add('<rect class="card" x="1382" y="1031" width="116" height="35" rx="8" fill="#FFFFFF" stroke="#0F172A" stroke-width="1.6" filter="url(#sh)"/>')
S.add('<path d="M1382.8,1039 Q1382.8,1031.8 1390,1031.8 H1432 V1065.2 H1390 Q1382.8,1065.2 1382.8,1058 Z" fill="#0F172A"/>')
S.add('<rect x="1498" y="1041" width="5" height="15" rx="1.5" fill="#0F172A"/>')
S.text(1407, 1054, "Batt", size=16, weight=700, fill="#FFFFFF", anchor="middle")
S.text(1465, 1054, "Check", size=16, weight=700, fill=INK, anchor="middle")

# Temp check
S.thermo(1590, 1049, 26)
S.text(1590, 1018, "Temp Check", size=16, weight=650, fill=INK, anchor="middle")

# Batt check options (replaces the old "Next channel mode (number blinks)" box)
S.card(1430, 1110, 172, 96, None, "blinky")
S.para(1442, 1131, [
    "**3C:** blink channel",
    "**1H★:** Batt Color ⇄ digits",
    "**8H★:** POVD brightness",
    "   __(while in Batt Color)__",
    "**2H★:** Powerbank host",
], size=12, lh=15.6)

S.star(1428, 1262, 48, 30, "SOS", accent="blinky", fill="#FFFBEB", n=14, size=17)
S.star(1590, 1262, 58, 30, "Beacon", accent="blinky", fill="#FFFBEB", n=16, size=17)
S.stopwatch(1772, 1267, 18)
S.text(1772, 1308, "Beacon frequency", size=15, weight=650, fill=INK, anchor="middle")
S.text(1805, 1265, "1 blink = 1 second pause", size=12.5, fill=BODY)
S.text(1805, 1282, "Smooth Steps: soft fade", size=12, fill=MUTED)

S.card(1730, 1048, 248, 160, "Thermal Configuration", "blinky", tsize=18)
S.para(1742, 1096, [
    "1) Release after first flash",
    ">• Set current temperature",
    ">>◦ Click n times for n °C",
    "2) Release after second flash",
    ">• Set temperature limit",
    ">>◦ Click n times for n + 30 °C",
    ">>   __(max. 70 °C)__",
], size=12.5, lh=15.6)

S.arrow("M1505,1048 L1564,1048", "2C", (1534, 1048))
S.arrow("M1610,1104 C1645,1135 1645,1200 1612,1228", "2C", (1638, 1166))
S.arrow("M1534,1268 C1510,1282 1490,1282 1474,1272", "2C", (1505, 1281))
S.arrow("M1405,1236 C1385,1180 1390,1110 1414,1070", "2C", (1396, 1112))
S.arrow("M1452,1068 L1466,1108", dash="3 4")
S.arrow("M1381,1052 C1360,1090 1365,1180 1344,1192", "7H", (1366, 1145))
S.arrow("M1610,1046 C1665,1056 1695,1120 1728,1150", "7H", (1676, 1094))
S.arrow("M1650,1262 L1748,1265", "HOLD", (1699, 1263))

# =====================================================================
#  ARROWS: ON
# =====================================================================
# fan to the left column: order of start points (left→right) = 10C, 5H, 9H
S.arrow("M646,790 C628,705 612,628 575,606", "10C", (614, 630))
S.arrow("M658,785 C652,640 640,530 575,513", "5H", (598, 519))
S.arrow("M670,783 C660,600 645,262 576,243", "9H", (640, 420))
S.arrow("M630,806 C600,700 520,668 470,668 L196,668 C172,668 165,660 165,646", "10H", (400, 668))
S.arrow("M688,783 C698,690 716,600 733,514", "7H", (722, 560))
S.arrow("M703,786 C712,700 735,640 764,626", "6C", (742, 642))
S.arrow("M724,806 C770,770 850,748 880,701", "3C", (790, 770), sub="(1 channel)", subpos="inside")
S.arrow("M627,821 L498,821", "3C", (560, 821))
S.arrow("M645,852 C560,915 330,915 246,872", "3H · 4H · 8H", (430, 901))
S.arrow("M736,821 L1099,821", "1C", (917, 821), start=True)
S.arrow("M706,854 C722,880 755,882 784,881", "5C", (742, 878))

# =====================================================================
#  ARROWS: OFF
# =====================================================================
S.arrow("M1106,806 C1080,785 1072,772 1042,772", "10C", (1068, 779))
S.arrow("M1110,843 C1050,872 990,880 932,881", "5C", (1020, 869))
S.arrow("M1114,848 C1080,930 1000,946 900,946 L700,946 C620,946 600,940 549,940", "3H", (640, 946), sub="(mode memorized)", subpos="inside")
# bus to the aux / version / reset column (left→right = top→bottom target)
S.arrow("M1128,854 C1115,935 1000,925 992,985 C988,1010 950,1018 900,1018", "7C / 8H★", (944, 1017))
S.arrow("M1136,857 C1125,945 1006,935 1003,1000 C1000,1070 970,1126 900,1128", "7H", (945, 1126))
S.arrow("M1143,858 C1132,950 1013,945 1012,1010 L1012,1080 C1012,1200 975,1236 900,1236", "15+C", (950, 1234))
S.arrow("M1150,859 C1140,955 1022,955 1020,1020 L1020,1100 C1020,1250 980,1303 900,1303", "13H", (950, 1302))
S.arrow("M1158,859 C1158,955 1180,976 1250,976 L1385,976 C1425,976 1432,995 1432,1027", "3C", (1250, 976))
S.arrow("M1172,855 C1185,900 1230,906 1293,906", "1H", (1235, 902))
S.arrow("M1204,812 C1240,792 1265,783 1293,783", "1C", (1252, 790), start=True)
S.arrow("M1192,793 C1212,720 1250,672 1293,666", "2C", (1220, 714))
S.arrow("M1178,786 C1186,690 1232,632 1293,626", "2H", (1250, 629), sub="(momentary)", subpos="above")
S.arrow("M1294,772 C1250,745 1250,668 1294,642", "2C", 0.3, start=True)
S.arrow("M1164,783 C1168,620 1200,590 1300,590 L1450,590 C1505,590 1516,640 1516,798", "4C", (1343, 590))
S.arrow("M1151,783 C1150,595 1180,569 1260,569 L1400,569 C1437,569 1437,520 1437,448", "9H", (1253, 569))
S.arrow("M1126,790 C1105,700 1048,580 1000,514", "10H", 0.5)
S.arrow("M1141,785 C1130,700 1115,600 1112,504", "6C", (1121, 662))
S.arrow("M1157,388 L1157,338", "7H", (1157, 363))

# =====================================================================
#  ARROWS: LOCKOUT  (node = card 1461..1571 x 801..845)
# =====================================================================
S.arrow("M1534,800 L1534,560", "3H", (1534, 690))
S.arrow("M1564,800 Q1574,792 1574,775 L1574,592 Q1574,570 1596,570 L1639,570", "10H", (1574, 680))
S.arrow("M1571,813 L1639,641", "7C", 0.58)
S.arrow("M1571,823 L1639,756", "7H", 0.55)
S.arrow("M1571,833 L1639,861", "1H", 0.55)
S.arrow("M1571,842 L1639,940", "2H", 0.55)
S.arrow("M1476,845 C1470,898 1450,906 1395,906", "4H", (1440, 905))
S.arrow("M1395,783 C1430,786 1445,812 1461,820", "4C", (1428, 792), start=True)
S.arrow("M1476,801 C1470,700 1450,666 1395,666", "5C", (1462, 700))
S.arrow("M1516,846 C1516,930 1430,940 1320,940 C1200,940 1170,922 1166,861", "3C", (1330, 940))

# ---- nodes on top of arrows
S.card(1461, 800, 110, 46, None, "lock", r=10, fill="#F5F3FF", strip=False)
S.lock(1482, 821, 20, col="#5B21B6")
S.text(1500, 822, "Lockout", size=16, weight=700, fill=INK)
S.text(1500, 839, "Mode", size=12.5, weight=600, fill="#6D28D9")
S.node(679, 821, 52, 38, "ON", size=34, glow="#FACC15")
S.node(1155, 821, 54, 38, "OFF", size=34)

# ---- small footer -------------------------------------------------------
S.text(1988, 1340, "Layout after the original Andúril 2 diagrams (lemmy.world/post/1038159) · redrawn & updated 2026-11",
       size=10, fill=MUTED, anchor="end")

open(sys.argv[1], "w").write(S.render())
