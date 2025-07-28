#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

environmentDit=".venv"
installScript="./scripts/install.sh"
startScript="./scripts/start.sh"

clear

if [ ! -d "$environmentDit" ]; then
    read -p "Environment directory '$environmentDit' not found. Create it and install all dependencies? (Yes/y): " answer

    if [[ "$answer" == "Yes" || "$answer" == "yes" || "$answer" == "Y" || "$answer" == "y" ]]; then
        echo "Installing dependencies..."

        bash "$installScript"

        echo "Dependencies installed!"
    else
        echo "Installation canceled. Exiting..."
        exit 0
    fi
fi

echo "Starting bots..."

bash "$startScript"
