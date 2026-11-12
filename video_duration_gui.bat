@echo off
setlocal
chcp 65001 >nul
title Video and Audio Duration Calculator
cd /d "%~dp0"

rem The GUI needs Python 3 + PySide6. pythonw keeps the console hidden.
where pythonw >nul 2>nul
if errorlevel 1 goto :nopython

pythonw -c "import PySide6" >nul 2>nul
if not errorlevel 1 goto :launch

echo.
echo PySide6 is not installed yet. Installing it once, please wait...
echo.
python -m pip install -r "%~dp0requirements.txt"
if errorlevel 1 goto :pipfailed

:launch
start "" pythonw "%~dp0video_duration_gui.py" %*
exit /b 0

:pipfailed
echo.
echo [ERROR] PySide6 could not be installed automatically.
echo Run this manually:  python -m pip install PySide6-Essentials
echo.
pause
exit /b 1

:nopython
echo.
echo [ERROR] Python 3 was not found.
echo Install it from https://www.python.org/downloads/ and enable "Add python.exe to PATH".
echo.
pause
exit /b 1
