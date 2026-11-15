# Changelog

All notable changes to *Shrub, Gently*. Each entry names the SHRUB firmware version it was written against.

## v1.0.0 (15 November 2026), SHRUB V1.04

Released as version 1.0 by the author's decision; physical FM-1 testing continues and will feed later versions.

- `VERSION` set to v1.0 (cover-to-end-page version strings on pp. 67 and 68).
- About This Edition (p. 67): "This preview has not yet been tested on a physical FM-1; a hands-on pass is the next step before version 1.0" became "This edition has not yet been tested on a physical FM-1; a hands-on pass is under way, and any corrections will appear in later versions."
- No other content changes from v0.9.2. Verified by text and pixel comparison: only pp. 67 and 68 differ.

---

## v0.9.2-preview (15 November 2026), SHRUB V1.04

Focused correction pass after an independent second review. Still 68 pages; still not tested on a physical FM-1. All v0.9.1 corrections are preserved.

| # | Issue in v0.9.1 | Where | Change | Verified by | Hardware test? |
|---|---|---|---|---|---|
| 1 | **Source not reproducible.** Built with WeasyPrint 68, the v0.9.1 source produced 68 pages but silently lost the ten small screen illustrations (and their captions' layout) on pp. 13, 15, 20, 21, 22, 26, 27, 33, 37 and 47. | `figures.py`, `build.py`, new `requirements.txt` | Cause: the screen illustrations were wrapped in an SVG `clipPath` (for rounded corners), which WeasyPrint 68 drops. The clip is removed and the corners are drawn into the shapes. `requirements.txt` pins WeasyPrint 70.0 (the version recorded in the delivered PDF's metadata) and every dependency. `build.py` now refuses to run on any WeasyPrint other than 70.x with a clear message. | Reproduced the failure under WeasyPrint 68.0; clean rebuild from the archive in a fresh virtual environment; text, page geometry and rendered pages compared (see QA report) | No |
| 2 | Changing preset described as stopping any pattern | p. 14 note; p. 49 step 17; p. 50 Have a Play; p. 61 troubleshooting | Arp and motion-sequencer lanes now distinguished. A latched arp stops when switched off or (with ARP+SCALE on PRESET) when another preset loads. Recorded lanes keep playing after loading a preset without lanes; PLAY stops the transport, and SEQ with CLEAR LANE or CLEAR ALL removes them. Lesson 7's ECHO STEPS procedure unchanged. | Guide p. 25 (lanes, loading presets with and without lanes); guide p. 10 (PLAY starts and stops the transport); arp behaviour from v0.9.1 emulator tests | Yes: confirm on hardware |
| 3 | "Twelve buttons" | p. 7 | "Twelve main buttons, plus the two octave buttons (2): fourteen in total." Diagram unchanged: it already shows all fourteen. | Guide p. 10 ("fourteen buttons") | No |
| 4 | FAVORITES implied to hold only the ten course patches, though Lesson 1 starred 042 PAD CHILL HAWK | p. 55, Tidy the bank | New optional step: unstar earlier factory favourites by loading them and holding HOME; removing a star doesn't change the sound. Favourites stated as optional. | Guide p. 12 (hold HOME to add or remove a favourite) | No |
| 5 | MPC cable partly called an "insert" cable | p. 4; p. 56 step 1 and figure | Consistently "3.5 mm TRS stereo to dual 6.35 mm TS mono breakout cable": stereo plug to FM-1 AUDIO OUT, left mono plug to AUDIO IN 1/L, right to 2/R. Procedure and diagram layout unchanged. | Akai MPC Sample User Guide (AUDIO IN 1/L and 2/R; Source Rear) | Cable fit only |

---

## v0.9.1-preview (15 November 2026), SHRUB V1.04

Technical correction and refinement pass, checked against the official **SHRUB Operation Guide** (PDF, 46 pages, firmware V1.04, guide v1.0) and the FM-1 emulator running the official `SHRUB.fwsc`. Still not tested on a physical FM-1. 68 pages (v0.9: 64).

Guide page numbers below refer to that 46-page PDF. "Verified by" says how each change was checked: **Guide** (official documentation), **Emulator** (fm1-emu running the V1.04 package) or **Editorial** (teaching or clarity decision).

### Corrections

