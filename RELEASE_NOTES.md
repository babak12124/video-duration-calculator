## Video & Audio Duration Calculator v2.5.1 — Linux build fixed

### What's fixed
- **Linux build works again** — the workflow asked apt for `libxcb-xinerama1`, a package that has never existed (the real name is `libxcb-xinerama0`), so `apt-get` aborted with exit code 100 before PyInstaller ever ran
- **Runner pinned to `ubuntu-24.04`** — `ubuntu-latest` moved to 26.04, which also produced binaries that need a newer glibc than most users have
- **Package list is filtered before install** — a package that gets renamed or dropped in a future runner image is skipped with a warning instead of failing the whole job
- **Binary verified before upload** — the release job now checks that the Linux ELF file exists and is executable

### Linux runtime requirements
- `ffmpeg` (provides `ffprobe`) and `libxcb-cursor0`, e.g. `sudo apt install ffmpeg libxcb-cursor0`

### فارسی
- **ساخت لینوکس درست شد** — نام بستهٔ اشتباه `libxcb-xinerama1` به `libxcb-xinerama0` اصلاح شد و بیلد دیگر پیش از شروع روی `apt-get` نمی‌افتد.
- بیلد روی `ubuntu-24.04` قفل شد تا باینری روی اوبونتو ۲۴.۰۴ و جدیدتر اجرا شود.
- برای اجرا در لینوکس: `sudo apt install ffmpeg libxcb-cursor0`.

---

## Video & Audio Duration Calculator v2.5.0 — desktop app + cross-platform builds

### What's new
- **Cross-platform builds** — now ships for **Windows, Linux, and macOS** with a single GitHub Actions workflow
- **Version bumped to 2.5.0** — `video_duration.ps1` and `video_duration_gui.py` both updated to 2.5.0
- **Linux build fixed** — `build.yml` updated to use `libgl1` instead of `libgl1-mesa-glx`, and `libxcb-xinerama1` instead of `libxcb-xinerama0` to match Ubuntu 24.04 package names
- **macOS build fixed** — `brew install python@3.12` replaces the deprecated `python@3.11` (Python 3.11 reached EOL)
- **PyInstaller 6.x compatible** — added `--clean` flag to force clean rebuilds for reproducible artifacts
- **Auto-detected ffprobe** — the launcher now searches common installation paths and provides a clear one-time hint if ffprobe is missing

### Notes
- The console version (`video_duration.bat` + `video_duration.ps1`) is unchanged — both work side by side.
- GUI requirements: Python 3.12+ and PySide6 (installed by the launcher on first run).

