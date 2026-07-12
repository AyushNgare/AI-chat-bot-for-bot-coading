@echo off
title Synthetix.AI Launcher
cls

echo ======================================================================
echo              SYNTHETIX.AI - ROBOTICS MATRIX SUITE LAUNCHER
echo ======================================================================
echo.

:: Step 1: Verify Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on this system.
    echo Ensure you check "Add Python to PATH" during installation.
    pause
    exit /b
)

:: Step 2: Install or update dependencies 
echo [STATUS] Verifying vital framework layers...
pip install --upgrade pywebview ollama pyserial

echo.
echo [STATUS] Starting local app instance...
echo [NOTE] Ensure your local Ollama server is running!
echo ----------------------------------------------------------------------
echo.

:: Step 3: Execute the script
python synthetix_ai_app.py

:: Step 4: Keep window open on crash
if %errorlevel% neq 0 (
    echo.
    echo [CRITICAL ERROR] The application closed unexpectedly.
    echo Review the error log above for missing drivers or code faults.
    echo.
    pause
)