@echo off
chcp 65001 >nul
echo ====================================
echo Video Sharing Website Startup Script
echo ====================================
echo.

REM Get script directory
cd /d "%~dp0"

echo Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python first
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Flask not detected, installing...
    pip install flask
    echo.
)

REM Check if video directory exists
if not exist "D:\videos-share-resouce" (
    echo [WARNING] Video directory "D:\videos-share-resouce" does not exist
    echo Creating directory...
    mkdir "D:\videos-share-resouce">nul
    if errorlevel 1 (
        echo [ERROR] Unable to create directory, please check permissions or create manually
    ) else (
        echo [SUCCESS] Directory created, please place video files in this directory
    )
    echo.
)

REM Check and stop old service process (if running single_file_videos_web_server.py)
echo Checking for old service process...
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr /i "PID:"') do (
    for /f "tokens=*" %%b in ('wmic process where "ProcessId=%%a" get CommandLine /format:list ^| findstr /i "single_file_videos_web_server.py.py"') do (
        echo Found old process PID: %%a
        taskkill /PID %%a /F >nul 2>&1
        if !errorlevel! equ 0 (
            echo [SUCCESS] Stopped old process
        )
    )
)
echo.

echo ====================================
echo Starting Flask server...
echo Access URL: http://localhost:80
echo Or: http://127.0.0.1:80
echo Press Ctrl+C to stop server
echo ====================================
echo.

REM Start Flask application
python single_file_videos_web_server.py

pause
