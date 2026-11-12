#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Video & Audio Duration Calculator 2.0 — a simple bilingual desktop app.

Recursively scans one or more folders, reads every media file's duration with
ffprobe, shows per-type and combined totals, and writes a CSV report.
The interface is built with PySide6 (Qt 6) and switches between English and
Persian, including right-to-left layout.

Run:  python video_duration_gui.py [folder ...]
"""

from __future__ import annotations

import csv
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import traceback
from pathlib import Path

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QButtonGroup,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QStyle,
    QTableWidget,
    QTableWidgetItem,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

APP_NAME = "Video & Audio Duration Calculator"
APP_VERSION = "2.0.0"
SCRIPT_DIR = Path(__file__).resolve().parent

VIDEO_EXTENSIONS = {
    ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".m4v", ".mpg", ".mpeg",
    ".ts", ".m2ts", ".mts", ".3gp", ".ogv", ".vob", ".divx", ".rmvb", ".asf", ".f4v", ".mxf",
}
AUDIO_EXTENSIONS = {
    ".mp3", ".m4a", ".m4b", ".aac", ".wav", ".flac", ".ogg", ".oga", ".opus", ".wma",
    ".aiff", ".aif", ".ape", ".wv", ".amr", ".mka", ".ac3", ".dts", ".alac",
}

CREATE_NO_WINDOW = 0x08000000 if os.name == "nt" else 0

STRINGS = {
    "en": {
        "app_title": "Video & Audio Duration Calculator",
        "tagline": "Total runtime of every video and audio file in a folder",
        "switch_lang": "فارسی",
        "folders": "Folders",
        "add_folder": "Add folder…",
        "remove": "Remove",
        "clear": "Clear",
        "folders_hint": "Drop folders onto the window or press “Add folder…”. After a scan, every folder shows its own total with subfolders nested underneath.",
        "folders_added": "{count} folder(s) added.",
        "folder_inside": "“{name}” is already inside “{root}”, so it will appear in that tree.",
        "col_folder": "Folder",
        "col_total": "Total",
        "col_video": "Video",
        "col_audio": "Audio",
        "col_files": "Files",
        "mode": "Count",
        "mode_both": "Video + audio",
        "mode_video": "Video only",
        "mode_audio": "Audio only",
        "scan": "Calculate total",
        "cancel": "Cancel",
        "ready": "Add one or more folders, then press “Calculate total”.",
        "discovering": "Scanning folders… {count} files found",
        "scanning": "Reading durations",
        "done": "Done in {seconds:.1f} s",
        "cancelled": "Cancelled.",
        "stat_video": "Total video",
        "stat_audio": "Total audio",
        "stat_combined": "Total combined",
        "hm": "{hours} hours and {minutes} minutes",
        "files": "Files",
        "col_kind": "Kind",
        "col_file": "File",
        "col_duration": "Duration",
        "col_status": "Status",
        "kind_video": "Video",
        "kind_audio": "Audio",
        "ok": "OK",
        "failed": "FAILED",
        "stats": "Folders: {folders}   ·   Video files: {video} (read {video_ok})   ·   Audio files: {audio} (read {audio_ok})   ·   Total seconds: {seconds}",
        "csv_written": "CSV: {name}",
        "csv_failed": "The CSV report could not be written.",
        "open_csv": "Open CSV",
        "need_folder_title": "No folders",
        "need_folder": "Add at least one folder first.",
        "no_files_title": "Nothing found",
        "no_files": "No matching media files were found in the selected folders.",
        "error_title": "Error",
        "ffprobe_title": "One-time setup",
        "ffprobe_text": (
            "To read how long each file is, the app uses FFmpeg (a free media tool).\n\n"
            "Install it once with:  winget install Gyan.FFmpeg\n"
            "or pick the ffprobe.exe file if it is already on your computer."
        ),
        "ffprobe_pick": "Pick ffprobe.exe…",
        "ffprobe_close": "Not now",
        "ffprobe_filter": "ffprobe (ffprobe.exe);;All files (*)",
        "ffprobe_bad": "That file does not look like ffprobe. Please try again.",
        "missing_title": "Missing folders",
        "missing_folders": "These folders no longer exist and will be skipped:\n{paths}",
    },
    "fa": {
        "app_title": "محاسبه‌گر مدت‌زمان ویدیو و صدا",
        "tagline": "مجموع زمان همهٔ ویدیوها و فایل‌های صوتی یک پوشه",
        "switch_lang": "English",
        "folders": "پوشه‌ها",
        "add_folder": "افزودن پوشه…",
        "remove": "حذف",
        "clear": "پاک کردن",
        "folders_hint": "پوشه‌ها را روی پنجره رها کنید یا «افزودن پوشه…» را بزنید. بعد از محاسبه، هر پوشه مجموع خودش را نشان می‌دهد و زیرپوشه‌ها تودرتو می‌آیند.",
        "folders_added": "{count} پوشه اضافه شد.",
        "folder_inside": "«{name}» داخل «{root}» است، پس در همان درخت نمایش داده می‌شود.",
        "col_folder": "پوشه",
        "col_total": "مجموع",
        "col_video": "ویدیو",
        "col_audio": "صدا",
        "col_files": "فایل‌ها",
        "mode": "شمارش",
        "mode_both": "ویدیو + صدا",
        "mode_video": "فقط ویدیو",
        "mode_audio": "فقط صدا",
        "scan": "محاسبهٔ مجموع",
        "cancel": "لغو",
        "ready": "یک یا چند پوشه اضافه کنید، بعد «محاسبهٔ مجموع» را بزنید.",
        "discovering": "در حال پیمایش پوشه‌ها… {count} فایل پیدا شد",
        "scanning": "خواندن مدت‌ها",
        "done": "تمام شد در {seconds:.1f} ثانیه",
        "cancelled": "لغو شد.",
        "stat_video": "مجموع ویدیو",
        "stat_audio": "مجموع صدا",
        "stat_combined": "مجموع کل",
        "hm": "{hours} ساعت و {minutes} دقیقه",
        "files": "فایل‌ها",
        "col_kind": "نوع",
        "col_file": "فایل",
        "col_duration": "مدت",
        "col_status": "وضعیت",
        "kind_video": "ویدیو",
        "kind_audio": "صدا",
        "ok": "سالم",
        "failed": "خطا",
        "stats": "پوشه‌ها: {folders}   ·   ویدیو: {video} (خوانده‌شده {video_ok})   ·   صدا: {audio} (خوانده‌شده {audio_ok})   ·   ثانیهٔ کل: {seconds}",
        "csv_written": "CSV: {name}",
        "csv_failed": "گزارش CSV نوشته نشد.",
        "open_csv": "باز کردن CSV",
        "need_folder_title": "بدون پوشه",
        "need_folder": "اول حداقل یک پوشه اضافه کنید.",
        "no_files_title": "چیزی پیدا نشد",
        "no_files": "در پوشه‌های انتخابی فایل ویدیویی یا صوتی پشتیبانی‌شده پیدا نشد.",
        "error_title": "خطا",
        "ffprobe_title": "یک تنظیم یک‌باره",
        "ffprobe_text": (
            "برای خواندن مدت هر فایل، برنامه از FFmpeg (یک ابزار رایگان رسانه) استفاده می‌کند.\n\n"
            "یک‌بار نصبش کنید:  winget install Gyan.FFmpeg\n"
            "یا اگر از قبل روی سیستم دارید، فایل ffprobe.exe را انتخاب کنید."
        ),
        "ffprobe_pick": "انتخاب ffprobe.exe…",
        "ffprobe_close": "فعلاً نه",
        "ffprobe_filter": "ffprobe (ffprobe.exe);;همهٔ فایل‌ها (*)",
        "ffprobe_bad": "این فایل ffprobe به نظر نمی‌رسد. دوباره تلاش کنید.",
        "missing_title": "پوشه‌های ناموجود",
        "missing_folders": "این پوشه‌ها دیگر وجود ندارند و رد می‌شوند:\n{paths}",
    },
}

STYLE = """
QWidget { color: #111827; }
QWidget#Central { background: #f5f6f8; }
QLabel#Title { color: #111827; font-size: 18pt; font-weight: 700; }
QLabel#Tagline { color: #6b7280; font-size: 9pt; }
QLabel#SectionTitle { color: #374151; font-size: 10pt; font-weight: 600; }
QLabel#Hint { color: #6b7280; font-size: 9pt; }
QLabel#StatTitle { color: #166534; font-size: 9pt; font-weight: 600; }
QLabel#StatValue { color: #15803d; font-size: 19pt; font-weight: 700; }
QLabel#StatSub { color: #4b5563; font-size: 9pt; }

QFrame#Card { background: #ffffff; border: 1px solid #e5e7eb; border-radius: 10px; }
QFrame#StatCard { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 10px; }

QTreeWidget {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px; padding: 4px;
    alternate-background-color: #fbfcfd;
}
QTreeWidget::item { padding: 3px 4px; border-radius: 4px; color: #111827; }
QTreeWidget::item:selected { background: #dcfce7; color: #14532d; }

QPushButton {
    background: #ffffff; border: 1px solid #d1d5db; border-radius: 8px;
    padding: 6px 14px; color: #111827;
}
QPushButton:hover { background: #f3f4f6; }
QPushButton:pressed { background: #e5e7eb; }
QPushButton:disabled { color: #9ca3af; border-color: #e5e7eb; }
QPushButton#Primary {
    background: #15803d; border: none; color: #ffffff;
    font-weight: 600; padding: 8px 22px;
}
QPushButton#Primary:hover { background: #166534; }
QPushButton#Primary:disabled { background: #86efac; }

QRadioButton { color: #111827; spacing: 6px; }

QProgressBar { border: none; border-radius: 6px; background: #e5e7eb; max-height: 12px; }
QProgressBar::chunk { background: #22c55e; border-radius: 6px; }

QTableWidget {
    background: #ffffff; border: 1px solid #e5e7eb; border-radius: 8px;
    alternate-background-color: #f9fafb; color: #111827;
    selection-background-color: #dcfce7; selection-color: #111827;
}
QHeaderView::section {
    background: #f9fafb; color: #374151; border: none;
    border-bottom: 1px solid #e5e7eb; padding: 6px 8px; font-weight: 600;
}
QTableWidget::item { padding: 2px 6px; }

QScrollBar:vertical { background: #ffffff; width: 10px; margin: 0; border: none; }
QScrollBar::handle:vertical { background: #d1d5db; border-radius: 5px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #9ca3af; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QToolTip {
    background: #111827; color: #ffffff; border: none;
    padding: 4px 8px; border-radius: 4px;
}
"""


def light_palette() -> QPalette:
    """A fixed light palette, so the app looks the same in Windows dark mode."""
    palette = QPalette()
    colors = {
        QPalette.ColorRole.Window: "#f5f6f8",
        QPalette.ColorRole.WindowText: "#111827",
        QPalette.ColorRole.Base: "#ffffff",
        QPalette.ColorRole.AlternateBase: "#f9fafb",
        QPalette.ColorRole.ToolTipBase: "#ffffff",
        QPalette.ColorRole.ToolTipText: "#111827",
        QPalette.ColorRole.Text: "#111827",
        QPalette.ColorRole.Button: "#ffffff",
        QPalette.ColorRole.ButtonText: "#111827",
        QPalette.ColorRole.BrightText: "#b91c1c",
        QPalette.ColorRole.Highlight: "#dcfce7",
        QPalette.ColorRole.HighlightedText: "#111827",
        QPalette.ColorRole.PlaceholderText: "#9ca3af",
    }
    for role, value in colors.items():
        palette.setColor(role, QColor(value))
    return palette


# --------------------------------------------------------------------------- #
# Core logic (GUI-free, so it can be tested on its own)
# --------------------------------------------------------------------------- #

def format_hms(seconds: float) -> str:
    """Seconds -> h:mm:ss, never wrapping at 24 hours."""
    total = int(round(seconds))
    hours, rest = divmod(total, 3600)
    minutes, secs = divmod(rest, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}"


def format_hm(seconds: float, lang: str) -> str:
    """Seconds -> '96 hours and 12 minutes' (rounded to the nearest minute)."""
    minutes_total = int(round(seconds / 60))
    hours, minutes = divmod(minutes_total, 60)
    return STRINGS[lang]["hm"].format(hours=hours, minutes=minutes)


def default_language() -> str:
    """Open in Persian on a Persian Windows, English everywhere else."""
    if os.name == "nt":
        try:
            import ctypes

            if (ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0x3FF) == 0x29:
                return "fa"
        except Exception:  # noqa: BLE001 - best effort only
            pass
    return "en"


def find_ffprobe() -> str | None:
    """Look on PATH, then in the usual WinGet / FFmpeg install folders."""
    found = shutil.which("ffprobe")
    if found:
        return found
    candidates = []
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        candidates.append(Path(local_app_data) / "Microsoft" / "WinGet" / "Links" / "ffprobe.exe")
    candidates += [
        Path("C:/ffmpeg/bin/ffprobe.exe"),
        Path("C:/Program Files/ffmpeg/bin/ffprobe.exe"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return None


def read_duration(ffprobe: str, path: str, timeout: float = 30.0) -> float | None:
    """Return the container duration in seconds, or None if ffprobe cannot read it."""
    command = [
        ffprobe, "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        "-i", path,
    ]
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            creationflags=CREATE_NO_WINDOW,
        )
    except (OSError, subprocess.SubprocessError):
        return None

    lines = (completed.stdout or "").strip().splitlines()
    if not lines:
        return None
    try:
        value = float(lines[0].strip())
    except ValueError:
        return None
    if not math.isfinite(value) or value <= 0:
        return None
    return value


def scan_folders(folders, include: str, ffprobe: str, cancel=None, progress=None) -> dict:
    """Scan folders and read durations.

    `progress(index, total, name)` is called while reading durations; during the
    discovery pass it is called as `progress(0, 0, count)`.
    """
    cancel = cancel or threading.Event()
    progress = progress or (lambda *args: None)
    wanted = ("Video", "Audio") if include == "Both" else (include,)

    started = time.perf_counter()
    items = []
    seen = set()
    scanned = 0
    for folder in folders:
        if cancel.is_set():
            break
        for root, _dirs, files in os.walk(folder, onerror=lambda _err: None):
            if cancel.is_set():
                break
            for name in files:
                scanned += 1
                extension = os.path.splitext(name)[1].lower()
                if extension in VIDEO_EXTENSIONS:
                    kind = "Video"
                elif extension in AUDIO_EXTENSIONS:
                    kind = "Audio"
                else:
                    continue
                if kind not in wanted:
                    continue
                full_path = os.path.join(root, name)
                key = os.path.normcase(os.path.abspath(full_path))
                if key in seen:
                    continue
                seen.add(key)
                items.append((full_path, kind))
            progress(0, 0, str(scanned))

    totals = {"Video": 0.0, "Audio": 0.0}
    counts = {"Video": {"found": 0, "read": 0}, "Audio": {"found": 0, "read": 0}}
    rows = []
    cancelled = cancel.is_set()

    for index, (full_path, kind) in enumerate(items, start=1):
        if cancel.is_set():
            cancelled = True
            break
        progress(index, len(items), os.path.basename(full_path))
        counts[kind]["found"] += 1

        seconds = read_duration(ffprobe, full_path)
        if seconds is not None:
            totals[kind] += seconds
            counts[kind]["read"] += 1

        try:
            size_mb = round(os.path.getsize(full_path) / (1024 * 1024), 2)
        except OSError:
            size_mb = 0.0

        rows.append({
            "kind": kind,
            "path": full_path,
            "size_mb": size_mb,
            "seconds": round(seconds, 3) if seconds is not None else None,
            "duration": format_hms(seconds) if seconds is not None else "",
            "status": "OK" if seconds is not None else "FAILED",
        })

    return {
        "folders": list(folders),
        "include": include,
        "rows": rows,
        "totals": totals,
        "counts": counts,
        "cancelled": cancelled,
        "elapsed": time.perf_counter() - started,
    }


def build_folder_stats(rows, roots) -> dict:
    """Aggregate per-folder durations for the folder tree.

    Returns {root_path: node} where each node is
    {"path", "seconds", "video_seconds", "audio_seconds", "files", "children": {path: node}}.
    A node's values include everything in its subtree, so a parent shows the total.
    """
    nodes: dict[str, dict] = {}

    def node_for(path: str) -> dict:
        key = os.path.normcase(path)
        node = nodes.get(key)
        if node is None:
            node = {"path": path, "seconds": 0.0, "video_seconds": 0.0, "audio_seconds": 0.0, "files": 0, "children": {}}
            nodes[key] = node
        return node

    root_lookup = {os.path.normcase(os.path.abspath(root)): os.path.abspath(root) for root in roots}

    for row in rows:
        if row["seconds"] is None:
            continue
        parent = os.path.dirname(os.path.abspath(row["path"]))
        kind = row["kind"]
        seconds = row["seconds"]

        root_path = None
        current = parent
        while True:
            found = root_lookup.get(os.path.normcase(current))
            if found is not None:
                root_path = found
                break
            parent_dir = os.path.dirname(current)
            if parent_dir == current:
                break
            current = parent_dir
        if root_path is None:
            continue

        current = parent
        while True:
            node = node_for(current)
            node["seconds"] += seconds
            if kind == "Video":
                node["video_seconds"] += seconds
            else:
                node["audio_seconds"] += seconds
            node["files"] += 1
            if os.path.normcase(current) == os.path.normcase(root_path):
                break
            parent_dir = os.path.dirname(current)
            if parent_dir == current:
                break
            current = parent_dir

    for node in nodes.values():
        parent_dir = os.path.dirname(node["path"])
        parent_node = nodes.get(os.path.normcase(parent_dir))
        if parent_node is not None and os.path.normcase(parent_dir) != os.path.normcase(node["path"]):
            parent_node["children"][node["path"]] = node

    return {
        root: nodes.get(os.path.normcase(os.path.abspath(root)))
        for root in roots
    }


def write_csv(rows) -> Path | None:
    """Write media_durations-<timestamp>.csv next to the script, else in %TEMP%."""
    stamp = time.strftime("%Y%m%d-%H%M%S")
    for base in (SCRIPT_DIR, Path(tempfile.gettempdir())):
        target = base / f"media_durations-{stamp}.csv"
        try:
            with open(target, "w", newline="", encoding="utf-8-sig") as handle:
                writer = csv.writer(handle)
                writer.writerow(["Kind", "Path", "SizeMB", "DurationSeconds", "Duration", "Status"])
                for row in rows:
                    writer.writerow([
                        row["kind"],
                        row["path"],
                        f'{row["size_mb"]:.2f}',
                        "" if row["seconds"] is None else f'{row["seconds"]:.3f}',
                        row["duration"],
                        row["status"],
                    ])
            return target
        except OSError:
            continue
    return None


# --------------------------------------------------------------------------- #
# Settings
# --------------------------------------------------------------------------- #

def settings_file() -> Path:
    base = os.getenv("APPDATA") or os.getenv("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base) / "video-duration-calculator" / "settings.json"


def load_settings() -> dict:
    try:
        with open(settings_file(), "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_settings(data: dict) -> None:
    try:
        target = settings_file()
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
    except OSError:
        pass


# --------------------------------------------------------------------------- #
# Worker thread
# --------------------------------------------------------------------------- #

class ScanThread(QThread):
    progressed = Signal(int, int, str)   # index, total (0 = discovery), name/count
    completed = Signal(dict)
    failed = Signal(str)

    def __init__(self, folders, include, ffprobe, cancel_event, parent=None):
        super().__init__(parent)
        self.folders = folders
        self.include = include
        self.ffprobe = ffprobe
        self.cancel_event = cancel_event

    def run(self) -> None:
        try:
            result = scan_folders(
                self.folders,
                self.include,
                self.ffprobe,
                cancel=self.cancel_event,
                progress=lambda index, total, name: self.progressed.emit(index, total, name),
            )
        except Exception as exc:  # noqa: BLE001 - reported in the UI
            self.failed.emit(str(exc))
            return
        self.completed.emit(result)


# --------------------------------------------------------------------------- #
# Main window
# --------------------------------------------------------------------------- #

class MainWindow(QMainWindow):
    def __init__(self, initial_folders=()):
        super().__init__()
        app = QApplication.instance()
        if app is not None:
            configure_app(app)
        self.settings = load_settings()
        saved_lang = self.settings.get("lang")
        self.lang = saved_lang if saved_lang in STRINGS else default_language()
        self.s = STRINGS[self.lang]

        self.folders: list[str] = []
        self.rows: list[dict] = []
        self.folder_stats: dict | None = None
        self.scanned_folders = 0
        self.totals = {"Video": 0.0, "Audio": 0.0}
        self.counts = {"Video": {"found": 0, "read": 0}, "Audio": {"found": 0, "read": 0}}
        self.csv_path: Path | None = None

        self.ffprobe = find_ffprobe() or self.settings.get("ffprobe") or ""
        if self.ffprobe and not Path(self.ffprobe).is_file():
            self.ffprobe = ""

        self.scan_thread: ScanThread | None = None
        self.cancel_event = threading.Event()
        self.status_key: str | None = "ready"
        self.status_args: dict = {}
        self.scanning = False

        self.setMinimumSize(860, 660)
        self.resize(1040, 820)
        self.setAcceptDrops(True)

        self._build_ui()
        self._apply_language()

        for folder in list(initial_folders) + list(self.settings.get("folders") or []):
            self._add_folder_path(folder)

    # -- construction ------------------------------------------------------ #

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("Central")
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(20, 16, 20, 16)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        self.lbl_title = QLabel()
        self.lbl_title.setObjectName("Title")
        self.lbl_tagline = QLabel()
        self.lbl_tagline.setObjectName("Tagline")
        title_box.addWidget(self.lbl_title)
        title_box.addWidget(self.lbl_tagline)
        header.addLayout(title_box)
        header.addStretch(1)
        self.btn_lang = QPushButton()
        self.btn_lang.setObjectName("LangSwitch")
        self.btn_lang.setFixedWidth(104)
        self.btn_lang.clicked.connect(self.toggle_language)
        header.addWidget(self.btn_lang, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(header)

        # Folders card
        self.card_folders = QFrame()
        self.card_folders.setObjectName("Card")
        folders_layout = QVBoxLayout(self.card_folders)
        folders_layout.setContentsMargins(14, 12, 14, 14)
        folders_layout.setSpacing(8)

        self.lbl_folders = QLabel()
        self.lbl_folders.setObjectName("SectionTitle")
        folders_layout.addWidget(self.lbl_folders)

        folders_row = QHBoxLayout()
        folders_row.setSpacing(8)
        self.tree_folders = QTreeWidget()
        self.tree_folders.setColumnCount(5)
        self.tree_folders.setFixedHeight(150)
        self.tree_folders.setRootIsDecorated(True)
        self.tree_folders.setUniformRowHeights(True)
        self.tree_folders.setAlternatingRowColors(True)
        self.tree_folders.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        tree_header = self.tree_folders.header()
        tree_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        tree_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        tree_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        tree_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        tree_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.tree_folders.setColumnWidth(1, 100)
        self.tree_folders.setColumnWidth(2, 90)
        self.tree_folders.setColumnWidth(3, 90)
        self.tree_folders.setColumnWidth(4, 70)
        self.tree_folders.itemSelectionChanged.connect(self._on_folder_selection_changed)
        folders_row.addWidget(self.tree_folders, 1)

        folder_buttons = QVBoxLayout()
        folder_buttons.setSpacing(6)
        self.btn_add = QPushButton()
        self.btn_add.setFixedWidth(132)
        self.btn_add.clicked.connect(self.add_folders)
        self.btn_remove = QPushButton()
        self.btn_remove.setFixedWidth(132)
        self.btn_remove.clicked.connect(self.remove_selected)
        self.btn_clear = QPushButton()
        self.btn_clear.setFixedWidth(132)
        self.btn_clear.clicked.connect(self.clear_folders)
        folder_buttons.addWidget(self.btn_add)
        folder_buttons.addWidget(self.btn_remove)
        folder_buttons.addWidget(self.btn_clear)
        folder_buttons.addStretch(1)
        folders_row.addLayout(folder_buttons)
        folders_layout.addLayout(folders_row)

        self.lbl_hint = QLabel()
        self.lbl_hint.setObjectName("Hint")
        self.lbl_hint.setWordWrap(True)
        folders_layout.addWidget(self.lbl_hint)
        root.addWidget(self.card_folders)

        # What to count
        mode_row = QHBoxLayout()
        mode_row.setSpacing(10)
        self.lbl_mode = QLabel()
        mode_row.addWidget(self.lbl_mode)
        self.mode_group = QButtonGroup(self)
        self.radios: dict[str, QRadioButton] = {}
        for value in ("Both", "Video", "Audio"):
            radio = QRadioButton()
            self.mode_group.addButton(radio)
            self.radios[value] = radio
            mode_row.addWidget(radio)
        self.radios["Both"].setChecked(True)
        mode_row.addStretch(1)
        root.addLayout(mode_row)

        # Actions
        actions = QHBoxLayout()
        actions.setSpacing(10)
        self.btn_scan = QPushButton()
        self.btn_scan.setObjectName("Primary")
        self.btn_scan.setMinimumHeight(38)
        self.btn_scan.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_scan.clicked.connect(self.start_scan)
        actions.addWidget(self.btn_scan)

        self.btn_cancel = QPushButton()
        self.btn_cancel.setMinimumHeight(38)
        self.btn_cancel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.btn_cancel.clicked.connect(self.cancel_scan)
        self.btn_cancel.hide()
        actions.addWidget(self.btn_cancel)

        self.progress_holder = QWidget()
        holder_layout = QHBoxLayout(self.progress_holder)
        holder_layout.setContentsMargins(0, 0, 0, 0)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        self.progress.hide()
        holder_layout.addWidget(self.progress)
        actions.addWidget(self.progress_holder, 1)
        root.addLayout(actions)

        self.lbl_status = QLabel()
        self.lbl_status.setObjectName("Hint")
        root.addWidget(self.lbl_status)

        # Totals
        self.stats_row = QHBoxLayout()
        self.stats_row.setSpacing(12)
        self.stat_widgets: dict[str, tuple[QFrame, QLabel, QLabel, QLabel]] = {}
        for key in ("Video", "Audio", "Combined"):
            card = QFrame()
            card.setObjectName("StatCard")
            card.setMinimumWidth(190)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(14, 10, 14, 12)
            card_layout.setSpacing(0)
            title = QLabel()
            title.setObjectName("StatTitle")
            value = QLabel()
            value.setObjectName("StatValue")
            sub = QLabel()
            sub.setObjectName("StatSub")
            card_layout.addWidget(title)
            card_layout.addWidget(value)
            card_layout.addWidget(sub)
            card.hide()
            self.stats_row.addWidget(card)
            self.stat_widgets[key] = (card, title, value, sub)
        self.stats_row.addStretch(1)
        root.addLayout(self.stats_row)

        # Files table
        self.card_files = QFrame()
        self.card_files.setObjectName("Card")
        files_layout = QVBoxLayout(self.card_files)
        files_layout.setContentsMargins(14, 12, 14, 14)
        files_layout.setSpacing(8)

        self.lbl_files = QLabel()
        self.lbl_files.setObjectName("SectionTitle")
        files_layout.addWidget(self.lbl_files)

        self.table = QTableWidget(0, 4)
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setWordWrap(False)
        table_header = self.table.horizontalHeader()
        table_header.setHighlightSections(False)
        table_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        table_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        table_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        table_header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 100)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 100)
        self.table.verticalHeader().setDefaultSectionSize(26)
        files_layout.addWidget(self.table, 1)
        root.addWidget(self.card_files, 1)

        # Footer
        footer = QGridLayout()
        footer.setHorizontalSpacing(10)
        footer.setVerticalSpacing(2)
        footer.setColumnStretch(0, 1)
        self.lbl_stats = QLabel()
        self.lbl_stats.setObjectName("Hint")
        self.lbl_csv = QLabel()
        self.lbl_csv.setObjectName("Hint")
        footer.addWidget(self.lbl_stats, 0, 0)
        footer.addWidget(self.lbl_csv, 1, 0)
        self.btn_open_csv = QPushButton()
        self.btn_open_csv.setEnabled(False)
        self.btn_open_csv.clicked.connect(self.open_csv)
        footer.addWidget(self.btn_open_csv, 0, 1, 2, 1, Qt.AlignmentFlag.AlignBottom)
        root.addLayout(footer)

    # -- language & styling ------------------------------------------------ #

    def toggle_language(self) -> None:
        self.lang = "fa" if self.lang == "en" else "en"
        self._apply_language()
        self.settings["lang"] = self.lang
        save_settings(self.settings)

    def _apply_language(self) -> None:
        self.s = STRINGS[self.lang]
        s = self.s
        rtl = self.lang == "fa"

        app = QApplication.instance()
        app.setLayoutDirection(
            Qt.LayoutDirection.RightToLeft if rtl else Qt.LayoutDirection.LeftToRight
        )
        family = "Tahoma" if rtl else "Segoe UI"
        app.setFont(QFont(family, 10))
        self.setFont(QFont(family, 10))

        self.setWindowTitle(f'{s["app_title"]} {APP_VERSION}')
        self.lbl_title.setText(s["app_title"])
        self.lbl_tagline.setText(s["tagline"])
        self.btn_lang.setText(s["switch_lang"])

        self.lbl_folders.setText(s["folders"])
        self.btn_add.setText(s["add_folder"])
        self.btn_remove.setText(s["remove"])
        self.btn_clear.setText(s["clear"])
        self.lbl_hint.setText(s["folders_hint"])

        self.lbl_mode.setText(s["mode"] + ":")
        self.radios["Both"].setText(s["mode_both"])
        self.radios["Video"].setText(s["mode_video"])
        self.radios["Audio"].setText(s["mode_audio"])

        self.btn_scan.setText(s["scan"])
        self.btn_cancel.setText(s["cancel"])
        if self.status_key:
            self._show_status(
                s[self.status_key].format(**self.status_args),
                self.status_key,
                **self.status_args,
            )

        for key, (_card, title, _value, _sub) in self.stat_widgets.items():
            title.setText(s["stat_" + key.lower()])

        self.lbl_files.setText(s["files"])
        self.table.setHorizontalHeaderLabels(
            [s["col_kind"], s["col_file"], s["col_duration"], s["col_status"]]
        )
        for index in range(self.table.columnCount()):
            item = self.table.horizontalHeaderItem(index)
            if item is None:
                continue
            if index == 1:
                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
            else:
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.btn_open_csv.setText(s["open_csv"])

        self.tree_folders.setHeaderLabels(
            [s["col_folder"], s["col_total"], s["col_video"], s["col_audio"], s["col_files"]]
        )

        self.setStyleSheet(STYLE)
        self._refresh_folder_tree()
        self._refresh_totals()
        self._refresh_summary()
        self._refresh_table()

    def _show_status(self, text: str, key: str | None = None, **kwargs) -> None:
        """Remember which message is shown so a language switch can rebuild it."""
        self.status_key = key
        self.status_args = kwargs
        self.lbl_status.setText(text)

    # -- folders ----------------------------------------------------------- #

    @staticmethod
    def _normalize(path: str) -> str:
        return os.path.normcase(os.path.abspath(path))

    def _is_within(self, path: str, parent: str) -> bool:
        child_key = self._normalize(path).rstrip("\\/")
        parent_key = self._normalize(parent).rstrip("\\/")
        return child_key == parent_key or child_key.startswith(parent_key + os.sep)

    def _add_folder_path(self, path: str) -> tuple[str, str]:
        """Add a folder as a tree root.

        Returns (status, root) where status is "added", "inside" (the folder is
        already covered by an existing root), "duplicate" or "invalid".
        """
        path = (path or "").strip().strip('"')
        if not path or not os.path.isdir(path):
            return "invalid", ""
        path = os.path.abspath(path)

        if any(self._normalize(existing) == self._normalize(path) for existing in self.folders):
            return "duplicate", path

        inside_root = next(
            (existing for existing in self.folders if self._is_within(path, existing)),
            None,
        )
        if inside_root is not None:
            return "inside", inside_root

        # A newly added parent takes over the roots it contains.
        absorbed = [existing for existing in self.folders if self._is_within(existing, path)]
        if absorbed:
            self.folders = [existing for existing in self.folders if existing not in absorbed]
        self.folders.append(path)

        self._invalidate_results()
        self._refresh_folder_tree()
        return "added", path

    def _refresh_folder_tree(self) -> None:
        self.tree_folders.clear()
        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_DirIcon)
        stats = self.folder_stats or {}
        for root in self.folders:
            node = stats.get(root)
            item = self._make_folder_item(root, root, node, icon, top=True)
            self.tree_folders.addTopLevelItem(item)
            if node:
                item.setExpanded(True)
        self._on_folder_selection_changed()

    def _make_folder_item(self, path, label, node, icon, top=False) -> QTreeWidgetItem:
        if node:
            total_sec = node["seconds"]
            video_sec = node.get("video_seconds", 0.0)
            audio_sec = node.get("audio_seconds", 0.0)
            files = node["files"]
            total_str = format_hms(total_sec) if total_sec > 0 else "—"
            video_str = format_hms(video_sec) if video_sec > 0 else "—"
            audio_str = format_hms(audio_sec) if audio_sec > 0 else "—"
            files_str = str(files)
        else:
            total_str = video_str = audio_str = "—"
            files_str = ""
        item = QTreeWidgetItem([label, total_str, video_str, audio_str, files_str])
        item.setToolTip(0, path)
        item.setIcon(0, icon)
        item.setData(0, Qt.ItemDataRole.UserRole, path)
        item.setTextAlignment(1, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(2, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(3, Qt.AlignmentFlag.AlignCenter)
        item.setTextAlignment(4, Qt.AlignmentFlag.AlignCenter)
        if top:
            font = item.font(0)
            font.setBold(True)
            for column in range(5):
                item.setFont(column, font)
        if node:
            children = sorted(
                node["children"].values(),
                key=lambda child: (-child["seconds"], os.path.basename(child["path"]).lower()),
            )
            for child in children:
                item.addChild(self._make_folder_item(
                    child["path"],
                    os.path.basename(child["path"]) or child["path"],
                    child,
                    icon,
                ))
        return item

    def _on_folder_selection_changed(self) -> None:
        has_root = any(item.parent() is None for item in self.tree_folders.selectedItems())
        self.btn_remove.setEnabled(has_root and not self.scanning)

    def _invalidate_results(self) -> None:
        if not self.rows and self.folder_stats is None:
            return
        self.rows = []
        self.folder_stats = None
        self.scanned_folders = 0
        self.totals = {"Video": 0.0, "Audio": 0.0}
        self.counts = {"Video": {"found": 0, "read": 0}, "Audio": {"found": 0, "read": 0}}
        self.csv_path = None
        self.table.setRowCount(0)
        self.lbl_stats.clear()
        self.lbl_csv.clear()
        self.btn_open_csv.setEnabled(False)
        self._refresh_totals()
        self._show_status(self.s["ready"], "ready")

    def add_folders(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, self.s["add_folder"], "")
        if not chosen:
            return
        status, root = self._add_folder_path(chosen)
        name = os.path.basename(chosen.rstrip("\\/")) or chosen
        if status == "inside":
            self._show_status(
                self.s["folder_inside"].format(name=name, root=root),
                "folder_inside", name=name, root=root,
            )
        elif status == "added":
            self._show_status(
                self.s["folders_added"].format(count=1), "folders_added", count=1
            )

    def remove_selected(self) -> None:
        roots = []
        for item in self.tree_folders.selectedItems():
            top = item
            while top.parent() is not None:
                top = top.parent()
            path = top.data(0, Qt.ItemDataRole.UserRole)
            if path and path not in roots:
                roots.append(path)
        if not roots:
            return
        self.folders = [folder for folder in self.folders if folder not in roots]
        self._invalidate_results()
        self._refresh_folder_tree()

    def clear_folders(self) -> None:
        self.folders.clear()
        self._invalidate_results()
        self._refresh_folder_tree()

    # -- drag & drop ------------------------------------------------------- #

    def dragEnterEvent(self, event) -> None:  # noqa: N802 - Qt override
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event) -> None:  # noqa: N802 - Qt override
        added = 0
        for url in event.mimeData().urls():
            if self._add_folder_path(url.toLocalFile()):
                added += 1
        if added:
            self._show_status(
                self.s["folders_added"].format(count=added), "folders_added", count=added
            )
        event.acceptProposedAction()

    # -- scanning ---------------------------------------------------------- #

    def start_scan(self) -> None:
        if self.scan_thread and self.scan_thread.isRunning():
            return
        if not self.folders:
            QMessageBox.information(self, self.s["need_folder_title"], self.s["need_folder"])
            return

        missing = [folder for folder in self.folders if not os.path.isdir(folder)]
        if missing:
            QMessageBox.warning(
                self,
                self.s["missing_title"],
                self.s["missing_folders"].format(paths="\n".join(missing)),
            )
            self.folders = [folder for folder in self.folders if os.path.isdir(folder)]
            self._refresh_folder_tree()
            if not self.folders:
                return

        self.ffprobe = find_ffprobe() or self.ffprobe
        if not (self.ffprobe and Path(self.ffprobe).is_file()):
            if not self._ask_for_ffprobe():
                return

        self.settings["folders"] = list(self.folders)
        save_settings(self.settings)

        self.rows = []
        self.csv_path = None
        self.totals = {"Video": 0.0, "Audio": 0.0}
        self.counts = {"Video": {"found": 0, "read": 0}, "Audio": {"found": 0, "read": 0}}
        self.table.setRowCount(0)
        self.lbl_stats.clear()
        self.lbl_csv.clear()
        self.btn_open_csv.setEnabled(False)
        self._refresh_totals()

        self.btn_scan.setEnabled(False)
        self.btn_cancel.show()
        for button in (self.btn_add, self.btn_remove, self.btn_clear):
            button.setEnabled(False)
        self.progress.show()
        self.progress.setRange(0, 0)
        self._show_status(self.s["discovering"].format(count=0), "discovering", count=0)

        self.cancel_event.clear()
        self.scanning = True
        include = next(
            value for value, radio in self.radios.items() if radio.isChecked()
        )
        self.scan_thread = ScanThread(
            list(self.folders), include, self.ffprobe, self.cancel_event, self
        )
        self.scan_thread.progressed.connect(self._on_progress)
        self.scan_thread.completed.connect(self._on_completed)
        self.scan_thread.failed.connect(self._on_failed)
        self.scan_thread.finished.connect(self._on_thread_finished)
        self.scan_thread.start()

    def _ask_for_ffprobe(self) -> bool:
        box = QMessageBox(self)
        box.setWindowTitle(self.s["ffprobe_title"])
        box.setText(self.s["ffprobe_text"])
        pick_button = box.addButton(self.s["ffprobe_pick"], QMessageBox.ButtonRole.AcceptRole)
        box.addButton(self.s["ffprobe_close"], QMessageBox.ButtonRole.RejectRole)
        box.exec()
        if box.clickedButton() is not pick_button:
            return False

        chosen, _ = QFileDialog.getOpenFileName(
            self, self.s["ffprobe_pick"], "", self.s["ffprobe_filter"]
        )
        if not chosen:
            return False
        if "ffprobe" not in Path(chosen).name.lower():
            QMessageBox.warning(self, self.s["error_title"], self.s["ffprobe_bad"])
            return False
        self.ffprobe = chosen
        self.settings["ffprobe"] = chosen
        save_settings(self.settings)
        return True

    def _on_progress(self, index: int, total: int, name: str) -> None:
        if total:
            if self.progress.maximum() != total:
                self.progress.setRange(0, total)
            self.progress.setValue(index)
            self._show_status(f'{self.s["scanning"]} {index} / {total} — {name}')
        else:
            self._show_status(self.s["discovering"].format(count=name), "discovering", count=name)

    def _on_completed(self, result: dict) -> None:
        self.rows = result["rows"]
        self.totals = result["totals"]
        self.counts = result["counts"]
        self.scanned_folders = len(result["folders"])

        self.folder_stats = build_folder_stats(self.rows, result["folders"])

        self._refresh_table()
        self._refresh_totals()
        self._refresh_summary()
        self._refresh_folder_tree()

        if result["cancelled"]:
            self._show_status(self.s["cancelled"], "cancelled")
        else:
            self._show_status(
                self.s["done"].format(seconds=result["elapsed"]), "done", seconds=result["elapsed"]
            )

        self.csv_path = write_csv(self.rows) if self.rows else None
        if self.csv_path:
            self.lbl_csv.setText(self.s["csv_written"].format(name=self.csv_path.name))
            self.lbl_csv.setToolTip(str(self.csv_path))
            self.btn_open_csv.setEnabled(True)
        elif self.rows:
            self.lbl_csv.setText(self.s["csv_failed"])

        self._reset_controls()

        if not self.rows and not result["cancelled"]:
            QMessageBox.information(self, self.s["no_files_title"], self.s["no_files"])

    def _on_failed(self, message: str) -> None:
        self._show_status(self.s["error_title"] + ": " + message)
        self._reset_controls()
        QMessageBox.critical(self, self.s["error_title"], message)

    def _on_thread_finished(self) -> None:
        thread = self.scan_thread
        self.scan_thread = None
        if thread is not None:
            thread.deleteLater()

    def _reset_controls(self) -> None:
        self.scanning = False
        self.btn_scan.setEnabled(True)
        self.btn_cancel.hide()
        self.progress.hide()
        for button in (self.btn_add, self.btn_remove, self.btn_clear):
            button.setEnabled(True)

    def cancel_scan(self) -> None:
        if self.scan_thread and self.scan_thread.isRunning():
            self.cancel_event.set()
            self.scanning = False
            self._show_status(self.s["cancelled"], "cancelled")

    # -- rendering --------------------------------------------------------- #

    def _refresh_table(self) -> None:
        self.table.setRowCount(0)
        self.table.setRowCount(len(self.rows))
        for position, row in enumerate(self.rows):
            failed = row["status"] != "OK"
            kind_item = QTableWidgetItem(
                self.s["kind_video"] if row["kind"] == "Video" else self.s["kind_audio"]
            )
            kind_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            file_item = QTableWidgetItem(row["path"])
            file_item.setToolTip(row["path"])

            duration_item = QTableWidgetItem(row["duration"] or "—")
            duration_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            status_item = QTableWidgetItem(self.s["failed"] if failed else self.s["ok"])
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if failed:
                color = QColor("#b91c1c")
                for item in (kind_item, file_item, duration_item, status_item):
                    item.setForeground(color)

            self.table.setItem(position, 0, kind_item)
            self.table.setItem(position, 1, file_item)
            self.table.setItem(position, 2, duration_item)
            self.table.setItem(position, 3, status_item)

    def _refresh_totals(self) -> None:
        video_found = self.counts["Video"]["found"]
        audio_found = self.counts["Audio"]["found"]
        visible = {
            "Video": video_found > 0,
            "Audio": audio_found > 0,
            "Combined": video_found > 0 and audio_found > 0,
        }
        values = {
            "Video": self.totals["Video"],
            "Audio": self.totals["Audio"],
            "Combined": self.totals["Video"] + self.totals["Audio"],
        }
        for key, (card, _title, value, sub) in self.stat_widgets.items():
            if not visible[key] or values[key] <= 0:
                card.hide()
                continue
            card.show()
            value.setText(format_hms(values[key]))
            sub.setText(format_hm(values[key], self.lang))

    def _refresh_summary(self) -> None:
        if not self.rows:
            self.lbl_stats.clear()
            return
        video = self.counts["Video"]
        audio = self.counts["Audio"]
        total_seconds = self.totals["Video"] + self.totals["Audio"]
        self.lbl_stats.setText(self.s["stats"].format(
            folders=self.scanned_folders,
            video=video["found"], video_ok=video["read"],
            audio=audio["found"], audio_ok=audio["read"],
            seconds=f"{total_seconds:,.1f}",
        ))

    # -- misc -------------------------------------------------------------- #

    def open_csv(self) -> None:
        if not self.csv_path or not self.csv_path.exists():
            return
        try:
            if os.name == "nt":
                os.startfile(self.csv_path)  # type: ignore[attr-defined]
            else:
                subprocess.Popen(["xdg-open", str(self.csv_path)])
        except OSError:
            QMessageBox.critical(self, self.s["error_title"], str(self.csv_path))

    def closeEvent(self, event) -> None:  # noqa: N802 - Qt override
        if self.scan_thread and self.scan_thread.isRunning():
            self.cancel_event.set()
            self.scan_thread.wait(3000)
        self.settings["folders"] = list(self.folders)
        self.settings["lang"] = self.lang
        if self.ffprobe:
            self.settings["ffprobe"] = self.ffprobe
        save_settings(self.settings)
        super().closeEvent(event)


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #

def install_excepthook() -> None:
    def handler(exc_type, exc_value, exc_tb):
        text = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        try:
            (SCRIPT_DIR / "video_duration_gui-error.log").write_text(text, encoding="utf-8")
        except OSError:
            pass
        try:
            QMessageBox.critical(None, APP_NAME, text[-1200:])
        except Exception:  # noqa: BLE001 - last resort
            pass

    sys.excepthook = handler


def configure_app(app: QApplication) -> None:
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    app.setStyle("Fusion")
    app.setPalette(light_palette())
    app.setFont(QFont("Segoe UI", 10))


def main() -> int:
    app = QApplication(sys.argv)
    configure_app(app)
    install_excepthook()

    initial = [argument for argument in sys.argv[1:] if os.path.isdir(argument)]
    window = MainWindow(initial)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
