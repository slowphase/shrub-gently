"""Shrub, Gently: vector figures.

Every diagram in the book is generated here as inline SVG, so text stays
selectable and everything stays sharp in print. Colours and fonts match
style.css. Add a figure by writing a function that returns an SVG string
and registering it in FIGS at the bottom.
"""
import math

# palette (mirrors :root in style.css)
FOREST = "#1F3A2B"
MOSS = "#3E6A49"
SAGE = "#9CB898"
MINT = "#DCE8D4"
PAPER = "#F5F2E6"
CREAM = "#FBF9F1"
INK = "#2A2D2A"
GREY = "#7E877C"
RULE = "#D2D7C5"
LIME = "#B3D234"
LIMEDK = "#7E9A12"
CLAY = "#B4603F"
SCREEN = "#1B1D1C"

SANS = "Archivo"
MONO = "Plex Mono"


def svg(w, h, body, cls=""):
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="{SANS}">{body}</svg>')


def t(x, y, s, size=11, fill=INK, weight=600, anchor="middle", family=None, ls=0, style=""):
    fam = f' font-family="{family}"' if family else ""
    lsp = f' letter-spacing="{ls}"' if ls else ""
    st = f' font-style="{style}"' if style else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" font-weight="{weight}" '
            f'text-anchor="{anchor}"{fam}{lsp}{st}>{s}</text>')


def path_from(points):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points)


# ---------------------------------------------------------------------------
# The FM-1 front panel
# Geometry measured from the emulator's panel (fm1-emu running SHRUB V1.04)
# and cross-checked with the Operation Guide's description of the controls.
# ---------------------------------------------------------------------------
OX, OY = 14, 14  # body origin inside the viewBox
KNOBS_L = {"MASTER": (44, 55), "SELECT": (106, 55), "PRESETS": (44, 127), "ALGORITHM": (106, 127)}
KNOBS_R = {"KNOB 1": (416, 49), "KNOB 2": (457, 49), "KNOB 3": (498, 49), "KNOB 4": (539, 49)}
BUTTONS = [["FX", "SCL", "ENV", "LFO", "EDIT", "GLO"], ["HOME", "SAVE", "ARP", "SEQ", "PLAY", "REC"]]
WHITE_N = 16
BLACK_AFTER = [0, 1, 2, 4, 5, 7, 8, 9, 11, 12, 14]  # black key sits after these white keys (F to G)


def _white_x(i):
    return 35 + 32.8 * i


def fm1_panel(hl=(), screen=None, keys_hl=(), labels=True, dim=True, width=None, cap_keys=None):
    """Front-panel schematic. hl: control names to highlight
    (MASTER, SELECT, PRESETS, ALGORITHM, KNOB 1-4, button names, OCT-, OCT+, KEYS, SCREEN)."""
    hl = set(hl)
    on_any = bool(hl)
    o = []
    W, H = 592, 384
    o.append(f'<rect x="{OX}" y="{OY}" width="564" height="355" rx="16" fill="#E8EBE0" stroke="{INK}" stroke-width="2"/>')
    # knob wells
    def knob(name, cx, cy, r, label_above=True):
        lit = name in hl
        op = 1 if (lit or not on_any or not dim) else .38
        cx, cy = cx + OX, cy + OY
        fill = FOREST if lit else "#5A5F58"
        ring = LIME if lit else "#9DA399"
        s = [f'<g opacity="{op}">']
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="none" stroke="{ring}" stroke-width="{2.4 if lit else 1.2}"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>')
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy - r + 3}" stroke="{CREAM}" stroke-width="2.4" stroke-linecap="round"/>')
        if labels:
            ly = cy - r - 9
            s.append(t(cx, ly, name, 8.4 if len(name) < 9 else 7.6, FOREST if lit else INK, 700, ls=.4))
        s.append("</g>")
        return "".join(s)

    for n, (x, y) in KNOBS_L.items():
        o.append(knob(n, x, y, 18 if n != "MASTER" else 16))
    for n, (x, y) in KNOBS_R.items():
        o.append(knob(n, x, y, 14))
    # octave buttons
    o.append(f'<rect x="{OX + 17}" y="{OY + 168}" width="116" height="30" rx="5" fill="none" stroke="#B9BEB2" stroke-width="1"/>')
    for i, name in enumerate(["OCT-", "OCT+"]):
        lit = name in hl
        op = 1 if (lit or not on_any or not dim) else .38
        x = OX + 22 + i * 56
        o.append(f'<g opacity="{op}"><rect x="{x}" y="{OY + 172}" width="50" height="22" rx="4" fill="{FOREST if lit else "#D6DACD"}" stroke="{INK}" stroke-width="1"/>')
        o.append(t(x + 25, OY + 186.5, name.replace("-", "&#8722;"), 8.6, CREAM if lit else INK, 700) + "</g>")
    # screen
    lit = "SCREEN" in hl
    op = 1 if (lit or not on_any or not dim or screen) else .6
    o.append(f'<g opacity="{op}"><rect x="{OX + 152}" y="{OY + 5}" width="232" height="230" rx="10" fill="#2E322E" stroke="{LIME if lit else INK}" stroke-width="{3 if lit else 1.5}"/>')
    o.append(f'<rect x="{OX + 161}" y="{OY + 13}" width="214" height="214" rx="3" fill="{SCREEN}"/>')
    if screen:
        o.append(f'<g transform="translate({OX + 161},{OY + 13}) scale({214 / 240:.4f})">{screen}</g>')
    elif labels:
        o.append(t(OX + 268, OY + 124, "SCREEN", 10, "#6C736A", 700, ls=2))
    o.append("</g>")
    # button grid
    o.append(f'<rect x="{OX + 397}" y="{OY + 94}" width="162" height="72" rx="6" fill="#D9DDD1" stroke="#B9BEB2"/>')
    for r, row in enumerate(BUTTONS):
        for c, name in enumerate(row):
            lit = name in hl
            op = 1 if (lit or not on_any or not dim) else .38
            x = OX + 401 + c * 26
            y = OY + 99 + r * 33
            o.append(f'<g opacity="{op}"><rect x="{x}" y="{y}" width="24" height="28" rx="3.5" fill="{FOREST if lit else "#F1F3EA"}" stroke="{INK}" stroke-width="1"/>')
            o.append(t(x + 12, y + 17.5, name, 6.4 if len(name) > 3 else 7, CREAM if lit else INK, 700) + "</g>")
    # keyboard
    kl = "KEYS" in hl
    op = 1 if (kl or keys_hl or not on_any or not dim) else .45
    o.append(f'<g opacity="{op}"><rect x="{OX + 9}" y="{OY + 247}" width="546" height="106" rx="10" fill="#C9CEC0" stroke="#AEB4A6"/>')
    for i in range(WHITE_N):
        x = OX + _white_x(i) - 13
        sel = ("W", i) in keys_hl or kl
        o.append(f'<rect x="{x:.1f}" y="{OY + 297}" width="26" height="50" rx="11" fill="{MOSS if sel else "#7A6A66"}" stroke="{INK}" stroke-width=".8"/>')
        o.append(f'<line x1="{x + 13:.1f}" y1="{OY + 305}" x2="{x + 13:.1f}" y2="{OY + 339}" stroke="#ffffff" stroke-opacity=".35" stroke-width="1.6" stroke-linecap="round"/>')
    for j, i in enumerate(BLACK_AFTER):
        x = OX + (_white_x(i) + _white_x(i + 1)) / 2 - 12
        sel = ("B", j) in keys_hl or kl
        o.append(f'<rect x="{x:.1f}" y="{OY + 251}" width="24" height="42" rx="10" fill="{MOSS if sel else "#6B5C58"}" stroke="{INK}" stroke-width=".8"/>')
        o.append(f'<line x1="{x + 12:.1f}" y1="{OY + 258}" x2="{x + 12:.1f}" y2="{OY + 285}" stroke="#ffffff" stroke-opacity=".3" stroke-width="1.4" stroke-linecap="round"/>')
    if cap_keys:
        o.append(t(OX + 282, OY + 376, cap_keys, 8, GREY, 600))
    o.append("</g>")
    style = f' style="width:{width}"' if width else ""
    return f'<svg class="panel" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H + (10 if cap_keys else 0)}" font-family="{SANS}"{style}>{"".join(o)}</svg>'


