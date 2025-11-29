# PowerShell script to start ngrok
# Usage: .\start_ngrok.ps1

Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host "Starting ngrok tunnel for port 8000"
Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host ""

# Check if ngrok is in PATH
$ngrokPath = Get-Command ngrok -ErrorAction SilentlyContinue

if ($ngrokPath) {
    Write-Host "Found ngrok in PATH"
    Write-Host "Starting ngrok http 8000..."
    Write-Host ""
    ngrok http 8000
} else {
    # Try common locations
    $possiblePaths = @(
        "C:\ngrok\ngrok.exe",
        "$env:USERPROFILE\ngrok\ngrok.exe",
        "$env:LOCALAPPDATA\ngrok\ngrok.exe"
    )
    
    $found = $false
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            Write-Host "Found ngrok at: $path"
            Write-Host "Starting ngrok http 8000..."
            Write-Host ""
            & $path http 8000
            $found = $true
            break
        }
    }
    
    if (-not $found) {
        Write-Host "ERROR: ngrok not found!" -ForegroundColor Red
        Write-Host ""
        Write-Host "Please install ngrok:"
        Write-Host "  1. Download from: https://ngrok.com/download"
        Write-Host "  2. Extract ngrok.exe to a folder (e.g., C:\ngrok\)"
        Write-Host "  3. Add to PATH or use full path"
        Write-Host ""
        Write-Host "Or run manually:"
        Write-Host "  ngrok http 8000"
        Write-Host ""
        Write-Host "See NGROK_SETUP.md for detailed instructions"
        exit 1
    }
}

