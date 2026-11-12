<#
.SYNOPSIS
    Video Duration Calculator - sums the runtime of every video in one or more folders.

.DESCRIPTION
    Recursively scans the given folders, reads each video's duration with ffprobe,
    prints the total as hours/minutes plus exact h:mm:ss, and writes a CSV report.

.PARAMETER Path
    One or more folder paths. Multiple paths may also be passed as a single
    semicolon-separated string ("D:\Movies; E:\Courses").

.EXAMPLE
    .\video_duration.ps1 -Path "D:\Movies"

.EXAMPLE
    .\video_duration.ps1 -Path "D:\Movies; E:\Courses"
#>
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Path
)

$ErrorActionPreference = 'Stop'
$script:Version = '1.1.0'

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$extensions = @('.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg', '.ts', '.3gp')

function Get-ScriptFolder {
    if ($PSScriptRoot) { return $PSScriptRoot }
    if ($env:VD_SCRIPT_DIR) { return $env:VD_SCRIPT_DIR }
    return (Get-Location).Path
}

function Write-ErrorLog {
    param([string]$Message)
    foreach ($dir in @((Get-ScriptFolder), $env:TEMP)) {
        try {
            $log = Join-Path $dir 'video_duration-error.log'
            "[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $Message |
                Add-Content -LiteralPath $log -Encoding UTF8
            return $log
        } catch { }
    }
    return $null
}

function Format-Hms {
    param([double]$Seconds)
    $ts = [TimeSpan]::FromSeconds([math]::Round($Seconds))
    '{0}:{1:00}:{2:00}' -f [math]::Floor($ts.TotalHours), $ts.Minutes, $ts.Seconds
}

function Find-Ffprobe {
    $cmd = Get-Command ffprobe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }

    $candidates = @(
        (Join-Path $env:LOCALAPPDATA 'Microsoft\WinGet\Links\ffprobe.exe'),
        'C:\ffmpeg\bin\ffprobe.exe',
        'C:\Program Files\ffmpeg\bin\ffprobe.exe'
    )
    foreach ($c in $candidates) { if ($c -and (Test-Path -LiteralPath $c)) { return $c } }
    return $null
}

function Split-Paths {
    param([string[]]$Values)
    $out = @()
    foreach ($v in $Values) {
        if ($null -eq $v) { continue }
        foreach ($part in ($v -split ';')) {
            $p = $part.Trim().Trim('"').Trim()
            if ($p) { $out += $p }
        }
    }
    return $out
}

