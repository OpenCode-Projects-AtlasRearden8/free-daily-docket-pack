# STATUS — Free Daily Docket Pack

Last updated: 2026-10-27

## What was built

A free, unbranded, ADHD-friendly printable planner pack: HTML/CSS sources that
build to one-page US Letter PDFs with a single build script, verified by a
pytest suite. No signups, no tracking, no personal data, no secrets.

Printable sheets (built into `printables/`):

- `day-docket.pdf` — everyday docket: energy-level tags (Bright / Steady /
  Low / Running on fumes), the three-tasks-max top, meeting and med lines,
  water cup counter (8) and step counter (12 boxes, ~1,000 steps each), a
  brain-dump corner with ruled lines, and the "Done is done. It counts."
  footer.
- `day-docket-lowspoons.pdf` — low-energy variant: two tasks max, water +
  meds lines (the keep-you-going basics), an optional "one nice thing", a
  compact brain-dump corner, a big "everything else can wait" panel, footer
  "Done is done. Rest counts too."
- `weekly-reset.pdf` — weekly loop-closer: what worked / what dragged, three
  wins, next week's three tops, a reset checklist (groceries, laundry, trash,
  meds refill check, sheets, one surface cleared), meds-refill date line, and
  next week's standing appointments.
- `blank-theme.pdf` — blank theme for flu weeks: date line, water sips, med
  dose boxes, and a full-height ruled scratch canvas; footer "Done is done.
  Being sick is a job; you did it."

Supporting files: `build.py` (render + validate), `sheets/docket-base.css`
(shared design system), `tests/test_build.py` (21 tests), `README.md`,
`LICENSE` (MIT, Copyright (c) 2026 Asdale Dynamics, LLC), `requirements.txt`.

## How to run it

```bash
python3 -m pip install -r requirements.txt   # weasyprint, pypdf, pytest
python3 build.py                             # build printables/*.pdf
python3 build.py --clean                     # wipe and rebuild
python3 build.py --out <dir>                 # build elsewhere (tests use this)
python3 -m pytest                            # run the test suite
```

Dependencies are system-level only (Python 3.13 + three packages); fonts are
the locally installed Nunito/Atkinson Hyperlegible stack. No network needed
at build or test time.

## Verification results

- `python3 build.py` — exit 0. All 4 sheets rendered as valid one-page
  Letter PDFs (92.7–176.6 KB), each containing its expected headline phrase.
- `python3 -m pytest` — **21 passed in ~30s**. Coverage: build script runs
  and reports success; `--clean` wipes and rebuilds; every PDF opens with
  pypdf, starts with `%PDF-`, has exactly 1 page sized ~612×792 pt; each
  sheet contains its expected section texts; PDF page text and metadata stay
  free of brand tokens (unbranded requirement); source HTML/CSS files exist
  and remain unbranded too.
- Visual QA: rasterized all four PDFs with `pdftoppm` and inspected each page.
  Fixed during review: fill-in slot lines collapsing to zero width (empty
  flex items in WeasyPrint) via `flex-grow: 1` on `.slot`, a wrapping energy
  pill via `white-space: nowrap`, and inline spans swapped for block divs.
  Final render checks: all sections present, lines aligned, no overflow onto
  a second page.

## Known gaps / ideas

- Letter size only. A4 printing works by picking "fit to page" (slight
  scaling), but a native A4 variant isn't built yet.
- Print-only: no fill-in-the-PDF form fields (AcroForm) — pages are meant for
  pen and paper.
- No dark mode or digital/Google-Docs twins; this pack is deliberately paper.
- The design system is one shared CSS file; a fifth sheet (e.g. "bonus
  round" tracker) would drop in, but none is included.
- Layouts are tuned for the container's fonts; on systems missing Nunito,
  fallback fonts (Atkinson Hyperlegible / Liberation Sans) shift spacing
  slightly (tests still pass there, but the container's look is the tested
  look).
