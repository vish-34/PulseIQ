# PowerShell Script to Test Crash Simulation

# Replace with your ngrok URL
$ngrokUrl = "https://6b2418a8108c.ngrok-free.app/api/trigger/crash"

# Or use localhost for local testing
# $ngrokUrl = "http://localhost:8000/api/trigger/crash"

# Set headers
$headers = @{
    "X-Trigger-Token" = "CRASH_BUTTON"
    "Content-Type" = "application/json"
}

Write-Host "Testing crash simulation..." -ForegroundColor Yellow
Write-Host "URL: $ngrokUrl" -ForegroundColor Cyan
Write-Host ""

try {
    # Make the request
    $response = Invoke-RestMethod -Uri $ngrokUrl -Method GET -Headers $headers
    
    # Display response
    Write-Host "✅ SUCCESS! Crash simulation triggered!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Response:" -ForegroundColor Yellow
    $response | ConvertTo-Json -Depth 10
    
} catch {
    Write-Host "❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
}

