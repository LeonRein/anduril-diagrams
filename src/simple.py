# SPDX-License-Identifier: GPL-3.0-only
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# usage: python3 simple.py OUT.svg [generic|e12]
from common import *
import common
E12 = len(sys.argv) > 2 and sys.argv[2] == "e12"
common.SHOW_STAR = not E12


def V(generic, e12):
    return e12 if E12 else generic

# Original layout was 1024x544; everything here is in 2x coordinates.
S = SVG(2048, 1120)
B = 18      # body size
PL = 20     # pill label size

# ---------------------------------------------------------------- extras group (new)
S.group(16, 40, 960, 252, "", "new")
S.text(38, 78, "Extra functions in this Simple UI", size=24, weight=700, fill=INK)
S.text(38, 104, V("Extended Simple UI — enabled by Fireflies (e.g. E12 Eclipse) and some other brands", "Extended Simple UI — enabled by Fireflies on the E12 Eclipse"), size=15, fill=MUTED)
S.para(40, 144, [
    "• **Ramp → 3C:** toggle smooth / stepped",
    "   __(6C if more than one channel is on)__",
    "• **Ramp → 5H:** Sunset timer",
    "   __(1 blink = 5 minutes)__",
    "• **Off → 7C / 7H:** aux LED pattern / color",
], size=19, lh=33)
S.para(500, 144, [
    "• **Lockout → 7C / 7H:** aux pattern / color",
    "• **Batt Check → 1H★:** Batt Color",
    "   __(voltage shown as color)__",
    "• **Batt Check → 2H★:** Powerbank host",
    "• __Strobes / blinkies: Advanced UI only__",
], size=19, lh=33)

# ---------------------------------------------------------------- actions
S.card(1000, 40, 476, 214, "Actions", "info", tsize=24)
S.para(1014, 110, [
    "**1C:** Click",
    "**1H:** Hold",
    "**2C:** Click, Click",
    "**2H:** Click, Hold",
], size=B, lh=26)
S.para(1232, 110, [
    "**nC / nH:** n presses",
    "__Number entry in menus:__",
    "**Click** = +1",
    "**Hold** = +10",
], size=B, lh=26)
S.text(1014, 214, "__Ovals & lock = modes · boxes = actions / menus__", size=16)
S.text(1014, 236, "__ON = Ramp: same mode, the bar shows its levels__", size=16)

# ---------------------------------------------------------------- title
S.card(1504, 40, 528, 494, None, "#0F172A")
S.text(1532, 156, "Andúril 2", size=108, weight=800, fill=INK, ls="-2")
S.text(1534, 222, V("Multi-Channel", "Fireflies E12 Eclipse"), size=V(50, 36), weight=700, fill=INK)
S.text(1534, 276, "Simple UI", size=44, weight=600, fill="#059669")
S.para(1534, 330, V([
    "**Firmware:** Andúril 2 release 2026-10-26",
    "**Diagram revision:** 2026-11-25",
    "**Source:** github.com/ToyKeeper/anduril",
], [
    "**Firmware:** fireflies-lume10 · model 0453",
    "**Release:** 2026-10-26 · **Diagram:** 2026-11-25",
    "**Source:** github.com/ToyKeeper/anduril",
]), size=20, lh=30)
S.add('<rect x="1524" y="428" width="488" height="92" rx="10" fill="#FFFBEB" stroke="#FCD34D"/>')
S.para(1540, 457, V([
    "**NOTE:** Some features are hardware-specific",
    "or may be disabled by manufacturers.",
    "★ = only on some lights (e.g. FF E12 Eclipse)",
], [
    "**Simple UI defaults:** stepped, 10–130, 5 steps",
    "2C = ceiling (130), no turbo in Simple UI",
    "Only Main channel on → Ramp 3C = ramp style",
]), size=17.5, lh=24)

# ---------------------------------------------------------------- aux legend
S.card(1504, 550, 528, 212, None, "aux")
S.text(1768, 590, "Aux LED Color for Cell Voltage", size=24, weight=650, fill=INK, anchor="middle")
S.wheel(1570, 652, 34)
S.battery(1640, 618, 340, 70, size=15)
S.text(1768, 736, V("Single-color aux: fast blink 3.3 – 2.9 V, off below 2.9 V", "Standby: 6 colors as shown · post-off display: smooth shades"), size=16, fill=BODY, anchor="middle")

