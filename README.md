# 🎬 Video Duration Calculator

> Add up the total runtime of every video in a folder — recursively — in seconds, with one double-click.

A tiny, dependency-light Windows script that walks a folder tree, reads the duration of every video file with **ffprobe**, and prints the total runtime as hours and minutes.

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
- 📊 **Instant total** — prints the grand total as *“X hours and Y minutes”*.
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

1. **Double-click `video_duration.bat`** (or run it from a terminal).
2. Enter a **folder path**, e.g. `D:\Movies` or `"C:\Users\Me\Videos\Course"`.
   - Quotes are fine and get stripped automatically.
   - The scan includes **all subfolders**.
3. Wait for the progress bar (`Reading durations 42 / 180`) to finish.
4. Read the total from the green line.

The window stays open until you press a key, so the result never disappears.

## Example Output

```text
Enter folder path (e.g. D:\Movies): D:\Movies

Video files found : 180
Durations read    : 179
Total duration    : 96 hours and 12 minutes

Could not read duration for:
  D:\Movies\clips\corrupted_clip.avi
```

- **Video files found** — every file with a supported extension, in the folder and all subfolders.
- **Durations read** — how many of those `ffprobe` could actually parse.
- **Total duration** — the sum, rounded to the nearest minute.

## Supported Formats

`.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.3gp`

Matching is case-insensitive (`Movie.MP4` counts). `ffprobe` can read many more containers — to support another format, add its extension to the `$ext` line near the top of the PowerShell block inside the script.

## How It Works

The `.bat` is a hybrid file: the Batch part re-launches itself through PowerShell, extracting everything after the `#PSSTART` marker and running it. Then it:

1. Locates `ffprobe` on `PATH` (or asks for its path).
2. Recursively enumerates the chosen folder for the extensions above.
3. For each file, runs:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
4. Parses the duration using **invariant culture** (so `1.5` is never misread as `15` on regional settings).
5. Sums the seconds, then converts to `hours` and `minutes`, rounding to the nearest minute.

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
Not yet — currently it prints to the console. Easy to add; see [Contributing](#contributing).

**Why is the total rounded to minutes?**
Because that's how humans quote viewing time (“96 hours, 12 minutes”). For second-level precision, remove the rounding step.

## Contributing

Issues and pull requests are welcome. Ideas that would fit well:

- CSV/TXT export of per-file durations
- Multi-folder/multi-drive support in one run
- Optional `hours:minutes:seconds` output
- A PowerShell module version
- Bash / macOS port

Please keep changes small, readable, and dependency-free.

## License

[MIT](LICENSE) © babak12124

---

<h1 id="فارسی">📖 راهنمای فارسی</h1>

# 🎬 محاسبه‌گر مدت‌زمان ویدیوها

> با یک دابل‌کلیک، مجموع زمان همهٔ ویدیوهای یک پوشه را — همراه با تمام زیرپوشه‌ها — حساب کن.

یک اسکریپت کوچک ویندوزی که درخت پوشه‌ها را پیمایش می‌کند، مدت‌زمان هر فایل ویدیویی را با **ffprobe** می‌خواند و مجموع را به ساعت و دقیقه چاپ می‌کند.

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
- 📊 **جمع فوری** — خروجی به شکل «X ساعت و Y دقیقه».
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

1. روی **`video_duration.bat` دابل‌کلیک** کنید (یا از ترمینال اجرایش کنید).
2. مسیر پوشه را وارد کنید، مثلاً `D:\Movies` یا `"C:\Users\Me\Videos\Course"`.
   - گذاشتن گیومه اشکالی ندارد و خودکار حذف می‌شود.
   - **همهٔ زیرپوشه‌ها** هم اسکن می‌شوند.
3. تا تمام شدن نوار پیشرفت (`Reading durations 42 / 180`) صبر کنید.
4. مجموع را از خط سبز بخوانید.

پنجره تا فشردن یک کلید باز می‌ماند، پس نتیجه از دست نمی‌رود.

## نمونهٔ خروجی

```text
Enter folder path (e.g. D:\Movies): D:\Movies

Video files found : 180
Durations read    : 179
Total duration    : 96 hours and 12 minutes

Could not read duration for:
  D:\Movies\clips\corrupted_clip.avi
```

- **Video files found** — تعداد فایل‌های با پسوند پشتیبانی‌شده در پوشه و زیرپوشه‌ها.
- **Durations read** — چند فایل را `ffprobe` واقعاً توانسته بخواند.
- **Total duration** — مجموع، گردشده به نزدیک‌ترین دقیقه.

## فرمت‌های پشتیبانی‌شده

`.mp4` · `.mkv` · `.avi` · `.mov` · `.wmv` · `.flv` · `.webm` · `.m4v` · `.mpg` · `.mpeg` · `.ts` · `.3gp`

تطبیق پسوند به بزرگی/کوچکی حروف حساس نیست (`Movie.MP4` هم حساب می‌شود). `ffprobe` کانتینرهای بیشتری را می‌شناسد؛ برای افزودن فرمت جدید، پسوند را به خط `$ext` در بخش PowerShell اسکریپت اضافه کنید.

## نحوهٔ کار

فایل `.bat` یک فایل ترکیبی است: بخش Batch خودش را از طریق PowerShell دوباره اجرا می‌کند و هر چیزی بعد از نشانگر `#PSSTART` را استخراج و اجرا می‌کند. سپس:

1. `ffprobe` را روی `PATH` پیدا می‌کند (یا مسیرش را می‌پرسد).
2. پوشهٔ انتخابی را به‌صورت بازگشتی برای پسوندهای بالا می‌گردد.
3. برای هر فایل این دستور را اجرا می‌کند:
   ```text
   ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 -i "<file>"
   ```
4. مدت‌زمان را با **invariant culture** تجزیه می‌کند (تا در تنظیمات منطقه‌ای، `1.5` اشتباهاً `15` خوانده نشود).
5. ثانیه‌ها را جمع و به ساعت و دقیقه تبدیل می‌کند، با گرد کردن به نزدیک‌ترین دقیقه.

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
فعلاً نه — نتیجه در کنسول چاپ می‌شود. افزودنش ساده است؛ بخش [مشارکت](#مشارکت) را ببینید.

**چرا جمع به دقیقه گرد می‌شود؟**
چون ما زمان تماشا را معمولاً به ساعت و دقیقه می‌گوییم («۹۶ ساعت و ۱۲ دقیقه»). برای دقت ثانیه‌ای، مرحلهٔ گرد کردن را حذف کنید.

## مشارکت

Issue و Pull Request خوش‌آمد است. ایده‌هایی که خوب جفت می‌شوند:

- خروجی CSV/TXT از مدت هر فایل
- پشتیبانی از چند پوشه/چند درایو در یک اجرا
- خروجی اختیاری به شکل `hours:minutes:seconds`
- نسخهٔ PowerShell Module
- پورت Bash / macOS

لطفاً تغییرات را کوچک، خوانا و بدون وابستگی نگه دارید.

## مجوز

[MIT](LICENSE) © babak12124
