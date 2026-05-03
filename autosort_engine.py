"""
╔══════════════════════════════════════════════════════════════╗
║                   AUTOSORT ENGINE v1.0                      ║
║         Automated File Organization & Management            ║
╚══════════════════════════════════════════════════════════════╝

A Python-based automation tool that scans a specified directory,
classifies files by their extensions into predefined categories,
and organizes them into structured subfolders automatically.

Uses only Python built-in libraries: os, shutil, pathlib, datetime.

Author : Anant
Created: 2026-05-03
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime


# ──────────────────────────────────────────────────────────────
# FILE CATEGORY DEFINITIONS
# Maps each category to a set of recognized file extensions.
# ──────────────────────────────────────────────────────────────

CATEGORY_MAP = {
    "Photos": {
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
        ".webp", ".tiff", ".tif", ".ico", ".heic", ".heif",
        ".raw", ".cr2", ".nef", ".psd",
    },
    "Documents": {
        ".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt",
        ".xls", ".xlsx", ".csv", ".ppt", ".pptx", ".ods",
        ".odp", ".tex", ".epub", ".pages", ".numbers", ".key",
    },
    "Videos": {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv",
        ".webm", ".m4v", ".mpg", ".mpeg", ".3gp", ".vob",
    },
    "Music": {
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma",
        ".m4a", ".opus", ".aiff", ".alac",
    },
    "Archives": {
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
        ".xz", ".iso", ".dmg", ".cab",
    },
    "Programs": {
        ".exe", ".msi", ".deb", ".rpm", ".dmg", ".app",
        ".bat", ".sh", ".cmd", ".apk",
    },
    "Code": {
        ".py", ".js", ".ts", ".jsx", ".tsx", ".html", ".css",
        ".java", ".c", ".cpp", ".h", ".hpp", ".cs", ".go",
        ".rb", ".php", ".rs", ".swift", ".kt", ".scala",
        ".sql", ".json", ".xml", ".yaml", ".yml", ".toml",
        ".ini", ".cfg", ".md", ".rst",
    },
    "Fonts": {
        ".ttf", ".otf", ".woff", ".woff2", ".eot",
    },
    "3D Models": {
        ".obj", ".stl", ".fbx", ".blend", ".3ds", ".dae",
    },
}


def build_extension_lookup():
    """
    Builds a reverse lookup dictionary: extension → category name.
    This allows O(1) classification of any file by its extension.
    """
    lookup = {}
    for category, extensions in CATEGORY_MAP.items():
        for ext in extensions:
            lookup[ext.lower()] = category
    return lookup


# Pre-build the lookup table at module load time
EXTENSION_LOOKUP = build_extension_lookup()


# ──────────────────────────────────────────────────────────────
# CONSOLE OUTPUT HELPERS
# ──────────────────────────────────────────────────────────────

# ANSI color codes for styled terminal output
class Colors:
    HEADER  = "\033[95m"
    BLUE    = "\033[94m"
    CYAN    = "\033[96m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    RED     = "\033[91m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"


def print_banner():
    """Display the application banner."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    +----------------------------------------------------------+
    |             AUTOSORT ENGINE  v1.0                         |
    |          Automated File Organization System              |
    +----------------------------------------------------------+
{Colors.RESET}"""
    print(banner)


def print_section(title):
    """Print a styled section header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'-' * 60}")
    print(f"  {title}")
    print(f"{'-' * 60}{Colors.RESET}")


def print_success(msg):
    print(f"  {Colors.GREEN}[OK]{Colors.RESET} {msg}")


def print_warning(msg):
    print(f"  {Colors.YELLOW}[!]{Colors.RESET} {msg}")


def print_error(msg):
    print(f"  {Colors.RED}[X]{Colors.RESET} {msg}")


def print_info(msg):
    print(f"  {Colors.CYAN}[i]{Colors.RESET} {msg}")


# ──────────────────────────────────────────────────────────────
# CORE ENGINE
# ──────────────────────────────────────────────────────────────

