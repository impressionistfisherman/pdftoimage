# PyInstaller spec for the PDFtoImage desktop GUI.
# Build (from repo root): pyinstaller packaging/pdftoimage.spec
# Produces a single portable executable in dist/PDFtoImage(.exe)

import sys
from pathlib import Path

block_cipher = None

repo_root = Path(SPECPATH).parent
entry_script = str(repo_root / "src" / "pdftoimage" / "gui.py")

a = Analysis(
    [entry_script],
    pathex=[str(repo_root / "src")],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    cipher=block_cipher,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PDFtoImage",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