def fm1_tour():
    """Big labelled overview with numbered callouts."""
    p = fm1_panel(labels=True, dim=False)
    inner = p[p.index(">") + 1:-6]
    calls = [
        (1, OX + 4, OY + 91, "Volume and presets"),
        (2, OX + 141, OY + 183, "Octave buttons"),
        (3, OX + 268, OY + 240, "Screen"),
        (4, OX + 566, OY + 49, "Four screen knobs"),
        (5, OX + 478, OY + 170, "Section buttons"),
        (6, OX + 282, OY + 300, "27 keys"),
    ]
    o = [inner]
    for n, x, y, _ in calls:
        o.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{LIME}" stroke="{FOREST}" stroke-width="2"/>')
        o.append(t(x, y + 4, str(n), 11, FOREST, 800))
    return svg(592, 384, "".join(o))


def rear_panel():
    o = [f'<rect x="10" y="20" width="560" height="70" rx="12" fill="#E8EBE0" stroke="{INK}" stroke-width="2"/>']
    items = [(110, "jack", "AUDIO OUT", "3.5 mm stereo: headphones,\nmonitors or the MPC"),
             (230, "jack", "MIDI IN", "3.5 mm TRS: a MIDI\nkeyboard or sequencer"),
             (360, "usb", "USB-C", "Charging, USB MIDI and\nUSB audio to a computer"),
             (480, "switch", "POWER", "Slide to switch\non and off")]
    for x, kind, lab, desc in items:
        if kind == "jack":
            o.append(f'<circle cx="{x}" cy="55" r="12" fill="#C9CEC0" stroke="{INK}" stroke-width="1.5"/><circle cx="{x}" cy="55" r="5" fill="{INK}"/>')
        elif kind == "usb":
            o.append(f'<rect x="{x - 18}" y="47" width="36" height="16" rx="8" fill="#C9CEC0" stroke="{INK}" stroke-width="1.5"/><rect x="{x - 10}" y="53" width="20" height="4" rx="2" fill="{INK}"/>')
        else:
            o.append(f'<rect x="{x - 20}" y="46" width="40" height="18" rx="4" fill="#C9CEC0" stroke="{INK}" stroke-width="1.5"/><rect x="{x - 18}" y="48" width="18" height="14" rx="3" fill="{FOREST}"/>')
        o.append(t(x, 112, lab, 10.5, FOREST, 800, ls=.6))
        for k, line in enumerate(desc.split("\n")):
            o.append(t(x, 127 + k * 12.5, line, 9, INK, 400))
    o.append(t(290, 14, "THE BACK EDGE (SCHEMATIC, NOT TO SCALE)", 7.5, GREY, 700, ls=1.6))
    return svg(580, 160, "".join(o))


# ---------------------------------------------------------------------------
# Screen mock-ups. Original drawings that follow the layout the Operation
# Guide describes (header, display, deck of four knobs). Not screenshots.
# ---------------------------------------------------------------------------
SECTION_COL = {"HOME": "#E2913A", "OSC": "#B6D63E", "SUB": "#B6D63E", "FILTER": "#58A7E6", "ENV": "#58A7E6",
               "LFO": "#58A7E6", "FX": "#E07A5A", "GLO": "#E3C341", "SAVE": "#E2913A", "ARP": "#A88BE0",
               "SCL": "#A88BE0", "SEQ": "#E07A5A", "MATRIX": "#58A7E6"}


def screen(title, col="OSC", pills=None, active=0, dots=None, big=None, sub=None, knobs=None,
           display=None, right=None, chips=None, num=None):
    c = SECTION_COL.get(col, col)
    # rounded corners are drawn into the shapes themselves (no clipPath: see build notes)
    o = [f'<rect width="240" height="240" rx="6" fill="{SCREEN}"/>']
    o.append(t(10, 21, title, 15, c, 800, "start", ls=.2))
    if dots:
        n, i = dots
        tx = 12 + len(title) * 9.6
        for k in range(n):
            o.append(f'<rect x="{tx + k * 9}" y="13" width="6" height="3" rx="1.5" fill="{c if k == i else "#555"}"/>')
    # meter
    o.append(f'<rect x="170" y="10" width="54" height="5" rx="2" fill="#2d3a2d"/><rect x="170" y="10" width="20" height="5" rx="2" fill="#4c9a4c"/>')
    o.append(f'<path d="M226,9 l4,0 l-2,3z" fill="#ddd"/>')
    o.append(f'<line x1="8" y1="28" x2="232" y2="28" stroke="#333" stroke-width="1"/>')
    y0 = 32
    if num:
        o.append(t(10, 46, num, 12, "#cfcfcf", 500, "start", family=MONO))
    if chips:
        x = 232
        for name, on in reversed(chips):
            w = len(name) * 7 + 4
            x -= w
            o.append(t(x + w / 2, 46, name, 8.5, "#E5735A" if on else "#4a4a4a", 700))
    if pills:
        n = len(pills)
        pw = (224 - (n - 1) * 4) / n
        for k, pl in enumerate(pills):
            x = 8 + k * (pw + 4)
            on = k == active
            o.append(f'<rect x="{x:.1f}" y="{y0}" width="{pw:.1f}" height="15" rx="7.5" fill="{c if on else "#262826"}" stroke="{c if on else "#444"}" stroke-width="1"/>')
            o.append(t(x + pw / 2, y0 + 11, pl, 7.6, SCREEN if on else "#9a9a9a", 700))
        y0 += 20
    if right:
        o.append(t(230, y0 + 12, right, 8.5, c, 700, "end"))
    if big:
        o.append(t(120, 92, big, 26 if len(big) < 12 else 20, "#5CC8F0", 600, family=None, ls=-.3))
    if sub:
        o.append(t(10, y0 + 14, sub, 10.5, "#e6e6e6", 700, "start"))
    if display:
        o.append(display)
    if knobs:
        o.append('<path d="M0,160 H240 V234 A6,6 0 0 1 234,240 H6 A6,6 0 0 1 0,234 Z" fill="#161817"/>')
        for k, kn in enumerate(knobs):
            if kn is None:
                continue
            lab, val = kn[0], kn[1]
            hi = len(kn) > 2 and kn[2]
            cx = 30 + k * 60
            o.append(f'<circle cx="{cx}" cy="186" r="16" fill="#2b2e2c" stroke="{LIME if hi else "#3b3e3c"}" stroke-width="{2.4 if hi else 1.4}"/>')
            ang = -130 + 260 * (kn[3] if len(kn) > 3 else .5)
            a = math.radians(ang - 90)
            o.append(f'<path d="{_arc(cx, 186, 19, -130, ang)}" stroke="{c}" stroke-width="2.4" fill="none"/>')
            o.append(f'<line x1="{cx}" y1="186" x2="{cx + 12 * math.cos(a):.1f}" y2="{186 + 12 * math.sin(a):.1f}" stroke="#eee" stroke-width="2.2" stroke-linecap="round"/>')
            o.append(t(cx, 218, lab, 8.4 if len(lab) < 9 else 7.2, "#e8e8e8", 700))
            o.append(t(cx, 230, val, 8.2, "#bdbdbd", 500))
    return "".join(o)


def _arc(cx, cy, r, a0, a1):
    a0r, a1r = math.radians(a0 - 90), math.radians(a1 - 90)
    x0, y0 = cx + r * math.cos(a0r), cy + r * math.sin(a0r)
    x1, y1 = cx + r * math.cos(a1r), cy + r * math.sin(a1r)
    large = 1 if (a1 - a0) > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} 1 {x1:.1f},{y1:.1f}"


def screen_svg(scr, width="46mm"):
    return f'<svg class="scr-mock" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" font-family="{SANS}" style="width:{width}">{scr}</svg>'


def _saw_display(x0=14, y0=60, w=212, h=90, col="#B6D63E"):
    pts = []
    for k in range(3):
        xa = x0 + k * w / 3
        pts += [(xa, y0 + h * .8), (xa + w / 3 - 1, y0 + h * .2), (xa + w / 3, y0 + h * .8)]
    return f'<path d="{path_from(pts)}" stroke="{col}" stroke-width="2.4" fill="none"/>'


def scr_home(name="INIT", num="102", cat="BASS", vals=("2.06 kHz", "10%", "1", "1"), hl=None, chips=None):
    hl = hl or []
    disp = (f'<rect x="12" y="104" width="100" height="40" rx="3" fill="#202320"/>'
            f'<path d="M16,136 L44,112 L44,136 L72,112 L72,136 L100,112" stroke="#B6D63E" stroke-width="2" fill="none"/>'
            f'<rect x="128" y="104" width="100" height="40" rx="3" fill="#202320"/>'
            f'<path d="M132,136 L160,112 L160,136 L188,112 L188,136 L216,112" stroke="#3b3f3b" stroke-width="2" fill="none"/>')
    return screen(cat, "HOME", big=name, num=num, display=disp,
                  chips=chips or [("SEQ", 0), ("ARP", 0), ("DST", 0), ("CHO", 0), ("DLY", 0), ("REV", 0)],
                  knobs=[("CUTOFF", vals[0], "CUTOFF" in hl, .62), ("RES", vals[1], "RES" in hl, .1),
                         ("A POS", vals[2], "A POS" in hl, 0), ("B POS", vals[3], "B POS" in hl, 0)])


