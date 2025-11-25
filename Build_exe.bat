@echo off
echo ===================================================
echo   Video Preview Generator - EXE Builder
echo ===================================================
echo.
echo Step 1: Installing PyInstaller...
pip install pyinstaller
echo.

echo Step 2: Cleaning up previous builds...
rmdir /s /q build dist
del /q *.spec

echo.
echo Step 3: Building the Executable...
echo This may take a minute or two. Please wait.
echo.
:: --noconsole: Hides the black command window
:: --onefile: Bundles everything into a single .exe
:: --name: Sets the output filename
pyinstaller --noconsole --onefile --name "VideoPreviewGenerator" VideoGIFPreviewer-GUI.py

echo.
echo ===================================================
echo   BUILD COMPLETE!
echo ===================================================
echo.
echo You can find your standalone application here:
echo   .\dist\VideoPreviewGenerator.exe
echo.
pause