<#
.SYNOPSIS
    Video & Audio Duration Calculator - sums the runtime of every media file in one or more folders.

.DESCRIPTION
    Recursively scans the given folders, reads each file's duration with ffprobe,
    prints totals as hours/minutes plus exact h:mm:ss (video and audio counted
    separately, then combined), and writes a CSV report.

.PARAMETER Path
    One or more folder paths, passed positionally. Multiple paths may also be
    given as a single semicolon-separated string ("D:\Movies; E:\Courses").

.PARAMETER Include
    Which media to count: Video, Audio, or Both (default). Passed as
    -Include Audio (also accepts -i / --include=audio).

.EXAMPLE
    .\video_duration.ps1 "D:\Movies"

.EXAMPLE
    .\video_duration.ps1 "D:\Music" -Include Audio

.EXAMPLE
    .\video_duration.ps1 "D:\Movies; D:\Music"
#>

# NOTE: arguments are parsed manually on purpose. With a param() block PowerShell
# would bind a lone positional path to -Include and reject it, which broke
# drag & drop / double-click usage.
$rawArguments = @($args)
$Include = 'Both'
$pathInputs = @()

$ErrorActionPreference = 'Stop'
$script:Version = '2.5.0'

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$videoExtensions = @(
    '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.mpg', '.mpeg',
    '.ts', '.m2ts', '.mts', '.3gp', '.ogv', '.vob', '.divx', '.rmvb', '.asf', '.f4v', '.mxf'
)
$audioExtensions = @(
    '.mp3', '.m4a', '.m4b', '.aac', '.wav', '.flac', '.ogg', '.oga', '.opus', '.wma',
    '.aiff', '.aif', '.ape', '.wv', '.amr', '.mka', '.ac3', '.dts', '.alac'
)

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