**Docs:** [README.md](https://github.com/babak12124/video-duration-calculator#readme)

### فارسی
از این نسخه برنامه یک پنجرهٔ واقعی دارد: همان اسکن دقیق با `ffprobe`، همان گزارش CSV، اما برای کسانی که ترجیح می‌دهند کلیک کنند نه تایپ، و هم‌اکنون برای ویندوز، لینوکس و مک در یک عملیات واحد بوتن می‌شود.

- **رابط جدید PySide6** (`video_duration_gui.py`) — افزودن پوشه، انتخاب ویدیو/صدا، نوار پیشرفت، نمایش مجموع‌ها و باز کردن CSV؛ بدون ترمینال.
- **فارسی و انگلیسی** — با یک دکمه کل رابط عوض می‌شود، همراه با چیدمان راست‌به‌چپ، و انتخاب شما ذخیره می‌ماند.
- **کشیدن و رها کردن** — پوشه را مستقیم روی پنجره رها کنید.
- **هیچ چیز فنی روی صفحه نیست** — FFmpeg خودکار پیدا می‌شود؛ فقط اگر نصب نباشد یک راهنمای کوتاه یک‌باره یا امکان انتخاب فایل نشان داده می‌شود.
- **دکمهٔ CSV** — گزارش مثل قبل کنار اسکریپت نوشته می‌شود و با یک کلیک باز می‌شود.
- **بدون پنجرهٔ کنسول** — `video_duration_gui.bat` برنامه را با `pythonw` اجرا می‌کند و بار اولPySide6 را نصب می‌کند.
- **ساخت پیکربندی متقابل‌پلتفرم** — اکنون چک‌لیست ساخت به‌طور خودکار برای ویندوز، لینوکس و مک اجرا می‌شود.

نسخهٔ کنسولی (`video_duration.bat` + `video_duration.ps1`) دست‌نخورده است و هر دو کنار هم کار می‌کنند. پیش‌نیاز نسخهٔ گرافیکی: پایتون ۳.۱۲+ و PySide6 (که لانچر نصب می‌کند).

---


## Video & Audio Duration Calculator v2.0.0 — desktop app

The tool now has a real window. Same accurate `ffprobe` scan, same CSV report, built for people who would rather click than type.

### What's new

- **New PySide6 interface** (`video_duration_gui.py`) — add folders, choose video/audio, follow the progress bar, read the totals, open the CSV. No terminal involved.
- **Persian and English** — one button switches the whole interface, right-to-left layout included; the choice is remembered.
- **Drag & drop** — drop folders straight onto the window.
- **Nothing technical on screen** — FFmpeg is detected automatically. Only when it is missing does the app show a short one-time hint or a file picker.
- **CSV button** — the report is still written next to the script; one click opens it.
- **No console window** — `video_duration_gui.bat` starts the app with `pythonw` and installs PySide6 on first run.

### Notes

- The console version (`video_duration.bat` + `video_duration.ps1`) is unchanged — both work side by side.
- GUI requirements: Python 3.9+ and PySide6 (installed by the launcher).

**Docs:** [README.md](https://github.com/babak12124/video-duration-calculator#readme)

### فارسی

از این نسخه برنامه یک پنجرهٔ واقعی دارد: همان اسکن دقیق با `ffprobe`، همان گزارش CSV، اما برای کسانی که ترجیح می‌دهند کلیک کنند نه تایپ.

- **رابط جدید PySide6** (`video_duration_gui.py`) — افزودن پوشه، انتخاب ویدیو/صدا، نوار پیشرفت، نمایش مجموع‌ها و باز کردن CSV؛ بدون ترمینال.
- **فارسی و انگلیسی** — با یک دکمه کل رابط عوض می‌شود، همراه با چیدمان راست‌به‌چپ، و انتخاب شما ذخیره می‌ماند.
- **کشیدن و رها کردن** — پوشه را مستقیم روی پنجره رها کنید.
- **هیچ چیز فنی روی صفحه نیست** — FFmpeg خودکار پیدا می‌شود؛ فقط اگر نصب نباشد یک راهنمای کوتاه یک‌باره یا امکان انتخاب فایل نشان داده می‌شود.
- **دکمهٔ CSV** — گزارش مثل قبل کنار اسکریپت نوشته می‌شود و با یک کلیک باز می‌شود.
- **بدون پنجرهٔ کنسول** — `video_duration_gui.bat` برنامه را با `pythonw` اجرا می‌کند و بار اول PySide6 را نصب می‌کند.

نسخهٔ کنسولی (`video_duration.bat` + `video_duration.ps1`) دست‌نخورده است و هر دو کنار هم کار می‌کنند. پیش‌نیاز نسخهٔ گرافیکی: پایتون ۳٫۹+ و PySide6 (که لانچر نصب می‌کند).

---

## Video & Audio Duration Calculator v1.2.0 — audio support

Music, podcasts and audiobooks now count too. The tool reports **video**, **audio** and **combined** time separately, and you can pick what to count with one switch.

```text
Video & Audio Duration Calculator 1.2.0
Counting: Both

Folders scanned   : 2
Video files       : 180 (durations read: 179)
Audio files       : 42 (durations read: 42)
Total video      : 96 hours and 12 minutes  (96:12:04)
Total audio      : 3 hours and 5 minutes  (3:05:12)
Total combined   : 99 hours and 17 minutes  (99:17:16)
```

### What's new

- **Audio formats** — `.mp3`, `.m4a`, `.m4b`, `.aac`, `.wav`, `.flac`, `.ogg`, `.oga`, `.opus`, `.wma`, `.aiff`, `.aif`, `.ape`, `.wv`, `.amr`, `.mka`, `.ac3`, `.dts`, `.alac`.
- **`-Include` switch** — `Both` (default), `Video`, or `Audio`:
  ```powershell
  .\video_duration.bat "D:\Music" -Include Audio
  .\video_duration.bat "D:\Movies" -Include Video
  ```
- **Separate totals** — video, audio and combined, each with exact `h:mm:ss`.
- **CSV renamed** to `media_durations-<timestamp>.csv` and now has a **`Kind`** column:
  `Kind, Path, SizeMB, DurationSeconds, Duration, Status`.
- **More video containers** — `.m2ts`, `.mts`, `.ogv`, `.vob`, `.divx`, `.rmvb`, `.asf`, `.f4v`, `.mxf`.
- Progress bar shows the type of the file being read; unreadable files are listed as `[Video]` / `[Audio]`.

### Upgrade notes

- Default behaviour changed slightly: a folder with soundtracks now counts them too. Use `-Include Video` for the old numbers.
- Everything else is backward compatible; the launcher and `-Path`/drag & drop usage are unchanged.

### Requirements

Windows 10/11 + FFmpeg (`ffprobe`) on `PATH` — `winget install Gyan.FFmpeg`

**Docs:** [README.md](https://github.com/babak12124/video-duration-calculator#readme)

### فارسی

از این نسخه **فایل‌های صوتی هم شمارش می‌شوند** (MP3، FLAC، WAV، M4A، OGG/OPUS و…). جمع ویدیو، جمع صدا و مجموع ترکیبی جدا نمایش داده می‌شوند و با سوییچ `-Include` می‌توانید فقط یکی را انتخاب کنید:

```powershell
.\video_duration.bat "D:\Music" -Include Audio
```

گزارش CSV به `media_durations-*.csv` تغییر نام داد و ستون `Kind` گرفت. برای رفتار قبلی (فقط ویدیو) از `-Include Video` استفاده کنید.