# ---------------------------------------------------------------- left boxes
S.card(206, 400, 492, 60, None, "info", strip=False)
S.text(680, 440, "Factory Reset", size=24, weight=650, fill=INK, anchor="end")
S.card(206, 480, 492, 116, None, "info")
S.text(680, 520, "Version Check", size=24, weight=650, fill=INK, anchor="end")
S.text(680, 550, "MODEL-YYYY-MM-DD(-SINCE-DIRTY)", size=17, weight=600, fill=BODY, anchor="end")
S.text(680, 578, V("Brand+Product ID · Year · Month · Day", "E12 with this release: 0453-2026-10-26"), size=17, fill=MUTED, anchor="end")

S.card(16, 620, 288, 288, "Next Channel Mode", "mode", tsize=24)
S.text(30, 686, V("(3C to cycle, stays in Ramp)", "(3C to cycle, stays in Ramp)"), size=17, fill=MUTED)
S.para(34, 722, V([
    "• Channel 1",
    "• Channel 2",
    "• 50/50",
    "• Tint Ramp",
    "• Autotint",
    "• HSV color★",
    "• Aux LED Channels",
], [
    "• Main LEDs",
    "• HSV color wheel",
    "• Aux Red · Yellow",
    "• Aux Green · Cyan",
    "• Aux Blue · Purple",
    "• Aux White",
    "__only Main is on at factory__",
]), size=B, lh=26)

S.card(414, 832, 212, 112, None, "mode")
S.text(520, 878, V("Tint Ramp", "Change Hue"), size=24, weight=650, fill=INK, anchor="middle")
S.text(520, 910, V("(if enabled)", "(HSV channel only)"), size=17, fill=MUTED, anchor="middle")

S.card(362, 1016, 342, 62, None, "info", strip=False)
S.text(533, 1056, "Switch to Advanced UI", size=24, weight=650, fill=INK, anchor="middle")

# ---------------------------------------------------------------- right boxes
S.card(1504, 782, 528, 106, None, "lock")
S.moon(1568, 835, 26)
S.text(1616, 830, "Momentary Moon", size=24, weight=650, fill=INK)
S.text(1616, 860, "Lowest floor", size=16.5, fill=MUTED)
S.card(1504, 916, 528, 112, None, "lock")
S.moon(1568, 972, 26)
S.text(1616, 962, "Momentary Low", size=24, weight=650, fill=INK)
S.text(1616, 992, "Highest floor or manual memory", size=16.5, fill=MUTED)

# ---------------------------------------------------------------- ramp
gid = S.nid("rb")
S.add('<defs><linearGradient id="%s" x1="0" x2="0" y1="0" y2="1">'
      '<stop offset="0" stop-color="#FEF9C3"/><stop offset="0.45" stop-color="#FDE68A"/>'
      '<stop offset="1" stop-color="#64748B"/></linearGradient></defs>' % gid)
S.glow_rect(1060, 490, 144, 434, 14)
S.add('<rect class="card" x="1060" y="490" width="144" height="434" rx="14" fill="url(#%s)" stroke="#94A3B8" filter="url(#sh)"/>' % gid)
S.text(1132, 522, "Ceiling", size=19, weight=650, fill=INK, anchor="middle")
S.text(1132, 912, "Floor", size=19, weight=650, fill="#FFFFFF", anchor="middle")
S.text(1118, 708, "Ramp", size=32, weight=700, fill=INK, anchor="middle", rotate=-90)
S.text(1154, 708, "2H Down / 1H Up", size=18, weight=500, fill=INK, anchor="middle", rotate=-90)
S.add('<line x1="1180" y1="545" x2="1180" y2="880" stroke="%s" stroke-width="2" marker-start="url(#ah)" marker-end="url(#ah)"/>' % INK)

