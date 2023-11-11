#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install a specific version of Google Chrome
install_google_chrome() {
    echo "Installing Google Chrome version 119.0.6045.123..."
    # Replace with the actual download link and package name
    wget [DIRECT_DOWNLOAD_LINK_FOR_GOOGLE_CHROME_VERSION_119.0.6045.123]
    sudo dpkg -i [DOWNLOADED_GOOGLE_CHROME_DEB_PACKAGE_NAME]
    sudo apt-get -f install -y
    rm [DOWNLOADED_GOOGLE_CHROME_DEB_PACKAGE_NAME]
}

# Install a specific version of ChromeDriver
install_chromedriver() {
    echo "Installing ChromeDriver version 119.0.6045.105..."

    # Define the ChromeDriver directory
    CHROMEDRIVER_DIR="$HOME/.local/bin"

    # Remove any existing ChromeDriver binaries in system paths and local bin
    sudo rm -f /usr/local/bin/chromedriver
    sudo rm -f /usr/bin/chromedriver
    rm -f "$CHROMEDRIVER_DIR/chromedriver"

    # Download and install ChromeDriver
    curl -L "https://chromedriver.storage.googleapis.com/119.0.6045.105/chromedriver_linux64.zip" -o chromedriver_linux64.zip
    unzip -o chromedriver_linux64.zip -d "$CHROMEDRIVER_DIR"
    rm chromedriver_linux64.zip
    chmod +x "$CHROMEDRIVER_DIR/chromedriver"
}

# Check if Python is installed
if ! command_exists python3.10; then
    echo "Python 3.10 is not installed. Installing Python 3.10.1."
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.10
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

# Check if unzip is installed, install it if not
if ! command_exists unzip; then
    echo "unzip is not installed. Installing unzip."
    sudo apt-get install unzip
fi

# Install Google Chrome if not installed
if ! command_exists google-chrome; then
    install_google_chrome
fi

# Install ChromeDriver
install_chromedriver

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