#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python; then
    echo "Python is not installed. Please install Python before proceeding."
    # Add steps here to download and install Python if you want to automate this process
    exit 1
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