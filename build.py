#!/usr/bin/env python3
"""Build the free printable daily docket pack.

Renders the HTML/CSS sheet sources in sheets/ into one-page US Letter PDFs
in printables/ using WeasyPrint, then validates each PDF (page count, page
size, expected text). Exits non-zero if any sheet fails validation.

No setup beyond Python 3 + the packages in requirements.txt; no network, no
signups, nothing tracked.
"""

import argparse
import sys
from pathlib import Path

from weasyprint import HTML
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
SHEETS_DIR = HERE / "sheets"
DEFAULT_OUT = HERE / "printables"

# output name -> (source html, expected page count, phrase that must appear
# in the PDF text, and a flag that the sheet must stay informative-but-plain)
SHEETS = {
    "day-docket.pdf": ("day-docket.html", 1, "Three tasks, tops"),
    "day-docket-lowspoons.pdf": ("day-docket-lowspoons.html", 1, "enough-for-today"),
    "weekly-reset.pdf": ("weekly-reset.html", 1, "Weekly reset"),
    "blank-theme.pdf": ("blank-theme.html", 1, "blank on purpose"),
}

FOOTER_PHRASE = "Done is done"

# US Letter in PostScript points (1 pt = 1/72 in)
LETTER_W_PT, LETTER_H_PT = 612.0, 792.0
SIZE_TOLERANCE_PT = 3.0

# Printable pages stay unbranded: no company, author, or store names.
UNBRANDED_TOKENS = ("asdale", "dylan")


def render_sheet(src: Path, dest: Path) -> list[str]:
    """Render one HTML sheet to PDF and validate it. Returns failure strings."""
    problems: list[str] = []

    if not src.is_file():
        return [f"{src.name}: source file is missing"]

    HTML(filename=str(src)).write_pdf(str(dest))
    if not dest.is_file() or dest.stat().st_size < 500:
        return [f"{dest.name}: PDF missing or suspiciously small"]

    reader = PdfReader(str(dest))
    pages = len(reader.pages)
    if pages != 1:
        problems.append(f"{dest.name}: expected a 1-page sheet, got {pages} pages")

    box = reader.pages[0].mediabox
    width, height = float(box.width), float(box.height)
    if abs(width - LETTER_W_PT) > SIZE_TOLERANCE_PT or abs(height - LETTER_H_PT) > SIZE_TOLERANCE_PT:
        problems.append(
            f"{dest.name}: page is {width:.0f}x{height:.0f}pt, expected ~612x792pt Letter"
        )

    text = "\n".join(page.extract_text() or "" for page in reader.pages).lower()
    for token in UNBRANDED_TOKENS:
        if token in text:
            problems.append(f"{dest.name}: PDFs should stay unbranded (found {token!r})")
    if FOOTER_PHRASE.lower() not in text:
        problems.append(f"{dest.name}: missing footer phrase {FOOTER_PHRASE!r}")

    return problems


def build(out_dir: Path, clean: bool = False) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    if clean:
        for old in sorted(out_dir.glob("*.pdf")):
            old.unlink()
            print(f"  removed {old.name}")

    failures: list[str] = []
    print(f"Building {len(SHEETS)} sheets into {out_dir}/ ...\n")
    for pdf_name, (html_name, _pages, phrase) in SHEETS.items():
        src = SHEETS_DIR / html_name
        dest = out_dir / pdf_name
        sheet_failures = render_sheet(src, dest)
        if sheet_failures:
            failures.extend(sheet_failures)
            print(f"  FAIL  {pdf_name}")
            for problem in sheet_failures:
                print(f"        {problem}")
        else:
            size_kb = dest.stat().st_size / 1024
            print(f"  ok    {pdf_name:<28} {size_kb:6.1f} KB  (contains {phrase!r})")

    print()
    if failures:
        print(f"{len(failures)} problem(s) found.")
        return 1
    print("All sheets built valid one-page Letter PDFs.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Render the docket pack HTML/CSS sheets to PDFs in printables/."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help="output directory for PDFs (default: printables/)",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="delete existing PDFs in the output directory first",
    )
    args = parser.parse_args(argv)
    resolved_out = args.out if args.out.is_absolute() else HERE / args.out
    return build(resolved_out, clean=args.clean)


if __name__ == "__main__":
    sys.exit(main())
