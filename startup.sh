#!/bin/bash

# Note: Make sure to make this script executable by running 'chmod +x startup.sh'

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if Python is installed
if ! command_exists python3.10; then
    echo "Python 3.10 is not installed. Installing Python 3.10.1."
    # Add appropriate installation commands here based on the OS
    # For example, on Ubuntu:
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.10
    # Re-run the script to refresh the environment
    exec "$0"
fi

# Check if pip is installed
if ! command_exists pip3.10; then
    echo "pip is not installed. Installing pip."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.10 get-pip.py
    rm get-pip.py

    # Add the directory where pip is installed to PATH
    PIP_PATH="$(python3.10 -m site --user-base)/bin"
    export PATH="$PIP_PATH:$PATH"
fi

# List of required Python packages
required_packages=("pandas" "selenium")

# Install required Python packages
for package in "${required_packages[@]}"; do
    pip3.10 install "$package"
done

# Define script relative paths
script_paths=(
    "./downloader_iea/main.py"
    "./downloader_imf/main.py"
)

# Navigate and run scripts
for path in "${script_paths[@]}"; do
    python3.10 "$path"
done

# Start Docker Compose services
docker-compose up --build