"""pdftoimage: convert PDF pages to image files from the command line."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import fitz  # PyMuPDF
import typer

from pdftoimage.core import PageRangeError, convert_pdf

app = typer.Typer(
    name="pdftoimage",
    help="Convert PDF pages into PNG/JPEG image files.",
    no_args_is_help=True,
)


@app.command()
def convert(
    input: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Path to the source PDF file."
    ),
    output_dir: Path = typer.Option(
        Path("."), "--output-dir", "-o", help="Directory to write image files into."
    ),
    format: str = typer.Option(
        "png", "--format", "-f", help="Output image format: 'png' or 'jpeg'."
    ),
    dpi: int = typer.Option(
        200, "--dpi", "-d", help="Rendering resolution in dots per inch."
    ),
    pages: Optional[str] = typer.Option(
        None,
        "--pages",
        "-p",
        help="1-indexed page selection, e.g. '1-3,5,8-9'. Default: all pages.",
    ),
    prefix: Optional[str] = typer.Option(
        None,
        "--prefix",
        help="Filename prefix for output images. Default: input file's stem.",
    ),
) -> None:
    """Convert PDF_FILE pages into individual image files."""
    try:
        written = convert_pdf(
            input_path=input,
            output_dir=output_dir,
            fmt=format,
            dpi=dpi,
            page_spec=pages,
            prefix=prefix,
        )
    except (PageRangeError, ValueError) as exc:
        typer.secho(f"Error: {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    for path in written:
        typer.echo(str(path))
    typer.secho(
        f"Wrote {len(written)} image(s) to {output_dir}", fg=typer.colors.GREEN
    )


@app.command()
def info(
    input: Path = typer.Argument(
        ..., exists=True, dir_okay=False, help="Path to the source PDF file."
    )
) -> None:
    """Show basic information about PDF_FILE (page count, page size)."""
    with fitz.open(input) as doc:
        typer.echo(f"File: {input}")
        typer.echo(f"Pages: {doc.page_count}")
        if doc.page_count > 0:
            rect = doc.load_page(0).rect
            typer.echo(f"First page size: {rect.width:.1f} x {rect.height:.1f} pt")


if __name__ == "__main__":
    app()
