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
