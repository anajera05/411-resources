#!/bin/bash

VENV_DIR=venv
REQUIREMENTS_FILE=requirements.txt

# Check if the virtual environment already exists
if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."

  # Create a virtual environment using python3
  python3 -m venv "$VENV_DIR"

  # Activate the virtual environment
  source "$VENV_DIR/bin/activate"

  # Install dependencies from requirements.txt if it exists
  if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing dependencies from $REQUIREMENTS_FILE..."
    pip install -r "$REQUIREMENTS_FILE"
  else
    echo "Error: $REQUIREMENTS_FILE not found."
    exit 1
  fi
else
  # If the virtual environment already exists, activate it
  echo "Virtual environment already exists. Activating..."
  source "$VENV_DIR/bin/activate"
fi
