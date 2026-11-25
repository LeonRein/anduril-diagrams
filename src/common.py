# SPDX-License-Identifier: GPL-3.0-only
"""Shared SVG helpers for the Anduril diagrams."""
import math, os, re
from PIL import ImageFont

# Inter font (Ubuntu/Debian: apt install fonts-inter); override with INTER_FONT_DIR
FONTDIR = os.environ.get("INTER_FONT_DIR", "/usr/share/fonts/opentype/inter/").rstrip("/") + "/"
_fonts = {}


def measure(s, size, weight=400):
    key = (size, weight)
    if key not in _fonts:
        name = {400: "Inter-Regular.otf", 500: "Inter-Medium.otf",
                600: "Inter-SemiBold.otf", 700: "Inter-Bold.otf",
                800: "Inter-ExtraBold.otf"}[weight]
        _fonts[key] = ImageFont.truetype(FONTDIR + name, max(1, int(round(size * 4))))
    return _fonts[key].getlength(s) / 4.0


# ---------------------------------------------------------------- palette
BG = "#F3F5F9"
CARD = "#FFFFFF"
STROKE = "#D5DCE6"
INK = "#0F172A"
BODY = "#334155"
MUTED = "#64748B"
ARROW = "#3F4B5E"

ACC = {
    "config": "#6366F1",   # indigo  – config menus
    "mode": "#0EA5E9",     # sky     – modes / actions
    "aux": "#14B8A6",      # teal    – aux LEDs
    "blinky": "#F59E0B",   # amber   – blinky / utility
    "strobe": "#F43F5E",   # rose    – strobe group
    "lock": "#8B5CF6",     # violet  – lockout
    "info": "#64748B",     # slate   – info
    "new": "#16A34A",
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


SHOW_STAR = True


def rich(s):
    """**bold**, __muted__, ★ markup -> tspans."""
    if not SHOW_STAR:
        s = s.replace("★", "")
    out = []
    parts = re.split(r"(\*\*.*?\*\*|__.*?__|★)", s)
    for p in parts:
        if not p:
            continue
        if p.startswith("**") and p.endswith("**"):
            out.append('<tspan font-weight="650" fill="%s">%s</tspan>' % (INK, esc(p[2:-2])))
        elif p.startswith("__") and p.endswith("__"):
            out.append('<tspan fill="%s">%s</tspan>' % (MUTED, esc(p[2:-2])))
        elif p == "★":
            out.append('<tspan fill="#D97706" font-weight="700">★</tspan>')
        else:
            out.append(esc(p))
    return "".join(out)


def plain(s):
    return re.sub(r"\*\*|__", "", s)


def path_points(d, step=1.0):
    """Sample an absolute M/L/C/Q/H/V path into points."""
    toks = re.findall(r"[MLCQHVZ]|-?\d+(?:\.\d+)?", d)
    pts, i, cmd, cur = [], 0, None, (0.0, 0.0)
    def take(n):
        nonlocal i
        v = [float(t) for t in toks[i:i + n]]; i += n; return v
    while i < len(toks):
        if toks[i] in "MLCQHVZ":
            cmd = toks[i]; i += 1
            if cmd == "Z": continue
        if cmd == "M":
            x, y = take(2); cur = (x, y); pts.append(cur); cmd = "L"
        elif cmd in "LHV":
            if cmd == "L": x, y = take(2)
            elif cmd == "H": x, y = take(1)[0], cur[1]
            else: x, y = cur[0], take(1)[0]
            n = max(1, int(math.hypot(x - cur[0], y - cur[1]) / step))
            for k in range(1, n + 1):
                pts.append((cur[0] + (x - cur[0]) * k / n, cur[1] + (y - cur[1]) * k / n))
            cur = (x, y)
        elif cmd in "CQ":
            if cmd == "C":
                x1, y1, x2, y2, x, y = take(6)
            else:
                qx, qy, x, y = take(4)
                x1, y1 = cur[0] + 2 / 3 * (qx - cur[0]), cur[1] + 2 / 3 * (qy - cur[1])
                x2, y2 = x + 2 / 3 * (qx - x), y + 2 / 3 * (qy - y)
            n = 200
            for k in range(1, n + 1):
                t = k / n; u = 1 - t
                pts.append((u**3 * cur[0] + 3 * u * u * t * x1 + 3 * u * t * t * x2 + t**3 * x,
                            u**3 * cur[1] + 3 * u * u * t * y1 + 3 * u * t * t * y2 + t**3 * y))
            cur = (x, y)
    return pts


def snap(d, at):
    pts = path_points(d)
    if isinstance(at, (int, float)):
        L = [0.0]
        for a, b in zip(pts, pts[1:]):
            L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
        target = at * L[-1]
        k = min(range(len(L)), key=lambda j: abs(L[j] - target))
        return pts[k]
    return min(pts, key=lambda q: (q[0] - at[0]) ** 2 + (q[1] - at[1]) ** 2)


class SVG:
    def __init__(self, w, h, scale_font=1.0):
        self.w, self.h = w, h
        self.o = []
        self.uid = 0
        self.fs = scale_font
        self.late = []
        self.defer = False

    def nid(self, p="i"):
        self.uid += 1
        return "%s%d" % (p, self.uid)

    def add(self, s):
        self.o.append(s)

    # ------------------------------------------------------------ text
    def text(self, x, y, s, size=13, weight=400, anchor="start", fill=BODY,
             italic=False, halo=False, family=None, rotate=None, ls=None):
        attrs = 'x="%.1f" y="%.1f" font-size="%.2f" font-weight="%d" text-anchor="%s" fill="%s"' % (
            x, y, size, weight, anchor, fill)
        if italic:
            attrs += ' font-style="italic"'
        if halo:
            attrs += ' stroke="%s" stroke-width="4" stroke-linejoin="round" paint-order="stroke"' % (
                halo if isinstance(halo, str) else BG)
        if family:
            attrs += ' font-family="%s"' % family
        if ls is not None:
            attrs += ' letter-spacing="%s"' % ls
        if rotate is not None:
            attrs += ' transform="rotate(%s %.1f %.1f)"' % (rotate, x, y)
        self.add('<text %s>%s</text>' % (attrs, rich(s)))

    def para(self, x, y, rows, size=13, lh=18, fill=BODY, indent=16):
        """rows: strings; leading '>' chars = indent level; '• ' bullets drawn as dots.
        returns y after last line."""
        for r in rows:
            if r is None:
                y += lh * 0.45
                continue
            lvl = 0
            while r.startswith(">"):
                lvl += 1
                r = r[1:]
            xx = x + lvl * indent
            if r.startswith("   "):
                xx += 12
                r = r.lstrip(" ")
            if r.startswith("• "):
                self.add('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="%s"/>' % (
                    xx + 3, y - size * 0.33, size * 0.16, MUTED if lvl > 1 else BODY))
                xx += 12
                r = r[2:]
            elif r.startswith("◦ "):
                self.add('<circle cx="%.1f" cy="%.1f" r="%.2f" fill="none" stroke="%s" stroke-width="1"/>' % (
                    xx + 3, y - size * 0.33, size * 0.17, MUTED))
                xx += 12
                r = r[2:]
            elif re.match(r"^\d\+?\)|^\d", r) and ") " in r[:5]:
                num, rest = r.split(") ", 1)
                bw = self.badge(xx + 8, y - size * 0.35, num, size)
                xx += max(21, bw + 9)
                r = rest
            self.text(xx, y, r, size=size, fill=fill)
            y += lh
        return y

    def badge(self, cx, cy, num, size):
        r = size * 0.62
        w = max(2 * r, measure(num, size * 0.78, 700) + size * 0.7)
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#EEF2FF"/>' % (
            cx - w / 2, cy - r, w, 2 * r, r))
        self.text(cx, cy + size * 0.28, num, size=size * 0.78, weight=700, anchor="middle", fill="#4338CA")
        return w

    # ------------------------------------------------------------ shapes
    def card(self, x, y, w, h, title=None, accent="info", tsize=18, sub=None,
             tx=None, ty=None, anchor="start", r=12, fill=CARD, strip=True):
        self.add('<rect class="card" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%d" fill="%s" stroke="%s" '
                 'stroke-width="1" filter="url(#sh)"/>' % (x, y, w, h, r, fill, STROKE))
        col = ACC.get(accent, accent)
        if strip:
            # thin coloured top strip that follows the rounded corners
            self.add('<path d="M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f H%.1f Q%.1f,%.1f %.1f,%.1f V%.1f H%.1f Z" fill="%s"/>' % (
                x + 0.5, y + 5, x + 0.5, y + 0.5, x + r, y + 0.5, x + w - r, x + w - 0.5, y + 0.5,
                x + w - 0.5, y + 5, y + 5, x + 0.5, col))
        if title:
            if tx is None:
                tx = x + 14 if anchor == "start" else (x + w / 2 if anchor == "middle" else x + w - 14)
            if ty is None:
                ty = y + 12 + tsize
            self.text(tx, ty, title, size=tsize, weight=650, fill=INK, anchor=anchor)
            if sub:
                self.text(tx, ty + tsize * 0.95, sub, size=tsize * 0.62, fill=MUTED, anchor=anchor)

    def group(self, x, y, w, h, title, accent, tsize=19, tx=None, anchor="start"):
        col = ACC.get(accent, accent)
        self.add('<rect class="grp" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="18" fill="%s" fill-opacity="0.06" '
                 'stroke="%s" stroke-opacity="0.55" stroke-width="1.6" stroke-dasharray="7 6"/>' % (
                     x, y, w, h, col, col))
        if tx is None:
            tx = x + 16 if anchor == "start" else x + w - 16
        if title:
            self.text(tx, y + 14 + tsize, title, size=tsize, weight=700, fill=INK, anchor=anchor)

    def star(self, cx, cy, rx, ry, label, accent="strobe", n=16, size=17, lines=None, fill=None):
        col = ACC.get(accent, accent)
        pts = []
        for i in range(2 * n):
            a = math.pi * i / n - math.pi / 2
            k = 1.0 if i % 2 == 0 else 0.80
            pts.append("%.1f,%.1f" % (cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        self.add('<polygon class="card" points="%s" fill="%s" stroke="%s" stroke-width="1.6" stroke-linejoin="round" filter="url(#sh)"/>' % (
            " ".join(pts), fill or "#FFF1F3" if accent == "strobe" else (fill or "#F0F9FF"), col))
        ls = lines or [label]
        y0 = cy + size * 0.35 - (len(ls) - 1) * size * 0.58
        for i, l in enumerate(ls):
            self.text(cx, y0 + i * size * 1.16, l, size=size, weight=600, fill=INK, anchor="middle")

    def node(self, cx, cy, rx, ry, label, size=34, glow=None):
        gid = self.nid("ng")
        self.add('<defs><radialGradient id="%s" cx="50%%" cy="35%%" r="70%%">'
                 '<stop offset="0" stop-color="#334155"/><stop offset="1" stop-color="#0B1220"/></radialGradient></defs>' % gid)
        if glow:
            self.add('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="none" stroke="%s" stroke-width="4" stroke-opacity="0.45"/>' % (
                cx, cy, rx + 3, ry + 3, glow))
        self.add('<ellipse class="card node" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="url(#%s)" filter="url(#sh2)"/>' % (cx, cy, rx, ry, gid))
        self.text(cx, cy + size * 0.36, label, size=size, weight=800, fill="#FFFFFF", anchor="middle", ls="0.5")

    # ------------------------------------------------------------ arrows
    def arrow(self, d, label=None, at=None, start=False, end=True, sub=None, lsize=14,
              color=ARROW, width=1.6, dash=None, subpos="right"):
        attrs = 'd="%s" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round" stroke-linejoin="round"' % (
            d, color, width)
        if end:
            attrs += ' marker-end="url(#ah)"'
        if start:
            attrs += ' marker-start="url(#ah)"'
        if dash:
            attrs += ' stroke-dasharray="%s"' % dash
        aid = self.nid("a")
        self.add('<path class="arr" data-id="%s" %s/>' % (aid, attrs))
        if label:
            at = snap(d, at if at is not None else 0.5)
            self.late.append((at[0], at[1], label, lsize, sub, subpos, aid))

    def pill(self, cx, cy, label, size=14, sub=None, subpos="right"):
        tw = measure(label, size, 700)
        ph = size + 8
        pw = tw + size * 0.95
        if sub and subpos == "inside":
            sw = measure(sub, size * 0.72, 500)
            pw = tw + sw + size * 1.25
            x0 = cx - pw / 2
            self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF" stroke="#B8C3D3" stroke-width="1"/>' % (
                x0, cy - ph / 2, pw, ph, ph / 2))
            self.text(x0 + size * 0.48, cy + size * 0.36, label, size=size, weight=700, fill=INK)
            self.text(x0 + size * 0.48 + tw + size * 0.3, cy + size * 0.33, sub, size=size * 0.72, weight=500, fill=MUTED)
            return
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF" stroke="#B8C3D3" stroke-width="1"/>' % (
            cx - pw / 2, cy - ph / 2, pw, ph, ph / 2))
        self.text(cx, cy + size * 0.36, label, size=size, weight=700, fill=INK, anchor="middle")
        if sub:
            subs = sub if isinstance(sub, list) else [sub]
            if subpos == "left":
                y0 = cy + size * 0.3 - (len(subs) - 1) * size * 0.45
                for i, t in enumerate(subs):
                    self.text(cx - pw / 2 - 5, y0 + i * size * 0.9, t, size=size * 0.8,
                              weight=500, fill=MUTED, anchor="end", halo=True)
            elif subpos == "above":
                for i, t in enumerate(subs):
                    self.text(cx, cy - ph / 2 - 4 - i * size * 0.95, t, size=size * 0.8,
                              weight=500, fill=MUTED, anchor="middle", halo=True)
            elif subpos == "below":
                for i, s in enumerate(subs):
                    self.text(cx, cy + ph / 2 + size * 0.95 + i * size * 0.95, s, size=size * 0.8,
                              weight=500, fill=MUTED, anchor="middle", halo=True)
            else:
                for i, s in enumerate(subs):
                    self.text(cx + pw / 2 + 5, cy + size * 0.3 + i * size * 0.9, s, size=size * 0.72,
                              weight=500, fill=MUTED, halo=True)

    def flush_pills(self):
        late, self.late = self.late, []
        for (x, y, l, ls, sub, sp, aid) in late:
            self.add('<g class="pillg" data-id="%s" data-label="%s">' % (aid, esc(l)))
            self.pill(x, y, l, ls, sub=sub, subpos=sp)
            self.add('</g>')

    # ------------------------------------------------------------ icons
    def stopwatch(self, cx, cy, r, col=INK, fillwedge=True):
        self.add('<g class="icon">')
        self.add('<g fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round">' % (col, r * 0.16))
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f"/>' % (cx, cy, r))
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx - r * 0.3, cy - r * 1.32, cx + r * 0.3, cy - r * 1.32))
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx, cy - r * 1.32, cx, cy - r * 1.02))
        self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (cx + r * 0.78, cy - r * 0.95, cx + r * 0.95, cy - r * 1.12))
        self.add('</g>')
        if fillwedge:
            rr = r * 0.66
            self.add('<path d="M%.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 1 1 %.1f,%.1f Z" fill="%s"/>' % (
                cx, cy, cx, cy - rr, rr, rr, cx - rr * 0.98, cy - rr * 0.2, col))
        self.add('</g>')

    def lock(self, cx, cy, s, col=INK):
        self.add('<g class="icon">')
        # body
        self.add('<path d="M%.1f,%.1f v-%.1f a%.1f,%.1f 0 0 1 %.1f,0 v%.1f" fill="none" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (
            cx - s * 0.32, cy - s * 0.05, s * 0.22, s * 0.32, s * 0.32, s * 0.64, s * 0.22, col, s * 0.13))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>' % (
            cx - s * 0.5, cy - s * 0.08, s, s * 0.72, s * 0.12, col))
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF"/>' % (cx, cy + s * 0.22, s * 0.1))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#FFFFFF"/>' % (
            cx - s * 0.04, cy + s * 0.24, s * 0.08, s * 0.2, s * 0.03))
        self.add('</g>')

    def moon(self, cx, cy, r, col="#4338CA"):
        self.add('<g class="icon">')
        mid = self.nid("mm")
        self.add('<defs><mask id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#fff"/>'
                 '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#000"/></mask></defs>' % (
                     mid, cx - r * 2, cy - r * 2, r * 4, r * 4, cx + r * 0.55, cy - r * 0.45, r * 0.9))
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" mask="url(#%s)"/>' % (cx, cy, r, col, mid))
        self.add('</g>')

    def auxsun(self, cx, cy, r, col=INK):
        self.add('<g class="icon">')
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (cx, cy, r * 0.55, col, r * 0.12))
        self.add('<path d="M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f Z" fill="%s"/>' % (
            cx, cy - r * 0.55, r * 0.55, r * 0.55, cx, cy + r * 0.55, col))
        for i in range(8):
            a = i * math.pi / 4
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (
                cx + r * 0.78 * math.cos(a), cy + r * 0.78 * math.sin(a),
                cx + r * 1.0 * math.cos(a), cy + r * 1.0 * math.sin(a), col, r * 0.12))
        self.add('</g>')

    def wheel(self, cx, cy, r, w=None):
        self.add('<g class="icon">')
        w = w or r * 0.38
        cols = ["#EF4444", "#F97316", "#EAB308", "#84CC16", "#22C55E", "#14B8A6",
                "#06B6D4", "#3B82F6", "#6366F1", "#8B5CF6", "#D946EF", "#EC4899"]
        n = len(cols)
        rm = r - w / 2
        for i, c in enumerate(cols):
            a0 = 2 * math.pi * i / n - math.pi / 2
            a1 = 2 * math.pi * (i + 1) / n - math.pi / 2 + 0.02
            self.add('<path d="M%.2f,%.2f A%.2f,%.2f 0 0 1 %.2f,%.2f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (
                cx + rm * math.cos(a0), cy + rm * math.sin(a0), rm, rm,
                cx + rm * math.cos(a1), cy + rm * math.sin(a1), c, w))
        self.add('</g>')

    def thermo(self, cx, cy, s, col=INK):
        self.add('<g class="icon">')
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="none" stroke="%s" stroke-width="%.1f"/>' % (
            cx - s * 0.16, cy - s * 0.75, s * 0.32, s * 1.1, s * 0.16, col, s * 0.09))
        self.add('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#EF4444" stroke="%s" stroke-width="%.1f"/>' % (
            cx, cy + s * 0.42, s * 0.3, col, s * 0.09))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#EF4444"/>' % (
            cx - s * 0.06, cy - s * 0.35, s * 0.12, s * 0.7))
        for i in range(4):
            yy = cy - s * 0.6 + i * s * 0.2
            self.add('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" stroke-linecap="round"/>' % (
                cx + s * 0.3, yy, cx + s * 0.55, yy, col, s * 0.07))
        self.add('</g>')

    def battery(self, x, y, w, h, labels=True, size=12):
        self.add('<g class="icon">')
        cols = ["#E11D48", "#FACC15", "#22C55E", "#7DD3FC", "#2563EB", "#9333EA"]
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#0F172A"/>' % (x, y, w, h, h * 0.18))
        self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="#0F172A"/>' % (
            x + w - 1, y + h * 0.3, h * 0.14, h * 0.4, h * 0.05))
        pad = h * 0.1
        sw = (w - 2 * pad) / 6
        for i, c in enumerate(cols):
            self.add('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (
                x + pad + i * sw, y + pad, sw + 0.4, h - 2 * pad, c))
        self.text(x + pad + sw / 2 + h * 0.08, y + h / 2, "LOW", size=h * 0.26, weight=700, fill="#FFFFFF",
                  anchor="middle", rotate=-90)
        self.text(x + pad + 5.5 * sw + h * 0.08, y + h / 2, "FULL", size=h * 0.26, weight=700, fill="#FFFFFF",
                  anchor="middle", rotate=-90)
        if labels:
            for i, v in enumerate(["3.0", "3.3", "3.5", "3.7", "3.9", "4.1 V"]):
                self.text(x + pad + i * sw + (size * 0.55 if i == 5 else 0), y + h + size + 3, v,
                          size=size, weight=600, fill=MUTED, anchor="middle")
        self.add('</g>')

    # ------------------------------------------------------------ output
    def render(self):
        head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
                'font-family="Inter, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif">' % (self.w, self.h, self.w, self.h))
        defs = ('<defs>'
                '<marker id="ah" viewBox="0 0 12 12" refX="10.5" refY="6" markerWidth="9" markerHeight="9" '
                'markerUnits="userSpaceOnUse" orient="auto-start-reverse">'
                '<path d="M1,1.5 L11,6 L1,10.5 L3.6,6 Z" fill="%s"/></marker>'
                '<filter id="sh" x="-5%%" y="-5%%" width="110%%" height="120%%">'
                '<feDropShadow dx="0" dy="1.5" stdDeviation="2.2" flood-color="#0F172A" flood-opacity="0.08"/></filter>'
                '<filter id="sh2" x="-20%%" y="-20%%" width="140%%" height="150%%">'
                '<feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#0F172A" flood-opacity="0.25"/></filter>'
                '</defs>' % ARROW)
        bg = '<rect width="100%%" height="100%%" fill="%s"/>' % BG
        self.flush_pills()
        return head + defs + bg + "\n".join(self.o) + "</svg>"