# batt check node + notes
S.add('<rect class="card" x="944" y="1020" width="174" height="54" rx="11" fill="#FFFFFF" stroke="#0F172A" stroke-width="2" filter="url(#sh)"/>')
S.add('<path d="M945,1031 Q945,1021 955,1021 H1022 V1073 H955 Q945,1073 945,1063 Z" fill="#0F172A"/>')
S.add('<rect x="1118" y="1036" width="7" height="22" rx="2" fill="#0F172A"/>')
S.text(983, 1055, "Batt", size=24, weight=700, fill="#FFFFFF", anchor="middle")
S.text(1070, 1055, "Check", size=24, weight=700, fill=INK, anchor="middle")
S.para(1146, 1040, [
    "Simple UI: displays voltage once",
    "Advanced UI: displays voltage continuously",
    "__1H★ Batt Color · 2H★ Powerbank host__",
], size=16.5, lh=22)

# ---------------------------------------------------------------- arrows
A = S.arrow
A("M448,710 L308,710", "3C", (378, 710), lsize=PL)
A("M594,710 L768,710", "1C", (681, 710), lsize=PL, start=True)
A("M918,710 L1056,710", "1C", (987, 710), lsize=PL, start=True)
A("M1208,710 L1314,710", "4C", (1261, 710), lsize=PL, start=True)
A("M520,768 L520,830", "3H", 0.5, lsize=PL)
# OFF top, left→right: 15+C, 13H, 4C, 2C, 2H
A("M814,660 C800,600 770,540 702,540", "15+C", 0.6, lsize=PL)
A("M826,658 C815,520 780,430 702,430", "13H", 0.72, lsize=PL)
A("M840,656 C840,430 870,412 960,412 L1340,412 C1385,412 1392,440 1392,688", "4C", (1160, 412), lsize=PL)
A("M852,657 C858,560 930,500 1056,496", "2C", 0.6, lsize=PL)
A("M874,660 C935,625 990,540 1056,532", "2H", 0.13, lsize=PL, sub="(momentary)", subpos="right")
A("M1056,694 C1026,668 1026,600 1056,572", "2C", 0.2, lsize=PL, start=True)
# OFF bottom, left→right: 10H, 3C→batt, 3C←lockout, 1H
A("M818,764 C805,900 790,1046 708,1046", "10H", 0.55, lsize=PL)
A("M832,766 C832,960 870,1046 940,1046", "3C", 0.72, lsize=PL)
A("M1392,748 C1392,940 1370,970 1300,970 L940,970 C866,970 848,930 848,768", "3C", (1100, 970), lsize=PL)
A("M866,764 C870,900 935,920 1056,920", "1H", 0.6, lsize=PL)
# lockout card 1322..1462 x 690..746
A("M1345,748 C1345,900 1300,920 1208,920", "4H", 0.55, lsize=PL)
A("M1340,690 C1338,560 1300,500 1208,500", "5C", 0.4, lsize=PL)
A("M1440,690 C1440,380 1420,360 1360,360 L230,360 C170,360 154,380 154,616", "3H", (790, 360), lsize=PL,
  sub="(to cycle)", subpos="inside")
A("M1446,748 C1452,815 1468,835 1500,835", "1H", 0.5, lsize=PL)
A("M1420,748 C1420,930 1450,972 1500,972", "2H", 0.55, lsize=PL)

# lockout + nodes on top
S.card(1316, 690, 152, 58, None, "lock", r=12, fill="#F5F3FF", strip=False)
S.lock(1344, 717, 28, col="#5B21B6")
S.text(1368, 716, "Lockout", size=21, weight=700, fill=INK)
S.text(1368, 738, "Mode", size=17, weight=600, fill="#6D28D9")
S.node(520, 710, 74, 54, "ON", size=50, glow="#FACC15", sub="Ramp mode")
S.node(844, 710, 76, 54, "OFF", size=50)

S.text(2036, 1112, "Based on the Andúril 2 diagrams by containerfan (github.com/containerfan/anduril2-diagrams) · redrawn & updated 2026-11 · GPL-3.0",
       size=14, fill=MUTED, anchor="end")

open(sys.argv[1], "w").write(S.render())
