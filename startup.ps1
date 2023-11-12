# Function to check if a command exists
function Test-CommandExists {
    param($command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = 'SilentlyContinue'
    try {
        if (Get-Command $command -ErrorAction SilentlyContinue) {
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
    Write-Output "Python is not installed. Installing Python 3.10.1."
    # Download Python installer
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.1/python-3.10.1-amd64.exe" -OutFile "python-3.10.1-amd64.exe"
    # Run installer
    Start-Process -FilePath ".\python-3.10.1-amd64.exe" -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1" -Wait

    # Update PATH for the current session
    $pythonPath = "C:\Python310\Scripts;C:\Python310"
    $env:Path += ";$pythonPath"
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