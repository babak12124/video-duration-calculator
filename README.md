# 🎬 Video Duration Calculator

> Add up the total runtime of every video in a folder — recursively — in seconds, with one double-click.

A tiny, dependency-light Windows script that walks one or more folder trees, reads the duration of every video file with **ffprobe**, and prints the total runtime as hours, minutes and `h:mm:ss` — plus a CSV report.

**English** · [فارسی](#فارسی)

![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows&logoColor=white)
![Shell](https://img.shields.io/badge/shell-Batch%20%2B%20PowerShell-5391FE?logo=powershell&logoColor=white)
![Requires](https://img.shields.io/badge/requires-FFmpeg%20(ffprobe)-007808?logo=ffmpeg&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Table of Contents

- [Why](#why)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
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

You have a folder full of movies, lectures, courses, or camera clips and you want to know **how long it all is** — without installing a media player, opening every file, or trusting file-size guesses. This script does exactly that, offline, with no telemetry and no third-party packages.

## Features

- 🔁 **Recursive scan** — descends into every subfolder automatically.
- 🎯 **Accurate durations** — reads real container/stream metadata via `ffprobe`, not file size or bitrate estimates.
- 📁 **Multiple folders at once** — type `D:\Movies; E:\Courses` and both are scanned (or drag a folder onto the `.bat`).
- 📊 **Instant total** — prints the grand total as *“X hours and Y minutes”* plus `h:mm:ss` and raw seconds.
- 🧾 **CSV report** — writes a timestamped `video_durations-*.csv` with one row per file (path, size, seconds, `hh:mm:ss`, status), importable into Excel.
- 🧹 **No double counting** — folders that overlap (e.g. a parent and its child) are de-duplicated.
- 🧾 **Full report** — shows how many video files were found and how many durations were read successfully.
- ⚠️ **Graceful errors** — lists every file whose duration could not be read instead of failing silently.
- 🪶 **Zero install footprint** — a single `.bat` file; nothing to compile, no Python, no Node.js.
- 🌍 **Unicode-safe** — UTF-8 console output, so non-English paths work.

## Requirements

| Requirement | Notes |
|---|---|
| **Windows 10 / 11** | Uses `cmd.exe` + Windows PowerShell 5.1 (built in). |
| **FFmpeg (`ffprobe`)** | The only real dependency. Install it and make sure `ffprobe` is on `PATH`. |

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
2. Enter one or more **folder paths**, e.g. `D:\Movies` or `"C:\Users\Me\Videos\Course"`, or several at once: `D:\Movies; E:\Courses`.
   - Quotes are fine and get stripped automatically.
   - Separate multiple paths with a **semicolon** `;`.
   - Every folder is scanned **recursively**, and duplicate files are counted once.
3. Wait for the progress bar (`Reading durations 42 / 180`) to finish.
4. Read the total from the green lines.

**Option B — drag & drop**

Drag a folder from Explorer onto `video_duration.bat`. It starts immediately with that folder — no typing.

**Option C — from a terminal**

```powershell
.\video_duration.bat "D:\Movies; E:\Courses"
```

The window stays open until you press a key, so the result never disappears. Every run also drops a CSV report next to the script (or in `%TEMP%` if that folder is read-only).

## Example Output

```text
Folders scanned   : 2
Video files found : 180
Durations read    : 179
Total duration    : 96 hours and 12 minutes  (96:12:04)
Total seconds     : 346324.6

Could not read duration for:
  D:\Movies\clips\corrupted_clip.avi

CSV written to    : D:\Tools\video_durations-20260114-210355.csv
```

- **Video files found** — every file with a supported extension, across all folders and subfolders.
- **Durations read** — how many of those `ffprobe` could actually parse.
- **Total duration** — the sum, rounded to the nearest minute, with exact `h:mm:ss` in parentheses.
- **CSV** — the same data per file: `Path, SizeMB, DurationSeconds, Duration, Status`.

## Supported Formats

`.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.3gp`

Matching is case-insensitive (`Movie.MP4` counts). `ffprobe` can read many more containers — to support another format, add its extension to the `$extensions` array at the top of [`video_duration.ps1`](video_duration.ps1).

## How It Works

The launcher is deliberately boring: `video_duration.bat` starts `video_duration.ps1` with `-NoProfile -ExecutionPolicy Bypass`, passes along any arguments (that's how drag & drop works), shows a readable error if the exit code is non-zero, and **always** waits for a keypress so the window can never vanish. The PowerShell script then:

1. Locates `ffprobe` on `PATH` (or in the usual WinGet/FFmpeg folders, or asks for its path).
2. Resolves the folder arguments, skipping invalid ones with a warning.
3. Recursively enumerates every chosen folder for the extensions above, de-duplicating files that appear in overlapping paths.
4. For each file, runs:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
5. Parses the duration using **invariant culture** (so `1.5` is never misread as `15` on regional settings), ignoring zero/negative/NaN/infinite values.
6. Sums the seconds, converts to `hours`/`minutes`/`h:mm:ss`, and writes the per-file CSV.

Errors are caught, printed in red, and appended to `video_duration-error.log` next to the script, so a failed run always leaves a breadcrumb instead of closing silently.

Everything is local. No network access, no data collection.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ffprobe was not found in PATH.` | Install FFmpeg (see above), or paste the full path to `ffprobe.exe` when asked. |
| `video_duration.ps1 was not found next to this file.` | The two files were separated. Keep `video_duration.bat` and `video_duration.ps1` in the same folder. |
| `None of the given folders exist.` | Check the path. Use quotes for paths with spaces; separate several paths with `;`. |
| `No video files were found in the selected folder(s).` | Confirm the folder has supported extensions; the scan is recursive, so subfolders are included. |
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
Yes. Each run writes `video_durations-<timestamp>.csv` next to the script (falls back to `%TEMP%` if the folder is read-only). Open it in Excel or any spreadsheet.

**Why is the total rounded to minutes?**
Because that's how humans quote viewing time (“96 hours, 12 minutes”). The exact `h:mm:ss` and total seconds are printed right below it.

## Changelog

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

# 🎬 محاسبه‌گر مدت‌زمان ویدیوها

> با یک دابل‌کلیک، مجموع زمان همهٔ ویدیوهای یک پوشه را — همراه با تمام زیرپوشه‌ها — حساب کن.

یک اسکریپت کوچک ویندوزی که یک یا چند درخت پوشه را پیمایش می‌کند، مدت‌زمان هر فایل ویدیویی را با **ffprobe** می‌خواند و مجموع را به ساعت، دقیقه و `h:mm:ss` — به‌همراه یک گزارش CSV — چاپ می‌کند.

## فهرست

- [چرا](#چرا)
- [امکانات](#امکانات)
- [پیش‌نیازها](#پیشنیازها)
- [نصب](#نصب)
- [نحوهٔ استفاده](#نحوهٔ-استفاده)
- [نمونهٔ خروجی](#نمونهٔ-خروجی)
- [فرمت‌های پشتیبانی‌شده](#فرمتهای-پشتیبانی-شده)
- [نحوهٔ کار](#نحوهٔ-کار)
- [رفع مشکل](#رفع-مشکل)
- [سؤالات متداول](#سؤالات-متداول)
- [تغییرات نسخه‌ها](#تغییرات-نسخهها)
- [مشارکت](#مشارکت)
- [مجوز](#مجوز)

## چرا

پوشه‌ای پر از فیلم، درس، دورهٔ آموزشی یا کلیپ دوربین دارید و می‌خواهید بدانید **در کل چقدر زمان می‌برد**. این اسکریپت بدون نصب پخش‌کننده، بدون باز کردن تک‌تک فایل‌ها و بدون حدس زدن از روی حجم فایل، دقیقاً همین را به‌صورت آفلاین حساب می‌کند. هیچ داده‌ای هم جایی فرستاده نمی‌شود.

## امکانات

- 🔁 **پیمایش بازگشتی** — همهٔ زیرپوشه‌ها خودکار بررسی می‌شوند.
- 🎯 **مدت‌زمان دقیق** — متادیتای واقعی فایل با `ffprobe` خوانده می‌شود، نه تخمین از روی حجم یا بیت‌ریت.
- 📁 **چند پوشه هم‌زمان** — بنویسید `D:\Movies; E:\Courses` تا هر دو اسکن شوند (یا پوشه را روی فایل `.bat` بکشید و رها کنید).
- 📊 **جمع فوری** — خروجی به شکل «X ساعت و Y دقیقه» به‌همراه `h:mm:ss` و ثانیهٔ خام.
- 🧾 **گزارش CSV** — هر اجرا یک فایل `video_durations-*.csv` با تاریخ‌وساعت می‌سازد؛ یک ردیف برای هر فایل (مسیر، حجم، ثانیه، `hh:mm:ss`، وضعیت) که در اکسل قابل بازکردن است.
- 🧹 **بدون شمارش تکراری** — اگر پوشه‌ها هم‌پوشانی داشته باشند (مثلاً پوشه و زیرپوشه‌اش)، فایل تکراری دوبار حساب نمی‌شود.
- 🧾 **گزارش کامل** — تعداد فایل‌های پیداشده و تعداد مدت‌های خوانده‌شده نمایش داده می‌شود.
- ⚠️ **مدیریت خطا** — فایل‌هایی که مدتشان خوانده نشود، فهرست می‌شوند؛ هیچ خطایی بی‌صدا رد نمی‌شود.
- 🪶 **بدون نصب** — فقط یک فایل `.bat`؛ نه کامپایل، نه پایتون، نه Node.js.
- 🌍 **سازگار با یونیکد** — خروجی کنسول UTF-8 است تا مسیرهای فارسی/غیرانگلیسی درست نمایش داده شوند.

## پیش‌نیازها

| نیاز | توضیح |
|---|---|
| **ویندوز ۱۰ یا ۱۱** | از `cmd.exe` و Windows PowerShell 5.1 (از پیش نصب‌شده) استفاده می‌کند. |
| **FFmpeg (`ffprobe`)** | تنها وابستگی واقعی. نصبش کنید و مطمئن شوید `ffprobe` روی `PATH` است. |

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
2. یک یا چند **مسیر پوشه** وارد کنید، مثلاً `D:\Movies` یا `"C:\Users\Me\Videos\Course"` یا چندتایی با هم: `D:\Movies; E:\Courses`.
   - گذاشتن گیومه اشکالی ندارد و خودکار حذف می‌شود.
   - مسیرهای متعدد را با **سمی‌کالن** `;` جدا کنید.
   - همهٔ پوشه‌ها **به‌صورت بازگشتی** اسکن می‌شوند و فایل‌های تکراری یک‌بار حساب می‌شوند.
3. تا تمام شدن نوار پیشرفت (`Reading durations 42 / 180`) صبر کنید.
4. مجموع را از خطوط سبز بخوانید.

**روش ب — کشیدن و رها کردن**

پوشه را از Explorer روی `video_duration.bat` بکشید. بدون هیچ تایپی، همان پوشه اسکن می‌شود.

**روش ج — از ترمینال**

```powershell
.\video_duration.bat "D:\Movies; E:\Courses"
```

پنجره تا فشردن یک کلید باز می‌ماند، پس نتیجه از دست نمی‌رود. هر اجرا یک گزارش CSV هم کنار اسکریپت می‌سازد (اگر آن پوشه فقط-خواندنی باشد، در `%TEMP%`).

## نمونهٔ خروجی

```text
Folders scanned   : 2
Video files found : 180
Durations read    : 179
Total duration    : 96 hours and 12 minutes  (96:12:04)
Total seconds     : 346324.6

Could not read duration for:
  D:\Movies\clips\corrupted_clip.avi

CSV written to    : D:\Tools\video_durations-20260114-210355.csv
```

- **Video files found** — همهٔ فایل‌های با پسوند پشتیبانی‌شده در تمام پوشه‌ها و زیرپوشه‌ها.
- **Durations read** — چند فایل را `ffprobe` واقعاً توانسته بخواند.
- **Total duration** — مجموع، گردشده به نزدیک‌ترین دقیقه، با `h:mm:ss` دقیق در پرانتز.
- **CSV** — همان داده‌ها به تفکیک فایل: `Path, SizeMB, DurationSeconds, Duration, Status`.

## فرمت‌های پشتیبانی‌شده

`.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.3gp`

تطبیق پسوند به بزرگی/کوچکی حروف حساس نیست (`Movie.MP4` هم حساب می‌شود). `ffprobe` کانتینرهای بیشتری را می‌شناسد؛ برای افزودن فرمت جدید، پسوند را به آرایهٔ `$extensions` در ابتدای [`video_duration.ps1`](video_duration.ps1) اضافه کنید.

## نحوهٔ کار

لانچر عمداً ساده است: `video_duration.bat` فایل `video_duration.ps1` را با `-NoProfile -ExecutionPolicy Bypass` اجرا می‌کند، آرگومان‌ها را پاس می‌دهد (به همین دلیل Drag & Drop کار می‌کند)، در صورت خطا پیام خوانا نشان می‌دهد و **همیشه** منتظر فشردن یک کلید می‌ماند تا پنجره هرگز ناگهان بسته نشود. سپس اسکریپت PowerShell:

1. `ffprobe` را روی `PATH` پیدا می‌کند (یا در پوشه‌های معمول WinGet/FFmpeg، یا مسیرش را می‌پرسد).
2. مسیرهای ورودی را اعتبارسنجی می‌کند و مسیرهای نامعتبر را با هشدار رد می‌کند.
3. همهٔ پوشه‌های انتخابی را به‌صورت بازگشتی برای پسوندهای بالا می‌گردد و فایل‌های تکراری در مسیرهای هم‌پوشان را یک‌بار حساب می‌کند.
4. برای هر فایل این دستور را اجرا می‌کند:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
5. مدت‌زمان را با **invariant culture** تجزیه می‌کند (تا در تنظیمات منطقه‌ای، `1.5` اشتباهاً `15` خوانده نشود) و مقادیر صفر/منفی/NaN/بی‌نهایت را نادیده می‌گیرد.
6. ثانیه‌ها را جمع، به ساعت/دقیقه/`h:mm:ss` تبدیل و فایل CSV را می‌نویسد.

خطاها گرفته می‌شوند، با رنگ قرمز چاپ می‌شوند و در فایل `video_duration-error.log` کنار اسکریپت ثبت می‌شوند؛ بنابراین یک اجرای ناموفق هم ردپا باقی می‌گذارد و بی‌صدا بسته نمی‌شود.

همه‌چیز محلی است. بدون دسترسی به شبکه و بدون جمع‌آوری داده.

## رفع مشکل

| مشکل | راه‌حل |
|---|---|
| `ffprobe was not found in PATH.` | FFmpeg را نصب کنید (بالا) یا وقتی پرسید، مسیر کامل `ffprobe.exe` را بدهید. |
| `video_duration.ps1 was not found next to this file.` | دو فایل از هم جدا شده‌اند. `video_duration.bat` و `video_duration.ps1` باید در یک پوشه باشند. |
| `None of the given folders exist.` | مسیر را بررسی کنید؛ برای مسیرهای دارای فاصله از گیومه استفاده کنید و چند مسیر را با `;` جدا کنید. |
| `No video files were found in the selected folder(s).` | مطمئن شوید پوشه پسوندهای پشتیبانی‌شده دارد؛ اسکن بازگشتی است، پس زیرپوشه‌ها هم شامل می‌شوند. |
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
بله. هر اجرا فایل `video_durations-<timestamp>.csv` را کنار اسکریپت می‌سازد (اگر پوشه فقط-خواندنی باشد، در `%TEMP%`). در اکسل یا هر برنامهٔ صفحه‌گسترده‌ای قابل بازکردن است.

**چرا جمع به دقیقه گرد می‌شود؟**
چون ما زمان تماشا را معمولاً به ساعت و دقیقه می‌گوییم («۹۶ ساعت و ۱۲ دقیقه»). مقدار دقیق `h:mm:ss` و ثانیهٔ خام هم بلافاصله زیرش چاپ می‌شود.

## تغییرات نسخه‌ها

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
