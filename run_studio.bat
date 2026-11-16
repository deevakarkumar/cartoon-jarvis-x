@echo off
title CARTOON-JARVIS: Zero-Budget Animation Studio
cd /d "%~dp0"

set PYTHON_EXE="E:\agent y\cartoon-jarvis\.venv\Scripts\python.exe"
if not exist %PYTHON_EXE% (
    set PYTHON_EXE=python
)

%PYTHON_EXE% main.py %*
pause