def validate_directory(dir_path):
    """
    Validates whether the provided path is a real, accessible directory.

    Args:
        dir_path (str): The directory path to validate.

    Returns:
        Path: A resolved pathlib.Path object if valid.

    Raises:
        FileNotFoundError: If the path does not exist.
        NotADirectoryError: If the path is not a directory.
        PermissionError: If the directory is not readable.
    """
    path = Path(dir_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")
    if not os.access(path, os.R_OK):
        raise PermissionError(f"No read access to directory: {path}")

    return path


def classify_file(file_path):
    """
    Determines the category of a file based on its extension.

    Args:
        file_path (Path): Path object of the file.

    Returns:
        str: The category name (e.g., "Photos", "Documents", "Others").
    """
    extension = file_path.suffix.lower()
    return EXTENSION_LOOKUP.get(extension, "Others")


def scan_directory(dir_path):
    """
    Scans a directory and classifies every file into categories.

    Only top-level files are scanned (not files inside subfolders).
    Folders and hidden system files are skipped.

    Args:
        dir_path (Path): The directory to scan.

    Returns:
        dict: A dictionary mapping category names to lists of file Paths.
              Example: {"Photos": [Path("a.jpg")], "Documents": [Path("b.pdf")]}
    """
    categorized = {}
    skipped = []

    for item in dir_path.iterdir():
        # Skip directories — we only organize files
        if item.is_dir():
            continue

        # Skip hidden files (starting with .)
        if item.name.startswith("."):
            skipped.append(item.name)
            continue

        # Skip the autosort script itself if it's in the target directory
        if item.name == "autosort_engine.py":
            continue

        category = classify_file(item)
        categorized.setdefault(category, []).append(item)

    if skipped:
        print_warning(f"Skipped {len(skipped)} hidden file(s)")

    return categorized


def organize_files(dir_path, categorized, dry_run=False):
    """
    Moves files into their respective category subfolders.

    If dry_run is True, no files are actually moved — the function
    only prints what *would* happen. This is useful for previewing
    the organization before committing.

    Args:
        dir_path (Path): The root directory being organized.
        categorized (dict): Output from scan_directory().
        dry_run (bool): If True, simulate without moving files.

    Returns:
        dict: Summary statistics with counts per category and any errors.
    """
    stats = {
        "moved": 0,
        "errors": 0,
        "categories": {},
    }

    for category, files in sorted(categorized.items()):
        category_dir = dir_path / category

        # Create the category folder if it doesn't exist
        if not dry_run:
            try:
                category_dir.mkdir(exist_ok=True)
            except OSError as e:
                print_error(f"Could not create folder '{category}': {e}")
                stats["errors"] += len(files)
                continue

        stats["categories"][category] = 0

        for file_path in files:
            dest = category_dir / file_path.name

            # Handle filename conflicts by appending a counter
            if dest.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                counter = 1
                while dest.exists():
                    dest = category_dir / f"{stem}_{counter}{suffix}"
                    counter += 1

            if dry_run:
                print_info(f"[DRY RUN] {file_path.name}  →  {category}/")
            else:
                try:
                    shutil.move(str(file_path), str(dest))
                    print_success(f"{file_path.name}  →  {category}/")
                    stats["moved"] += 1
                    stats["categories"][category] += 1
                except PermissionError:
                    print_error(f"Permission denied: {file_path.name}")
                    stats["errors"] += 1
                except shutil.Error as e:
                    print_error(f"Could not move {file_path.name}: {e}")
                    stats["errors"] += 1
                except OSError as e:
                    print_error(f"OS error moving {file_path.name}: {e}")
                    stats["errors"] += 1

    return stats


def print_summary(categorized, stats, dry_run=False):
    """Print a formatted summary of the organization results."""
    total_files = sum(len(f) for f in categorized.values())

    print_section("SUMMARY")

    mode_label = " (DRY RUN)" if dry_run else ""
    print(f"\n  Total files found  : {Colors.BOLD}{total_files}{Colors.RESET}")
    print(f"  Categories created : {Colors.BOLD}{len(categorized)}{Colors.RESET}")

    if not dry_run:
        print(f"  Files moved        : {Colors.GREEN}{stats['moved']}{Colors.RESET}")
        if stats["errors"]:
            print(f"  Errors             : {Colors.RED}{stats['errors']}{Colors.RESET}")

    # Category breakdown table
    if categorized:
        print(f"\n  {'Category':<15} {'Files':>6}")
        print(f"  {'-' * 23}")
        for category in sorted(categorized.keys()):
            count = len(categorized[category])
            print(f"  {category:<15} {count:>6}")
        print(f"  {'-' * 23}")
        print(f"  {'TOTAL':<15} {total_files:>6}")

    print()


def print_supported_categories():
    """Display all supported categories and their extensions."""
    print_section("SUPPORTED CATEGORIES")
    for category, extensions in sorted(CATEGORY_MAP.items()):
        ext_list = ", ".join(sorted(extensions))
        print(f"\n  {Colors.BOLD}{category}{Colors.RESET}")
        print(f"  {Colors.DIM}{ext_list}{Colors.RESET}")
    print(f"\n  {Colors.BOLD}Others{Colors.RESET}")
    print(f"  {Colors.DIM}Any extension not listed above{Colors.RESET}\n")


# ──────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ──────────────────────────────────────────────────────────────

def main():
    """
    Main function — interactive CLI for the Autosort Engine.

    Workflow:
      1. Display banner
      2. Prompt user for a directory path
      3. Scan and classify all files
      4. Show a dry-run preview
      5. Ask for confirmation before moving files
      6. Move files and display summary
    """
    print_banner()

    # ── Get directory path ──────────────────────────────
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
        print_info(f"Target directory (from argument): {target_dir}")
    else:
        print(f"  {Colors.BOLD}Enter the directory path to organize{Colors.RESET}")
        print(f"  {Colors.DIM}(e.g., C:\\Users\\You\\Downloads){Colors.RESET}\n")
        target_dir = input(f"  {Colors.CYAN}>{Colors.RESET} Path: ").strip()

    if not target_dir:
        print_error("No directory path provided. Exiting.")
        sys.exit(1)

    # ── Validate directory ──────────────────────────────
    try:
        dir_path = validate_directory(target_dir)
    except FileNotFoundError as e:
        print_error(str(e))
        sys.exit(1)
    except NotADirectoryError as e:
        print_error(str(e))
        sys.exit(1)
    except PermissionError as e:
        print_error(str(e))
        sys.exit(1)

    print_success(f"Directory validated: {dir_path}")

    # ── Scan and classify ───────────────────────────────
    print_section("SCANNING FILES")

    categorized = scan_directory(dir_path)

    if not categorized:
        print_warning("No files found to organize. The directory is empty or")
        print_warning("contains only folders/hidden files.")
        sys.exit(0)

    total_files = sum(len(f) for f in categorized.values())
    print_success(f"Found {total_files} file(s) across {len(categorized)} category(ies)")

    # ── Dry-run preview ─────────────────────────────────
    print_section("PREVIEW (Dry Run)")

    for category in sorted(categorized.keys()):
        files = categorized[category]
        print(f"\n  {Colors.BOLD}{Colors.CYAN}{category}/{Colors.RESET}")
        for f in files:
            print(f"    {Colors.DIM}|--{Colors.RESET} {f.name}")

    # ── Confirm ─────────────────────────────────────────
    print(f"\n  {Colors.YELLOW}{Colors.BOLD}Proceed with organizing {total_files} file(s)?{Colors.RESET}")
    confirm = input(f"  {Colors.CYAN}>{Colors.RESET} [Y/n]: ").strip().lower()

    if confirm not in ("", "y", "yes"):
        print_warning("Operation cancelled by user.")
        sys.exit(0)

    # ── Organize ────────────────────────────────────────
    print_section("ORGANIZING FILES")

    stats = organize_files(dir_path, categorized, dry_run=False)

    # ── Summary ─────────────────────────────────────────
    print_summary(categorized, stats)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  {Colors.DIM}Completed at {timestamp}{Colors.RESET}")
    print(f"  {Colors.GREEN}{Colors.BOLD}[OK] Organization complete!{Colors.RESET}\n")


if __name__ == "__main__":
    main()
