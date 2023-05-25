#!/bin/bash

PYTHON_SCRIPT="encrypt.py"

# Change directory to the script's directory
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is required but not installed. Aborting."
    exit 1
fi

# Check if required packages are installed
REQUIRED_PACKAGES=("python-pycryptodome" "python-termcolor")
for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import ${package}" &>/dev/null; then
        echo "${package} is not installed. Installing..."
        sudo pacman -Sy --noconfirm ${package}
    fi
done

# Run the Python script
python3 "$PYTHON_SCRIPT"
