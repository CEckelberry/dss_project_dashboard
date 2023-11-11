function Test-CommandExists {
    param($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    try {
        if (Get-Command $command) {
            return $true
        }
        else {
            return $false
        }
    }
    finally {
        $ErrorActionPreference = $oldPreference
    }
}

# Check if Python is installed
if (-not (Test-CommandExists 'python')) {
    Write-Output "Python is not installed. Please install Python before proceeding."
    # Add steps here to download and install Python if you want to automate this process
    exit
}

# Check if pip is installed
if (-not (Test-CommandExists 'pip')) {
    Write-Output "pip is not installed. Installing pip."
    python -m ensurepip
}

# List of required Python packages
$requiredPackages = @('pandas', 'selenium')

# Install required Python packages
foreach ($package in $requiredPackages) {
    pip install $package
}

# Define script relative paths
$scriptPaths = @(
    ".\downloader_iea\main.py",
    ".\downloader_imf\main.py"
)

# Save current directory
$currentDir = Get-Location

# Navigate and run scripts
foreach ($path in $scriptPaths) {
    $scriptDir = Join-Path $currentDir $path
    python $scriptDir
}

# Start Docker Compose services
docker-compose up --build
