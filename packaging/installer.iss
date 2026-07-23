; Inno Setup script for the PDFtoImage installer.
; Build (on Windows, after PyInstaller has produced dist\PDFtoImage.exe):
;   iscc packaging\installer.iss
; Produces dist\installer\PDFtoImageSetup.exe

#define MyAppName "PDF to Image"
#define MyAppVersion "0.1.0"
#define MyAppExeName "PDFtoImage.exe"

[Setup]
AppId={{B8B8C6C0-6C7A-4B9E-9B9B-PDFTOIMAGE01}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\PDFtoImage
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=dist\installer
OutputBaseFilename=PDFtoImageSetup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Files]
Source: "..\dist\PDFtoImage.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "바탕화면에 아이콘 만들기"; GroupDescription: "추가 아이콘:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName} 실행"; Flags: nowait postinstall skipifsilent