| # | Issue in v0.9 | Where (v0.9.1 page) | Change | Authority | Verified by | Hardware test? |
|---|---|---|---|---|---|---|
| A | Signal flow puts the filter before ENV 1 (flagged in review) | p. 10 | **No change.** Correct as drawn. | Guide p. 35: "SHRUB even puts ENV 1 after the filter" | Guide | No |
| B | Pluck: "the envelope no longer cares how long you hold the key" | p. 27, Listen For | Holding *longer* than the decay changes nothing; releasing *early* still hands over to the release, so short taps sound shorter. | Guide p. 16 (ENV stages); general synthesis | Editorial | No |
| C | ENV 2 described as if per note | pp. 30–31, 33, 34 | New paragraph: one ENV 2 shared by every note, restarts from where it is, releases when the last key is up. Step 14 notes overlapping notes bloom less. Wrap-up updated. | Guide p. 16 and p. 35 | Guide | No |
| D | Bass: OSC A at OCT −1 and SUB default OCT −1 described as "beneath" | p. 32 step 6; p. 34; p. 60 | Kept the settings (musically sound); rewrote the explanation: the sine doubles the saw's fundamental at the same octave. Added *fundamental* to Lesson 2 and the glossary. | SUB OCT default −1 seen in emulator | Emulator + Editorial | No |
| E1 | LFO rates 0.10 and 0.05 Hz repeat together every 20 s, yet text said "never quite repeats" | p. 39 steps 15–17; Listen For; p. 60 | LFO 2 now **about 0.07 Hz**. Text: they line up only after well over a minute. "Never repeats" reserved for CHAOS. | Guide p. 17 (CHAOS "never quite loops") | Emulator: 0.07 Hz and 0.10 Hz both selectable with BPM off | Listen on hardware |
| E2 | LFO diagram and text said modulation moves "either side" of the setting | p. 36 figure and AMOUNT bullet; p. 38 step 8 | BIPOLAR defaults **OFF** on INIT, so the LFO pushes one way (up and back). Figure redrawn unipolar; BIPOLAR explained; steps say leave it OFF; Have a Play tries it ON. | Guide p. 17 (BIPOLAR on page 2) | Emulator: LFO 1 page 2 BIPOLAR OFF on INIT | Confirm direction by ear |
| F | WIDE SKY used 5 voices (A) + 3 (B) and asked for big chords | pp. 40–44; figures; p. 60 | Now **3 voices on A, 1 on B** plus sub. New "Thickness costs notes" section and table. Step 10 checks VOICING shows 4 NOTES; step 12 demonstrates the trade-off. | Guide p. 21 (four notes, 16-voice pool) | **Emulator, VOICING page:** INIT 8 NOTES; A=5 → 3; A=3 → 5; A=5+B=3 → 2; A=3+B=1 → **4** | Confirm on hardware (see Discrepancy 1) |
| G | ECHO STEPS told readers to switch the arp off before saving | pp. 48–49 | Save **with the arp on and latched**. New part F: stop by loading another preset; reload 107 to bring it back. States the arp doesn't run on the transport. | Guide p. 21 ("A preset you save keeps what's set either way"); p. 24 (ARP on/off) | **Emulator:** arp played with PLAY unlit; saved with arp on, reloaded, ARP chip on HOME lit and pattern played; PLAY didn't stop a latched arp | Confirm on hardware |
| G2 | "Saved only when ARP+SCALE is PRESET" | p. 49 sidebar; Lesson 1 note | Rewritten: arp, scale and tempo always save with the preset; ARP+SCALE is a device setting that decides what happens when you change presets. | Guide p. 21 (ARP+SCALE bullet; device-wide settings list) | Guide | No |
| H | FX RACK KNOB 4 label | p. 47; Quick Reference | Instructions use **MODE** (what the screen shows). Small note: the guide's knob table says ON. | Guide p. 19 table says ON; **its own screenshot on p. 19 reads MODE** | Guide screenshot + Emulator | No |

### Smaller technical and usability fixes

