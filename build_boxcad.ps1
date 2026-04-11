# Configuration
$venvPath = ".\.venv\Scripts\python.exe"
$distPath = "$PSScriptRoot\dist"
$buildTemp = "$PSScriptRoot\build_temp"
$specPath = "$PSScriptRoot\build_config"
$splashPath = "$PSScriptRoot\assets\splash_screen_600x400.png"

$addData = @(
    "$PSScriptRoot\.venv\Lib\site-packages\casadi;casadi",
    "$PSScriptRoot\ui;ui",
    "$PSScriptRoot\viewer.html;.",
    "$PSScriptRoot\viewer.css;.",
    "$PSScriptRoot\viewer.js;.",
    "$PSScriptRoot\assets;assets",
    "$PSScriptRoot\libs;libs",
    "$PSScriptRoot\startingModel.stl;."
)

# Safety check
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ Error: Virtual environment not found at .\.venv" -ForegroundColor Red
    Write-Host "Please ensure you have a .venv folder in this directory."
    Read-Host "Press Enter to exit"
    exit
}

# Menu
Write-Host "--- BoxCAD Build Script ---" -ForegroundColor Cyan
Write-Host "1) Continue"
Write-Host "q) Quit"
$choice = Read-Host "Choose an option"

switch ($choice) {
    "1" { $continue = $true }
    "q" { exit }
    Default {
        Write-Host "Invalid choice." -ForegroundColor Red
        exit
    }
}

# Build process
if ($continue) {
    Write-Host "`n🚀 Building BoxCAD..." -ForegroundColor Magenta

    # Build argument array properly
    $pyInstallerArgs = @(
        "--specpath", $specPath
        "--workpath", $buildTemp
        "--noconfirm"
        "--onefile"
        "--windowed"
        "--name", "BoxCAD"
        "--distpath", $distPath
        "--splash", $splashPath
        "--hidden-import", "main_window"
    )

    # Add all --add-data entries correctly
    foreach ($item in $addData) {
        $pyInstallerArgs += "--add-data"
        $pyInstallerArgs += $item
    }

    # Entry script
    $pyInstallerArgs += "$PSScriptRoot\main.py"

    # Run PyInstaller
    & $venvPath -m PyInstaller @pyInstallerArgs
}

# Cleanup
Write-Host "`n🧹 Cleaning up build artifacts..." -ForegroundColor Yellow

if (Test-Path $buildTemp) {
    Remove-Item -Recurse -Force $buildTemp
}

if (Test-Path $specPath) {
    Get-ChildItem $specPath -Filter "*.spec" | Remove-Item -Force
}

Write-Host "`n✅ Build Process Complete!" -ForegroundColor Green
Read-Host "`nPress Enter to close this window"
