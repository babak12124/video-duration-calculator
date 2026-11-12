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

1. Download [`video_duration.bat`](video_duration.bat) (or clone the repo).
2. Put it anywhere — Desktop, `D:\Tools`, a network share.
3. That's it. No installer, no admin rights required.

```powershell
git clone https://github.com/babak12124/video-duration-calculator.git
```

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

Matching is case-insensitive (`Movie.MP4` counts). `ffprobe` can read many more containers — to support another format, add its extension to the `$ext` line near the top of the PowerShell block inside the script.

## How It Works

The `.bat` is a hybrid file: the Batch part re-launches itself through PowerShell, extracting everything after the `#PSSTART` marker and running it. Then it:

1. Locates `ffprobe` on `PATH` (or asks for its path).
2. Recursively enumerates every chosen folder for the extensions above, de-duplicating files that appear in overlapping paths.
3. For each file, runs:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
4. Parses the duration using **invariant culture** (so `1.5` is never misread as `15` on regional settings), ignoring zero/negative/NaN values.
5. Sums the seconds, converts to `hours`/`minutes`/`h:mm:ss`, and writes the per-file CSV.

Everything is local. No network access, no data collection.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `ffprobe was not found in PATH.` | Install FFmpeg (see above), or paste the full path to `ffprobe.exe` when asked. |
| `Folder not found.` | Check the path. Use quotes for paths with spaces. |
| `No video files found.` | Confirm the folder has supported extensions; the scan is recursive, so subfolders are included. |
| Some files listed as unreadable | The file is corrupt, still being downloaded, or uses an exotic codec/container. `ffprobe` prints the reason with `-v error`. |
| Total looks wrong | Rounded to the nearest minute by design. Themes/regional settings cannot break parsing — the script uses invariant culture. |
| Window closes instantly | Run it from a terminal (`cmd` → drag the `.bat` in → Enter) to see the error. |

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

1. فایل [`video_duration.bat`](video_duration.bat) را دانلود کنید (یا ریپو را clone کنید).
2. هر جایی که خواستید بگذارید — دسکتاپ، `D:\Tools`، یا یک درایو شبکه.
3. تمام. نصب‌کننده و دسترسی ادمین لازم نیست.

```powershell
git clone https://github.com/babak12124/video-duration-calculator.git
```

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

تطبیق پسوند به بزرگی/کوچکی حروف حساس نیست (`Movie.MP4` هم حساب می‌شود). `ffprobe` کانتینرهای بیشتری را می‌شناسد؛ برای افزودن فرمت جدید، پسوند را به خط `$ext` در بخش PowerShell اسکریپت اضافه کنید.

## نحوهٔ کار

فایل `.bat` یک فایل ترکیبی است: بخش Batch خودش را از طریق PowerShell دوباره اجرا می‌کند و هر چیزی بعد از نشانگر `#PSSTART` را استخراج و اجرا می‌کند. سپس:

1. `ffprobe` را روی `PATH` پیدا می‌کند (یا مسیرش را می‌پرسد).
2. همهٔ پوشه‌های انتخابی را به‌صورت بازگشتی برای پسوندهای بالا می‌گردد و فایل‌های تکراری در مسیرهای هم‌پوشان را یک‌بار حساب می‌کند.
3. برای هر فایل این دستور را اجرا می‌کند:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
4. مدت‌زمان را با **invariant culture** تجزیه می‌کند (تا در تنظیمات منطقه‌ای، `1.5` اشتباهاً `15` خوانده نشود) و مقادیر صفر/منفی/NaN را نادیده می‌گیرد.
5. ثانیه‌ها را جمع، به ساعت/دقیقه/`h:mm:ss` تبدیل و فایل CSV را می‌نویسد.

همه‌چیز محلی است. بدون دسترسی به شبکه و بدون جمع‌آوری داده.

## رفع مشکل

| مشکل | راه‌حل |
|---|---|
| `ffprobe was not found in PATH.` | FFmpeg را نصب کنید (بالا) یا وقتی پرسید، مسیر کامل `ffprobe.exe` را بدهید. |
| `Folder not found.` | مسیر را بررسی کنید؛ برای مسیرهای دارای فاصله از گیومه استفاده کنید. |
| `No video files found.` | مطمئن شوید پوشه پسوندهای پشتیبانی‌شده دارد؛ اسکن بازگشتی است، پس زیرپوشه‌ها هم شامل می‌شوند. |
| چند فایل به‌عنوان ناخوانا فهرست شدند | فایل خراب است، هنوز در حال دانلود است، یا کدک/کانتینر غیرمعمولی دارد. `ffprobe` با `-v error` دلیل را چاپ می‌کند. |
| مجموع به‌نظر اشتباه است | به‌صورت عمدی به دقیقه گرد می‌شود. تم و تنظیمات منطقه‌ای هم نمی‌توانند تجزیه را خراب کنند. |
| پنجره فوراً بسته می‌شود | از داخل ترمینال اجرا کنید (`cmd` → فایل `.bat` را داخلش بکشید → Enter) تا خطا را ببینید. |

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
