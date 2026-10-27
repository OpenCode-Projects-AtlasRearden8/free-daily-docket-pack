# Free Daily Docket Pack

Free, printable, ADHD-friendly daily dockets: one-page paper planners that keep a
day small enough to actually happen. Three tasks max, a brain-dump corner,
energy-level tags, meeting-and-med lines, water-and-step counters, and a
"done is done" footer — plus a weekly reset sheet and a blank theme for flu
weeks.

Printable pages are unbranded: no logos, no upsells, nothing to sign up for.
The HTML/CSS sources build to PDFs with one script, and the test suite verifies
every sheet builds a valid single-page PDF.

Made with plain English and low-pressure design by **Asdale Dynamics, LLC**
(Dylan Asdale's LLC behind *The Massive AI Manual* and
[dylanasdale.github.io](https://dylanasdale.github.io)). It pairs with the
*gentle-productivity-manual*: the manual explains the thinking; this pack is
the paper you can hold.

## What's inside

| PDF (in `printables/`) | Use it when |
| --- | --- |
| `day-docket.pdf` | The everyday docket: energy tags, the Daily Three, meetings + meds, water cups, step boxes, and a big brain-dump corner. |
| `day-docket-lowspoons.pdf` | A lighter load for low-energy days: two tasks, meds and water only, and a big "everything else can wait" box. |
| `weekly-reset.pdf` | A once-a-week loop-closer: what worked / what dragged, three wins, next week's top three, and a kind-housekeeping checklist. |
| `blank-theme.pdf` | A docket-shaped blank page for flu weeks and do-little days — water sips, med boxes, and free scratch space only. |

Every sheet prints one page, US Letter portrait, at 100% scale.

## Print it (zero setup)

1. Grab any PDF from [`printables/`](printables/).
2. Print on US Letter, portrait, at **100% / Actual size** — not "fit to page"
   — and turn off "scale to fit" and any print dialogs' headers/footers.
3. No A4 or grayscale concerns: layouts work in black-and-white too.

## Rebuild it

Python 3.9+ with three packages is all it needs; everything runs locally:

```bash
python3 -m pip install -r requirements.txt
python3 build.py              # renders printables/*.pdf
python3 -m pytest             # verifies every sheet builds a valid PDF
```

`build.py` renders each HTML sheet in `sheets/` with WeasyPrint and then
validates the result (one page, Letter size, expected text, still unbranded).
It exits non-zero if anything is off, so a bad edit can't ship quietly.
Useful flags: `--out DIR` (render somewhere else) and `--clean` (wipe the
output directory first).

## Repo layout

```
build.py            # single build script: render + validate every sheet
sheets/             # HTML/CSS sources (one HTML file per printable page)
  docket-base.css   # shared design system: grid, lines, counters, footer
printables/         # the built PDFs, ready to print
tests/              # pytest suite validating every built PDF
```

## Design notes (why it looks like that)

- **Three tasks, tops.** A docket is a day you can finish. Anything beyond
  three is a bonus round, so the page says so.
- **Energy tags first.** Pick Bright / Steady / Low / Running on fumes before
  planning; the right plan depends on today's battery, not an ideal version
  of it.
- **Meetings and meds are boring-but-important lines.** They share the page
  so they don't get forgotten between appointments.
- **Water and steps are counters, not goals.** Shade a cup or a box when it
  happens; the page doesn't judge partial days.
- **Brain-dump corner.** Everything rattling around gets one home, so it
  stops interrupting the other stuff.
- **Done is done.** The footer repeats the rule: finished counts, even when
  it was small, late, or lonely.

This pack is everyday life-organization, not medical advice. Nothing here
tracks, syncs, or collects anything — no signups, no accounts, no telemetry,
no personal data in the files.

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Asdale Dynamics, LLC.