$code = 0
$logPath = Join-Path (Get-ScriptFolder) 'video_duration-error.log'
try {
    if (Test-Path -LiteralPath $logPath) { Remove-Item -LiteralPath $logPath -Force -ErrorAction SilentlyContinue }

    Write-Host "Video Duration Calculator $script:Version" -ForegroundColor Cyan
    Write-Host ""

    # --- locate ffprobe ---
    $ffprobe = Find-Ffprobe
    if (-not $ffprobe) {
        Write-Host "ffprobe was not found in PATH." -ForegroundColor Red
        Write-Host "Install FFmpeg (winget install Gyan.FFmpeg) or paste the full path below." -ForegroundColor DarkGray
        $answer = Read-Host "Path to ffprobe.exe"
        if ($answer) {
            $candidate = $answer.Trim().Trim('"')
            if (Test-Path -LiteralPath $candidate -PathType Leaf) { $ffprobe = $candidate }
        }
        if (-not $ffprobe) { throw 'ffprobe was not found. Install FFmpeg and try again.' }
    }

    # --- collect folder paths ---
    $rawPaths = Split-Paths -Values $Path
    if ($rawPaths.Count -eq 0) {
        Write-Host "Enter one or more folder paths." -ForegroundColor Cyan
        Write-Host "Separate multiple paths with a semicolon ( ; ). Quotes are allowed." -ForegroundColor DarkGray
        for ($attempt = 1; $attempt -le 3; $attempt++) {
            $answer = Read-Host "Folder path(s) (e.g. D:\Movies; E:\Courses)"
            $rawPaths = Split-Paths -Values @($answer)
            if ($rawPaths.Count -gt 0) { break }
            Write-Host "Nothing entered - try again." -ForegroundColor Yellow
        }
        if ($rawPaths.Count -eq 0) { throw 'No folder path was provided.' }
    }

    $folders = @()
    $invalid = @()
    foreach ($p in $rawPaths) {
        if (Test-Path -LiteralPath $p -PathType Container) {
            $folders += (Resolve-Path -LiteralPath $p).ProviderPath
        } else {
            $invalid += $p
        }
    }
    if ($invalid.Count -gt 0) {
        Write-Host ""
        Write-Host "Skipping invalid path(s):" -ForegroundColor Yellow
        $invalid | ForEach-Object { Write-Host "  $_" }
    }
    if ($folders.Count -eq 0) { throw 'None of the given folders exist.' }

    # --- collect video files (de-duplicated) ---
    $seen = @{}
    $files = New-Object System.Collections.Generic.List[object]
    foreach ($folder in $folders) {
        Get-ChildItem -LiteralPath $folder -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            if ($extensions -contains $_.Extension.ToLower()) {
                $key = $_.FullName.ToLowerInvariant()
                if (-not $seen.ContainsKey($key)) {
                    $seen[$key] = $true
                    $files.Add($_)
                }
            }
        }
    }
    if ($files.Count -eq 0) { throw 'No video files were found in the selected folder(s).' }

    # --- read durations ---
    $totalSec = 0.0
    $ok = 0
    $rows = New-Object System.Collections.Generic.List[object]
    $i = 0

    foreach ($f in $files) {
        $i++
        Write-Progress -Activity "Reading durations" -Status "$i / $($files.Count) : $($f.Name)" `
                       -PercentComplete (($i / $files.Count) * 100)

        $out = & $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i $f.FullName 2>$null
        $sec = 0.0
        $good = $false
        if ($out) {
            $first = ($out | Select-Object -First 1)
            if ([double]::TryParse($first, [Globalization.NumberStyles]::Float,
                                   [Globalization.CultureInfo]::InvariantCulture, [ref]$sec) -and
                $sec -gt 0 -and -not [double]::IsNaN($sec) -and -not [double]::IsInfinity($sec)) {
                $totalSec += $sec
                $ok++
                $good = $true
            }
        }

        $durSec = $null
        $durStr = ''
        $status = 'FAILED'
        if ($good) {
            $durSec = [math]::Round($sec, 3)
            $durStr = Format-Hms -Seconds $sec
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

    Write-Host ""
    Write-Host "Folders scanned   : $($folders.Count)"
    Write-Host "Video files found : $($files.Count)"
    Write-Host "Durations read    : $ok"
    Write-Host "Total duration    : $h hours and $m minutes  ($(Format-Hms -Seconds $totalSec))" -ForegroundColor Green
    Write-Host ("Total seconds     : {0:N1}" -f $totalSec) -ForegroundColor DarkGray

    $failed = @($rows | Where-Object { $_.Status -ne 'OK' })
    if ($failed.Count -gt 0) {
        Write-Host ""
        Write-Host "Could not read duration for:" -ForegroundColor Yellow
        $failed | ForEach-Object { Write-Host "  $($_.Path)" }
    }

    # --- CSV report ---
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $written = $false
    foreach ($dir in @((Get-ScriptFolder), $env:TEMP)) {
        $csv = Join-Path $dir "video_durations-$stamp.csv"
        try {
            $rows | Export-Csv -LiteralPath $csv -NoTypeInformation -Encoding UTF8
            Write-Host ""
            Write-Host "CSV written to    : $csv" -ForegroundColor Cyan
            $written = $true
            break
        } catch { }
    }
    if (-not $written) { Write-Host ""; Write-Host "Could not write the CSV report." -ForegroundColor Yellow }

} catch {
    $code = 1
    Write-Host ""
    Write-Host "[ERROR] $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "If this keeps happening, report it at https://github.com/babak12124/video-duration-calculator/issues" -ForegroundColor DarkGray
    $log = Write-ErrorLog -Message ("{0}`n{1}" -f $_.Exception.Message, $_.ScriptStackTrace)
    if ($log) { Write-Host "Details written to: $log" -ForegroundColor DarkGray }
}

exit $code
