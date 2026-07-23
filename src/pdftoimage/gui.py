"""PDF to Image — desktop GUI (PySide6) built on top of pdftoimage.core."""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QGridLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from pdftoimage.core import PageRangeError, convert_pdf


class ConversionWorker(QThread):
    progress = Signal(str)
    finished_ok = Signal(list)
    failed = Signal(str)

    def __init__(
        self,
        input_path: Path,
        output_dir: Path,
        fmt: str,
        dpi: int,
        page_spec: str | None,
        prefix: str | None,
    ) -> None:
        super().__init__()
        self.input_path = input_path
        self.output_dir = output_dir
        self.fmt = fmt
        self.dpi = dpi
        self.page_spec = page_spec
        self.prefix = prefix

    def run(self) -> None:
        try:
            self.progress.emit(f"{self.input_path.name} 변환 중...")
            written = convert_pdf(
                input_path=self.input_path,
                output_dir=self.output_dir,
                fmt=self.fmt,
                dpi=self.dpi,
                page_spec=self.page_spec,
                prefix=self.prefix,
            )
            self.finished_ok.emit(written)
        except (PageRangeError, ValueError, FileNotFoundError) as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PDF to Image")
        self.resize(560, 420)
        self.worker: ConversionWorker | None = None

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        layout.addWidget(self._build_file_group())
        layout.addWidget(self._build_options_group())

        self.convert_button = QPushButton("변환 시작")
        self.convert_button.clicked.connect(self.on_convert_clicked)
        layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

    def _build_file_group(self) -> QGroupBox:
        group = QGroupBox("파일")
        grid = QGridLayout(group)

        self.input_edit = QLineEdit()
        input_browse = QPushButton("찾아보기...")
        input_browse.clicked.connect(self.browse_input)
        grid.addWidget(QLabel("PDF 파일"), 0, 0)
        grid.addWidget(self.input_edit, 0, 1)
        grid.addWidget(input_browse, 0, 2)

        self.output_edit = QLineEdit(str(Path.cwd()))
        output_browse = QPushButton("찾아보기...")
        output_browse.clicked.connect(self.browse_output)
        grid.addWidget(QLabel("출력 폴더"), 1, 0)
        grid.addWidget(self.output_edit, 1, 1)
        grid.addWidget(output_browse, 1, 2)

        return group

    def _build_options_group(self) -> QGroupBox:
        group = QGroupBox("옵션")
        grid = QGridLayout(group)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["png", "jpeg"])
        grid.addWidget(QLabel("포맷"), 0, 0)
        grid.addWidget(self.format_combo, 0, 1)

        self.dpi_spin = QSpinBox()
        self.dpi_spin.setRange(36, 1200)
        self.dpi_spin.setValue(200)
        grid.addWidget(QLabel("DPI"), 0, 2)
        grid.addWidget(self.dpi_spin, 0, 3)

        self.pages_edit = QLineEdit()
        self.pages_edit.setPlaceholderText("예: 1-3,5  (비우면 전체 페이지)")
        grid.addWidget(QLabel("페이지"), 1, 0)
        grid.addWidget(self.pages_edit, 1, 1, 1, 3)

        self.prefix_edit = QLineEdit()
        self.prefix_edit.setPlaceholderText("비우면 파일명 사용")
        grid.addWidget(QLabel("파일명 접두사"), 2, 0)
        grid.addWidget(self.prefix_edit, 2, 1, 1, 3)

        return group

    def browse_input(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "PDF 파일 선택", "", "PDF Files (*.pdf)")
        if path:
            self.input_edit.setText(path)

    def browse_output(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "출력 폴더 선택", self.output_edit.text())
        if path:
            self.output_edit.setText(path)

    def on_convert_clicked(self) -> None:
        input_text = self.input_edit.text().strip()
        if not input_text:
            QMessageBox.warning(self, "입력 필요", "변환할 PDF 파일을 선택해주세요.")
            return

        input_path = Path(input_text)
        output_dir = Path(self.output_edit.text().strip() or ".")
        page_spec = self.pages_edit.text().strip() or None
        prefix = self.prefix_edit.text().strip() or None

        self.convert_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.log.clear()

        self.worker = ConversionWorker(
            input_path=input_path,
            output_dir=output_dir,
            fmt=self.format_combo.currentText(),
            dpi=self.dpi_spin.value(),
            page_spec=page_spec,
            prefix=prefix,
        )
        self.worker.progress.connect(self.log.appendPlainText)
        self.worker.finished_ok.connect(self.on_finished)
        self.worker.failed.connect(self.on_failed)
        self.worker.start()

    def on_finished(self, written: list[Path]) -> None:
        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        for path in written:
            self.log.appendPlainText(str(path))
        self.log.appendPlainText(f"완료: 이미지 {len(written)}개 생성")

    def on_failed(self, message: str) -> None:
        self.progress_bar.setVisible(False)
        self.convert_button.setEnabled(True)
        self.log.appendPlainText(f"오류: {message}")
        QMessageBox.critical(self, "변환 실패", message)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