def scr_save(slot="101", name="MY CHILL PAD", cat="PAD", replaces="INIT"):
    disp = (t(10, 48, f"SAVE TO {slot}", 9.5, "#e6e6e6", 700, "start") + t(230, 48, f"REPLACES {replaces}", 8.5, "#bdbdbd", 700, "end")
            + t(120, 98, name, 20 if len(name) < 11 else 15, "#ffffff", 600)
            + f'<rect x="{120 - len(cat) * 4.5 - 8}" y="110" width="{len(cat) * 9 + 16}" height="15" rx="7.5" fill="#E2913A"/>'
            + t(120, 121, cat, 8.5, SCREEN, 800)
            + t(120, 146, "PRESS SAVE AGAIN TO SAVE", 8, "#7fb3d6", 700))
    return screen("SAVE", "SAVE", display=disp,
                  knobs=[("SLOT", slot, True, .8), ("CURSOR", "1", False, 0), ("LETTER", name[0], False, .3), ("CATEGORY", cat, False, .5)])


def scr_env(vals=("0.5 ms", "1.00 s", "0.0 dB", "15 ms"), active=0, shape=(0.02, .45, 1.0, .05), hl=()):
    a, d, s, r = shape
    x0, y0, w, h = 14, 58, 212, 92
    pts = [(x0, y0 + h), (x0 + a * w, y0), (x0 + (a + d * .45) * w, y0 + h * (1 - s)), (x0 + .78 * w, y0 + h * (1 - s)), (x0 + min(.78 + r * .8, .99) * w, y0 + h)]
    disp = f'<path d="{path_from(pts)}" stroke="#58A7E6" stroke-width="2.4" fill="#58A7E6" fill-opacity=".12"/>'
    labs = ["ATTACK", "DECAY", "SUSTAIN", "RELEASE"]
    return screen(f"ENV {active + 1}", "ENV", pills=["ENV 1", "ENV 2", "ENV 3", "MATRIX"], active=active, dots=(2, 0), display=disp,
                  knobs=[(labs[i], vals[i], labs[i] in hl, [.05, .5, 1, .1][i]) for i in range(4)])


def scr_filter(ftype="LP 24", vals=("2.06 kHz", "10%", "0%", "100%"), hl=(), page=0, labels=None):
    x0, y0, w, h = 14, 70, 212, 76
    pts = []
    fc = .55
    for k in range(101):
        x = k / 100
        db = 0 if x < fc - .05 else -min(1, (x - (fc - .05)) * 3.2)
        bump = .12 * math.exp(-((x - fc + .04) ** 2) / .0012)
        pts.append((x0 + x * w, y0 + h * (.25 - bump - db * .75)))
    disp = t(10, 62, ftype, 10.5, "#e6e6e6", 700, "start") + f'<path d="{path_from(pts)}" stroke="#58A7E6" stroke-width="2.4" fill="none"/>'
    labels = labels or ["CUTOFF", "RES", "DRIVE", "MIX"]
    return screen("FILTER", "FILTER", dots=(3, page), display=disp,
                  knobs=[(labels[i], vals[i], labels[i] in hl, [.6, .1, 0, 1][i]) for i in range(4)])


def scr_osc(title="OSC A", table="DEFAULT", frame="1 / 9", vals=("1", "OFF", "0%", "75%"), labels=None, hl=(), pills=True, dots=(4, 0)):
    disp = t(10, 64, table, 10, "#e6e6e6", 700, "start") + t(230, 148, frame, 8.5, "#B6D63E", 700, "end")
    # stacked frames (pseudo 3D)
    for k in range(6, -1, -1):
        dx, dy = k * 9, -k * 7
        col = "#B6D63E" if k == 0 else "#4f6a2a"
        pts = [(26 + dx, 140 + dy), (98 + dx, 96 + dy), (98 + dx, 140 + dy), (170 + dx, 96 + dy - k * 1.5)]
        o = path_from(pts)
        disp += f'<path d="{o}" stroke="{col}" stroke-width="{2.4 if k == 0 else 1}" fill="none"/>'
    labels = labels or ["WT POS", "WARP", "AMOUNT", "LEVEL"]
    return screen(title, "OSC", pills=["OSC A", "OSC B", "SUB", "FILTER"] if pills else None,
                  active={"OSC A": 0, "OSC B": 1, "SUB": 2}.get(title, 0), dots=dots, display=disp,
                  knobs=[(labels[i], vals[i], labels[i] in hl, [.0, 0, 0, .75][i]) for i in range(4)])


def scr_lfo(vals=("0.10 Hz", "TRIANGLE", "A WT POS", "40%"), hl=(), mode="FREE"):
    pts = [(14, 148), (120, 64), (226, 148)]
    disp = t(230, 64, mode, 8.5, "#58A7E6", 700, "end") + f'<path d="{path_from(pts)}" stroke="#58A7E6" stroke-width="2.4" fill="#58A7E6" fill-opacity=".12"/><circle cx="70" cy="104" r="4" fill="#fff"/>'
    labs = ["RATE", "SKEW", "DEST", "AMOUNT"]
    return screen("LFO 1", "LFO", pills=["LFO 1", "LFO 2", "LFO 3", "LFO 4", "CHAOS", "MATRIX"], active=0, dots=(4, 0), display=disp,
                  knobs=[(labs[i], vals[i], labs[i] in hl, [.2, .5, .1, .7][i]) for i in range(4)])


def scr_rack(rows, sel=2, vals=("3", "DELAY", "UP / DOWN", "NORMAL"), hl=()):
    disp = ""
    for i, (name, state) in enumerate(rows):
        y = 44 + i * 15
        if i == sel:
            disp += f'<rect x="6" y="{y - 11}" width="228" height="14" rx="3" fill="#7d55c7"/>'
        disp += t(14, y, f"{i + 1}", 9, "#bbb", 700, "start") + t(28, y, name, 9, "#eee" if name != "EMPTY" else "#666", 700, "start")
        disp += t(230, y, state, 8, "#ccc" if state == "ON" else "#777", 700, "end")
    labs = ["SLOT", vals[1] and f"SLOT {vals[0]}", "MOVE", "MODE"]
    return screen("FX RACK", "FX", display=disp,
                  knobs=[("SLOT", vals[0], "SLOT" in hl, .3), (f"SLOT {vals[0]}", vals[1], False, .5), ("MOVE", vals[2], False, .5), ("MODE", vals[3], "MODE" in hl, .3)])


# ---------------------------------------------------------------------------
# Teaching diagrams
# ---------------------------------------------------------------------------
def _wave(kind, x0, y0, w, h, cycles=2, n=240):
    pts = []
    for k in range(n + 1):
        ph = (k / n) * cycles % 1
        if kind == "sine":
            v = math.sin(2 * math.pi * ph)
        elif kind == "triangle":
            v = 1 - 4 * abs(ph - .25) if ph < .75 else -1 + 4 * (ph - .75)
            v = 4 * ph if ph < .25 else (2 - 4 * ph if ph < .75 else 4 * ph - 4)
        elif kind == "saw":
            v = 1 - 2 * ph
        elif kind == "square":
            v = 1 if ph < .5 else -1
        else:
            v = 0
        pts.append((x0 + w * k / n, y0 + h / 2 - v * h / 2))
    if kind == "saw":  # crisp verticals
        pts2 = []
        for c in range(cycles):
            xa = x0 + w * c / cycles
            xb = x0 + w * (c + 1) / cycles
            pts2 += [(xa, y0), (xb, y0 + h), (xb, y0)] if False else [(xa, y0 + h / 2 - h / 2), (xb, y0 + h)]
        pts = []
        for c in range(cycles):
            xa = x0 + w * c / cycles
            xb = x0 + w * (c + 1) / cycles
            pts += [(xa, y0), (xb, y0 + h)]
            if c < cycles - 1:
                pts.append((xb, y0))
    if kind == "square":
        pts = []
        for c in range(cycles):
            xa = x0 + w * c / cycles
            xm = xa + w / cycles / 2
            xb = x0 + w * (c + 1) / cycles
            pts += [(xa, y0 + h / 2), (xa, y0), (xm, y0), (xm, y0 + h), (xb, y0 + h), (xb, y0 + h / 2)]
    return path_from(pts)


