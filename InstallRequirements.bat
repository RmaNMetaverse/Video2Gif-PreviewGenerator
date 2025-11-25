@echo off
echo ===================================================
echo   Installing Python Libraries for Video Previewer
echo ===================================================
echo.
echo 1. Upgrading pip to avoid errors...
python -m pip install --upgrade pip
echo.
echo 2. Installing OpenCV (Video processing)...
pip install opencv-python
echo.
echo 3. Installing ImageIO (GIF creation)...
pip install imageio
echo.
echo 4. Installing PyInstaller (For building .exe)...
pip install pyinstaller
echo.
echo ===================================================
echo   All libraries installed successfully!
echo ===================================================
pause