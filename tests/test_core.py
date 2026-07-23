from pathlib import Path

import pytest

from pdftoimage.core import PageRangeError, convert_pdf, parse_page_spec


def test_parse_page_spec_all_pages():
    assert parse_page_spec(None, 5) == [0, 1, 2, 3, 4]


def test_parse_page_spec_ranges_and_singles():
    assert parse_page_spec("1-3,5", 5) == [0, 1, 2, 4]


def test_parse_page_spec_deduplicates_and_sorts():
    assert parse_page_spec("3,1-2,2", 5) == [0, 1, 2]


def test_parse_page_spec_out_of_bounds():
    with pytest.raises(PageRangeError):
        parse_page_spec("1-10", 3)


def test_parse_page_spec_invalid_token():
    with pytest.raises(PageRangeError):
        parse_page_spec("abc", 3)


def test_parse_page_spec_zero_or_negative():
    with pytest.raises(PageRangeError):
        parse_page_spec("0", 3)


def test_convert_pdf_all_pages_png(sample_pdf: Path, tmp_path: Path):
    out_dir = tmp_path / "out"
    written = convert_pdf(sample_pdf, out_dir, fmt="png", dpi=100)
    assert len(written) == 3
    for path in written:
        assert path.exists()
        assert path.suffix == ".png"


def test_convert_pdf_jpeg_format(sample_pdf: Path, tmp_path: Path):
    written = convert_pdf(sample_pdf, tmp_path / "out", fmt="jpeg", dpi=100)
    assert all(p.suffix == ".jpg" for p in written)


def test_convert_pdf_page_subset(sample_pdf: Path, tmp_path: Path):
    written = convert_pdf(sample_pdf, tmp_path / "out", page_spec="1,3", dpi=100)
    assert len(written) == 2
    assert "p01" in written[0].stem
    assert "p03" in written[1].stem


def test_convert_pdf_custom_prefix(sample_pdf: Path, tmp_path: Path):
    written = convert_pdf(
        sample_pdf, tmp_path / "out", page_spec="1", dpi=100, prefix="custom"
    )
    assert written[0].name.startswith("custom_p")


def test_convert_pdf_invalid_format(sample_pdf: Path, tmp_path: Path):
    with pytest.raises(ValueError):
        convert_pdf(sample_pdf, tmp_path / "out", fmt="bmp")


def test_convert_pdf_invalid_dpi(sample_pdf: Path, tmp_path: Path):
    with pytest.raises(ValueError):
        convert_pdf(sample_pdf, tmp_path / "out", dpi=0)


def test_convert_pdf_missing_input(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        convert_pdf(tmp_path / "missing.pdf", tmp_path / "out")


def test_convert_pdf_higher_dpi_produces_larger_file(
    sample_pdf: Path, tmp_path: Path
):
    low = convert_pdf(sample_pdf, tmp_path / "low", page_spec="1", dpi=72)
    high = convert_pdf(sample_pdf, tmp_path / "high", page_spec="1", dpi=300)
    assert high[0].stat().st_size >= low[0].stat().st_size