HARM = {"sine": [1], "triangle": [1, 0, 1 / 9, 0, 1 / 25, 0, 1 / 49, 0],
        "saw": [1, 1 / 2, 1 / 3, 1 / 4, 1 / 5, 1 / 6, 1 / 7, 1 / 8], "square": [1, 0, 1 / 3, 0, 1 / 5, 0, 1 / 7, 0]}


def waveforms_fig():
    rows = [("sine", "SINE", "Pure and round. Just one frequency: soft, flute-like, deep in the bass."),
            ("triangle", "TRIANGLE", "A little brighter. A few quiet harmonics: gentle and hollow."),
            ("square", "SQUARE", "Hollow and woody. Only the odd-numbered harmonics."),
            ("saw", "SAW", "Bright and buzzy. Every harmonic: the raw material for most synth sounds.")]
    o = [t(70, 14, "WAVEFORM", 8, GREY, 700, ls=1.6), t(240, 14, "WHAT YOU HEAR", 8, GREY, 700, ls=1.6, anchor="start"),
         t(530, 14, "HARMONICS", 8, GREY, 700, ls=1.6)]
    for i, (k, name, desc) in enumerate(rows):
        y = 26 + i * 64
        o.append(f'<rect x="0" y="{y}" width="600" height="56" rx="6" fill="{CREAM if i % 2 == 0 else PAPER}"/>')
        o.append(f'<line x1="12" y1="{y + 28}" x2="140" y2="{y + 28}" stroke="{RULE}" stroke-width="1"/>')
        o.append(f'<path d="{_wave(k, 12, y + 10, 128, 36)}" stroke="{FOREST}" stroke-width="2.4" fill="none" stroke-linejoin="round"/>')
        o.append(t(160, y + 23, name, 10.5, FOREST, 800, "start", ls=.8))
        words = desc.split(" ")
        line, lines = "", []
        for wd in words:
            if len(line + wd) > 38:
                lines.append(line)
                line = ""
            line += wd + " "
        lines.append(line)
        for j, ln in enumerate(lines[:2]):
            o.append(t(240, y + 23 + j * 14, ln.strip(), 10, INK, 400, "start"))
        for j, a in enumerate(HARM[k]):
            if a:
                bh = 36 * a
                o.append(f'<rect x="{480 + j * 13}" y="{y + 46 - bh:.1f}" width="8" height="{bh:.1f}" fill="{MOSS if j == 0 else SAGE}"/>')
        o.append(f'<line x1="476" y1="{y + 46}" x2="586" y2="{y + 46}" stroke="{INK}" stroke-width=".8"/>')
    return svg(600, 286, "".join(o))


def pitch_fig():
    o = []
    for i, (cyc, lab, note) in enumerate([(2, "LOWER NOTE", "fewer cycles each second"), (6, "HIGHER NOTE", "more cycles each second")]):
        y = 18 + i * 74
        o.append(t(0, y, lab, 8.5, FOREST, 800, "start", ls=1.2))
        o.append(t(600, y, note, 9, GREY, 400, "end", style="italic"))
        pts = [(10 + 580 * k / 400, y + 32 - 22 * math.sin(2 * math.pi * cyc * k / 400)) for k in range(401)]
        o.append(f'<line x1="10" y1="{y + 32}" x2="590" y2="{y + 32}" stroke="{RULE}"/>')
        o.append(f'<path d="{path_from(pts)}" stroke="{FOREST if i == 0 else MOSS}" stroke-width="2.4" fill="none"/>')
    o.append(f'<line x1="10" y1="160" x2="590" y2="160" stroke="{INK}" stroke-width="1"/><path d="M590,160 l-7,-4 l0,8z" fill="{INK}"/>')
    o.append(t(300, 176, "the same slice of time", 9, INK, 500))
    return svg(600, 182, "".join(o))


def harmonics_fig():
    o = [t(150, 14, "A SAW WAVE IS A STACK OF SINES", 8.5, GREY, 700, ls=1.4)]
    cols = [FOREST, MOSS, "#5E8A64", SAGE]
    y0 = 60
    for h in range(1, 5):
        pts = [(10 + 280 * k / 300, y0 + (h - 1) * 0 - 34 / h * math.sin(2 * math.pi * h * 2 * k / 300)) for k in range(301)]
        o.append(f'<path d="{path_from(pts)}" stroke="{cols[h - 1]}" stroke-width="{2.4 - .4 * h}" fill="none" opacity=".9"/>')
    o.append(t(150, 116, "1st, 2nd, 3rd and 4th harmonics", 9.5, INK, 500))
    # sum
    pts = []
    for k in range(301):
        x = 2 * k / 300
        v = sum(math.sin(2 * math.pi * h * x) / h for h in range(1, 13))
        pts.append((330 + 260 * k / 300, 60 - 22 * v))
    o.append(f'<path d="{path_from(pts)}" stroke="{FOREST}" stroke-width="2.4" fill="none"/>')
    o.append(t(460, 116, "together: the saw's sharp edge", 9.5, INK, 500))
    o.append(f'<path d="M300,60 l18,0" stroke="{LIMEDK}" stroke-width="3"/><path d="M318,60 l-6,-5 l0,10z" fill="{LIMEDK}"/>')
    return svg(600, 126, "".join(o))


def wavetable_fig():
    o = []
    n = 9
    for k in range(n - 1, -1, -1):
        dx, dy = k * 26, -k * 13
        mix = k / (n - 1)
        pts = []
        for s in range(161):
            ph = (s / 160) * 2 % 1
            saw = 1 - 2 * ph
            sq = 1 if ph < .5 else -1
            v = saw * (1 - mix) + sq * mix
            pts.append((30 + dx + 200 * s / 160, 170 + dy - v * 30))
        sel = k == 3
        o.append(f'<path d="{path_from(pts)}" stroke="{LIMEDK if sel else (FOREST if k in (0, n - 1) else SAGE)}" stroke-width="{3 if sel else 1.4}" fill="none" stroke-linejoin="round"/>')
    o.append(t(130, 222, "FRAME 1: a saw", 9, FOREST, 700))
    o.append(t(470, 56, "LAST FRAME: a square", 9, FOREST, 700))
    # slider
    o.append(f'<line x1="70" y1="246" x2="530" y2="246" stroke="{INK}" stroke-width="1.4"/>')
    for k in range(n):
        x = 70 + 460 * k / (n - 1)
        o.append(f'<line x1="{x}" y1="241" x2="{x}" y2="251" stroke="{INK}" stroke-width="1"/>')
    xs = 70 + 460 * 3 / (n - 1)
    o.append(f'<circle cx="{xs}" cy="246" r="8" fill="{LIME}" stroke="{FOREST}" stroke-width="2"/>')
    o.append(t(xs, 270, "WT POS chooses which frame plays", 9.5, INK, 600))
    o.append(t(300, 14, "A WAVETABLE: A STACK OF SINGLE-CYCLE WAVES, CALLED FRAMES", 8.5, GREY, 700, ls=1.2))
    return svg(600, 280, "".join(o))


