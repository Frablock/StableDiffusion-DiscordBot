#!/bin/bash

# Define the path to your virtual environment
VENV_PATH="./venv"

# Check if the virtual environment exists
if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment not found at $VENV_PATH"
    echo "Creating venv"
    python -m venv $VENV_PATH
    exit 1
fi

# Activate the virtual environment
source "$VENV_PATH/bin/activate"

pip -r install requirements.txt

python start.py
