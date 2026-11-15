# Credits

## The firmware and instrument this book is about

- **Steve Duda** and **[Xfer Inc.](https://xferrecords.com/)**, for **[SHRUB](https://shrub.audio/)**: a free wavetable synthesiser firmware for the M-VAVE FM-1, with its browser editor and VST3.
- The official **[SHRUB Operation Guide](https://shrub.audio/guide/)** (firmware V1.04, guide version 1.0, November 2026). Every button, page, knob and step in the handbook was checked against it.
- **M-VAVE**, makers of the FM-1.

## Verification tools

- **[fm1-emu](https://github.com/joakimeriksson/fm1-emu)** by **Joakim Eriksson**, which runs the official SHRUB firmware package in a browser (via [shrub.audio/play](https://shrub.audio/play)). It was used to confirm screen labels, starting values, the polyphony readout, arpeggiator saving and LFO rate steps.
- The **SHRUB browser editor** (build 1.04), used for the factory preset list and wavetable names.

## For the optional MPC section

- The official **[Akai MPC Sample User Guide](https://www.akaipro.com/guides/mpc-sample/introduction.htm)**, for the AUDIO IN connections, Source settings and REC GAIN.

## Background reading

Published coverage of the FM-1 helped confirm its rear-panel connections. Only the official SHRUB Operation Guide was used as the authority for instructions.

- [Synth Anatomy: M-VAVE FM-1 review](https://synthanatomy.com/2026/07/m-vave-fm-1-review-low-budget-pocket-fm-ynthesizer-with-iconic-sounds.html)
- [Synthtopia: M-VAVE introduces the FM-1](https://www.synthtopia.com/content/2026/07/13/m-vave-introduces-fm-1-fm-pocket-synthesizer/)

## Artwork

Every illustration in the handbook and this repository is this project's own: the cover shrub, the simplified FM-1 panel drawings, the screen illustrations and all teaching diagrams. They are drawn in code (`source/book/figures.py`). The panel drawings follow the FM-1's layout but are simplified and not to scale. The screen illustrations follow the layout the Operation Guide describes; they are not screenshots.

The preview images in `previews/` are rendered from the handbook. The README hero uses the cover illustration.

## Typefaces

- **Archivo** by The Archivo Project Authors (SIL OFL 1.1)
- **Source Serif 4** by Adobe (SIL OFL 1.1)
- **IBM Plex Mono** by IBM Corp. (SIL OFL 1.1)
- **Michroma** by The Michroma Project Authors (SIL OFL 1.1)
- **Fraunces** by The Fraunces Project Authors (SIL OFL 1.1): the cover title, a fixed Black instance (soft, largest optical size) made from the variable font
- **Jost** by The Jost Project Authors (SIL OFL 1.1): the cover subtitle
- Delivered through [Fontsource](https://fontsource.org/).

## How the handbook was made

*Shrub, Gently* was researched, written, illustrated and laid out with AI assistance (Claude, by Anthropic) for the research, the writing, the build code, the page layout and repeated rounds of review against the official SHRUB documentation.

Steve Duda, Xfer Inc. and M-VAVE were not involved in making it, and it is not endorsed by them. Any mistakes are this project's own. Please [report them](https://github.com/slowphase/shrub-gently/issues/new/choose).
