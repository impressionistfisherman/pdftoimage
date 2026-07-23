"""Core PDF-to-image conversion logic (no CLI dependencies)."""

from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF


class PageRangeError(ValueError):
    """Raised when a page range spec is malformed or out of bounds."""


def parse_page_spec(spec: str | None, page_count: int) -> list[int]:
    """Parse a 1-indexed page spec like "1-3,5,8-9" into a sorted list of
    unique 0-indexed page numbers. `spec=None` returns every page."""
    if spec is None or spec.strip() == "":
        return list(range(page_count))

    pages: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_str, _, end_str = part.partition("-")
            try:
                start, end = int(start_str), int(end_str)
            except ValueError as exc:
                raise PageRangeError(f"Invalid page range: '{part}'") from exc
            if start < 1 or end < start:
                raise PageRangeError(f"Invalid page range: '{part}'")
            for page in range(start, end + 1):
                pages.add(page)
        else:
            try:
                page = int(part)
            except ValueError as exc:
                raise PageRangeError(f"Invalid page number: '{part}'") from exc
            if page < 1:
                raise PageRangeError(f"Invalid page number: '{part}'")
            pages.add(page)

    out_of_bounds = [p for p in pages if p > page_count]
    if out_of_bounds:
        raise PageRangeError(
            f"Page(s) {sorted(out_of_bounds)} exceed document length ({page_count} pages)"
        )

    return sorted(p - 1 for p in pages)


def convert_pdf(
    input_path: Path,
    output_dir: Path,
    fmt: str = "png",
    dpi: int = 200,
    page_spec: str | None = None,
    prefix: str | None = None,
) -> list[Path]:
    """Render selected pages of `input_path` to image files in `output_dir`.

    Returns the list of written file paths, in page order.
    """
    fmt = fmt.lower()
    if fmt not in ("png", "jpeg", "jpg"):
        raise ValueError(f"Unsupported format: '{fmt}' (use 'png' or 'jpeg')")
    ext = "jpg" if fmt == "jpeg" else fmt

    if dpi <= 0:
        raise ValueError(f"DPI must be positive, got {dpi}")

    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    stem = prefix if prefix else input_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    written: list[Path] = []

    with fitz.open(input_path) as doc:
        page_indices = parse_page_spec(page_spec, doc.page_count)
        pad = max(len(str(doc.page_count)), 2)
        for index in page_indices:
            page = doc.load_page(index)
            pix = page.get_pixmap(matrix=matrix)
            out_path = output_dir / f"{stem}_p{index + 1:0{pad}d}.{ext}"
            pix.save(out_path)
            written.append(out_path)

    return written
