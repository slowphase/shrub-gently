# Changelog

## v0.9.2-preview, November 2026

- **Reproducible build.** The source now pins WeasyPrint 70.0 and its dependencies in `source/book/requirements.txt`, and `build.py` stops with a clear message on any other WeasyPrint version. The screen illustrations no longer use an SVG clip path, which WeasyPrint 68 silently dropped. A clean rebuild from the source archive matches the PDF in text, page geometry and rendered pages.
- **Arpeggiator vs motion sequencer.** The book now distinguishes a latched arp (stops when switched off or when another preset loads) from recorded sequencer lanes (keep playing after loading a preset without lanes; stop with PLAY, remove with SEQ and CLEAR LANE or CLEAR ALL). Pages 14, 49, 50 and 61.
- **Button count.** Twelve main buttons plus two octave buttons, fourteen in total (page 7).
- **Favourites.** Lesson 8 explains how to unstar factory presets starred earlier, so FAVORITES can hold only your own bank (page 55).
- **MPC cable.** Consistently described as a 3.5 mm TRS stereo to dual 6.35 mm TS mono breakout cable (pages 4 and 56).
- Still 68 pages; still pending physical-hardware validation. Details: [source/book/CHANGELOG.md](source/book/CHANGELOG.md).

## v0.9.1-preview, November 2026

- First public release. 68 pages, written for SHRUB firmware V1.04 and checked against the official *SHRUB Operation Guide* (V1.04, guide v1.0) and the FM-1 emulator running the official firmware.
- **WIDE SKY** (Lesson 6) rebuilt to play four-note chords, with a new section on how unison voices share a pool of 16 and reduce polyphony.
- **ECHO STEPS** (Lesson 7) now saves with the arpeggiator on and latched; the lesson shows how to stop it (change preset, not PLAY) and bring it back. Scales moved to Have a Play.
- **SLOW TIDE** (Lesson 5) uses LFO rates of 0.10 and 0.07 Hz; BIPOLAR explained and the LFO diagram redrawn.
- Lesson 4 explains the shared ENV 2 and why the sine sub doubles the bass's fundamental.
- New optional "sound with no recipe" challenge in Lesson 8; Lesson 8 now 60 to 90 minutes or two sittings.
- Slot-safety guidance: every save checks for REPLACES INIT, so you never overwrite a sound of your own.
- FX RACK KNOB 4 follows the screen label MODE (the guide's table says ON; its own screenshot says MODE).
- MPC recording: exact cable (3.5 mm TRS stereo to two 6.35 mm TS mono), inputs 1/L and 2/R, Source Rear.
- Fuller save warnings, troubleshooting and glossary.
- Only bundled fonts are embedded.
- Still pending physical-hardware validation. Full manuscript history, with guide page references for each change: [source/book/CHANGELOG.md](source/book/CHANGELOG.md).

## v0.9.0-preview, November 2026 (unreleased)

- First complete draft: eight lessons, ten patches, 64 pages. Superseded by v0.9.1 before publication.
