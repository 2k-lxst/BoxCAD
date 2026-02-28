# --- Configuration ---
$venvPath = ".\.venv\Scripts\python.exe"

# Safety check: Ensure the venv actually exists
if (!(Test-Path $venvPath)) {
    Write-Host "❌ Error: Virtual environment not found at .\.venv" -ForegroundColor Red
    Write-Host "Please ensure you have a .venv folder in this directory."
    Read-Host "Press Enter to exit"
    exit
}

Write-Host "--- BoxCAD Build System ---" -ForegroundColor Cyan
Write-Host "1) Build Main Window"
Write-Host "2) Build Welcome Screen"
Write-Host "3) Build Both"
Write-Host "q) Quit"
$choice = Read-Host "Choose an option"

$buildMain = $false
$buildWelcome = $false

switch ($choice) {
    "1" { $buildMain = $true }
    "2" { $buildWelcome = $true }
    "3" { $buildMain = $true; $buildWelcome = $true }
    "q" { exit }
    Default { Write-Host "Invalid choice."; exit }
}

# --- Build Execution ---

if ($buildMain) {
    Write-Host "`n🚀 Building BoxCAD-MainWindow..." -ForegroundColor Magenta

    # Using & $venvPath ensures we use the project's specific Python environment
    & $venvPath -m PyInstaller --specpath "build_config" `
        --workpath "build_temp" `
        --noconfirm `
        --onefile `
        --windowed `
        --name "BoxCAD-MainWindow" `
        --distpath "$PSScriptRoot/dist/" `
        --splash "$PSScriptRoot/assets/splash_screen_600x400.png" `
        --add-data "$PSScriptRoot/.venv/Lib/site-packages/casadi;casadi" `
        --add-data "$PSScriptRoot/ui;ui" `
        --add-data "$PSScriptRoot/viewer.html;." `
        --add-data "$PSScriptRoot/viewer.css;." `
        --add-data "$PSScriptRoot/viewer.js;." `
        --add-data "$PSScriptRoot/assets;assets" `
        --add-data "$PSScriptRoot/libs;libs" `
        "$PSScriptRoot/main_window.py"
}

if ($buildWelcome) {
    Write-Host "`n🚀 Building BoxCAD-WelcomeScreen..." -ForegroundColor Magenta

    & $venvPath -m PyInstaller --specpath "$PSScriptRoot/build_config" `
        --workpath "$PSScriptRoot/build_temp" `
        --noconfirm `
        --onefile `
        --windowed `
        --name "BoxCAD-WelcomeScreen" `
        --distpath "$PSScriptRoot/dist/" `
        --splash "$PSScriptRoot/assets/splash_screen_600x400.png" `
        --add-data "$PSScriptRoot/ui;ui" `
        "$PSScriptRoot/main.py"
}

# --- Cleanup Phase ---

Write-Host "`n🧹 Cleaning up build artifacts..." -ForegroundColor Yellow

if (Test-Path "build_temp") {
    Remove-Item -Recurse -Force "build_temp"
}

if (Test-Path "build_config") {
    Get-ChildItem "build_config" -Filter "*.spec" | Remove-Item -Force
}

Write-Host "`n✅ Build Process Complete!" -ForegroundColor Green
Read-Host "`nPress Enter to close this window"
