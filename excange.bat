@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ====================================
echo Current Directory Video Converter
echo ====================================
echo.

REM Check FFmpeg
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] FFmpeg not installed, please run "install_ffmpeg.bat" first
    pause
    exit /b 1
)

REM Use script directory
cd /d "%~dp0"
echo Current directory: %CD%
echo.

set /a COUNT=0

echo Starting conversion...
echo.

REM Convert all video files in current directory
for %%f in (*.rmvb *.RMVB *.mkv *.MKV *.avi *.AVI *.flv *.FLV) do (
    set /a COUNT+=1
    echo [!COUNT!] Converting: %%f
    echo Output: %%~nf.mp4
    
    if exist "%%~nf.mp4" (
        echo [SKIP] MP4 file already exists
    ) else (
        ffmpeg -i "%%f" -c:v libx264 -crf 23 -preset medium -c:a aac -b:a 192k -movflags +faststart "%%~nf.mp4" -y
        
        if !errorlevel! equ 0 (
            echo [SUCCESS] Conversion completed
        ) else (
            echo [FAILED] Conversion failed
        )
    )
    echo.
)

if !COUNT! equ 0 (
    echo No video files found in current directory for conversion
    echo Supported formats: RMVB, MKV, AVI, FLV
)

echo ====================================
echo Conversion complete! Converted !COUNT! files
echo ====================================
pause
