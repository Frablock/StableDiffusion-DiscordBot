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

REM Execute your script here
REM For example, if your script is named `my_script.py`, you can run it like this:
python start.py
