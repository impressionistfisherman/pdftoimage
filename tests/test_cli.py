from pathlib import Path

from typer.testing import CliRunner

from pdftoimage.cli import app

runner = CliRunner()


def test_convert_writes_all_pages(sample_pdf: Path, tmp_path: Path):
    out_dir = tmp_path / "out"
    result = runner.invoke(
        app, ["convert", str(sample_pdf), "-o", str(out_dir), "--dpi", "100"]
    )
    assert result.exit_code == 0
    assert len(list(out_dir.glob("*.png"))) == 3


def test_convert_page_range(sample_pdf: Path, tmp_path: Path):
    out_dir = tmp_path / "out"
    result = runner.invoke(
        app,
        ["convert", str(sample_pdf), "-o", str(out_dir), "-p", "2", "--dpi", "100"],
    )
    assert result.exit_code == 0
    assert len(list(out_dir.glob("*.png"))) == 1


def test_convert_invalid_pages_reports_error(sample_pdf: Path, tmp_path: Path):
    result = runner.invoke(
        app, ["convert", str(sample_pdf), "-p", "99", "--dpi", "100"]
    )
    assert result.exit_code == 1
    assert "Error" in result.output


def test_convert_missing_file_reports_error(tmp_path: Path):
    result = runner.invoke(app, ["convert", str(tmp_path / "missing.pdf")])
    assert result.exit_code != 0


def test_info_command(sample_pdf: Path):
    result = runner.invoke(app, ["info", str(sample_pdf)])
    assert result.exit_code == 0
    assert "Pages: 3" in result.output
