# 🎬 Video & Audio Duration Calculator

> Add up the total runtime of every video **and** audio file in a folder — recursively — with one double-click.

A tiny, dependency-light Windows script that walks one or more folder trees, reads the duration of every video **and audio** file with **ffprobe**, and prints totals as hours, minutes and `h:mm:ss` — counted separately per type, then combined — plus a CSV report.

**English** · [فارسی](#فارسی)

![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![Shell](https://img.shields.io/badge/shell-Batch%20%2B%20PowerShell-5391FE?logo=powershell&logoColor=white)
![Media](https://img.shields.io/badge/media-video%20%2B%20audio-8A2BE2)
![Requires](https://img.shields.io/badge/requires-FFmpeg%20(ffprobe)-007808?logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

- [Why](#why)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Graphical version (Python)](#graphical-version-python)
- [Example Output](#example-output)
- [Supported Formats](#supported-formats)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [License](#license)

---

## Why

You have a folder full of movies, lectures, courses, camera clips, music albums or podcasts and you want to know **how long it all is** — without installing a media player, opening every file, or trusting file-size guesses. This script does exactly that, offline, with no telemetry and no third-party packages.

## Features

- 🔁 **Recursive scan** — descends into every subfolder automatically.
- 🎵 **Audio included** — MP3, FLAC, WAV, M4A and more, counted with the same accuracy as video.
- 🎯 **Accurate durations** — reads real container/stream metadata via `ffprobe`, not file size or bitrate estimates.
- 📁 **Multiple folders at once** — type `D:\Movies; E:\Music` and both are scanned (or drag a folder onto the `.bat`).
- 🎛 **Pick what to count** — `-Include Both` (default), `Video`, or `Audio`.
- 📊 **Separate + combined totals** — video time, audio time, and the grand total, each as *“X hours and Y minutes”* with exact `h:mm:ss`.
- 🧾 **CSV report** — writes a timestamped `media_durations-*.csv` with one row per file (`Kind`, path, size, seconds, `h:mm:ss`, status), importable into Excel.
- 🧹 **No double counting** — folders that overlap (e.g. a parent and its child) are de-duplicated.
- 🧾 **Full report** — shows how many files were found per type and how many durations were read successfully.
- ⚠️ **Graceful errors** — lists every file whose duration could not be read instead of failing silently.
- 🖥 **Graphical version (v2.0)** — `video_duration_gui.py` does the same scan in a clean PySide6 window with drag & drop, a Persian/English switch and right-to-left layout; the console version stays available.
- 🪶 **Zero install footprint** — the console version is a launcher plus a script; nothing to compile, no Python, no Node.js. (The optional GUI needs Python 3 + PySide6, installed automatically on first launch.)
- 🌍 **Unicode-safe** — UTF-8 console output, so non-English paths work.

## Requirements

| Requirement | Notes |
|---|---|
| **Windows 10 / 11** | Uses `cmd.exe` + Windows PowerShell 5.1 (built in). |
| **FFmpeg (`ffprobe`)** | The only real dependency. Install it and make sure `ffprobe` is on `PATH`. |
| **Python 3.9+** *(GUI only)* | Only for `video_duration_gui.py`; the launcher installs PySide6 the first time. |

### Installing FFmpeg on Windows

Pick one:

```powershell
# Option 1 — WinGet (recommended)
winget install Gyan.FFmpeg

# Option 2 — Chocolatey
choco install ffmpeg

# Option 3 — Scoop
scoop install ffmpeg
```

Or download a build from <https://ffmpeg.org/download.html>, extract it, and add its `bin` folder to your `PATH`.

Verify:

```powershell
ffprobe -version
```

> If `ffprobe` is **not** on `PATH`, the script asks you for the full path to `ffprobe.exe` — no need to edit anything.

## Installation

1. Download **both** files from the [latest release](https://github.com/babak12124/video-duration-calculator/releases/latest) (or clone the repo):
   - [`video_duration.bat`](video_duration.bat) — the launcher you double-click
   - [`video_duration.ps1`](video_duration.ps1) — the actual logic
2. Put them in the **same folder** — Desktop, `D:\Tools`, a network share.
3. That's it. No installer, no admin rights required.

```powershell
git clone https://github.com/babak12124/video-duration-calculator.git
```

> ℹ️ Files downloaded from the internet carry a "mark of the web" that some antivirus tools treat suspiciously. If Windows blocks the script, right-click the file **→ Properties → Unblock**, or run `Unblock-File .\video_duration.*`. Nothing is hidden: both files are plain text you can read.

## Usage

**Option A — double-click**

1. Double-click `video_duration.bat`.
2. Enter one or more **folder paths**, e.g. `D:\Movies` or `"C:\Users\Me\Videos\Course"`, or several at once: `D:\Movies; E:\Music`.
   - Quotes are fine and get stripped automatically.
   - Separate multiple paths with a **semicolon** `;`.
   - Every folder is scanned **recursively**, and duplicate files are counted once.
3. Wait for the progress bar (`Reading durations 42 / 180`) to finish.
4. Read the totals from the green lines.

By default **both** video and audio are counted and shown separately. To narrow it down, pass `-Include`:

```powershell
.\video_duration.bat "D:\Music" -Include Audio     # podcasts / albums only
.\video_duration.bat "D:\Movies" -Include Video    # video only (old behaviour)
.\video_duration.bat "D:\Media" -Include Both      # default
```

**Option B — drag & drop**

Drag a folder from Explorer onto `video_duration.bat`. It starts immediately with that folder — no typing.

**Option C — from a terminal**

```powershell
.\video_duration.bat "D:\Movies; D:\Music"
```

The window stays open until you press a key, so the result never disappears. Every run also drops a CSV report next to the script (or in `%TEMP%` if that folder is read-only).

## Graphical version (Python)

`video_duration_gui.py` is the same tool with a window — same recursive scan, same `ffprobe` readings, same CSV — built with PySide6 (Qt 6). **Version 2.0.**

**Requirements:** Python 3.9+ and PySide6. Nothing to install by hand: `video_duration_gui.bat` installs PySide6 the first time it runs.

1. Double-click `video_duration_gui.bat` — no console window appears.
2. Press **Add folder…**, or drag folders straight onto the window. Then pick **Video + audio**, **Video only** or **Audio only**.
3. Press **Calculate total**. Durations are read in the background, so the window never freezes; **Cancel** stops at any time.
4. Totals show up per type and combined, every file is listed in the table (unreadable ones in red), and the CSV is written next to the script.

Notes:

- The **فارسی / English** button switches the whole interface — right-to-left layout included — and remembers your choice.
- FFmpeg is found automatically. Only if it is missing does the app show a short one-time message with the install command and an optional file picker; no technical setting sits on screen.
- You can also run `python video_duration_gui.py "D:\Movies"`.
- Settings (last folders, language, `ffprobe` path) are stored in `%APPDATA%\video-duration-calculator\settings.json`.
- The `.bat` + PowerShell version is unchanged and still works — the GUI is an alternative, not a replacement.

## Example Output

```text
Video & Audio Duration Calculator 1.2.0
Counting: Both

Folders scanned   : 2
Video files       : 180 (durations read: 179)
Audio files       : 42 (durations read: 42)
Total video      : 96 hours and 12 minutes  (96:12:04)
Total audio      : 3 hours and 5 minutes  (3:05:12)
Total combined   : 99 hours and 17 minutes  (99:17:16)
Total seconds    : 357316.6

Could not read duration for:
  [Video] D:\Movies\clips\corrupted_clip.avi

CSV written to    : D:\Tools\media_durations-20260114-210355.csv
```

- **Video/Audio files** — every file with a supported extension, across all folders and subfolders.
- **durations read** — how many of those `ffprobe` could actually parse.
- **Total video / audio / combined** — sums rounded to the nearest minute, with exact `h:mm:ss` in parentheses.
- **CSV** — the same data per file: `Kind, Path, SizeMB, DurationSeconds, Duration, Status`.

## Supported Formats

**Video** — `.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.m2ts` · `.mts` · `.3gp` · `.ogv` · `.vob` · `.divx` · `.rmvb` · `.asf` · `.f4v` · `.mxf`

**Audio** — `.mp3` · `.m4a` · `.m4b` · `.aac` · `.wav` · `.flac` · `.ogg` · `.oga` · `.opus` · `.wma` · `.aiff` · `.aif` · `.ape` · `.wv` · `.amr` · `.mka` · `.ac3` · `.dts` · `.alac`

Matching is case-insensitive (`Song.MP3` counts) and based on the file extension. `ffprobe` can read many more containers — add an extension to `$videoExtensions` or `$audioExtensions` at the top of [`video_duration.ps1`](video_duration.ps1).

## How It Works

The launcher is deliberately boring: `video_duration.bat` starts `video_duration.ps1` with `-NoProfile -ExecutionPolicy Bypass`, passes along any arguments (that's how drag & drop and `-Include` work), shows a readable error if the exit code is non-zero, and **always** waits for a keypress so the window can never vanish. The PowerShell script then:

1. Locates `ffprobe` on `PATH` (or in the usual WinGet/FFmpeg folders, or asks for its path).
2. Resolves the folder arguments, skipping invalid ones with a warning.
3. Recursively enumerates every chosen folder, classifies each file as **Video** or **Audio** by extension, filters by `-Include`, and de-duplicates files that appear in overlapping paths.
4. For each file, runs:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
5. Parses the duration using **invariant culture** (so `1.5` is never misread as `15` on regional settings), ignoring zero/negative/NaN/infinite values.
6. Adds the seconds to the matching bucket (video or audio), then prints per-type and combined totals and writes the per-file CSV with a `Kind` column.

Errors are caught, printed in red, and appended to `video_duration-error.log` next to the script, so a failed run always leaves a breadcrumb instead of closing silently.

Everything is local. No network access, no data collection.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ffprobe was not found in PATH.` | Install FFmpeg (see above), or paste the full path to `ffprobe.exe` when asked. |
| `video_duration.ps1 was not found next to this file.` | The two files were separated. Keep `video_duration.bat` and `video_duration.ps1` in the same folder. |
| `None of the given folders exist.` | Check the path. Use quotes for paths with spaces; separate several paths with `;`. |
| `No matching media files were found (mode: Both).` | Confirm the folder contains supported extensions, or try `-Include Both`; the scan is recursive, so subfolders are included. |
| Some files listed as unreadable | The file is corrupt, still being downloaded, or uses an exotic codec/container. `ffprobe` prints the reason with `-v error`. |
| Total looks wrong | Rounded to the nearest minute by design; the exact `h:mm:ss` is printed next to it. Regional settings cannot break parsing — invariant culture is used. |
| Antivirus or SmartScreen blocked it | Right-click the files → **Properties → Unblock**, or run `Unblock-File .\video_duration.*`. Both files are plain text; nothing is obfuscated. |
| Window still closes instantly | Almost always the browser/antivirus killing the process. Run it from a terminal (`cmd` → drag the `.bat` in → Enter) and check `video_duration-error.log` next to the script; open an [issue](https://github.com/babak12124/video-duration-calculator/issues) with that log. |

## FAQ

**Does it modify or move my files?**
No. It only reads metadata. Nothing is written, renamed, or deleted.

**Does it need internet?**
No, never.

**Can it work on macOS/Linux?**
The `.bat` wrapper is Windows-only. The underlying idea is one `ffprobe` call per file; a Bash equivalent is a few lines. PRs welcome.

**Can it export the result to a file?**
Yes. Each run writes `media_durations-<timestamp>.csv` next to the script (falls back to `%TEMP%` if the folder is read-only). Open it in Excel or any spreadsheet.

**Does it count music and podcasts too?**
Yes — since v1.2.0 audio files are counted and reported separately from video. Use `-Include Audio` if you only want the music/podcast total.

**Why is the total rounded to minutes?**
Because that's how humans quote viewing time (“96 hours, 12 minutes”). The exact `h:mm:ss` and total seconds are printed right below it.

## Changelog

### v1.2.0 — audio support

- **Audio files are counted too**: MP3, M4A/M4B, AAC, WAV, FLAC, OGG/OPUS, WMA, AIFF, APE, WV, AMR, MKA, AC3, DTS, ALAC.
- New `-Include` switch: `Both` (default), `Video`, or `Audio`.
- Console now reports **video, audio and combined** totals separately.
- CSV renamed to `media_durations-*.csv` and gained a **`Kind`** column (`Video`/`Audio`).
- Expanded video extensions: `.m2ts`, `.mts`, `.ogv`, `.vob`, `.divx`, `.rmvb`, `.asf`, `.f4v`, `.mxf`.
- `video_duration.bat "D:\Music" -Include Audio` works, so drag & drop and terminal usage stay in sync.
- Arguments are parsed manually, so a lone folder path is never mistaken for `-Include` (a regression the tests caught before release).

### v1.1.0 — bug fix

- **Fixed:** on some machines the window opened and closed instantly. The old `.bat` re-launched itself and executed an embedded PowerShell payload via `Invoke-Expression` — a pattern antivirus heuristics often kill silently. It is now a plain launcher + a readable `.ps1`.
- The window now **always** waits for a keypress, and failures print a red message plus a `video_duration-error.log`.
- Missing `video_duration.ps1`, invalid paths, and empty input are reported instead of failing quietly.
- `h:mm:ss` no longer wraps at 24 hours (a 30-hour total shows `30:15:22`, not `06:15:22`).
- Folder prompts retry up to 3 times; `ffprobe` is also auto-detected in the WinGet/FFmpeg install folders.

### v1.0.0 — first release

- Recursive duration total, multi-folder scan, drag & drop, CSV report, bilingual docs.

## Contributing

Issues and pull requests are welcome. Ideas that would fit well:

- Multi-drive scan in parallel (faster on slow HDDs)
- Optional `hours:minutes:seconds`-only output mode
- A PowerShell module version
- Bash / macOS port
- Grafana/JSON report output

Please keep changes small, readable, and dependency-free.

## License

[MIT](LICENSE) © babak12124

---

<h1 id="فارسی">📖 راهنمای فارسی</h1>

# 🎬 محاسبه‌گر مدت‌زمان ویدیو و صدا

> با یک دابل‌کلیک، مجموع زمان همهٔ ویدیوها **و فایل‌های صوتی** یک پوشه را — همراه با تمام زیرپوشه‌ها — حساب کن.

یک اسکریپت کوچک ویندوزی که یک یا چند درخت پوشه را پیمایش می‌کند، مدت‌زمان هر فایل ویدیویی **و صوتی** را با **ffprobe** می‌خواند و مجموع را به ساعت، دقیقه و `h:mm:ss` — جدا برای هر نوع و سپس ترکیبی، به‌همراه یک گزارش CSV — چاپ می‌کند.

## فهرست

- [چرا](#چرا)
- [امکانات](#امکانات)
- [پیش‌نیازها](#پیشنیازها)
- [نصب](#نصب)
- [نحوهٔ استفاده](#نحوهٔ-استفاده)
- [نسخهٔ گرافیکی (پایتون)](#نسخهٔ-گرافیکی-پایتون)
- [نمونهٔ خروجی](#نمونهٔ-خروجی)
- [فرمت‌های پشتیبانی‌شده](#فرمتهای-پشتیبانی-شده)
- [نحوهٔ کار](#نحوهٔ-کار)
- [رفع مشکل](#رفع-مشکل)
- [سؤالات متداول](#سؤالات-متداول)
- [تغییرات نسخه‌ها](#تغییرات-نسخهها)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)

## چرا

پوشه‌ای پر از فیلم، درس، دورهٔ آموزشی، کلیپ دوربین، آلبوم موسیقی یا پادکست دارید و می‌خواهید بدانید **در کل چقدر زمان می‌برد**. این اسکریپت بدون نصب پخش‌کننده، بدون باز کردن تک‌تک فایل‌ها و بدون حدس زدن از روی حجم فایل، دقیقاً همین را به‌صورت آفلاین حساب می‌کند. هیچ داده‌ای هم جایی فرستاده نمی‌شود.

## امکانات

- 🔁 **پیمایش بازگشتی** — همهٔ زیرپوشه‌ها خودکار بررسی می‌شوند.
- 🎵 **پشتیبانی از صدا** — MP3، FLAC، WAV، M4A و بیشتر، با همان دقت ویدیو.
- 🎯 **مدت‌زمان دقیق** — متادیتای واقعی فایل با `ffprobe` خوانده می‌شود، نه تخمین از روی حجم یا بیت‌ریت.
- 📁 **چند پوشه هم‌زمان** — بنویسید `D:\Movies; E:\Music` تا هر دو اسکن شوند (یا پوشه را روی فایل `.bat` بکشید و رها کنید).
- 🎛 **انتخاب نوع شمارش** — `-Include Both` (پیش‌فرض)، `Video` یا `Audio`.
- 📊 **جمع جداگانه + ترکیبی** — زمان ویدیو، زمان صدا و مجموع کل، هرکدام به شکل «X ساعت و Y دقیقه» با `h:mm:ss` دقیق.
- 🧾 **گزارش CSV** — هر اجرا یک فایل `media_durations-*.csv` با تاریخ‌وساعت می‌سازد؛ یک ردیف برای هر فایل (`Kind`، مسیر، حجم، ثانیه، `hh:mm:ss`، وضعیت) که در اکسل قابل بازکردن است.
- 🧹 **بدون شمارش تکراری** — اگر پوشه‌ها هم‌پوشانی داشته باشند (مثلاً پوشه و زیرپوشه‌اش)، فایل تکراری دوبار حساب نمی‌شود.
- 🧾 **گزارش کامل** — تعداد فایل‌های پیداشده به تفکیک نوع و تعداد مدت‌های خوانده‌شده نمایش داده می‌شود.
- ⚠️ **مدیریت خطا** — فایل‌هایی که مدتشان خوانده نشود، فهرست می‌شوند؛ هیچ خطایی بی‌صدا رد نمی‌شود.
- 🖥 **نسخهٔ گرافیکی (نسخهٔ ۲٫۰)** — `video_duration_gui.py` همان کار را در یک پنجرهٔ تمیز PySide6 با کشیدن‌و‌رهاکردن پوشه، سوییچ فارسی/انگلیسی و چیدمان راست‌به‌چپ انجام می‌دهد؛ نسخهٔ کنسولی هم سر جایش است.
- 🪶 **بدون نصب** — نسخهٔ کنسولی یک لانچر + یک اسکریپت است؛ نه کامپایل، نه پایتون، نه Node.js. (نسخهٔ گرافیکی اختیاری به پایتون ۳ + PySide6 نیاز دارد که بار اول خودکار نصب می‌شود.)
- 🌍 **سازگار با یونیکد** — خروجی کنسول UTF-8 است تا مسیرهای فارسی/غیرانگلیسی درست نمایش داده شوند.

## پیش‌نیازها

| نیاز | توضیح |
|---|---|
| **ویندوز ۱۰ یا ۱۱** | از `cmd.exe` و Windows PowerShell 5.1 (از پیش نصب‌شده) استفاده می‌کند. |
| **FFmpeg (`ffprobe`)** | تنها وابستگی واقعی. نصبش کنید و مطمئن شوید `ffprobe` روی `PATH` است. |
| **پایتون ۳٫۹+** *(فقط نسخهٔ گرافیکی)* | فقط برای `video_duration_gui.py`؛ لانچر بار اول PySide6 را نصب می‌کند. |

### نصب FFmpeg در ویندوز

یکی را انتخاب کنید:

```powershell
# روش ۱ — WinGet (پیشنهادی)
winget install Gyan.FFmpeg

# روش ۲ — Chocolatey
choco install ffmpeg

# روش ۳ — Scoop
scoop install ffmpeg
```

یا از <https://ffmpeg.org/download.html> یک نسخه دانلود، از حالت فشرده خارج و پوشهٔ `bin` آن را به `PATH` اضافه کنید.

بررسی نصب:

```powershell
ffprobe -version
```

> اگر `ffprobe` روی `PATH` نباشد، اسکریپت مسیر کامل `ffprobe.exe` را از شما می‌پرسد؛ لازم نیست چیزی را دستی ویرایش کنید.

## نصب

1. **هر دو فایل** را از [آخرین Release](https://github.com/babak12124/video-duration-calculator/releases/latest) دانلود کنید (یا ریپو را clone کنید):
   - [`video_duration.bat`](video_duration.bat) — فایلی که رویش دابل‌کلیک می‌کنید
   - [`video_duration.ps1`](video_duration.ps1) — منطق اصلی برنامه
2. هر دو را در **یک پوشه** بگذارید — دسکتاپ، `D:\Tools`، یا یک درایو شبکه.
3. تمام. نصب‌کننده و دسترسی ادمین لازم نیست.

```powershell
git clone https://github.com/babak12124/video-duration-calculator.git
```

> ℹ️ فایل‌های دانلودشده از اینترنت یک نشانهٔ «mark of the web» دارند که برخی آنتی‌ویروس‌ها به آن حساس‌اند. اگر ویندوز اجرا را بلاک کرد، روی فایل راست‌کلیک کنید → **Properties → Unblock**، یا `Unblock-File .\video_duration.*` را اجرا کنید. هیچ چیز پنهانی وجود ندارد: هر دو فایل متن ساده و قابل خواندن‌اند.

## نحوهٔ استفاده

**روش الف — دابل‌کلیک**

1. روی `video_duration.bat` دابل‌کلیک کنید.
2. یک یا چند **مسیر پوشه** وارد کنید، مثلاً `D:\Movies` یا `"C:\Users\Me\Videos\Course"` یا چندتایی با هم: `D:\Movies; E:\Music`.
   - گذاشتن گیومه اشکالی ندارد و خودکار حذف می‌شود.
   - مسیرهای متعدد را با **سمی‌کالن** `;` جدا کنید.
   - همهٔ پوشه‌ها **به‌صورت بازگشتی** اسکن می‌شوند و فایل‌های تکراری یک‌بار حساب می‌شوند.
3. تا تمام شدن نوار پیشرفت (`Reading durations 42 / 180`) صبر کنید.
4. مجموع‌ها را از خطوط سبز بخوانید.

به‌صورت پیش‌فرض **هم ویدیو و هم صدا** شمارش می‌شوند و جدا نمایش داده می‌شوند. برای محدود کردن، از `-Include` استفاده کنید:

```powershell
.\video_duration.bat "D:\Music" -Include Audio     # فقط موسیقی/پادکست
.\video_duration.bat "D:\Movies" -Include Video    # فقط ویدیو (رفتار قبلی)
.\video_duration.bat "D:\Media" -Include Both      # پیش‌فرض
```

**روش ب — کشیدن و رها کردن**

پوشه را از Explorer روی `video_duration.bat` بکشید. بدون هیچ تایپی، همان پوشه اسکن می‌شود.

**روش ج — از ترمینال**

```powershell
.\video_duration.bat "D:\Movies; D:\Music"
```

پنجره تا فشردن یک کلید باز می‌ماند، پس نتیجه از دست نمی‌رود. هر اجرا یک گزارش CSV هم کنار اسکریپت می‌سازد (اگر آن پوشه فقط-خواندنی باشد، در `%TEMP%`).

## نسخهٔ گرافیکی (پایتون)

`video_duration_gui.py` همان ابزار با یک پنجره است — همان اسکن بازگشتی، همان خواندن با `ffprobe`، همان CSV — این بار با PySide6 (Qt 6). **نسخهٔ ۲٫۰.**

**پیش‌نیاز:** پایتون ۳٫۹ یا بالاتر و PySide6. لازم نیست دستی چیزی نصب کنید: فایل `video_duration_gui.bat` بار اول خودش PySide6 را نصب می‌کند.

1. روی `video_duration_gui.bat` دابل‌کلیک کنید — پنجرهٔ کنسول باز نمی‌شود.
2. **افزودن پوشه…** را بزنید، یا پوشه‌ها را مستقیم روی پنجره رها کنید. بعد **ویدیو + صدا**، **فقط ویدیو** یا **فقط صدا** را انتخاب کنید.
3. **محاسبهٔ مجموع** را بزنید. مدت‌ها در پس‌زمینه خوانده می‌شوند، پس پنجره فریز نمی‌شود؛ **لغو** هر لحظه کار را متوقف می‌کند.
4. مجموع‌ها جدا و ترکیبی نمایش داده می‌شوند، همهٔ فایل‌ها در جدول می‌آیند (فایل‌های ناخوانا قرمز) و CSV کنار اسکریپت نوشته می‌شود.

نکته‌ها:

- دکمهٔ **فارسی / English** کل رابط را عوض می‌کند — همراه با چیدمان راست‌به‌چپ — و انتخاب شما را یادش می‌ماند.
- FFmpeg خودکار پیدا می‌شود. فقط اگر نصب نباشد، برنامه یک پیام کوتاه یک‌باره با دستور نصب و امکان انتخاب فایل نشان می‌دهد؛ در حالت عادی هیچ تنظیم فنی روی صفحه نیست.
- می‌توانید `python video_duration_gui.py "D:\Movies"` را هم اجرا کنید.
- تنظیمات (آخرین پوشه‌ها، زبان، مسیر `ffprobe`) در `%APPDATA%\video-duration-calculator\settings.json` ذخیره می‌شود.
- نسخهٔ `.bat` + PowerShell دست‌نخورده و سالم است — رابط گرافیکی جایگزین نیست، گزینهٔ اضافه است.

## نمونهٔ خروجی

```text
Video & Audio Duration Calculator 1.2.0
Counting: Both

Folders scanned   : 2
Video files       : 180 (durations read: 179)
Audio files       : 42 (durations read: 42)
Total video      : 96 hours and 12 minutes  (96:12:04)
Total audio      : 3 hours and 5 minutes  (3:05:12)
Total combined   : 99 hours and 17 minutes  (99:17:16)
Total seconds    : 357316.6

Could not read duration for:
  [Video] D:\Movies\clips\corrupted_clip.avi

CSV written to    : D:\Tools\media_durations-20260114-210355.csv
```

- **Video/Audio files** — همهٔ فایل‌های با پسوند پشتیبانی‌شده در تمام پوشه‌ها و زیرپوشه‌ها.
- **durations read** — چند فایل را `ffprobe` واقعاً توانسته بخواند.
- **Total video / audio / combined** — مجموع‌ها، گردشده به نزدیک‌ترین دقیقه، با `h:mm:ss` دقیق در پرانتز.
- **CSV** — همان داده‌ها به تفکیک فایل: `Kind, Path, SizeMB, DurationSeconds, Duration, Status`.

## فرمت‌های پشتیبانی‌شده

**ویدیو** — `.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.m2ts` · `.mts` · `.3gp` · `.ogv` · `.vob` · `.divx` · `.rmvb` · `.asf` · `.f4v` · `.mxf`

**صدا** — `.mp3` · `.m4a` · `.m4b` · `.aac` · `.wav` · `.flac` · `.ogg` · `.oga` · `.opus` · `.wma` · `.aiff` · `.aif` · `.ape` · `.wv` · `.amr` · `.mka` · `.ac3` · `.dts` · `.alac`

تطبیق پسوند به بزرگی/کوچکی حروف حساس نیست (`Song.MP3` هم حساب می‌شود) و بر اساس پسوند فایل است. `ffprobe` کانتینرهای بیشتری را می‌شناسد؛ برای افزودن فرمت جدید، پسوند را به آرایهٔ `$videoExtensions` یا `$audioExtensions` در ابتدای [`video_duration.ps1`](video_duration.ps1) اضافه کنید.

## نحوهٔ کار

لانچر عمداً ساده است: `video_duration.bat` فایل `video_duration.ps1` را با `-NoProfile -ExecutionPolicy Bypass` اجرا می‌کند، آرگومان‌ها را پاس می‌دهد (به همین دلیل Drag & Drop و `-Include` کار می‌کنند)، در صورت خطا پیام خوانا نشان می‌دهد و **همیشه** منتظر فشردن یک کلید می‌ماند تا پنجره هرگز ناگهان بسته نشود. سپس اسکریپت PowerShell:

1. `ffprobe` را روی `PATH` پیدا می‌کند (یا در پوشه‌های معمول WinGet/FFmpeg، یا مسیرش را می‌پرسد).
2. مسیرهای ورودی را اعتبارسنجی می‌کند و مسیرهای نامعتبر را با هشدار رد می‌کند.
3. همهٔ پوشه‌های انتخابی را به‌صورت بازگشتی می‌گردد، هر فایل را بر اساس پسوند به **ویدیو** یا **صدا** دسته‌بندی می‌کند، با `-Include` فیلتر می‌کند و فایل‌های تکراری در مسیرهای هم‌پوشان را یک‌بار حساب می‌کند.
4. برای هر فایل این دستور را اجرا می‌کند:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
5. مدت‌زمان را با **invariant culture** تجزیه می‌کند (تا در تنظیمات منطقه‌ای، `1.5` اشتباهاً `15` خوانده نشود) و مقادیر صفر/منفی/NaN/بی‌نهایت را نادیده می‌گیرد.
6. ثانیه‌ها را به سبد مربوطه (ویدیو یا صدا) اضافه می‌کند، جمع‌های جداگانه و ترکیبی را چاپ می‌کند و فایل CSV را با ستون `Kind` می‌نویسد.

خطاها گرفته می‌شوند، با رنگ قرمز چاپ می‌شوند و در فایل `video_duration-error.log` کنار اسکریپت ثبت می‌شوند؛ بنابراین یک اجرای ناموفق هم ردپا باقی می‌گذارد و بی‌صدا بسته نمی‌شود.

همه‌چیز محلی است. بدون دسترسی به شبکه و بدون جمع‌آوری داده.

## رفع مشکل

| مشکل | راه‌حل |
|---|---|
| `ffprobe was not found in PATH.` | FFmpeg را نصب کنید (بالا) یا وقتی پرسید، مسیر کامل `ffprobe.exe` را بدهید. |
| `video_duration.ps1 was not found next to this file.` | دو فایل از هم جدا شده‌اند. `video_duration.bat` و `video_duration.ps1` باید در یک پوشه باشند. |
| `None of the given folders exist.` | مسیر را بررسی کنید؛ برای مسیرهای دارای فاصله از گیومه استفاده کنید و چند مسیر را با `;` جدا کنید. |
| `No matching media files were found (mode: Both).` | مطمئن شوید پوشه پسوندهای پشتیبانی‌شده دارد، یا `-Include Both` را امتحان کنید؛ اسکن بازگشتی است، پس زیرپوشه‌ها هم شامل می‌شوند. |
| چند فایل به‌عنوان ناخوانا فهرست شدند | فایل خراب است، هنوز در حال دانلود است، یا کدک/کانتینر غیرمعمولی دارد. `ffprobe` با `-v error` دلیل را چاپ می‌کند. |
| مجموع به‌نظر اشتباه است | به‌صورت عمدی به دقیقه گرد می‌شود؛ مقدار دقیق `h:mm:ss` کنارش چاپ می‌شود. تنظیمات منطقه‌ای هم نمی‌تواند تجزیه را خراب کند. |
| آنتی‌ویروس یا SmartScreen بلاک کرد | روی فایل‌ها راست‌کلیک → **Properties → Unblock**، یا `Unblock-File .\video_duration.*` را اجرا کنید. هر دو فایل متن ساده‌اند و هیچ چیز مبهمی ندارند. |
| پنجره همچنان فوراً بسته می‌شود | تقریباً همیشه کار مرورگر/آنتی‌ویروس است که پروسه را می‌کشد. از ترمینال اجرا کنید (`cmd` → فایل `.bat` را داخلش بکشید → Enter) و فایل `video_duration-error.log` کنار اسکریپت را ببینید؛ همان را در یک [Issue](https://github.com/babak12124/video-duration-calculator/issues) بفرستید. |

## سؤالات متداول

**آیا فایل‌هایم تغییر می‌کنند یا جابه‌جا می‌شوند؟**
نه. فقط متادیتا خوانده می‌شود. هیچ چیزی نوشته، تغییرنام یا حذف نمی‌شود.

**به اینترنت نیاز دارد؟**
هرگز نه.

**روی مک یا لینوکس کار می‌کند؟**
پوستهٔ `.bat` فقط برای ویندوز است. ایدهٔ اصلی یک فراخوانی `ffprobe` برای هر فایل است؛ معادل Bash چند خط بیشتر نیست. Pull Request پذیرفته می‌شود.

**می‌شود خروجی را در فایل ذخیره کرد؟**
بله. هر اجرا فایل `media_durations-<timestamp>.csv` را کنار اسکریپت می‌سازد (اگر پوشه فقط-خواندنی باشد، در `%TEMP%`). در اکسل یا هر برنامهٔ صفحه‌گسترده‌ای قابل بازکردن است.

**موسیقی و پادکست هم حساب می‌شود؟**
بله — از نسخهٔ v1.2.0 فایل‌های صوتی هم شمارش و جدا از ویدیو گزارش می‌شوند. اگر فقط جمع موسیقی/پادکست را می‌خواهید، از `-Include Audio` استفاده کنید.

**چرا جمع به دقیقه گرد می‌شود؟**
چون ما زمان تماشا را معمولاً به ساعت و دقیقه می‌گوییم («۹۶ ساعت و ۱۲ دقیقه»). مقدار دقیق `h:mm:ss` و ثانیهٔ خام هم بلافاصله زیرش چاپ می‌شود.

## تغییرات نسخه‌ها

### v2.5.1 — رفع ساخت لینوکس و انتشار دوباره

- **ساخت لینوکس درست شد** — بستهٔ ناموجود `libxcb-xinerama1` (نام درست: `libxcb-xinerama0`) باعث می‌شد `apt-get` با کد ۱۰۰ بیلد را متوقف کند؛ حالا نصب کتابخانه‌ها ابتدا بسته‌های موجود در ایمیج را تشخیص می‌دهد و بقیه را با هشدار رد می‌کند
- **قفل‌شدن روی `ubuntu-24.04`** — `ubuntu-latest` به ۲۶.۰۴ منتقل شده بود؛ باینری ساخته‌شده روی ۲۶.۰۴ روی اوبونتو ۲۴.۰۴ اجرا نمی‌شد (نسخهٔ glibc). با قفل‌شدن روی ۲۴.۰۴ باینری روی ۲۴.۰۴ و جدیدتر کار می‌کند
- **بررسی باینری پیش از آپلود** — وجود و نوع فایل ELF قبل از ساخت ریلیز چک می‌شود
- **پیش‌نیاز اجرای نسخهٔ لینوکس** — `ffmpeg` و `libxcb-cursor0` (مثلاً `sudo apt install ffmpeg libxcb-cursor0`)

### v2.5.0 — پشتیبانی از ساختار متقابل‌پلتفرم و رفع باگ‌های ساخت

- **ساخت پیکربندی متقابل‌پلتفرم** — اکنون نسخه‌ی **ویندوز، لینوکس و مک** با یک workflow واحد GitHub Actions تولید و توزیع می‌شود
- **به‌روزرسانی نسخه‌ی ۲.۵.۰** — فایل‌های `video_duration.ps1` و `video_duration_gui.py` هم‌اکنون به نسخه ۲.۵.۰ آپدیت شده‌اند
- **رفع باگ ساخت لینوکس** — نام بستهٔ ناموجود `libxcb-xinerama1` به `libxcb-xinerama0` اصلاح شد، بیلد روی `ubuntu-24.04` قفل شد و نصب کتابخانه‌ها اکنون فقط بسته‌های موجود در ایمیج را نصب می‌کند؛ بنابراین تغییر نام یا حذف یک بسته در نسخه‌های بعدی اوبونتو دیگر کل بیلد را نمی‌شکند
- **رفع باگ ساخت مک** — `brew install python@3.12` به‌جای `python@3.11` که قبلاً به اتمام رسید (EOL) است
- **سامانه‌پشتیبانی PyInstaller ۶.x** — افزودن فلگ `--clean` برای بوتن‌های تکرارپذیر
- **توصیف خودکار ffprobe** — لانچر حالا مسیرهای نصب رایج ffprobe رو جستجو می‌کنه و یک پیام یک‌باره واضح در صورت عدم یافتن بوتن می‌ده


### v1.2.0 — پشتیبانی از فایل‌های صوتی

- **فایل‌های صوتی هم شمارش می‌شوند**: MP3، M4A/M4B، AAC، WAV، FLAC، OGG/OPUS، WMA، AIFF، APE، WV، AMR، MKA، AC3، DTS، ALAC.
- سوییچ جدید `-Include` با مقادیر `Both` (پیش‌فرض)، `Video` و `Audio`.
- کنسول حالا جمع **ویدیو، صدا و ترکیبی** را جدا نشان می‌دهد.
- نام فایل CSV به `media_durations-*.csv` تغییر کرد و ستون **`Kind`** (`Video`/`Audio`) اضافه شد.
- پسوندهای ویدیویی بیشتر: `.m2ts`، `.mts`، `.ogv`، `.vob`، `.divx`، `.rmvb`، `.asf`، `.f4v`، `.mxf`.
- دستور `video_duration.bat "D:\Music" -Include Audio` کار می‌کند؛ Drag & Drop و استفاده از ترمینال همگام ماندند.
- آرگومان‌ها دستی تجزیه می‌شوند تا یک مسیر تنها هرگز به‌اشتباه `-Include` تفسیر نشود (باگ شناسایی‌شده در تست، پیش از انتشار).

### v1.1.0 — رفع باگ

- **رفع مشکل:** روی بعضی سیستم‌ها پنجره باز و سریع بسته می‌شد. فایل `.bat` قبلی خودش را دوباره اجرا می‌کرد و یک بدنهٔ PowerShell جاسازی‌شده را با `Invoke-Expression` اجرا می‌کرد — الگویی که ضدویروس‌ها معمولاً بی‌صدا می‌کشند. حالا فقط یک لانچر ساده + یک فایل `.ps1` خوانا است.
- پنجره حالا **همیشه** منتظر فشردن کلید می‌ماند و خطاها با پیام قرمز و فایل `video_duration-error.log` گزارش می‌شوند.
- نبودِ `video_duration.ps1`، مسیر نامعتبر و ورودی خالی، به‌جای شکست بی‌صدا گزارش می‌شوند.
- `h:mm:ss` دیگر بعد از ۲۴ ساعت صفر نمی‌شود (۳۰ ساعت به‌صورت `30:15:22` نمایش داده می‌شود، نه `06:15:22`).
- پرسش مسیر تا ۳ بار تکرار می‌شود؛ `ffprobe` در پوشه‌های نصب WinGet/FFmpeg هم خودکار پیدا می‌شود.

### v1.0.0 — اولین انتشار

- محاسبهٔ بازگشتی مجموع، چند پوشه، Drag & Drop، گزارش CSV و مستندات دوزبانه.

## مشارکت

Issue و Pull Request خوش‌آمد است. ایده‌هایی که خوب جفت می‌شوند:

- اسکن موازی چند درایو (سریع‌تر روی هاردهای کند)
- حالت خروجی فقط `hours:minutes:seconds`
- نسخهٔ PowerShell Module
- پورت Bash / macOS
- خروجی JSON برای داشبورد

لطفاً تغییرات را کوچک، خوانا و بدون وابستگی نگه دارید.

## مجوز

[MIT](LICENSE) © babak12124