def adsr_fig():
    o = []
    x0, base, top = 40, 190, 40
    sus = 110
    A, D, S, R = 80, 90, 190, 120
    pts = [(x0, base), (x0 + A, top), (x0 + A + D, sus), (x0 + A + D + S, sus), (x0 + A + D + S + R, base)]
    o.append(f'<path d="{path_from(pts)}" stroke="{FOREST}" stroke-width="3" fill="{SAGE}" fill-opacity=".28" stroke-linejoin="round"/>')
    segs = [(x0, x0 + A, "ATTACK", "how fast it rises"), (x0 + A, x0 + A + D, "DECAY", "how fast it falls"),
            (x0 + A + D, x0 + A + D + S, "SUSTAIN", "the level while held"), (x0 + A + D + S, x0 + A + D + S + R, "RELEASE", "the fade after you let go")]
    for a, b, lab, d in segs:
        o.append(f'<line x1="{b}" y1="{top - 8}" x2="{b}" y2="{base}" stroke="{RULE}" stroke-dasharray="3 3"/>')
        o.append(t((a + b) / 2, 22, lab, 9.5, FOREST, 800, ls=.8))
        o.append(t((a + b) / 2, 214, d, 8.6, INK, 400, style="italic"))
    o.append(f'<line x1="{x0}" y1="{base}" x2="580" y2="{base}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x0}" y2="{top - 10}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(t(x0 - 8, top + 4, "loud", 8.5, GREY, 600, "end"))
    o.append(t(x0 - 8, base, "silent", 8.5, GREY, 600, "end"))
    # key bar
    kx0, kx1 = x0, x0 + A + D + S
    o.append(f'<rect x="{kx0}" y="232" width="{kx1 - kx0}" height="12" rx="6" fill="{FOREST}"/>')
    o.append(t((kx0 + kx1) / 2, 241.5, "KEY HELD DOWN", 7.6, CREAM, 800, ls=1.2))
    o.append(t(kx1 + 8, 242, "key let go", 8.6, INK, 600, "start"))
    o.append(f'<circle cx="{x0 + A + D + S}" cy="{sus}" r="4" fill="{LIME}" stroke="{FOREST}"/>')
    return svg(600, 252, "".join(o))


def adsr_shapes_fig():
    shapes = [("PLUCK", "fast attack, short decay,\nno sustain", [(0, 1), (.03, 0), (.35, 1), (.6, 1)], ),
              ("PAD", "slow attack, full sustain,\nlong release", [(0, 1), (.35, 0), (.7, 0), (1, 1)]),
              ("ORGAN", "instant on, full sustain,\ninstant off", [(0, 1), (.01, 0), (.75, 0), (.76, 1)]),
              ("SWELL", "slow rise, quick release", [(0, 1), (.6, .05), (.72, .05), (.8, 1)])]
    o = []
    for i, (name, d, pts) in enumerate(shapes):
        x0 = i * 150 + 6
        o.append(f'<rect x="{x0}" y="4" width="138" height="122" rx="6" fill="{CREAM}" stroke="{RULE}"/>')
        P = [(x0 + 12 + 114 * x, 22 + 50 * y) for x, y in pts]
        o.append(f'<path d="{path_from(P)}" stroke="{FOREST}" stroke-width="2.4" fill="{SAGE}" fill-opacity=".3" stroke-linejoin="round"/>')
        o.append(t(x0 + 69, 92, name, 9.5, FOREST, 800, ls=1))
        for j, ln in enumerate(d.split("\n")):
            o.append(t(x0 + 69, 106 + j * 11, ln, 8.2, INK, 400))
    return svg(600, 130, "".join(o))


def filter_fig(kind="lp"):
    o = []
    x0, x1, y0, y1 = 40, 580, 52, 192
    fc = .5
    pts = []
    for k in range(201):
        x = k / 200
        if kind == "lp":
            att = 0 if x < fc else min(1, (x - fc) * 2.6)
            bump = .22 * math.exp(-((x - fc) ** 2) / .0016)
        else:
            att = 0 if x > fc else min(1, (fc - x) * 2.6)
            bump = .22 * math.exp(-((x - fc) ** 2) / .0016)
        pts.append((x0 + (x1 - x0) * x, y0 + 30 + (y1 - y0 - 30) * att - 70 * bump))
    # harmonic bars behind
    for h in range(1, 26):
        x = x0 + (x1 - x0) * (h / 26)
        amp = 1 / h ** .55
        xn = h / 26
        if kind == "lp":
            g = 1 if xn < fc else max(0, 1 - (xn - fc) * 2.6)
        else:
            g = 1 if xn > fc else max(0, 1 - (fc - xn) * 2.6)
        hh = 110 * amp
        o.append(f'<rect x="{x - 4}" y="{y1 - hh:.1f}" width="8" height="{hh:.1f}" fill="{RULE}"/>')
        o.append(f'<rect x="{x - 4}" y="{y1 - hh * g:.1f}" width="8" height="{hh * g:.1f}" fill="{SAGE}"/>')
    o.append(f'<path d="{path_from(pts)}" stroke="{FOREST}" stroke-width="3" fill="none"/>')
    xc = x0 + (x1 - x0) * fc
    o.append(f'<line x1="{xc}" y1="{y0 - 6}" x2="{xc}" y2="{y1}" stroke="{LIMEDK}" stroke-width="1.6" stroke-dasharray="4 3"/>')
    o.append(f'<rect x="{xc - 30}" y="{y0 - 22}" width="60" height="16" rx="3" fill="{LIME}"/>' + t(xc, y0 - 10.5, "CUTOFF", 8.5, FOREST, 800, ls=1))
    o.append(t(xc + 14, y0 + 6, "resonance: a peak right at the cutoff", 8.8, INK, 500, "start", style="italic"))
    o.append(f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(t(x0, y1 + 16, "low", 8.5, GREY, 600, "start") + t(x1, y1 + 16, "high", 8.5, GREY, 600, "end"))
    o.append(t((x0 + x1) / 2, y1 + 16, "harmonics, from low to high", 8.5, GREY, 600))
    lab = "LOW-PASS: lows pass through, highs are removed" if kind == "lp" else "HIGH-PASS: highs pass through, lows are removed"
    o.append(t(x0, 12, lab.upper(), 8.5, FOREST, 800, "start", ls=1))
    return svg(600, 218, "".join(o))


def env2_sweep_fig():
    o = []
    x0, x1 = 50, 580
    # envelope
    pts = [(x0, 120), (x0 + 6, 30), (x0 + 120, 112), (x0 + 330, 112), (x0 + 345, 120)]
    o.append(t(x0, 16, "ENV 2 (DECAY ABOUT 300 MS, SUSTAIN DOWN)", 8.2, FOREST, 800, "start", ls=1))
    o.append(f'<path d="{path_from(pts)}" stroke="{FOREST}" stroke-width="2.6" fill="{SAGE}" fill-opacity=".3"/>')
    o.append(f'<line x1="{x0}" y1="120" x2="{x1}" y2="120" stroke="{INK}"/>')
    # cutoff line
    o.append(t(x0, 140, "WHERE THE CUTOFF SITS", 8.2, FOREST, 800, "start", ls=1))
    base = 238
    pts2 = [(x0, base - 10), (x0 + 6, base - 70), (x0 + 120, base - 14), (x0 + 330, base - 14), (x0 + 345, base - 10), (x1, base - 10)]
    o.append(f'<path d="{path_from(pts2)}" stroke="{LIMEDK}" stroke-width="2.6" fill="none"/>')
    o.append(f'<line x1="{x0}" y1="{base - 10}" x2="{x1}" y2="{base - 10}" stroke="{RULE}" stroke-dasharray="4 3"/>')
    o.append(t(x1, base - 16, "the CUTOFF knob's own setting", 8.6, GREY, 500, "end", style="italic"))
    o.append(t(x0 + 26, base - 76, "bright at the start of each note,", 8.8, INK, 500, "start"))
    o.append(t(x0 + 130, base - 22, "then settling dark", 8.8, INK, 500, "start"))
    o.append(f'<line x1="{x0}" y1="{base}" x2="{x1}" y2="{base}" stroke="{INK}"/>')
    o.append(f'<path d="M{x1},{base} l-7,-4 l0,8z" fill="{INK}"/>' + t(x1, base + 14, "time", 8.5, GREY, 600, "end"))
    return svg(600, 258, "".join(o))


def lfo_fig():
    """LFO 1 moving WT POS. BIPOLAR is OFF by default (LFO page 2), so the
    LFO pushes the knob upward from where you set it and back down again."""
    o = []
    x0, x1 = 60, 580
    o.append(t(x0, 14, "LFO 1: A SLOW TRIANGLE, ABOUT ONE CYCLE EVERY TEN SECONDS", 8.2, FOREST, 800, "start", ls=1))
    tri = []
    for k in range(401):
        ph = (k / 400 * 2) % 1
        v = 2 * ph if ph < .5 else 2 - 2 * ph          # 0 -> 1 -> 0, unipolar
        tri.append((x0 + (x1 - x0) * k / 400, v))
    o.append(f'<line x1="{x0}" y1="98" x2="{x1}" y2="98" stroke="{RULE}"/>')
    o.append(f'<path d="{path_from([(x, 98 - 66 * v) for x, v in tri])}" stroke="{FOREST}" stroke-width="2.6" fill="none"/>')
    o.append(t(x0 - 8, 36, "top", 8.4, GREY, 600, "end") + t(x0 - 8, 101, "rest", 8.4, GREY, 600, "end"))
    o.append(f'<path d="M300,112 l0,26" stroke="{LIMEDK}" stroke-width="3"/><path d="M300,142 l-6,-8 l12,0z" fill="{LIMEDK}"/>')
    o.append(t(312, 132, "DEST: A WT POS. AMOUNT sets how far it pushes.", 9, INK, 600, "start"))
    o.append(t(x0, 168, "WT POS, PUSHED UP BY THE LFO AND BACK", 8.2, FOREST, 800, "start", ls=1))
    for k in range(12):
        o.append(f'<rect x="{x0 + k * (x1 - x0) / 12}" y="178" width="{(x1 - x0) / 12 - 2}" height="70" fill="{MINT if k % 2 else CREAM}"/>')
    o.append(f'<path d="{path_from([(x, 238 - 50 * v) for x, v in tri])}" stroke="{LIMEDK}" stroke-width="3" fill="none"/>')
    o.append(f'<line x1="{x0}" y1="238" x2="{x1}" y2="238" stroke="{FOREST}" stroke-dasharray="5 4"/>')
    o.append(t(x1 + 4, 241, "your WT POS", 8.2, FOREST, 700, "start"))
    o.append(t(x1 + 4, 191, "+ AMOUNT", 8.2, LIMEDK, 700, "start"))
    o.append(t(x0 - 8, 192, "later", 8.2, GREY, 600, "end") + t(x0 - 8, 241, "set", 8.2, GREY, 600, "end"))
    return svg(650, 258, "".join(o))


def signal_flow():
    o = []
    def box(x, y, w, h, title, sub, fill=CREAM, stroke=FOREST, tc=FOREST):
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.8"/>'
        s += t(x + w / 2, y + h / 2 - 1 if sub else y + h / 2 + 4, title, 10.5, tc, 800, ls=.6)
        if sub:
            s += t(x + w / 2, y + h / 2 + 13, sub, 8.4, INK if tc == FOREST else MINT, 400)
        return s
    srcs = [("OSC A", "wavetable"), ("OSC B", "wavetable"), ("SUB", "simple wave"), ("NOISE", "hiss and rumble")]
    for i, (a, b) in enumerate(srcs):
        y = 20 + i * 52
        o.append(box(10, y, 110, 42, a, b))
        o.append(f'<path d="M120,{y + 21} C150,{y + 21} 150,122 176,122" stroke="{FOREST}" stroke-width="1.8" fill="none"/>')
    o.append(f'<path d="M176,122 l-7,-4 l0,8z" fill="{FOREST}"/>')
    o.append(box(178, 96, 112, 52, "FILTER", "shapes the tone", MINT))
    o.append(f'<path d="M290,122 L318,122" stroke="{FOREST}" stroke-width="1.8"/><path d="M318,122 l-7,-4 l0,8z" fill="{FOREST}"/>')
    o.append(box(320, 96, 112, 52, "ENV 1", "each note's volume", MINT))
    o.append(f'<path d="M432,122 L460,122" stroke="{FOREST}" stroke-width="1.8"/><path d="M460,122 l-7,-4 l0,8z" fill="{FOREST}"/>')
    o.append(box(462, 96, 112, 52, "FX RACK", "up to seven effects", MINT))
    o.append(f'<path d="M574,122 L600,122" stroke="{FOREST}" stroke-width="1.8"/><path d="M606,122 l-8,-5 l0,10z" fill="{FOREST}"/>')
    o.append(t(608, 126, "OUT", 9.5, FOREST, 800, "start"))
    # modulation lane
    o.append(f'<rect x="178" y="200" width="396" height="50" rx="8" fill="{FOREST}"/>')
    o.append(t(376, 221, "MODULATION: LFO 1–4, ENV 2 and 3, CHAOS, MACROS", 9.5, CREAM, 800, ls=.4))
    o.append(t(376, 237, "wired through the 16-slot MATRIX to almost any knob", 8.6, MINT, 400))
    for x in (234, 376, 518):
        o.append(f'<path d="M{x},200 L{x},156" stroke="{LIMEDK}" stroke-width="2" stroke-dasharray="4 3"/><path d="M{x},150 l-5,8 l10,0z" fill="{LIMEDK}"/>')
    o.append(t(10, 254, "SOUND", 8, GREY, 700, "start", ls=1.6))
    return svg(640, 262, "".join(o))


def unison_fig():
    o = []
    o.append(t(150, 14, "ONE VOICE", 8.5, FOREST, 800, ls=1.2))
    o.append(t(450, 14, "THREE VOICES, DETUNED AND SPREAD", 8.5, FOREST, 800, ls=1.2))
    pts = [(20 + 260 * k / 300, 70 - 28 * math.sin(2 * math.pi * 3 * k / 300)) for k in range(301)]
    o.append(f'<path d="{path_from(pts)}" stroke="{FOREST}" stroke-width="2.6" fill="none"/>')
    cols = [SAGE, FOREST, SAGE]
    for v, det in enumerate([-.05, 0, .05]):
        pts = [(320 + 260 * k / 300, 70 - 28 * math.sin(2 * math.pi * (3 + det * 6) * k / 300 + v)) for k in range(301)]
        o.append(f'<path d="{path_from(pts)}" stroke="{cols[v]}" stroke-width="1.6" fill="none" opacity=".85"/>')
    o.append(t(150, 122, "a single, clean line", 9, INK, 500, style="italic"))
    o.append(t(450, 122, "slightly out of tune with each other: a shimmering choir", 9, INK, 500, style="italic"))
    # stereo spread
    o.append(f'<line x1="320" y1="150" x2="580" y2="150" stroke="{INK}"/>')
    o.append(t(320, 166, "LEFT", 8, GREY, 700, "start") + t(580, 166, "RIGHT", 8, GREY, 700, "end") + t(450, 166, "WIDTH spreads them across the stereo field", 8.4, INK, 500))
    for k, x in enumerate([336, 450, 564]):
        o.append(f'<circle cx="{x}" cy="150" r="6" fill="{cols[k]}" stroke="{FOREST}"/>')
    o.append(f'<line x1="20" y1="150" x2="280" y2="150" stroke="{INK}"/><circle cx="150" cy="150" r="6" fill="{FOREST}"/>')
    return svg(600, 176, "".join(o))


def layering_fig():
    o = []
    rows = [("OSC A", "DEFAULT, 3 unison voices", "the body", FOREST), ("OSC B", "one voice, an octave up, quieter", "the sparkle", MOSS),
            ("SUB", "a sine, an octave down", "the floor", SAGE)]
    for i, (a, b, c, col) in enumerate(rows):
        y = 10 + i * 46
        o.append(f'<rect x="10" y="{y}" width="360" height="38" rx="6" fill="{col}" opacity="{1 - i * .12}"/>')
        o.append(t(24, y + 24, a, 11, CREAM, 800, "start") + t(96, y + 24, b, 10, CREAM, 500, "start"))
        o.append(t(380, y + 24, c, 10, INK, 500, "start", style="italic"))
        o.append(f'<path d="M470,{y + 19} C500,{y + 19} 505,79 525,79" stroke="{FOREST}" stroke-width="1.6" fill="none"/>')
    o.append(f'<circle cx="545" cy="79" r="22" fill="{LIME}" stroke="{FOREST}" stroke-width="2"/>' + t(545, 83, "ONE", 9.5, FOREST, 800) + t(545, 116, "one patch", 8.5, INK, 500))
    return svg(600, 150, "".join(o))


def delay_reverb_fig():
    o = [t(150, 14, "DELAY: DISTINCT ECHOES", 8.5, FOREST, 800, ls=1.2), t(450, 14, "REVERB: A WASH OF REFLECTIONS", 8.5, FOREST, 800, ls=1.2)]
    for k in range(7):
        h = 90 * (.62 ** k)
        x = 30 + k * 36
        o.append(f'<rect x="{x}" y="{120 - h:.1f}" width="14" height="{h:.1f}" rx="2" fill="{FOREST if k == 0 else SAGE}"/>')
    o.append(t(150, 142, "each repeat quieter (FEEDBACK), spaced by TIME", 8.6, INK, 500, style="italic"))
    o.append(f'<rect x="330" y="30" width="12" height="90" rx="2" fill="{FOREST}"/>')
    import random
    rnd = random.Random(4)
    for k in range(120):
        x = 346 + k * 2
        h = 74 * math.exp(-k / 40) * (.55 + .45 * rnd.random())
        o.append(f'<rect x="{x}" y="{120 - h:.1f}" width="1.4" height="{h:.1f}" fill="{SAGE}"/>')
    o.append(t(450, 142, "thousands of tiny echoes blur into a tail (DECAY)", 8.6, INK, 500, style="italic"))
    o.append(f'<line x1="20" y1="120" x2="280" y2="120" stroke="{INK}"/><line x1="320" y1="120" x2="590" y2="120" stroke="{INK}"/>')
    return svg(600, 150, "".join(o))


def arp_fig():
    o = []
    o.append(t(110, 14, "YOU HOLD", 8.5, FOREST, 800, ls=1.2))
    o.append(t(400, 14, "THE ARP PLAYS (UP, 2 OCTAVES)", 8.5, FOREST, 800, ls=1.2))
    notes = [0, 3, 7]
    for i, n in enumerate(notes):
        y = 140 - n * 8
        o.append(f'<rect x="40" y="{y}" width="140" height="10" rx="3" fill="{FOREST}"/>')
    seq = [0, 3, 7, 12, 15, 19] * 2
    for i, n in enumerate(seq):
        y = 140 - n * 5.2
        o.append(f'<rect x="{230 + i * 29}" y="{y:.1f}" width="24" height="9" rx="3" fill="{MOSS if n < 12 else LIMEDK}"/>')
    o.append(f'<line x1="230" y1="160" x2="580" y2="160" stroke="{INK}"/>')
    for i in range(13):
        o.append(f'<line x1="{230 + i * 29}" y1="156" x2="{230 + i * 29}" y2="164" stroke="{INK}"/>')
    o.append(t(405, 178, "one note every 1/16 (RATE); the second octave in lime", 8.6, INK, 500, style="italic"))
    o.append(t(110, 178, "a three-note chord", 8.6, INK, 500, style="italic"))
    return svg(600, 186, "".join(o))


def mpc_hookup_fig():
    o = []
    # FM-1 mini
    o.append(f'<rect x="10" y="40" width="170" height="110" rx="10" fill="#E8EBE0" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<rect x="64" y="50" width="62" height="56" rx="4" fill="{SCREEN}"/>' + t(95, 82, "SHRUB", 8.5, LIME, 800))
    o.append(t(95, 140, "FM-1", 11, FOREST, 800))
    o.append(f'<circle cx="180" cy="70" r="6" fill="{INK}"/>' + t(186, 90, "AUDIO OUT", 7.6, FOREST, 800, "start"))
    # cable
    o.append(f'<path d="M186,70 C260,70 280,60 330,60" stroke="{INK}" stroke-width="3" fill="none"/>')
    o.append(f'<path d="M330,60 C360,60 380,78 418,78" stroke="{INK}" stroke-width="2.4" fill="none"/>')
    o.append(f'<path d="M330,60 C360,60 380,106 418,106" stroke="{INK}" stroke-width="2.4" fill="none"/>')
    o.append(f'<circle cx="330" cy="60" r="5" fill="{LIME}" stroke="{INK}"/>')
    o.append(t(300, 22, "3.5 mm TRS stereo to dual 6.35 mm TS mono breakout cable", 8.6, INK, 600))
    o.append(t(380, 72, "L", 9, FOREST, 800) + t(380, 121, "R", 9, FOREST, 800))
    # MPC mini
    o.append(f'<rect x="420" y="30" width="170" height="140" rx="10" fill="#E8EBE0" stroke="{INK}" stroke-width="2"/>')
    o.append(f'<circle cx="420" cy="78" r="6" fill="{INK}"/><circle cx="420" cy="106" r="6" fill="{INK}"/>')
    for r in range(3):
        for c in range(4):
            o.append(f'<rect x="{470 + c * 26}" y="{62 + r * 26}" width="22" height="22" rx="3" fill="#C9CEC0" stroke="{INK}" stroke-width=".8"/>')
    o.append(t(505, 158, "MPC SAMPLE", 10, FOREST, 800) + t(430, 50, "AUDIO IN", 7.6, FOREST, 800, "start"))
    o.append(t(430, 82, "1/L", 7.6, FOREST, 800, "start") + t(430, 110, "2/R", 7.6, FOREST, 800, "start"))
    o.append(t(300, 196, "Source on the MPC: Rear (both sides) for stereo", 9, INK, 500, style="italic"))
    return svg(600, 204, "".join(o))


def bank_fig():
    names = {101: ("MY CHILL PAD", "PAD"), 102: ("FIRST WAVE", "SYNTH"), 103: ("SOFT PLUCK", "PLUCK"), 104: ("DEEP BASS", "BASS"),
             105: ("SLOW TIDE", "PAD"), 106: ("WIDE SKY", "SYNTH"), 107: ("ECHO STEPS", "SEQ"), 108: ("NIGHT DRONE", "MISC"),
             109: ("GLASS KEYS", "PLUCK"), 110: ("WIND", "MISC")}
    catcol = {"PAD": SAGE, "SYNTH": MOSS, "PLUCK": LIMEDK, "BASS": FOREST, "SEQ": CLAY, "MISC": GREY}
    o = []
    for i in range(16):
        n = 101 + i
        c, r = i % 4, i // 4
        x, y = 6 + c * 148, 6 + r * 50
        if n in names:
            nm, cat = names[n]
            o.append(f'<rect x="{x}" y="{y}" width="140" height="42" rx="5" fill="{catcol[cat]}"/>')
            o.append(t(x + 8, y + 15, str(n), 8.5, CREAM, 500, "start", family=MONO) + t(x + 132, y + 15, cat, 7.2, CREAM, 800, "end", ls=1))
            o.append(t(x + 8, y + 33, nm, 10, CREAM, 800, "start"))
        else:
            o.append(f'<rect x="{x}" y="{y}" width="140" height="42" rx="5" fill="none" stroke="{RULE}" stroke-dasharray="4 3"/>')
            o.append(t(x + 8, y + 15, str(n), 8.5, GREY, 500, "start", family=MONO) + t(x + 8, y + 33, "INIT", 9.5, GREY, 600, "start"))
    return svg(600, 208, "".join(o))


def screen_anatomy():
    scr = scr_osc(vals=("1", "OFF", "0%", "75%"))
    o = [f'<g transform="translate(200,10) scale(.95)"><rect x="-6" y="-6" width="252" height="252" rx="12" fill="#2E322E"/>{scr}</g>']
    calls = [(30, "HEADER", "the part you're on, its page dots, and the level meter", 214),
             (100, "DISPLAY", "a picture of the part: here, a wavetable", 214),
             (200, "DECK", "the four values KNOB 1 to KNOB 4 change on this page", 214)]
    for y, h, d, xr in calls:
        o.append(f'<line x1="186" y1="{y + 10}" x2="200" y2="{y + 10}" stroke="{FOREST}" stroke-width="1.6"/><circle cx="186" cy="{y + 10}" r="3" fill="{FOREST}"/>')
        o.append(t(178, y + 8, h, 9.5, FOREST, 800, "end", ls=1))
        words, line, lines = d.split(), "", []
        for wd in words:
            if len(line + wd) > 26:
                lines.append(line)
                line = ""
            line += wd + " "
        lines.append(line)
        for j, ln in enumerate(lines):
            o.append(t(178, y + 22 + j * 12, ln.strip(), 8.8, INK, 400, "end"))
    o.append(t(452, 40, "pills: the parts", 8.8, INK, 500, "start", style="italic") + f'<line x1="430" y1="47" x2="448" y2="37" stroke="{FOREST}"/>')
    return svg(600, 256, "".join(o))


_ADV = None


def text_width(txt, size, path="fonts/archivo-latin-500-normal.woff2"):
    """Width of a string in the bundled Archivo 500, for laying out SVG text."""
    global _ADV
    if _ADV is None:
        import os
        from fontTools.ttLib import TTFont
        f = TTFont(os.path.join(os.path.dirname(os.path.abspath(__file__)), path))
        cmap, hmtx, upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
        _ADV = (cmap, hmtx, upm)
    cmap, hmtx, upm = _ADV
    return sum(hmtx[cmap.get(ord(c), cmap[32])][0] for c in txt) * size / upm


def section_map():
    """What each section button opens. Arrows are drawn as shapes, because
    the bundled fonts have no arrow glyph."""
    rows = [("EDIT", ["OSC A", "OSC B", "SUB", "FILTER"]), ("ENV", ["ENV 1", "ENV 2", "ENV 3", "MATRIX"]),
            ("LFO", ["LFO 1", "LFO 2", "LFO 3", "LFO 4", "CHAOS", "MATRIX"]), ("FX", ["FX RACK", "each effect in the rack"]),
            ("GLO", ["VOICING", "GLOBAL", "MACROS"]), ("SCL", ["SCALE"]), ("ARP", ["the arp (press again: on / off)"]),
            ("SEQ", ["the motion sequencer's lanes"]), ("HOME", ["the preset (hold: favourite)"]), ("SAVE", ["the save page (press again: save)"])]
    o = []
    for i, (b, parts) in enumerate(rows):
        y = 6 + i * 24
        o.append(f'<rect x="6" y="{y}" width="48" height="19" rx="3" fill="{FOREST}"/>' + t(30, y + 13.2, b, 8.6, CREAM, 800))
        x = 66
        for k, part in enumerate(parts):
            o.append(t(x, y + 13.5, part, 10, INK, 500, "start"))
            x += text_width(part, 10) + 6
            if k < len(parts) - 1:
                o.append(f'<path d="M{x:.1f},{y + 10:.1f} l10,0" stroke="{MOSS}" stroke-width="1.4"/><path d="M{x + 12:.1f},{y + 10:.1f} l-5,-3.2 l0,6.4z" fill="{MOSS}"/>')
                x += 18
        o.append(f'<line x1="66" y1="{y + 21.5}" x2="594" y2="{y + 21.5}" stroke="{RULE}" stroke-width=".7"/>')
    return svg(600, 248, "".join(o))


def keyboard_fig():
    o = []
    for i in range(16):
        x = 10 + i * 36
        o.append(f'<rect x="{x}" y="40" width="32" height="70" rx="5" fill="{CREAM}" stroke="{INK}"/>')
    names = "F G A B C D E F G A B C D E F G".split()
    for i, n in enumerate(names):
        o.append(t(26 + i * 36, 100, n, 9, GREY, 700))
    for j, i in enumerate(BLACK_AFTER):
        x = 10 + i * 36 + 36 - 11
        o.append(f'<rect x="{x}" y="40" width="22" height="42" rx="4" fill="{INK}"/>')
    c_idx = [4, 11]
    for c in c_idx:
        o.append(f'<circle cx="{26 + c * 36}" cy="122" r="3" fill="{LIMEDK}"/>')
    o.append(t(26 + 4 * 36, 138, "C", 8.5, FOREST, 800) + t(26 + 11 * 36, 138, "C", 8.5, FOREST, 800))
    o.append(t(300, 22, "27 KEYS: FROM F UP TO G, JUST OVER TWO OCTAVES", 8.5, GREY, 700, ls=1.2))
    return svg(600, 146, "".join(o))


def cover_art():
    """Original cover illustration: a shrub whose branches are waveforms."""
    import random
    rnd = random.Random(7)
    o = []
    def branch(x, y, ang, length, depth):
        if depth == 0 or length < 6:
            col = rnd.choice([LIME, "#CFE36A", SAGE, MINT, "#8DB36C"])
            r = rnd.uniform(3, 7.5)
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}" opacity="{rnd.uniform(.55, .95):.2f}"/>')
            return
        a = math.radians(ang)
        x2, y2 = x + length * math.cos(a), y - length * math.sin(a)
        # wavy branch
        n = 14
        pts = []
        for k in range(n + 1):
            f = k / n
            px, py = x + (x2 - x) * f, y + (y2 - y) * f
            off = math.sin(f * math.pi * 3) * length * .05
            pts.append((px + off * math.sin(a), py + off * math.cos(a)))
        o.append(f'<path d="{path_from(pts)}" stroke="#7FA37F" stroke-width="{max(.8, depth * .9):.1f}" fill="none" stroke-linecap="round" opacity=".9"/>')
        for d in (-1, 1):
            branch(x2, y2, ang + d * rnd.uniform(16, 34), length * rnd.uniform(.64, .8), depth - 1)
        if rnd.random() < .35:
            branch(x2, y2, ang + rnd.uniform(-8, 8), length * .6, depth - 1)
    branch(300, 470, 90, 108, 8)
    # ground line as sine
    pts = [(0 + 600 * k / 300, 474 + 5 * math.sin(k / 300 * math.pi * 10)) for k in range(301)]
    o.append(f'<path d="{path_from(pts)}" stroke="{SAGE}" stroke-width="1.6" fill="none" opacity=".7"/>')
    return f'<svg class="coverart" xmlns="http://www.w3.org/2000/svg" viewBox="0 20 600 470">{"".join(o)}</svg>'


def opener_sprig(seed=1):
    import random
    rnd = random.Random(seed)
    o = []
    def br(x, y, ang, L, d):
        if d == 0:
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(2, 4.2):.1f}" fill="{rnd.choice([LIME, SAGE, MINT])}" opacity=".9"/>')
            return
        a = math.radians(ang)
        x2, y2 = x + L * math.cos(a), y - L * math.sin(a)
        o.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#86A886" stroke-width="{d * .7:.1f}" stroke-linecap="round"/>')
        for s in (-1, 1):
            br(x2, y2, ang + s * rnd.uniform(18, 32), L * .72, d - 1)
    br(60, 118, 90, 30, 6)
    return f'<svg class="sprig" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">{"".join(o)}</svg>'


