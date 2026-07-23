# pdftoimage

Convert PDF pages into PNG or JPEG image files from the command line.

## Install

```bash
pip install -e .
```

(Requires Python 3.9+. Uses [PyMuPDF](https://pymupdf.readthedocs.io/), so no
external Poppler/ImageMagick install is needed.)

## Quick start

```bash
# Convert every page of report.pdf to PNG files in the current directory
pdftoimage convert report.pdf

# JPEG output at 300 DPI into a specific folder
pdftoimage convert report.pdf --format jpeg --dpi 300 --output-dir ./out

# Only pages 1-3 and 5
pdftoimage convert report.pdf --pages 1-3,5

# Inspect page count / size before converting
pdftoimage info report.pdf
```

Output files are named `<prefix>_pNN.<ext>`, e.g. `report_p01.png`. The
prefix defaults to the input file's name and can be overridden with
`--prefix`.

## Commands

### `pdftoimage convert PDF_FILE [OPTIONS]`

| Option | Default | Description |
|---|---|---|
| `-o, --output-dir PATH` | `.` | Directory to write images into (created if missing) |
| `-f, --format [png\|jpeg]` | `png` | Output image format |
| `-d, --dpi INTEGER` | `200` | Rendering resolution |
| `-p, --pages TEXT` | all pages | 1-indexed page selection, e.g. `1-3,5,8-9` |
| `--prefix TEXT` | input file stem | Output filename prefix |

### `pdftoimage info PDF_FILE`

Prints the page count and first page dimensions.

## Development

```bash
pip install -e ".[dev]"
pytest
```
