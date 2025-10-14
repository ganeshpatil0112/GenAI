# PowerShell Script to Transfer Files to H100 Server
# Usage: .\transfer_to_h100.ps1

# ==================== CONFIGURATION ====================
# CHANGE THESE VALUES TO MATCH YOUR H100 SERVER
$SERVER_IP = "192.168.1.100"        # Your H100 server IP address
$SERVER_USER = "username"            # Your username on H100 server
$SERVER_PATH = "~/finetuningfinal"  # Destination directory

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Transfer to H100 GPU Server" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Check if models exist
if (-not (Test-Path "models")) {
    Write-Host "ERROR: models/ directory not found!" -ForegroundColor Red
    Write-Host "Make sure you're in the finetuningfinal directory" -ForegroundColor Red
    exit 1
}

Write-Host "`n1. Preparing files for transfer..." -ForegroundColor Yellow

# Files and directories to transfer
$itemsToTransfer = @(
    "models",
    "datasets",
    "api_server.py",
    "Dockerfile",
    "docker-compose.yml",
    "requirements.txt",
    "requirements_api.txt",
    "start_api.py",
    "client_example.py",
    "test_api.py",
    "README.md",
    "API_README.md"
)

Write-Host "Checking files..." -ForegroundColor Cyan
$existingItems = @()
foreach ($item in $itemsToTransfer) {
    if (Test-Path $item) {
        Write-Host "  ✓ $item" -ForegroundColor Green
        $existingItems += $item
    } else {
        Write-Host "  ✗ $item (not found - skipping)" -ForegroundColor Yellow
    }
}

if ($existingItems.Count -eq 0) {
    Write-Host "`nERROR: No files found to transfer!" -ForegroundColor Red
    exit 1
}

# Calculate total size
$totalSize = 0
foreach ($item in $existingItems) {
    $size = (Get-ChildItem $item -Recurse -File | Measure-Object -Property Length -Sum).Sum
    $totalSize += $size
}

Write-Host "`nTotal size: $([math]::Round($totalSize / 1GB, 2)) GB" -ForegroundColor Cyan
Write-Host "Server: $SERVER_USER@$SERVER_IP" -ForegroundColor Cyan

$confirmation = Read-Host "`nProceed with transfer? (y/n)"
if ($confirmation -ne 'y') {
    Write-Host "Transfer cancelled" -ForegroundColor Yellow
    exit 0
}

Write-Host "`n2. Creating compressed archive..." -ForegroundColor Yellow

# Create timestamp for unique filename
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$archiveName = "finetuning_h100_$timestamp.zip"

Write-Host "Creating archive: $archiveName" -ForegroundColor Cyan
Write-Host "This may take 5-10 minutes for large model files..." -ForegroundColor Yellow

Compress-Archive -Path $existingItems -DestinationPath $archiveName -Force

$archiveSize = (Get-Item $archiveName).Length / 1GB
Write-Host "✓ Archive created successfully!" -ForegroundColor Green
Write-Host "  Archive size: $([math]::Round($archiveSize, 2)) GB" -ForegroundColor Cyan

Write-Host "`n3. Transferring to H100 server..." -ForegroundColor Yellow
Write-Host "Progress will show below..." -ForegroundColor Cyan
Write-Host "This may take 10-30 minutes depending on network speed..." -ForegroundColor Yellow

# Transfer using SCP
try {
    Write-Host "`nExecuting: scp $archiveName ${SERVER_USER}@${SERVER_IP}:~/" -ForegroundColor Gray
    
    # Use scp command
    & scp $archiveName "${SERVER_USER}@${SERVER_IP}:~/"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Transfer completed successfully!" -ForegroundColor Green
        
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "Next Steps on H100 Server:" -ForegroundColor Cyan
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "1. Connect to server:" -ForegroundColor Yellow
        Write-Host "   ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor White
        Write-Host ""
        Write-Host "2. Extract files:" -ForegroundColor Yellow
        Write-Host "   unzip ~/$archiveName -d ~/finetuningfinal" -ForegroundColor White
        Write-Host ""
        Write-Host "3. Navigate to directory:" -ForegroundColor Yellow
        Write-Host "   cd ~/finetuningfinal" -ForegroundColor White
        Write-Host ""
        Write-Host "4. Deploy with Docker:" -ForegroundColor Yellow
        Write-Host "   docker-compose up -d" -ForegroundColor White
        Write-Host ""
        Write-Host "5. Check status:" -ForegroundColor Yellow
        Write-Host "   docker-compose logs -f" -ForegroundColor White
        Write-Host "========================================" -ForegroundColor Cyan
        
        # Cleanup
        Write-Host "`n4. Cleanup local archive?" -ForegroundColor Yellow
        $cleanup = Read-Host "Delete local $archiveName? (y/n)"
        if ($cleanup -eq 'y') {
            Remove-Item $archiveName
            Write-Host "✓ Archive deleted" -ForegroundColor Green
        } else {
            Write-Host "Archive kept: $archiveName" -ForegroundColor Cyan
        }
        
        Write-Host "`n✓ All done! SSH to your H100 server and follow the steps above." -ForegroundColor Green
        
    } else {
        throw "SCP command failed with exit code: $LASTEXITCODE"
    }
    
} catch {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "ERROR: Transfer Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify SSH access:" -ForegroundColor Cyan
    Write-Host "   ssh ${SERVER_USER}@${SERVER_IP}" -ForegroundColor White
    Write-Host ""
    Write-Host "2. Check if server IP and username are correct" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "3. Alternative: Use WinSCP (GUI method)" -ForegroundColor Cyan
    Write-Host "   Download from: https://winscp.net" -ForegroundColor White
    Write-Host "   Transfer file: $archiveName" -ForegroundColor White
    Write-Host ""
    Write-Host "4. Alternative: Use rsync" -ForegroundColor Cyan
    Write-Host "   Install: winget install cwrsync" -ForegroundColor White
    Write-Host ""
    
    Write-Host "Archive file location: $(Get-Location)\$archiveName" -ForegroundColor Yellow
}