# ---------------------------------------------------------------------------
# Lesson panels: which controls each lesson highlights
# ---------------------------------------------------------------------------
PANELS = {
    "l1": ["MASTER", "PRESETS", "ALGORITHM", "SELECT", "HOME", "SAVE", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4", "OCT-", "OCT+"],
    "l2": ["EDIT", "SELECT", "ALGORITHM", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4", "OCT-", "OCT+", "SAVE"],
    "l3": ["ENV", "SELECT", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4", "PRESETS", "SAVE"],
    "l4": ["EDIT", "ENV", "GLO", "SELECT", "ALGORITHM", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4"],
    "l5": ["LFO", "EDIT", "ENV", "SELECT", "ALGORITHM", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4"],
    "l6": ["EDIT", "SELECT", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4", "GLO"],
    "l7": ["FX", "ARP", "SCL", "GLO", "PLAY", "REC", "SEQ", "SELECT", "ALGORITHM", "KNOB 1", "KNOB 2", "KNOB 3", "KNOB 4"],
    "l8": ["HOME", "SAVE", "PRESETS", "ALGORITHM", "EDIT", "LFO", "FX"],
}


def lesson_panel(key):
    return fm1_panel(PANELS[key])


FIGS = {
    "fm1_tour": fm1_tour,
    "rear_panel": rear_panel,
    "waveforms": waveforms_fig,
    "pitch": pitch_fig,
    "harmonics": harmonics_fig,
    "wavetable": wavetable_fig,
    "adsr": adsr_fig,
    "adsr_shapes": adsr_shapes_fig,
    "filter_lp": lambda: filter_fig("lp"),
    "filter_hp": lambda: filter_fig("hp"),
    "env2_sweep": env2_sweep_fig,
    "lfo": lfo_fig,
    "signal_flow": signal_flow,
    "unison": unison_fig,
    "layering": layering_fig,
    "delay_reverb": delay_reverb_fig,
    "arp": arp_fig,
    "mpc_hookup": mpc_hookup_fig,
    "bank": bank_fig,
    "screen_anatomy": screen_anatomy,
    "section_map": section_map,
    "keyboard": keyboard_fig,
}

SCREENS = {
    "home_init": lambda: scr_home(),
    "home_cut": lambda: scr_home(vals=("22.1 kHz", "10%", "1", "1"), hl=["CUTOFF"]),
    "home_pad": lambda: scr_home(name="PAD CHILL HAWK", num="042", cat="PAD", vals=("1.20 kHz", "12%", "20", "8"), hl=["CUTOFF", "A POS"],
                                 chips=[("SEQ", 0), ("ARP", 0), ("CHO", 1), ("DLY", 1), ("REV", 1)]),
    "save_l1": lambda: scr_save("101", "MY CHILL PAD", "PAD"),
    "save_l2": lambda: scr_save("102", "FIRST WAVE", "SYNTH"),
    "env_init": lambda: scr_env(hl=()),
    "env_pluck": lambda: scr_env(vals=("0.5 ms", "350 ms", "-inf dB", "250 ms"), shape=(.01, .25, 0, .15), hl=("DECAY", "SUSTAIN", "RELEASE")),
    "filter_bass": lambda: scr_filter(vals=("250 Hz", "30%", "20%", "100%"), hl=("CUTOFF", "RES", "DRIVE")),
    "filter_p2": lambda: scr_filter(vals=("0%", "0%", "40%", "50%"), labels=["FAT", "KEY TRK", "ENV 2", "STEREO"], hl=("ENV 2",), page=1),
    "osc_init": lambda: scr_osc(),
    "osc_sub": lambda: screen("SUB", "SUB", pills=["OSC A", "OSC B", "SUB", "FILTER"], active=2, dots=(2, 0),
                              display=f'<path d="{_wave("sine", 14, 70, 212, 70, 2)}" stroke="#B6D63E" stroke-width="2.4" fill="none"/>',
                              knobs=[("SHAPE", "SINE", False, 0), ("OCT", "-1", False, .4), ("SUB", "70%", True, .7), ("NOISE", "0%", False, 0)]),
    "lfo_tide": lambda: scr_lfo(),
    "rack_delay": lambda: scr_rack([("DISTORTION", "OFF"), ("CHORUS", "OFF"), ("DELAY", "ON"), ("COMPRESSOR", "OFF"), ("REVERB", "OFF"), ("EMPTY", ""), ("EMPTY", "")], sel=2, hl=("MODE",)),
}
