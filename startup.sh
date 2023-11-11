#!/bin/bash

# Note: Make sure to make this script executable by running 'chmod +x startup.sh'

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Google Chrome
install_google_chrome() {
    echo "Installing Google Chrome..."
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i google-chrome-stable_current_amd64.deb
    sudo apt-get -f install -y
    rm google-chrome-stable_current_amd64.deb
}

# Install ChromeDriver matching Google Chrome version
install_chromedriver() {
    # Get the installed version of Google Chrome
    CHROME_VERSION=$(google-chrome --version | grep -oP "Google Chrome \K[^ ]+")
    CHROME_MAIN_VERSION=$(echo $CHROME_VERSION | cut -d'.' -f1)

    # Get the corresponding ChromeDriver version
    CHROMEDRIVER_VERSION=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_MAIN_VERSION")

    echo "Installing ChromeDriver version $CHROMEDRIVER_VERSION for Google Chrome version $CHROME_VERSION..."

    # Download ChromeDriver
    curl -L "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -o chromedriver_linux64.zip
    
    # Extract ChromeDriver and move it to a known directory
    CHROMEDRIVER_DIR="$HOME/.local/bin"
    unzip -o chromedriver_linux64.zip -d "$CHROMEDRIVER_DIR"
    rm chromedriver_linux64.zip

    # Add execute permissions
    chmod +x "$CHROMEDRIVER_DIR/chromedriver"

    # Add the ChromeDriver directory to PATH
    export PATH="$CHROMEDRIVER_DIR:$PATH"
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

# Check if unzip is installed, install it if not
if ! command_exists unzip; then
    echo "unzip is not installed. Installing unzip."
    sudo apt-get install unzip
fi

# Install Google Chrome if not installed
if ! command_exists google-chrome; then
    install_google_chrome
fi

# Check if ChromeDriver is installed or if its version matches Google Chrome
if ! command_exists chromedriver; then
    install_chromedriver
else
    # Check if the ChromeDriver version matches the Google Chrome version
    INSTALLED_CHROMEDRIVER_VERSION=$(chromedriver --version | grep -oP "ChromeDriver \K[^ ]+" | cut -d'.' -f1)
    if [ "$INSTALLED_CHROMEDRIVER_VERSION" != "$CHROME_MAIN_VERSION" ]; then
        echo "ChromeDriver version does not match Google Chrome version. Reinstalling ChromeDriver..."
        install_chromedriver
    fi
fi

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