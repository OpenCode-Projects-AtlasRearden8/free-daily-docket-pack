"""Tests for the free daily docket pack.

Every sheet must build a valid, single-page, unbranded US Letter PDF.
Runs the real build script into a temp directory and inspects the PDFs.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build.py"
SHEETS_DIR = ROOT / "sheets"

PDF_NAMES = (
    "day-docket.pdf",
    "day-docket-lowspoons.pdf",
    "weekly-reset.pdf",
    "blank-theme.pdf",
)

LETTER_W_PT, LETTER_H_PT = 612.0, 792.0

# text that must appear (case-insensitive) in each PDF's extracted text
EXPECTED_TEXT = {
    "day-docket.pdf": [
        "docket",
        "date",
        "energy",
        "bright",
        "three tasks, tops",
        "meetings",
        "meds",
        "water",
        "steps",
        "brain-dump corner",
        "done is done",
    ],
    "day-docket-lowspoons.pdf": [
        "low-spoons docket",
        "enough-for-today",
        "meds",
        "water",
        "one nice thing",
        "everything else can wait",
        "done is done",
        "rest counts",
    ],
    "weekly-reset.pdf": [
        "weekly reset",
        "week of",
        "what worked",
        "what dragged",
        "three wins",
        "next week, three tops",
        "reset checklist",
        "laundry",
        "meds refill check",
        "meds refills",
        "done is done",
    ],
    "blank-theme.pdf": [
        "blank docket",
        "blank on purpose",
        "water",
        "meds",
        "done is done",
    ],
}

BRAND_TOKENS = ("asdale", "dylan")


def run_build(out_dir: Path, extra_args: tuple[str, ...] = ()) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(BUILD), "--out", str(out_dir), *extra_args],
        capture_output=True,
        text=True,
        timeout=300,
    )


@pytest.fixture(scope="module")
def built(tmp_path_factory: pytest.TempPathFactory) -> Path:
    out = tmp_path_factory.mktemp("printables")
    result = run_build(out)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


def pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    return "\n".join(page.extract_text() or "" for page in reader.pages).lower()


class TestBuildScript:
    def test_build_reports_success(self, built: Path, tmp_path: Path):
        result = run_build(tmp_path)
        assert result.returncode == 0
        assert "All sheets built" in result.stdout
        for name in PDF_NAMES:
            assert name in result.stdout

    def test_clean_flag_rebuilds_fresh(self, tmp_path: Path):
        first = run_build(tmp_path)
        assert first.returncode == 0
        again = run_build(tmp_path, extra_args=("--clean",))
        assert again.returncode == 0
        assert "removed" in again.stdout
        assert tmp_path.joinpath("day-docket.pdf").is_file()


class TestPdfValidity:
    def test_all_four_pdfs_exist(self, built: Path):
        for name in PDF_NAMES:
            pdf = built / name
            assert pdf.is_file(), f"missing {name}"
            assert pdf.stat().st_size > 5_000, f"{name} suspiciously small"
            assert pdf.read_bytes()[:5] == b"%PDF-", f"{name} is not a PDF"

    @pytest.mark.parametrize("name", PDF_NAMES)
    def test_single_letter_page(self, built: Path, name: str):
        reader = PdfReader(str(built / name))
        assert len(reader.pages) == 1, f"{name} must be a one-page sheet"
        box = reader.pages[0].mediabox
        assert abs(float(box.width) - LETTER_W_PT) <= 3, f"{name} page width {box.width}pt"
        assert abs(float(box.height) - LETTER_H_PT) <= 3, f"{name} page height {box.height}pt"

    @pytest.mark.parametrize("name", tuple(EXPECTED_TEXT))
    def test_expected_content(self, built: Path, name: str):
        text = pdf_text(built / name)
        for phrase in EXPECTED_TEXT[name]:
            assert phrase in text, f"{name} is missing {phrase!r}"


class TestUnbrandedPdfs:
    @pytest.mark.parametrize("name", PDF_NAMES)
    def test_no_brand_tokens_in_page_text(self, built: Path, name: str):
        text = pdf_text(built / name)
        for token in BRAND_TOKENS:
            assert token not in text, f"{name} contains brand token {token!r}"

    @pytest.mark.parametrize("name", PDF_NAMES)
    def test_no_brand_tokens_in_metadata(self, built: Path, name: str):
        reader = PdfReader(str(built / name))
        metadata = reader.metadata or {}
        for value in metadata.values():
            assert isinstance(value, str)
            lowered = value.lower()
            for token in BRAND_TOKENS:
                assert token not in lowered, f"{name} metadata contains {token!r}"


class TestSources:
    def test_sources_exist(self):
        for name in PDF_NAMES:
            html = SHEETS_DIR / (name.replace(".pdf", "") + ".html")
            assert html.is_file(), f"missing source {html.name}"
            assert (SHEETS_DIR / "docket-base.css").is_file()

    def test_sources_stay_unbranded(self):
        for src in SHEETS_DIR.iterdir():
            if src.suffix in (".html", ".css"):
                lowered = src.read_text(encoding="utf-8").lower()
                for token in BRAND_TOKENS:
                    assert token not in lowered, f"{src.name} contains {token!r}"
