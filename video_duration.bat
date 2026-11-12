@echo off
chcp 65001 >nul
title Video Duration Calculator
powershell -NoProfile -ExecutionPolicy Bypass -Command "$c = Get-Content -LiteralPath '%~f0' -Raw -Encoding UTF8; $c = $c.Substring($c.IndexOf('#PS' + 'START')); Invoke-Expression $c"
echo.
pause
exit /b
#PSSTART
[Console]::InputEncoding  = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# --- find ffprobe ---
$ffprobe = $null
$cmd = Get-Command ffprobe -ErrorAction SilentlyContinue
if ($cmd) { $ffprobe = $cmd.Source }
if (-not $ffprobe) {
    Write-Host "ffprobe was not found in PATH." -ForegroundColor Red
    $p = (Read-Host "Enter full path to ffprobe.exe").Trim().Trim('"')
    if (Test-Path -LiteralPath $p) { $ffprobe = $p } else { Write-Host "Not found." -ForegroundColor Red; return }
}

# --- ask for folder ---
$folder = (Read-Host "Enter folder path (e.g. D:\Movies)").Trim().Trim('"')
if (-not (Test-Path -LiteralPath $folder -PathType Container)) {
    Write-Host "Folder not found." -ForegroundColor Red
    return
}

$ext = '.mp4','.mkv','.avi','.mov','.wmv','.flv','.webm','.m4v','.mpg','.mpeg','.ts','.3gp'
$files = Get-ChildItem -LiteralPath $folder -Recurse -File |
         Where-Object { $ext -contains $_.Extension.ToLower() }

if (-not $files) {
    Write-Host "No video files found." -ForegroundColor Yellow
    return
}

$totalSec = 0.0
$ok = 0
$failed = @()
$i = 0

foreach ($f in $files) {
    $i++
    Write-Progress -Activity "Reading durations" -Status "$i / $($files.Count)" -PercentComplete (($i / $files.Count) * 100)

    $out = & $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i $f.FullName 2>$null
    $sec = 0.0
    if ($out -and [double]::TryParse(($out | Select-Object -First 1), [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$sec)) {
        $totalSec += $sec
        $ok++
    } else {
        $failed += $f.FullName
    }
}
Write-Progress -Activity "Reading durations" -Completed

$mins = [math]::Round($totalSec / 60)
$h = [math]::Floor($mins / 60)
$m = $mins % 60

Write-Host ""
Write-Host "Video files found : $($files.Count)"
Write-Host "Durations read    : $ok"
Write-Host "Total duration    : $h hours and $m minutes" -ForegroundColor Green

if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Could not read duration for:" -ForegroundColor Yellow
    $failed | ForEach-Object { Write-Host "  $_" }
}