function Format-Total {
    param([double]$Seconds)
    $mins = [math]::Round($Seconds / 60)
    $h = [math]::Floor($mins / 60)
    $m = $mins % 60
    "$h hours and $m minutes  ($(Format-Hms -Seconds $Seconds))"
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

    # --- parse arguments (-Include must never swallow a folder path) ---
    for ($i = 0; $i -lt $rawArguments.Count; $i++) {
        $arg = [string]$rawArguments[$i]
        if ($arg -match '^(?i)-{1,2}(?:include|i)$') {
            if ($i + 1 -ge $rawArguments.Count) { throw 'The -Include switch needs a value: Both, Video or Audio.' }
            $Include = [string]$rawArguments[$i + 1]
            $i++
        }
        elseif ($arg -match '^(?i)-{1,2}include=(.+)$') {
            $Include = $Matches[1]
        }
        elseif ($arg -match '^(?i)-{1,2}(?:path|p)$') {
            if ($i + 1 -lt $rawArguments.Count) { $pathInputs += [string]$rawArguments[$i + 1]; $i++ }
        }
        else {
            $pathInputs += $arg
        }
    }

    switch ($Include.ToLowerInvariant()) {
        'both'   { $Include = 'Both' }
        'all'    { $Include = 'Both' }
        'video'  { $Include = 'Video' }
        'videos' { $Include = 'Video' }
        'audio'  { $Include = 'Audio' }
        'audios' { $Include = 'Audio' }
        'music'  { $Include = 'Audio' }
        default  { throw "Invalid -Include value: '$Include'. Use Both, Video or Audio." }
    }

    Write-Host "Video & Audio Duration Calculator $script:Version" -ForegroundColor Cyan
    Write-Host "Counting: $Include" -ForegroundColor DarkGray
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
    $rawPaths = Split-Paths -Values $pathInputs
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

    # --- which kinds to count ---
    $wantedKinds = switch ($Include) {
        'Video' { @('Video') }
        'Audio' { @('Audio') }
        default { @('Video', 'Audio') }
    }

    # --- collect media files (de-duplicated) ---
    $seen = @{}
    $items = New-Object System.Collections.Generic.List[object]
    foreach ($folder in $folders) {
        Get-ChildItem -LiteralPath $folder -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
            $file = $_
            $ext = $file.Extension.ToLowerInvariant()
            $kind = $null
            if ($videoExtensions -contains $ext) { $kind = 'Video' }
            elseif ($audioExtensions -contains $ext) { $kind = 'Audio' }
            if (-not $kind) { return }
            if ($wantedKinds -notcontains $kind) { return }

            $key = $file.FullName.ToLowerInvariant()
            if (-not $seen.ContainsKey($key)) {
                $seen[$key] = $true
                $items.Add([pscustomobject]@{ File = $file; Kind = $kind })
            }
        }
    }
    if ($items.Count -eq 0) {
        throw "No matching media files were found (mode: $Include). Try -Include Both, or check the folder."
    }

    # --- read durations ---
    $totals = @{ Video = 0.0; Audio = 0.0 }
    $counts = @{ Video = @{ Found = 0; Read = 0 }; Audio = @{ Found = 0; Read = 0 } }
    $rows = New-Object System.Collections.Generic.List[object]
    $i = 0

    foreach ($item in $items) {
        $i++
        $f = $item.File
        Write-Progress -Activity "Reading durations" -Status "$i / $($items.Count) : $($item.Kind) : $($f.Name)" `
                       -PercentComplete (($i / $items.Count) * 100)

        $counts[$item.Kind].Found++

        $out = & $ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i $f.FullName 2>$null
        $sec = 0.0
        $good = $false
        if ($out) {
            $first = ($out | Select-Object -First 1)
            if ([double]::TryParse($first, [Globalization.NumberStyles]::Float,
                                   [Globalization.CultureInfo]::InvariantCulture, [ref]$sec) -and
                $sec -gt 0 -and -not [double]::IsNaN($sec) -and -not [double]::IsInfinity($sec)) {
                $totals[$item.Kind] += $sec
                $counts[$item.Kind].Read++
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
            Kind            = $item.Kind
            Path            = $f.FullName
            SizeMB          = [math]::Round($f.Length / 1MB, 2)
            DurationSeconds = $durSec
            Duration        = $durStr
            Status          = $status
        })
    }
    Write-Progress -Activity "Reading durations" -Completed

    # --- report ---
    Write-Host ""
    Write-Host "Folders scanned   : $($folders.Count)"
    foreach ($kind in $wantedKinds) {
        $c = $counts[$kind]
        if ($c.Found -gt 0) {
            Write-Host ("{0,-17} : {1} (durations read: {2})" -f "$kind files", $c.Found, $c.Read)
        }
    }

    $foundKinds = @($wantedKinds | Where-Object { $counts[$_].Found -gt 0 })
    foreach ($kind in $foundKinds) {
        Write-Host ("{0,-17}: {1}" -f "Total $($kind.ToLower())", (Format-Total -Seconds $totals[$kind])) -ForegroundColor Green
    }
    if ($foundKinds.Count -gt 1) {
        $sum = $totals['Video'] + $totals['Audio']
        Write-Host ("{0,-17}: {1}" -f 'Total combined', (Format-Total -Seconds $sum)) -ForegroundColor Green
    }
    $grandTotal = ($foundKinds | ForEach-Object { $totals[$_] } | Measure-Object -Sum).Sum
    Write-Host ("Total seconds    : {0:N1}" -f $grandTotal) -ForegroundColor DarkGray

    $failed = @($rows | Where-Object { $_.Status -ne 'OK' })
    if ($failed.Count -gt 0) {
        Write-Host ""
        Write-Host "Could not read duration for:" -ForegroundColor Yellow
        $failed | ForEach-Object { Write-Host "  [$($_.Kind)] $($_.Path)" }
    }

    # --- CSV report ---
    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $written = $false
    foreach ($dir in @((Get-ScriptFolder), $env:TEMP)) {
        $csv = Join-Path $dir "media_durations-$stamp.csv"
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
