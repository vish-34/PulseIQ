# PowerShell script to get your IP address for network sharing
# Run this to find your IP address to give to your friend

Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host "Finding Your IP Address for Network Sharing"
Write-Host "=" -NoNewline
Write-Host ("=" * 69)
Write-Host ""

# Get IPv4 addresses
$ipAddresses = Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike "127.*" -and 
    $_.IPAddress -notlike "169.254.*"
} | Select-Object IPAddress, InterfaceAlias

if ($ipAddresses) {
    Write-Host "Your IP Address(es):" -ForegroundColor Green
    Write-Host ""
    
    foreach ($ip in $ipAddresses) {
        Write-Host "  IP: $($ip.IPAddress)" -ForegroundColor Yellow
        Write-Host "  Interface: $($ip.InterfaceAlias)"
        Write-Host ""
    }
    
    # Get the first non-localhost IP (usually WiFi)
    $mainIP = ($ipAddresses | Where-Object { $_.InterfaceAlias -like "*Wi-Fi*" -or $_.InterfaceAlias -like "*Wireless*" } | Select-Object -First 1)
    
    if ($mainIP) {
        Write-Host "=" -NoNewline
        Write-Host ("=" * 69)
        Write-Host "RECOMMENDED IP (WiFi):" -ForegroundColor Green
        Write-Host "  $($mainIP.IPAddress)" -ForegroundColor Yellow -BackgroundColor Black
        Write-Host ""
        Write-Host "Give this URL to your friend:"
        Write-Host "  http://$($mainIP.IPAddress):8000/api/trigger/crash" -ForegroundColor Cyan
        Write-Host "=" -NoNewline
        Write-Host ("=" * 69)
    } else {
        $firstIP = $ipAddresses[0].IPAddress
        Write-Host "=" -NoNewline
        Write-Host ("=" * 69)
        Write-Host "RECOMMENDED IP:"
        Write-Host "  $firstIP" -ForegroundColor Yellow -BackgroundColor Black
        Write-Host ""
        Write-Host "Give this URL to your friend:"
        Write-Host "  http://$firstIP:8000/api/trigger/crash" -ForegroundColor Cyan
        Write-Host "=" -NoNewline
        Write-Host ("=" * 69)
    }
} else {
    Write-Host "ERROR: Could not find IP address!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Try running: ipconfig"
}

Write-Host ""

