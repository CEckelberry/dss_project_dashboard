#!/bin/bash

# Note: Make sure to make this script executable by running 'chmod +x startup.sh'

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Flag to indicate if Python was installed
python_installed=0

# Check if Python is installed
if ! command_exists python3; then
    echo "Python is not installed. Installing Python 3.10.1."
    # Add appropriate installation commands here based on the OS
    # For example, on Ubuntu:
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.10
    python_installed=1
fi

# Check if pip is installed
if ! command_exists pip3; then
    echo "pip is not installed. Installing pip."
    python3 -m ensurepip
fi

# If Python was just installed, re-run the script
if [ "$python_installed" -eq 1 ]; then
    exec "$0"
fi

# List of required Python packages
required_packages=("pandas" "selenium")

# Install required Python packages
for package in "${required_packages[@]}"; do
    pip3 install "$package"
done

# Define script relative paths
script_paths=(
    "./downloader_iea/main.py"
    "./downloader_imf/main.py"
)

# Navigate and run scripts
for path in "${script_paths[@]}"; do
    python3 "$path"
done

# Start Docker Compose services
docker-compose up --build