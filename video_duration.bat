@echo off
chcp 65001 >nul
title Video Duration Calculator
set "VD_SCRIPT_DIR=%~dp0"
if not "%~1"=="" set "VD_PATH=%~1"
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

# --- ask for folder(s) ---
$raw = $env:VD_PATH
if (-not $raw -or -not $raw.Trim()) {
    Write-Host "Enter one or more folder paths." -ForegroundColor Cyan
    Write-Host "Separate multiple paths with a semicolon ( ; ). Quotes are allowed." -ForegroundColor DarkGray
    $raw = Read-Host "Folder path(s) (e.g. D:\Movies; E:\Courses)"
}
if ($null -eq $raw) { $raw = '' }
$raw = $raw.Trim()
if (-not $raw) { Write-Host "No path entered." -ForegroundColor Yellow; return }

$folders = @()
$invalid = @()
foreach ($part in ($raw -split ';')) {
    $p = $part.Trim().Trim('"').Trim()
    if (-not $p) { continue }
    if (Test-Path -LiteralPath $p -PathType Container) { $folders += (Resolve-Path -LiteralPath $p).Path }
    else { $invalid += $p }
}

if ($invalid.Count -gt 0) {
    Write-Host ""
    Write-Host "Skipping invalid path(s):" -ForegroundColor Yellow
    $invalid | ForEach-Object { Write-Host "  $_" }
}
if ($folders.Count -eq 0) { Write-Host "Folder not found." -ForegroundColor Red; return }

# --- collect video files (duplicates removed) ---
$ext = '.mp4','.mkv','.avi','.mov','.wmv','.flv','.webm','.m4v','.mpg','.mpeg','.ts','.3gp'
$seen = @{}
$files = @()
foreach ($folder in $folders) {
    Get-ChildItem -LiteralPath $folder -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        if ($ext -contains $_.Extension.ToLower()) {
            $key = $_.FullName.ToLower()
            if (-not $seen.ContainsKey($key)) { $seen[$key] = $true; $files += $_ }
        }
    }
}

if ($files.Count -eq 0) {
    Write-Host "No video files found." -ForegroundColor Yellow
    return
}

# --- read durations ---
$totalSec = 0.0
$ok = 0
$rows = New-Object System.Collections.Generic.List[object]
$i = 0

foreach ($f in $files) {
    $i++
    Write-Progress -Activity "Reading durations" -Status "$i / $($files.Count) : $($f.Name)" -PercentComplete (($i / $files.Count) * 100)

    $out = & $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i $f.FullName 2>$null
    $sec = 0.0
    $good = $false
    if ($out -and [double]::TryParse(($out | Select-Object -First 1), [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$sec) -and $sec -ge 0 -and -not [double]::IsNaN($sec)) {
        $totalSec += $sec
        $ok++
        $good = $true
    }

    $durSec = $null
    $durStr = ''
    $status = 'FAILED'
    if ($good) {
        $durSec = [math]::Round($sec, 3)
        $durStr = [TimeSpan]::FromSeconds([math]::Round($sec)).ToString('hh\:mm\:ss')
        $status = 'OK'
    }
    $rows.Add([pscustomobject]@{
        Path            = $f.FullName
        SizeMB          = [math]::Round($f.Length / 1MB, 2)
        DurationSeconds = $durSec
        Duration        = $durStr
        Status          = $status
    })
}
Write-Progress -Activity "Reading durations" -Completed

# --- totals ---
$mins = [math]::Round($totalSec / 60)
$h = [math]::Floor($mins / 60)
$m = $mins % 60
$span = [TimeSpan]::FromSeconds([math]::Round($totalSec))
$hms = '{0}:{1:00}:{2:00}' -f [math]::Floor($span.TotalHours), $span.Minutes, $span.Seconds

Write-Host ""
Write-Host "Folders scanned   : $($folders.Count)"
Write-Host "Video files found : $($files.Count)"
Write-Host "Durations read    : $ok"
Write-Host "Total duration    : $h hours and $m minutes  ($hms)" -ForegroundColor Green
Write-Host ("Total seconds     : {0:N1}" -f $totalSec) -ForegroundColor DarkGray

$failed = $rows | Where-Object { $_.Status -ne 'OK' }
if ($failed.Count -gt 0) {
    Write-Host ""
    Write-Host "Could not read duration for:" -ForegroundColor Yellow
    $failed | ForEach-Object { Write-Host "  $($_.Path)" }
}

# --- export CSV (next to the script when possible, otherwise current folder) ---
$outDir = $env:VD_SCRIPT_DIR
if (-not $outDir -or -not (Test-Path -LiteralPath $outDir -PathType Container)) { $outDir = (Get-Location).Path }
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$csv = Join-Path $outDir "video_durations-$stamp.csv"
try {
    $rows | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8
    Write-Host ""
    Write-Host "CSV written to    : $csv" -ForegroundColor Cyan
} catch {
    $csv = Join-Path $env:TEMP "video_durations-$stamp.csv"
    try {
        $rows | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8
        Write-Host ""
        Write-Host "CSV written to    : $csv" -ForegroundColor Cyan
    } catch {
        Write-Host ""
        Write-Host "Could not write CSV: $($_.Exception.Message)" -ForegroundColor Red
    }
}
