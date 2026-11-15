# Shrub, Gently: research and technical verification

Edition: **v0.9.2 Preview**, 15 November 2026
Written against: **SHRUB firmware V1.04** for the M-VAVE FM-1
Primary authority: **SHRUB Operation Guide**, PDF export of shrub.audio/guide, 46 pages, "Firmware V1.04 · Guide version 1.0 · November 2026". Page numbers below refer to that PDF.

**Nothing in this book has been tested on a physical FM-1.**

## 1. Sources and methods

| Source | Used for | Limits |
|---|---|---|
| SHRUB Operation Guide PDF (46 pp.) | All documented behaviour, control names, knob tables, saving, recovery | Its knob table and its screenshot disagree on FX RACK KNOB 4 (see below) |
| fm1-emu v0.5.1 (Joakim Eriksson) running the official `SHRUB.fwsc` V1.04, via shrub.audio/play | Screen labels, INIT defaults, polyphony readout, arp saving and recall, LFO rate resolution | Emulates the chip at 100 MHz (real unit 240 MHz). Mouse and keyboard input. Sound not judged. |
| SHRUB editor, build 1.04 (shrub.audio/editor) | Factory preset list, wavetable names and frame counts, matrix destination order | Editor screens differ from device screens |
| Akai MPC Sample User Guide (akaipro.com/guides/mpc-sample; v1.3.0 PDF) | AUDIO IN sockets (1/L, 2/R), Source names, REC GAIN, Monitor | Not tested with an FM-1 |
| FM-1 press (Synth Anatomy review, Synthtopia) | Rear panel: 3.5 mm stereo out (speaker mutes), 3.5 mm TRS MIDI IN, USB-C, power switch | Stock-firmware features (Bluetooth) not claimed for SHRUB |

## 2. Official-guide cross-check, issue by issue

### A. Signal flow (book p. 10): confirmed, unchanged
Guide p. 35: the filter is shared, and "SHRUB even puts ENV 1 after the filter". Sources → filter → ENV 1 → FX is correct. A/B/N/S switches route sources around the filter (guide p. 15, p. 35); the book teaches the SUB switch in Lesson 4.

### B. Pluck envelope (book p. 27): clarified
Sustain at −inf dB: holding beyond the decay changes nothing; an early release enters the release stage from the current level. Standard ADSR behaviour, consistent with guide p. 16.

### C. ENV 2 shared (book pp. 30–34): clarified
Guide p. 16: "ENV 2 and ENV 3 are shared by all notes: a new note restarts them from where they are, and they let go when the last key is up." Guide p. 35 repeats this. The bass is mono with GLIDE, so the exercise is unaffected.

### D. Bass octaves (book p. 32): explanation fixed, settings kept
Emulator: SUB page 1 on INIT reads SHAPE SINE, OCT −1, SUB 0%. With OSC A at OCT −1 the sine sits at the same octave as the saw's fundamental. The book now says so. Alternative considered: SUB OCT −2. Rejected because it would sit two octaves below the keys, too deep for most playback, and the brief asked not to change settings when wording suffices.

### E. LFO rates and BIPOLAR (book pp. 36–40)
- Guide p. 17: page 2 is BPM, MODE, PHASE, BIPOLAR. Rate shows Hz with BPM off.
- Emulator: LFO 1 page 2 on INIT read BPM ON, MODE RETRIG, PHASE 0 deg, **BIPOLAR OFF**. With BPM off, RATE displayed 0.00 Hz at the bottom and stepped through 0.02, 0.07 Hz upwards; 0.07 and 0.10 Hz are both reachable.
- 0.10 Hz (10 s) and 0.07 Hz (about 14.3 s) coincide at roughly 100 s, versus 20 s for 0.10 and 0.05 Hz. The book says "well over a minute".
- Unipolar behaviour (pushes up from the set value) is the conventional meaning of BIPOLAR OFF in Serum-derived engines and matches the guide's wording. The direction has not been heard on hardware.

### F. Polyphony and unison (book pp. 40–44)
Guide p. 21: "SHRUB plays up to four notes at once, each with up to eight unison voices per oscillator, from a pool of 16 voices. A thick unison patch plays fewer notes; one note always plays."

Emulator, VOICING page readout (POLY, n NOTES):

| OSC A voices | OSC B (LEVEL > 0) voices | VOICING showed |
|---|---|---|
| 1 | B silent | 8 NOTES |
| 5 | B silent | 3 NOTES |
| 3 | B silent | 5 NOTES |
| 3 | 1 | **4 NOTES** (WIDE SKY v0.9.1) |
| 5 | 3 | 2 NOTES (WIDE SKY v0.9) |

Interpretation: notes ≈ floor(16 ÷ voices per note), with B counting only when it's audible. The readout can exceed the guide's "four notes". The book quotes the guide's ceiling, tells readers to trust the VOICING page, and builds WIDE SKY to show 4.

