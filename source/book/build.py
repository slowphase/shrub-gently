"""Build Shrub, Gently.

    pip install weasyprint
    python3 build.py              # writes Shrub-Gently.pdf
    python3 build.py out.pdf

Text lives in content/*.html (read in name order). Markup helpers:
    [[EDIT]]            a button chip
    [[@KNOB 1]]         a knob chip (any of the seven endless knobs, or MASTER)
    [[~SAVED]]          text exactly as it appears on the FM-1 screen
    <!--FIG:name|caption-->        a diagram from figures.FIGS
    <!--PANEL:l3|caption-->        a lesson's FM-1 panel; the next <dl class="controls"> sits beside it
    <!--SCR:name|caption|left-->   a small screen mock-up from figures.SCREENS, floated (right unless 'left')
    <!--SPRIG:n-->                 the little branch on a lesson opener
    <!--COVERART-->                the cover illustration
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
import figures as F  # noqa: E402
import weasyprint  # noqa: E402

VERSION = "v0.9.1 Preview"
FIRMWARE = "V1.04"


def fig_sub(m):
    name, _, cap = m.group(1).partition("|")
    cap = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="diagram">{F.FIGS[name]()}{cap}</figure>'


def scr_sub(m):
    parts = m.group(1).split("|")
    name = parts[0]
    cap = parts[1] if len(parts) > 1 else ""
    side = " left" if len(parts) > 2 and parts[2] == "left" else ""
    cap = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="scrfig{side}">{F.screen_svg(F.SCREENS[name](), "42mm")}{cap}</figure>'


def panel_sub(m):
    key, _, cap = m.group(1).partition("|")
    return (f'<table class="meetgrid"><tr><td class="mfig"><figure class="panelfig">{F.lesson_panel(key)}'
            f'<figcaption>{cap}</figcaption></figure></td><!--MEETSPLIT-->')


def chip(m):
    s = m.group(1)
    if s.startswith("@"):
        return f'<span class="kn">{s[1:]}</span>'
    if s.startswith("~"):
        return f'<span class="scr">{s[1:]}</span>'
    return f'<span class="k">{s}</span>'


def bm(m):
    tag, title = m.group(2), re.sub(r"<[^>]+>", "", m.group(3)).strip()
    label = (tag + ": " + title).replace('"', "&quot;")
    return f'<h2{m.group(1)} data-bm="{label}"><span class="tag">{tag}</span>{m.group(3)}</h2>'


def smart_quotes(html):
    """Curly apostrophes and quotes in text only (never inside tags or SVG)."""
    out = []
    for part in re.split(r"(<svg.*?</svg>|<[^>]+>)", html, flags=re.S):
        if part.startswith("<"):
            out.append(part)
            continue
        part = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", part)
        part = re.sub(r"(\w)'", "\\1\u2019", part)
        part = re.sub(r"'(\w)", "\u2018\\1", part)
        part = re.sub(r'"(\w)', "\u201c\\1", part)
        part = re.sub(r'(\S)"', "\\1\u201d", part)
        out.append(part)
    return "".join(out)


def build(out):
    body = "\n".join(open(f, encoding="utf-8").read() for f in sorted(glob.glob("content/*.html")))
    body = body.replace("{{VERSION}}", VERSION).replace("{{FIRMWARE}}", FIRMWARE)
    body = re.sub(r"<!--FIG:(.*?)-->", fig_sub, body)
    body = re.sub(r"<!--SCR:(.*?)-->", scr_sub, body)
    body = re.sub(r"<!--PANEL:(.*?)-->", panel_sub, body)
    body = re.sub(r"<!--SPRIG:(\d+)-->", lambda m: F.opener_sprig(int(m.group(1))), body)
    body = body.replace("<!--COVERART-->", F.cover_art())
    body = re.sub(r'(<table class="meetgrid">.*?<!--MEETSPLIT-->)\s*((?:<p>.*?</p>\s*)?<dl class="controls">.*?</dl>)',
                  lambda m: m.group(1) + '<td class="meetlist">' + m.group(2) + "</td></tr></table>", body, flags=re.S)
    body = re.sub(r'<h2([^>]*)><span class="tag">(.*?)</span>(.*?)</h2>', bm, body)
    body = re.sub(r"\[\[(.+?)\]\]", chip, body)
    body = re.sub(r'<ol class="steps" start="(\d+)">', lambda m: f'<ol class="steps" style="counter-reset: st {int(m.group(1)) - 1}">', body)

    body = smart_quotes(body)

    # house style: no em dashes anywhere
    for bad in ("—", "&mdash;", "&#8212;"):
        assert bad not in body, "em dash found"

    html = f"""<!doctype html><html lang="en-AU"><head><meta charset="utf-8">
<title>Shrub, Gently</title>
<meta name="author" content="slowphase">
<meta name="description" content="An illustrated beginner's guide to wavetable synthesis on the M-VAVE FM-1 running SHRUB {FIRMWARE}">
<meta name="keywords" content="SHRUB, M-VAVE FM-1, synthesis, beginner, wavetable">
<link rel="stylesheet" href="style.css"></head><body>
{body}
</body></html>"""
    open("book.html", "w", encoding="utf-8").write(html)
    doc = weasyprint.HTML("book.html", base_url=ROOT).render()
    print("pages:", len(doc.pages))
    doc.write_pdf(out)
    print("wrote", out, os.path.getsize(out) // 1024, "KB")


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "Shrub-Gently.pdf")
