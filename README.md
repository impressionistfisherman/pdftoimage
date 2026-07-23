# PDF to Image

Windows 데스크톱 GUI 앱입니다. PDF 파일의 각 페이지를 PNG/JPEG 이미지로 변환합니다.

## 사용 (일반 사용자)

[Releases](../../releases) 또는 CI 빌드 아티팩트에서 둘 중 하나를 받으세요:

- **PDFtoImage.exe** — 포터블 버전. 설치 없이 더블클릭으로 바로 실행됩니다.
- **PDFtoImageSetup.exe** — 설치형 버전. 실행하면 설치 마법사가 뜨고, 시작 메뉴/바탕화면 아이콘이 생성됩니다.

실행 화면에서:
1. **찾아보기...**로 변환할 PDF 파일 선택
2. 출력 폴더, 이미지 포맷(PNG/JPEG), DPI, 변환할 페이지 범위(예: `1-3,5`, 비우면 전체) 지정
3. **변환 시작** 클릭

결과 이미지는 `<파일명>_pNN.png` 형식으로 출력 폴더에 저장됩니다.

## 개발 환경에서 실행

```bash
pip install -e ".[dev]"
python -m pdftoimage.gui        # 또는: pdftoimage-gui
```

핵심 변환 로직은 `src/pdftoimage/core.py`에 있고, GUI(`gui.py`, PySide6)와
CLI(`cli.py`, Typer) 양쪽에서 재사용합니다. CLI가 필요하면 `pdftoimage convert ...`,
`pdftoimage info ...` 로 사용할 수 있습니다.

## Windows 실행 파일 빌드

Windows 머신에서:

```powershell
pip install -e ".[dev]"

# 포터블 exe (dist\PDFtoImage.exe)
pyinstaller packaging\pdftoimage.spec

# 설치형 exe (Inno Setup 필요: https://jrsoftware.org/isinfo.php)
# dist\PDFtoImage.exe 가 먼저 빌드되어 있어야 함
iscc packaging\installer.iss   # -> dist\installer\PDFtoImageSetup.exe
```

`.github/workflows/build-windows.yml`가 `main` 브랜치 푸시/태그마다 두 아티팩트를
자동으로 빌드합니다 (Actions 탭 → 워크플로 실행 → Artifacts).

## 테스트

```bash
pip install -e ".[dev]"
pytest
```

GUI 테스트는 `pytest-qt`로 화면 없이(offscreen) 실행됩니다. Linux에서 실행 시
`libegl1 libgl1 libxkbcommon0` 시스템 패키지가 필요할 수 있습니다.
