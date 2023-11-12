#!/bin/bash

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Homebrew if not installed
if ! command_exists brew; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python 3.10 using Homebrew
if ! command_exists python3.10; then
    echo "Installing Python 3.10..."
    brew install python@3.10
    # Add Python 3.10 to PATH
    echo 'export PATH="/usr/local/opt/python@3.10/bin:$PATH"' >> ~/.bash_profile
    source ~/.bash_profile
fi

# Install pip
if ! command_exists pip3.10; then
    echo "Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3.10 get-pip.py
    rm get-pip.py
fi

# Install required Python packages
required_packages=("pandas" "selenium")
for package in "${required_packages[@]}"; do
    pip3.10 install "$package"
done

# Install ChromeDriver
install_chromedriver() {
    echo "Installing ChromeDriver..."

    CHROMEDRIVER_DIR="$HOME/.local/bin"
    mkdir -p "$CHROMEDRIVER_DIR"
    curl -L "https://chromedriver.storage.googleapis.com/119.0.6045.105/chromedriver_mac64.zip" -o chromedriver_mac64.zip
    unzip -o chromedriver_mac64.zip -d "$CHROMEDRIVER_DIR"
    rm chromedriver_mac64.zip
    chmod +x "$CHROMEDRIVER_DIR/chromedriver"
}
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