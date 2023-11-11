#!/bin/bash

# Note: Make sure to make this script executable by running 'chmod +x startup.sh'

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python; then
    echo "Python is not installed. Installing Python 3.10.1."
    # Add appropriate installation commands here based on the OS
    # For example, on Ubuntu:
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.10
fi

# Check if pip is installed
if ! command_exists pip; then
    echo "pip is not installed. Installing pip."
    python -m ensurepip
fi

# List of required Python packages
required_packages=("pandas" "selenium")

# Install required Python packages
for package in "${required_packages[@]}"; do
    pip install "$package"
done

# Define script relative paths
script_paths=(
    "./downloader_iea/main.py"
    "./downloader_imf/main.py"
)

# Navigate and run scripts
for path in "${script_paths[@]}"; do
    python "$path"
done

# Start Docker Compose services
docker-compose up --build