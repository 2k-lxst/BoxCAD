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

    python -m PyInstaller --specpath "build_config" `
        --workpath "build_temp" `
        --noconfirm `
        --onefile `
        --windowed `
        --name "BoxCAD-MainWindow" `
        --distpath "./dist/" `
        --splash "assets/splash_screen_600x400.png" `
        --add-data ".venv/Lib/site-packages/casadi;casadi" `
        --add-data "ui;ui" `
        --add-data "viewer.html;." `
        --add-data "viewer.css;." `
        --add-data "viewer.js;." `
        --add-data "assets;assets" `
        --add-data "libs;libs" `
        "main_window.py"
}

if ($buildWelcome) {
    Write-Host "`n🚀 Building BoxCAD-WelcomeScreen..." -ForegroundColor Magenta

    python -m PyInstaller --specpath "build_config" `
        --workpath "build_temp" `
        --noconfirm `
        --onefile `
        --windowed `
        --name "BoxCAD-WelcomeScreen" `
        --distpath "./dist/" `
        --splash "assets/splash_screen_600x400.png" `
        --add-data "ui;ui" `
        "main.py"
}

# --- Cleanup Phase ---

Write-Host "`n🧹 Cleaning up build artifacts..." -ForegroundColor Yellow

# Remove the temporary work directory
if (Test-Path "build_temp") {
    Remove-Item -Recurse -Force "build_temp"
}

# Remove the spec files created in the build_config folder
if (Test-Path "build_config") {
    Get-ChildItem "build_config" -Filter "*.spec" | Remove-Item -Force
}

Write-Host "`n✅ Build Process Complete!" -ForegroundColor Green
Read-Host "`nPress Enter to close this window"
