@echo off
title Zanaks AI Server
echo ========================================================
echo   Starting Zanaks AI (formerly CodeBuddy)
echo   Local Address: http://127.0.0.1:5000
echo ========================================================
echo.

if exist .venv\Scripts\python.exe (
    echo Using virtual environment: .venv
    .venv\Scripts\python.exe app.py
) else if exist venv\Scripts\python.exe (
    echo Using virtual environment: venv
    venv\Scripts\python.exe app.py
) else (
    echo Using system Python
    python app.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Server exited with code %ERRORLEVEL%.
    pause
)
