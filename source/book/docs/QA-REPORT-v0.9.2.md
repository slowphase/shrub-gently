# Shrub, Gently v0.9.2 Preview: QA report

Date: 15 November 2026 · Firmware target: SHRUB V1.04 · File: `Shrub-Gently-v0.9.2-preview.pdf` · Source: `shrub-gently-source-v0.9.2.zip`

## Summary
| Check | Result |
|---|---|
| Page count | **68** (unchanged from v0.9.1). Page size 160 × 244 mm on every page. |
| Renderer | **WeasyPrint 70.0** (recorded in the PDF metadata as `Producer: WeasyPrint 70.0`) |
| Dependencies (pinned in `source/book/requirements.txt`) | pydyf 0.13.0, tinycss2 1.5.1, tinyhtml5 2.1.0, cssselect2 0.10.1, fontTools 4.67.0, Pillow 12.3.0, Pyphen 0.18.1, cffi 2.1.1, pycparser 3.0, Brotli 1.2.1, zopfli 0.4.3, webencodings 0.6.1. Python 3.13.18, Linux. |
| Clean rebuild | **Passed.** See below. |
| Pages visually inspected | **All 68**, at reading resolution (62 dpi, 8-up). The nine pages changed by this revision (4, 5, 7, 14, 49, 50, 55, 56, 61) were also read at 95 dpi, close to A4 print size. |
| Bookmarks | 62 entries; 17 top-level (Contents, three front chapters, eight lessons, five back chapters), each landing on its correct page. |
| Internal links | 102 link annotations, 0 broken. |
| Metadata | Title "Shrub, Gently"; Author "slowphase"; Subject names SHRUB V1.04; Keywords set. |
| Selectable text | Yes, on every page (89,410 characters; no image-only pages). |
| Fonts | 13 embedded subsets, all from the bundled OFL families (Archivo, Source Serif 4, IBM Plex Mono, Michroma, Fraunces, Jost). No fallback fonts. |
| Em dashes | 0 (the build refuses to run if one is present). |

## 1. The reproducibility fault, reproduced and fixed
- **Reproduced:** the v0.9.1 source built under WeasyPrint 68.0 gave 68 pages, but text extraction differed on 10 pages (13, 15, 20, 21, 22, 26, 27, 33, 37, 47) and the floated screen illustrations on those pages were missing entirely.
- **Cause:** those illustrations were wrapped in an SVG `<clipPath>` to round their corners. WeasyPrint 68 dropped the clipped group.
- **Fix:** no clip path; the rounded corners are drawn directly into the screen background and the knob-deck shapes. Comparing v0.9.2 against v0.9.1 at 200 dpi, the corners are visually identical (differences of a few hundred anti-aliased pixels per page, all at the rounded corners).
- **Guard:** `build.py` exits with code 1 and this message on any WeasyPrint other than 70.x:
  `ERROR: This book needs WeasyPrint 70.x, but WeasyPrint 68.0 is installed. Other versions can silently drop drawings or text. Run: pip install -r requirements.txt`
  Tested with WeasyPrint 68.0: refused as expected.
- **Robustness check (not a supported route):** forcing the v0.9.2 source through WeasyPrint 68.0 with `SHRUB_ALLOW_ANY_WEASYPRINT=1` now gives identical text on all 68 pages and no visible image differences at 50 dpi. The root cause is gone; the pin remains so the layout can't drift with future renderer changes.

## 2. Clean-build test
1. Extracted `shrub-gently-source-v0.9.2.zip` into an empty directory.
2. Created a new virtual environment (`python3 -m venv --clear`) and ran `pip install --no-cache-dir -r source/book/requirements.txt`. `pip freeze` listed exactly the 13 pinned packages.
3. Ran `python3 build.py` from `source/book`: `pages: 68 | WeasyPrint 70.0`.
4. Compared the result with the delivered PDF:

| Comparison | Result |
|---|---|
| Page count and page sizes | 68 = 68; all sizes identical |
| Extracted text, page by page | Identical on all 68 pages |
| Word geometry | 16,021 words compared; same words in the same order on every page; maximum position difference **0.0000 pt** |
| Vector objects (lines, rects, curves) per page | Identical counts on all pages |
| Rendered images at 100 dpi | **Pixel-identical on all 68 pages** |
| Bytes | Differ, as expected: WeasyPrint writes a timestamp and randomly named font subsets into each file |

## 3. Pages changed in v0.9.2 (pixel diff against v0.9.1)
| Page | Change |
|---|---|
| 4 | Equipment list: breakout cable wording |
| 5 | Reflow only (text moved from p. 4) |
| 7 | Twelve main buttons plus two octave buttons, fourteen in total |
| 14 | Lesson 1 note: arpeggiator versus recorded lanes |
| 49 | Lesson 7 step 17: arp stops by switching off or loading a preset (ARP+SCALE PRESET) |
| 50 | Lesson 7 Have a Play: lanes keep playing after loading a preset without lanes; PLAY stops them |
| 55 | Lesson 8: optional unstarring of earlier factory favourites |
| 56 | MPC cable wording in step 1 and the figure label |
| 61 | Troubleshooting: separate fixes for a latched arp and for recorded lanes |
| 13, 15, 20, 21, 22, 26, 27, 33, 37, 47 | Corner anti-aliasing only (clip path removed) |
| 67, 68 | Version string v0.9.2 |

All other pages are unchanged.

## 4. Layout checks on changed pages
Text wrapping, callouts, step numbering, tables, the MPC figure, headers, footers and page numbers all checked at 95 dpi. No orphaned headings, clipped text, collisions or unexpected blank space. Section breaks unchanged.

## 5. Remaining known issues
- Physical FM-1 testing is still outstanding (see RESEARCH-AND-VERIFICATION.md, section 6). The new checklist item covers lanes continuing after a preset change.
- Have a Play boxes that continue across a page repeat their dark background on the new page, by design.
- Build tested on Linux only. macOS and Windows need WeasyPrint's system libraries (Pango); the pinned Python packages are the same.
