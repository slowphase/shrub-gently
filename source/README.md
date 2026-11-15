# Shrub, Gently: editable source

This folder holds everything needed to rebuild the handbook, for example after hardware testing or a firmware update. You don't need any of it to *read* the book: the finished PDF is on the [Releases page](https://github.com/slowphase/shrub-gently/releases), along with this same source as a ZIP.

One manuscript, one edition (160 × 244 mm, sized for the iPad mini).

## What's where

| Path | What it is |
| --- | --- |
| `book/content/*.html` | The manuscript, in reading order: front matter, Lessons 1 to 8, then the reference pages. **Edit the words here.** |
| `book/build.py` | Assembles the manuscript, draws the diagrams into it, expands control "chips", applies curly quotes and renders the PDF with bookmarks and links. Set `VERSION` and `FIRMWARE` at the top. |
| `book/figures.py` | Draws the FM-1 panel, the screen illustrations, the teaching diagrams and the cover shrub (Python that writes SVG). `PANELS` sets which controls light up in each lesson. |
| `book/style.css` | The design system: palette, typography, page size, callouts and layout. |
| `book/fonts/` | Archivo, Source Serif 4, IBM Plex Mono, Michroma, Jost (latin subsets) and a fixed Fraunces instance (SIL OFL 1.1). |
| `book/docs/RESEARCH-AND-VERIFICATION.md` | Sources, every check against the Operation Guide and emulator, discrepancies, and the hardware checklist for v1.0. |
| `book/CHANGELOG.md` | Detailed manuscript history, with guide page references for each correction. |

## Writing conventions

The manuscript uses short tokens that the build turns into the small labels you see in the book:

| You write | You get |
| --- | --- |
| `[[EDIT]]` | a button |
| `[[@KNOB 1]]` | a knob (any of the seven endless knobs, or MASTER) |
| `[[~SAVED]]` | words on the FM-1's screen |
| `<span class="target">about 350 ms</span>` | a target value |
| `<!--PANEL:l3\|caption-->` | the lesson's FM-1 panel; the next `<dl class="controls">` sits beside it |
| `<!--FIG:adsr\|caption-->` | a teaching diagram from `figures.FIGS` |
| `<!--SCR:env_pluck\|caption\|left-->` | a floated screen illustration from `figures.SCREENS` |
| `<ol class="steps" start="7">` | numbered steps continuing from 7 |

## Building

You'll need Python 3 with `weasyprint` (version 70 was used; it also installs `fontTools`, which the figures use to measure text).

```
cd source/book
pip install weasyprint
python3 build.py                 # writes Shrub-Gently.pdf
python3 build.py other-name.pdf  # or choose the output name
```

A full build takes under a minute. Afterwards, `pdffonts Shrub-Gently.pdf` should list only the bundled typefaces. Anything else (Inter, DejaVu, a bold Plex Mono) means a character or weight the bundled fonts don't cover; the arrow glyph (→) and the non-breaking hyphen are known gaps, so draw arrows in `figures.py` instead.

## Rules the build keeps

- No em dashes anywhere: the build stops if it finds one.
- Every hardware instruction restates something checked against the official *SHRUB Operation Guide* or observed on the emulator or a real FM-1. When updating, say which in the changelog.
- Where the official guide is silent or disagrees with the screen, the book follows the screen and the verification notes record it.
- Navigation is always "press EDIT until OSC A is lit", never a fixed number of presses. Values are targets ("about 350 ms"), never click counts; name the on-screen target (a wavetable name, a mode) instead.
- Every save checks that the SAVE page says REPLACES INIT before saving, so readers never overwrite a sound of their own.
- Australian spelling; screen text exactly as the FM-1 shows it (including its US spellings, such as COLOR and FAVORITES).

## Licences

The original text, artwork and diagrams are CC BY-SA 4.0. The build scripts and stylesheet are MIT. The fonts are SIL OFL 1.1. Full details are in [LICENSE.md](../LICENSE.md).
