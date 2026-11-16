@echo off
title CARTOON-JARVIS: Animation Studio Dashboard
cd /d "%~dp0"

echo ========================================================
echo   Launching CARTOON-JARVIS Studio Web UI...
echo ========================================================

set PYTHON_EXE="E:\agent y\cartoon-jarvis\.venv\Scripts\python.exe"
if not exist %PYTHON_EXE% (
    set PYTHON_EXE=python
)

%PYTHON_EXE% -m streamlit run web_ui.py --server.port 8501 --server.headless false
pause
