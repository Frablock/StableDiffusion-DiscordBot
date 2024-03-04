@echo off
REM Define the path to your virtual environment
set VENV_PATH=.\venv

REM Check if the virtual environment exists
if not exist "%VENV_PATH%" (
    echo Virtual environment not found at %VENV_PATH%
    echo Creating venv
    python -m venv %VENV_PATH%
    exit /b 1
)

REM Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

pip -r install requirements.txt

python start.py
