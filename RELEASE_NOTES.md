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