### G. Arp state, latch, transport and saving (book pp. 48–49)
Guide p. 24: press ARP to open, again to turn on or off. Guide p. 21: ARP+SCALE PRESET/GLOBAL governs recall when changing presets; "A preset you save keeps what's set either way." Guide p. 21 also lists ARP+SCALE among device settings.

Emulator tests on an INIT slot:
1. ARP pressed twice (open, on). Held three keys: arp played UP 1/16 with the PLAY button unlit. **The arp does not need the transport.**
2. SAVE to 123. Moved to 125, back to 123: HOME showed U123 with the **ARP chip lit**, and holding keys played the arp. **On state and settings recall.**
3. LATCH ON, released keys: the pattern continued. Pressed PLAY (transport started, PLAY lit), then pressed it again: **the latched pattern kept playing**. Turning PRESETS to another slot stopped it.

The book's procedure follows these results: save with the arp on; stop by changing preset; reload to recall.

### H. FX RACK KNOB 4: ON vs MODE
- Guide p. 19, knob table: SLOT, MODULE, MOVE, **ON** ("on or off").
- Guide p. 19, **screenshot of the FX RACK page beside that table**: knobs labelled SLOT, SLOT 1, MOVE, **MODE**, value OFF.
- Emulator (V1.04): MODE. Turning it on DELAY went OFF → NORMAL → PING-PONG; the rack list showed ON.
- Conclusion: the firmware labels the knob MODE; the guide's table uses an older or shorthand name. The book instructs MODE and notes the guide's wording once (p. 47) and in the Quick Reference.

### I. Arpeggiator vs motion-sequencer lanes (added v0.9.2)
Two different things can make a sound keep moving, and they stop differently:

| | Arpeggiator (LATCH on) | Motion-sequencer lanes |
|---|---|---|
| Needs the transport (PLAY)? | No. Plays whenever it's on and notes are held or latched (emulator, v0.9.1). | Yes. Lanes play back on the transport; REC starts it (guide p. 25). |
| Does PLAY stop it? | No (emulator, v0.9.1). | Yes: PLAY starts and stops the transport (guide p. 10). |
| Does loading another preset stop it? | Yes, with ARP+SCALE on PRESET, the default: the new preset brings its own arp state (guide p. 21; emulator, v0.9.1). With GLOBAL, the arp carries on by design. | Only if the new preset has lanes of its own, which replace them. A preset without lanes leaves them running (guide p. 25). |
| How to remove it | Press ARP on the arp page to switch it off. | SEQ, choose the lane with SELECT, POINT to CLEAR LANE, press SEQ; or CLEAR ALL (press SEQ twice), which wipes every lane in the current sound (guide p. 25). |

The book's wording on pp. 14, 49, 50 and 61 follows this table. Not yet confirmed on hardware.

## 3. Full-book verification summary
Every button, knob and screen label in the book was compared against guide pp. 10–29 and, where the book quotes a starting value, the emulator.

| Area | Result |
|---|---|
| Panel layout (7 endless knobs, MASTER, 14 buttons, 27 keys) | Guide p. 10; emulator panel. OK (v0.9.2: text now says twelve main buttons plus two octave buttons, fourteen in total) |
| Section order (EDIT, ENV, LFO, FX, GLO) | Guide p. 10 table. OK |
| HOME knobs CUTOFF, RES, A POS, B POS | Guide p. 12. OK |
| 128 slots, 100 factory, 7 categories, INIT 101–128, U prefix | Guide p. 12; emulator. OK |
| Save page knobs and messages | Guide p. 13. OK; messages expanded |
| OSC pages 1–4, warp list, SUB/NOISE pages | Guide p. 14. OK |
| Filter: 76 types, pages 1–3, paraphonic | Guide p. 15. OK |
| ENV pages, ENV 1 per note, ENV 2/3 shared | Guide p. 16. OK; book clarified |
| LFO pages 1–4, modes FREE/RETRIG/ENVELOPE, DEST shortcut, CHAOS | Guide p. 17. OK |
| Matrix 16 slots, sources list | Guide pp. 17–18. OK |
| FX modules, delay modes, reverb modes | Guide pp. 19–20. OK (MODE label, see H) |
| VOICING, GLOBAL pages, ARP+SCALE, USB LEVEL, hold GLOBAL | Guide p. 21. OK |
| SCL: 51 scales, CHORD | Guide p. 23. OK |
| ARP pages, 19 patterns, LATCH | Guide p. 24. OK |
| SEQ: REC, lanes, POINT/CLEAR LANE/CLEAR ALL, confirm | Guide p. 25. OK |
| Recovery: USB recovery (OCT− + OCT+), safe start, watchdog, red screen, BAT LOW | Guide p. 28. OK |
| Installer advice, going back to M-VAVE firmware | Guide p. 9. OK |
| .shrubbank contents (128 slots, wavetables, MIDI map) | Guide pp. 42–43. OK |
| Wavetable names used (DEFAULT, BASIC SHAPES, SAW>SQUARE, DUDA CHOIR, NICE PLUGGER, RULE …) | Editor list; DUDA CHOIR 38 frames, SAW>SQUARE 64, DEFAULT 9. OK |
| Factory preset 042 PAD CHILL HAWK | Editor list. OK |

