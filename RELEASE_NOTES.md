## Video Duration Calculator v1.1.0 — bug fix

**Fixed: the window opened and closed instantly on some machines.** The old single-file `.bat` re-launched itself and executed an embedded PowerShell payload through `Invoke-Expression`. Antivirus heuristics and SmartScreen kill that pattern silently — the window flashes and disappears, so it looks like nothing happened.

The project is now a plain, readable **launcher + script** pair:

```
video_duration.bat   ->  video_duration.ps1
```

### What changed

- **No more self-extracting / obfuscated-looking script.** `video_duration.bat` simply calls `video_duration.ps1` with `-NoProfile -ExecutionPolicy Bypass` and forwards arguments (drag & drop still works).
- **The window can never vanish.** The launcher always waits for a keypress, and any non-zero exit prints the error and dumps the log.
- **Visible errors + log file.** Failures are shown in red and appended to `video_duration-error.log` next to the script.
- **Clear messages** for a missing `video_duration.ps1`, invalid paths, and empty input.
- **`h:mm:ss` fixed** — no longer wraps at 24 hours (`30:15:22` instead of `06:15:22`).
- **Smarter `ffprobe` discovery** — checks `PATH`, the WinGet links folder, and common FFmpeg install paths; still asks for a path if needed.
- Folder prompt retries up to 3 times instead of exiting on a typo.

### Install

Download **both** `video_duration.bat` and `video_duration.ps1` (or the `.zip`) and keep them in the same folder.

Requires Windows 10/11 + FFmpeg (`ffprobe`) on `PATH`:

```powershell
winget install Gyan.FFmpeg
```

If Windows blocks the downloaded files, right-click → **Properties → Unblock** (or `Unblock-File .\video_duration.*`).

### Still there from v1.0.0

Recursive scan · multiple folders (`D:\Movies; E:\Courses`) · drag & drop · accurate `ffprobe` totals · CSV report · bilingual docs.

**Docs:** [README.md](https://github.com/babak12124/video-duration-calculator#readme)

### فارسی

**رفع باگ: روی بعضی سیستم‌ها پنجره باز و بلافاصله بسته می‌شد.** فایل `.bat` قبلی خودش را دوباره اجرا می‌کرد و یک بدنهٔ PowerShell جاسازی‌شده را با `Invoke-Expression` اجرا می‌کرد؛ آنتی‌ویروس‌ها این الگو را بی‌صدا می‌کشند. حالا پروژه یک جفت فایل ساده و خوانا است: `video_duration.bat` فقط `video_duration.ps1` را صدا می‌زند.

پنجره دیگر هرگز ناگهان بسته نمی‌شود، خطاها با رنگ قرمز و فایل `video_duration-error.log` گزارش می‌شوند، و `h:mm:ss` بعد از ۲۴ ساعت دیگر صفر نمی‌شود.

**نصب:** هر دو فایل (یا فایل zip) را دانلود و در یک پوشه نگه دارید. پیش‌نیاز: ویندوز ۱۰/۱۱ و FFmpeg (`ffprobe`).
