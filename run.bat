@echo off
title PDF & Word Converter
cd /d "%~dp0"

echo.
echo ============================================
echo   Setting up PDF & Word Converter...
echo ============================================
echo.

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo ============================================
echo   Starting converter... browser will open.
echo   Keep this window open while using it.
echo ============================================
echo.

python app.py
pause