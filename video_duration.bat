@echo off
setlocal
chcp 65001 >nul
title Video Duration Calculator
set "VD_HOME=%~dp0"
set "VD_PS=%VD_HOME%video_duration.ps1"
set "VD_LOG=%VD_HOME%video_duration-error.log"

if not exist "%VD_PS%" (
    echo.
    echo [ERROR] video_duration.ps1 was not found next to this file.
    echo Expected: %VD_PS%
    echo Keep video_duration.bat and video_duration.ps1 in the same folder.
    goto :finish
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%VD_PS%" %*
set "VD_RC=%ERRORLEVEL%"

if not "%VD_RC%"=="0" (
    echo.
    echo [ERROR] The script stopped with exit code %VD_RC%.
    if exist "%VD_LOG%" (
        echo ---------------------------- log ----------------------------
        type "%VD_LOG%"
        echo ------------------------------------------------------------
        echo Log file: %VD_LOG%
    )
)

:finish
echo.
echo Press any key to close this window . . .
pause >nul
exit /b 0
