@echo off
title PDF and Word Converter
cd /d "%~dp0"

echo.
echo ============================================
echo   Setting up PDF and Word Converter...
echo ============================================
echo.

py -3 -m pip install --upgrade pip
py -3 -m pip install -r requirements.txt

echo.
echo ============================================
echo   Starting converter... browser will open.
echo   Keep this window open while using it.
echo ============================================
echo.

py -3 app.py
pause
