import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from pdftoimage.gui import MainWindow  # noqa: E402


def test_main_window_creates(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    assert window.windowTitle() == "PDF to Image"
    assert window.convert_button.text() == "변환 시작"


def test_convert_without_input_shows_warning(qtbot, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)

    warned = {}
    monkeypatch.setattr(
        "pdftoimage.gui.QMessageBox.warning",
        lambda *args, **kwargs: warned.setdefault("called", True),
    )
    window.on_convert_clicked()
    assert warned.get("called") is True


def test_full_conversion_via_worker(qtbot, sample_pdf: Path, tmp_path: Path):
    window = MainWindow()
    qtbot.addWidget(window)

    out_dir = tmp_path / "out"
    window.input_edit.setText(str(sample_pdf))
    window.output_edit.setText(str(out_dir))
    window.dpi_spin.setValue(100)

    window.on_convert_clicked()
    assert window.worker is not None
    qtbot.waitUntil(lambda: len(list(out_dir.glob("*.png"))) == 3, timeout=5000)
    qtbot.waitUntil(lambda: window.convert_button.isEnabled(), timeout=5000)
