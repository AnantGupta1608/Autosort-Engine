<div align="center">

```
 █████╗ ██╗   ██╗████████╗ ██████╗ ███████╗ ██████╗ ██████╗ ████████╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██╔══██╗╚══██╔══╝
███████║██║   ██║   ██║   ██║   ██║███████╗██║   ██║██████╔╝   ██║   
██╔══██║██║   ██║   ██║   ██║   ██║╚════██║██║   ██║██╔══██╗   ██║   
██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████║╚██████╔╝██║  ██║   ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝  
                     E  N  G  I  N  E    v 1 . 0
```

**Automated File Organization & Management System**

*Transform a cluttered folder into a perfectly structured directory — instantly.*

---

![Python](https://img.shields.io/badge/Python-3.6%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-Open%20Source-blue?style=for-the-badge)

</div>

---

## What Is Autosort Engine?

**Autosort Engine** is a lightweight, zero-dependency Python automation tool that takes a messy, unorganized folder — like your `Downloads` — and instantly sorts every file into neat, labeled subfolders based on file type.

No manual dragging. No guessing where things go. Just one command.

---

## Features

| Feature | Description |
|---|---|
| **Smart Classification** | Recognizes **117 file extensions** across 9 categories |
| **Safe Dry-Run Preview** | Shows exactly what will change — before touching a single file |
| **Duplicate Protection** | Auto-renames conflicts as `file_1.ext`, `file_2.ext` — never overwrites |
| **Colored Terminal Output** | Clean, styled CLI with color-coded status messages |
| **Error Resilience** | Skips locked or inaccessible files and continues gracefully |
| **Zero Dependencies** | Pure Python — only uses `os`, `shutil`, `pathlib`, `datetime` |

---

## Supported Categories

> The engine recognizes **117 extensions** and sorts them into 9 smart categories.
> Anything unrecognized lands safely in **Others**.

| # | Category | Common Extensions |
|---|---|---|
| 1 | **Photos** | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` `.heic` `.raw` `.psd` |
| 2 | **Documents** | `.pdf` `.doc` `.docx` `.txt` `.xls` `.xlsx` `.ppt` `.csv` `.epub` |
| 3 | **Videos** | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.flv` `.webm` `.3gp` |
| 4 | **Music** | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.m4a` `.opus` `.wma` |
| 5 | **Archives** | `.zip` `.rar` `.7z` `.tar` `.gz` `.bz2` `.iso` `.cab` |
| 6 | **Programs** | `.exe` `.msi` `.deb` `.apk` `.bat` `.sh` `.cmd` |
| 7 | **Code** | `.py` `.js` `.html` `.css` `.java` `.cpp` `.json` `.md` `.sql` |
| 8 | **Fonts** | `.ttf` `.otf` `.woff` `.woff2` `.eot` |
| 9 | **3D Models** | `.obj` `.stl` `.fbx` `.blend` `.dae` |
| — | **Others** | *Any extension not listed above* |

---

## Quickstart

### Option A — Interactive Mode *(Recommended)*

```bash
python autosort_engine.py
```

The program will prompt you step-by-step:

```
> Path: C:\Users\Anant\Downloads
```

### Option B — Direct Argument

```bash
python autosort_engine.py "C:\Users\Anant\Downloads"
```

Pass the folder path directly and skip the prompt.

> **Requirement:** Python 3.6 or newer. No pip installs needed.

---

## How It Works — Step by Step

```
  Step 1 ── You provide a folder path
               │
               ▼
  Step 2 ── Program validates the path
             (Does it exist? Is it a folder? Is it readable?)
               │
               ▼
  Step 3 ── All top-level files are scanned
             (Subfolders and hidden files are skipped)
               │
               ▼
  Step 4 ── Each file's extension is matched to a category
             (.jpg → Photos,  .pdf → Documents,  .mp3 → Music ...)
               │
               ▼
  Step 5 ── A DRY-RUN PREVIEW is displayed
             (No files have moved yet)
               │
               ▼
  Step 6 ── YOU CONFIRM  [Y/n]
               │
               ▼
  Step 7 ── Category folders are created (if not already there)
             Files are moved into their respective folders
               │
               ▼
  Step 8 ── A summary report is printed
             (Files moved, categories created, any errors)
```

---

## Under the Hood — How It Accesses Your Computer

> The program runs **entirely on your local machine**. No internet. No uploads. No external connections.

<details>
<summary><strong>Click to expand — technical breakdown</strong></summary>

<br>

### Step 1 — You Give It a Path

You type a folder path like `C:\Users\Anant\Downloads`. That's just a string of text. Python works only within the boundary you give it — nothing else on your system is touched.

---

### Step 2 — Python Reads the File System via the OS

Python asks Windows (or macOS/Linux) to list the contents of your folder — the same thing File Explorer does when you open a folder. The library responsible:

| Library | Role |
|---|---|
| `pathlib` | Converts your path string into a real file system object and iterates through files |
| `os` | Checks read/write permissions before doing anything |

The key line in the code:
```python
for item in dir_path.iterdir():   # asks Windows: "list everything in this folder"
    if item.is_dir(): continue    # skips subfolders — only files are organized
```
`iterdir()` receives filenames and metadata from the OS. **No file is opened or read at this point** — only names are seen.

---

### Step 3 — Files Are Classified by Extension (Nothing Is Read)

The program checks only the **file extension** — the part after the dot. It never opens a file or reads its contents.

```python
extension = file_path.suffix.lower()          # e.g., ".jpg"
category  = EXTENSION_LOOKUP.get(extension, "Others")   # instant dictionary lookup
```

The `EXTENSION_LOOKUP` dictionary is built once at startup mapping every known extension to its category. Each file classification is an **O(1) lookup** — no loops, no reading, just a dictionary key check.

---

### Step 4 — Folders Are Created by Python

```python
category_dir.mkdir(exist_ok=True)
```

This tells the OS: *"Create a folder here."* If it already exists, the call is silently ignored. No data is written into these folders yet.

---

### Step 5 — Files Are Moved Using `shutil`

```python
shutil.move(str(file_path), str(dest))
```

`shutil.move` is Python's equivalent of **Cut → Paste** in File Explorer. The file is relocated within the same drive — it is not duplicated, and no file content is read. It is instant.

---

### What This Program Cannot Do

- Cannot access the internet or make any network calls
- Cannot read the contents of your files — only their names and extensions
- Cannot access any folder other than the one you specify
- Cannot run in the background automatically
- Cannot undo moves (no built-in rollback)

</details>

---

## Before & After

**Before — A chaotic Downloads folder:**

```
Downloads/
├── vacation_photo.jpg
├── Q3_Report.pdf
├── setup_chrome.exe
├── Avengers.mp4
├── project_backup.zip
├── resume.docx
├── favourite_song.mp3
├── random_script.py
└── font_pack.ttf
```

**After — Clean and organized in seconds:**

```
Downloads/
├── Photos/
│   └── vacation_photo.jpg
├── Documents/
│   ├── Q3_Report.pdf
│   └── resume.docx
├── Programs/
│   └── setup_chrome.exe
├── Videos/
│   └── Avengers.mp4
├── Archives/
│   └── project_backup.zip
├── Music/
│   └── favourite_song.mp3
├── Code/
│   └── random_script.py
└── Fonts/
    └── font_pack.ttf
```

---

## Error Handling

The engine is built to handle real-world messiness without crashing.

| Scenario | What Happens |
|---|---|
| Path doesn't exist | Clear error message → program exits safely |
| Path points to a file | Notifies you it must be a folder → exits |
| No read permission | Permission denied message → exits before any changes |
| File is locked by another app | Skips that file, logs a warning, continues the rest |
| Duplicate filename at destination | Renames to `file_1.ext`, `file_2.ext` — **never overwrites** |
| Hidden file (`.dotfile`) | Silently skipped — system files stay untouched |
| Empty directory | Informs you, exits cleanly with no changes |
| User cancels at confirmation | Program exits — **zero files are moved** |

---

## Technical Details

```
Language  :  Python 3.6+
Libraries :  pathlib · shutil · os · sys · datetime
Scope     :  Top-level files only (non-recursive by design)
Speed     :  O(1) per file — uses pre-built extension lookup dictionary
Safety    :  Always previews before moving; requires explicit confirmation
```

---

## Project Structure

```
File organizer/
├── autosort_engine.py   ← The entire program (424 lines)
└── README.md            ← This file
```

---

## Author

**Anant** — Built with Python, 2026

> *"A place for everything, and everything in its place."*

---

<div align="center">

*Made with Python · No external dependencies · Safe by design*

</div>