### INIT defaults quoted in the book (emulator)
HOME CUTOFF 2.06 kHz, RES 10%; OSC A DEFAULT, WT POS 1, LEVEL 75%, VOICES 1, DETUNE 50%, BLEND 75%, WIDTH +100%, OCT 0; OSC B LEVEL 0%; SUB SINE, OCT −1, 0%; FILTER LP 24, all sources ON; ENV 1 0.5 ms / 1.00 s / 0.0 dB / 15 ms; LFO 1 RATE 1/4 (BPM on), RETRIG, BIPOLAR OFF; FX RACK DISTORTION, CHORUS, DELAY, COMPRESSOR, REVERB all OFF; VOICING POLY, 8 NOTES; GLOBAL TEMPO 120, LEVEL −6.0 dB, ARP+SCALE PRESET; ARP RATE 1/16, GATE 100%, OCTAVES 1; SCALE KEY −−.

## 4. Confirmed vs unresolved

**Confirmed (guide and emulator agree):** shared filter and ENV 1 placement; ENV 2/3 shared; MODE label on screen; arp saved on and recalled; arp independent of transport; unison reduces notes; BIPOLAR off by default; U prefix after saving; 0.07 Hz selectable.

**Discrepancies recorded:**
1. **Polyphony ceiling.** Guide: up to four notes. Emulator VOICING: up to 8 NOTES on a one-voice patch. The book quotes the guide and relies on the on-screen readout. Needs hardware.
2. **ON vs MODE.** Guide table vs firmware screen; resolved in favour of the screen (the guide's own screenshot agrees).
3. **EDIT re-entry.** Emulator reopened the last-visited part; guide p. 14 says EDIT opens OSC A. Book wording ("press until OSC A is lit") works either way.

## 5. Renderer dependency and reproducibility (added v0.9.2)

- The delivered PDFs record `Producer: WeasyPrint 70.0` in their metadata. That is the renderer the layout was tuned for.
- **Fault found in v0.9.1:** rebuilt with WeasyPrint 68.0, the v0.9.1 source produced 68 pages, but the ten floated screen illustrations (pp. 13, 15, 20, 21, 22, 26, 27, 33, 37, 47) vanished and their pages' text extraction differed. Cause: the illustrations were wrapped in an SVG `<clipPath>`, which WeasyPrint 68 dropped along with its contents.
- **Fixes:** the clip path is removed (rounded corners are drawn into the shapes, visually identical at print size); `source/book/requirements.txt` pins WeasyPrint 70.0 and every dependency to the exact versions used; `build.py` exits with an explanatory error on any WeasyPrint other than 70.x (override with `SHRUB_ALLOW_ANY_WEASYPRINT=1` only for testing).
- **Test:** fresh extraction of the v0.9.2 source ZIP into an empty directory, fresh Python 3.13 virtual environment, `pip install -r requirements.txt`, `python3 build.py`. The result was compared with the delivered PDF by extracted text per page, page size, every word's position, and rendered page images at 100 dpi. Results are in QA-REPORT-v0.9.2.md.
- Byte-for-byte identity is not expected: WeasyPrint writes a creation timestamp and randomly named font subsets into each PDF.

## 6. Hardware checklist for v1.0
- [ ] Run every lesson end to end on a physical FM-1 at V1.04.
- [ ] VOICING note counts: INIT (expect 8 or 4?), WIDE SKY (expect 4), 5+3 (expect 2). Does a four-note chord on WIDE SKY sound complete?
- [ ] EDIT from another section: OSC A or last part?
- [ ] LFO with BIPOLAR OFF: does WT POS move only upward from the set frame?
- [ ] Arp: saved on and recalled; PLAY does not stop it; preset change does.
- [ ] Lanes: record a CUTOFF move, load a factory preset without lanes, and confirm the movement continues until PLAY is pressed; CLEAR LANE removes it.
- [ ] Arp page wording when switched on (HOLD NOTES TO ARPEGGIATE).
- [ ] SAVE page: leftover characters such as "[E]"; position of the space in LETTER.
- [ ] Lesson 4: ENV 2 at about 40% audibly blooms; SUB filter switch reads OFF.
- [ ] Lesson 5: 0.07 and 0.10 Hz both reachable on real encoders.
- [ ] Lesson 7: ping-pong delay timing at 90 BPM; CLEAR LANE removes only the chosen lane.
- [ ] MPC: breakout cable fit, Source Rear stereo image, usable FM-1 MASTER and REC GAIN range.