| Issue | Where | Change | Verified by |
|---|---|---|---|
| Slots 101–110 assumed empty | p. 5 sidebar; each save step; challenge | New "Already used some of these slots?" box: save only when REPLACES INIT shows, otherwise move SLOT on. Lessons 2 and 7 add a one-line fallback. | Guide p. 13 (REPLACES, U prefix); Emulator showed U123 after saving |
| U prefix on saved slots | Lesson 1 step 19; Quick Reference; troubleshooting | Explains every saved slot shows a U (v0.9 implied only factory slots) | Emulator (saved INIT showed U123) |
| Leftover characters when naming | Lesson 1 step 16 | Mentions names like "INIT [E]" appear on the save page | Emulator (save page showed INIT [E]) |
| "KNOB 1to KNOB 4" | p. 6 | Sentence rebuilt so text never starts with a chip | Rendered PDF inspection |
| Wavetable choice relied on click counts | p. 22 step 15 | Target is the displayed name SAW>SQUARE | Editorial |
| DEST one click | p. 38 step 10 | Removed "only a click" | Editorial |
| Unison defaults wrong (DETUNE and WIDTH) | pp. 42–43 | DETUNE starts at 50% and WIDTH at +100%; steps rewritten around that | Emulator (OSC A page 2 on INIT: DETUNE 50%, WIDTH +100%) |
| "No wrong notes" | Lesson 7 | Scale moved to Have a Play; now "keeps you inside one family of notes", not a guarantee | Editorial |
| CLEAR ALL warning | Lesson 7 Have a Play; troubleshooting | Prefer CLEAR LANE on the chosen lane; CLEAR ALL wipes every lane and asks to confirm; loading a lane-less preset doesn't clear lanes | Guide p. 25 |
| Lesson 1 note said PLAY stops patterns | p. 14 | Explains patterns belong to the preset; changing preset stops them | Emulator (PLAY didn't stop the arp) |
| Arp switch-on screen text | Lesson 7 step 10 | Uses HOLD NOTES TO ARPEGGIATE (seen on screen) instead of unverified wording | Emulator |
| MPC cable | p. 56 step 1; figure | 3.5 mm TRS stereo to two 6.35 mm TS mono plugs; L to AUDIO IN 1/L, R to 2/R; Source Rear = stereo | Akai MPC Sample User Guide (Input Configuration: Rear = 1/L and 2/R in stereo) |
| Gain values | p. 56 step 4 | Set by meters; no invented numbers | Akai guide (REC GAIN sets line-level AUDIO IN) |
| .shrubbank contents | p. 55 | 128 slots, their wavetables and the MIDI map | Guide p. 42–43 |
| Save warnings | p. 62 | Adds AUX CUT, LFOS CUT and NO LFO 4, with recovery advice | Guide p. 13 |
| Chromatic MPC playback | p. 57; Where Next | One note is one sample; repitch on the MPC or record each note | Editorial |
| Fallback fonts | p. 1, p. 5, p. 8, p. 13 | Non-breaking hyphens, arrow glyphs and bold mono digits fell back to system fonts (Inter, Plex Mono Bold). Replaced so only bundled OFL fonts embed. | pdffonts |
| Diagram labels | p. 6 callouts 1 and 4; p. 36 LFO figure; p. 56 MPC figure | Callouts moved off labels; clipped and colliding labels fixed | Rendered PDF inspection |

### Educational changes
- **Lesson 7 simplified:** delay, reverb and the arp form the main recipe. The scale moved to Have a Play. New "Stop, and bring it back" part teaches loading a preset to stop a latched arp and that the arp saves with the patch. Time reduced to about 40 minutes.
- **Lesson 8 strengthened:** five design questions (space now separate from movement). New optional challenge "A sound with no recipe" (imagine, plan on paper, build in an unused slot, compare, refine). Time is now 60 to 90 minutes or two sittings; the welcome page says so.
- **Lesson 6:** teaches the voice budget explicitly, with a demonstration of losing notes.
- **Lesson 5:** BIPOLAR explained; LFO rates corrected.
- Glossary adds *Bipolar*, *Fundamental* and *Transport*.

### Unchanged by design
Title, cover, palette, page size, eight-lesson structure, six-part lessons, the ten patches and their slots, all other diagrams.

---

## v0.9.0-preview (15 November 2026), SHRUB V1.04

First complete edition. Not yet tested on a physical FM-1.

- Front matter, eight lessons and back matter; ten patches in slots 101 to 110.
- Original vector illustrations and simplified screen illustrations.
- PDF bookmarks and linked contents.
- Research and verification notes.

## Planned for the next version
- Full hands-on pass of every lesson on a physical FM-1 at V1.04 or later (checklist in docs/RESEARCH-AND-VERIFICATION.md).
- Resolve remaining hardware questions; update screens and values where hardware differs.
