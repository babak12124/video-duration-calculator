## Video Duration Calculator v1.0.0

Add up the total runtime of every video in one or more folders — offline, in a single double-click.

### Highlights

- **Recursive scan** of one or many folders (`D:\Movies; E:\Courses`) — or drag & drop a folder onto the `.bat`
- **Accurate totals** via `ffprobe`: `96 hours and 12 minutes (96:12:04)` plus raw seconds
- **CSV report** for every run: `Path, SizeMB, DurationSeconds, Duration, Status`
- **De-duplicated** results when scanned paths overlap
- **Graceful failures**: unreadable files are listed, never silently skipped
- **Bilingual documentation** (English + فارسی)

### Requirements

Windows 10/11 and FFmpeg (`ffprobe`) on `PATH`:

```powershell
winget install Gyan.FFmpeg
```

### Install

Download `video_duration.bat` from the assets below and run it. No installer, no admin rights.

**Full docs:** [README.md](https://github.com/babak12124/video-duration-calculator#readme)

### فارسی

مجموع مدت‌زمان همهٔ ویدیوهای یک یا چند پوشه را آفلاین و با یک دابل‌کلیک حساب می‌کند. فایل `video_duration.bat` را دانلود و اجرا کنید؛ تنها پیش‌نیاز، FFmpeg است.
