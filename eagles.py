import os
import sys
import webbrowser

# Attempt to import mutagen for reading internal audio tags
try:
    import mutagen
except ImportError:
    print("[!] Mutagen library not found. Install it with: pip install mutagen")
    sys.exit(1)

# ==============================================================================
# Script: Hotel California Eviction Notice Protocol
#
# "I hate the fuckin' Eagles, man!" - The Dude
#
# Description:
# Opens The Big Lebowski clip in Chrome/Browser, scans directory trees for audio
# files, inspects both filenames AND internal ID3 metadata for "The Eagles",
# and prompts the user before deleting.
# ==============================================================================

# URL of The Dude getting kicked out of the cab over The Eagles
DUDE_YOUTUBE_URL = "https://youtu.be/-JlmvtAHhnc?t=21"

AUDIO_EXTENSIONS = {".mp3", ".flac", ".m4a", ".wav", ".aac", ".ogg", ".wma"}
TARGET_KEYWORDS = ["the eagles", "eagles"]

SEARCH_DIRECTORIES = [
    os.path.expanduser("~/Music"),
    os.path.expanduser("~/Downloads"),
    # Add extra directories as needed:
    # os.path.expanduser("~/Desktop"),
]


def play_dude_clip():
    """
    Opens Chrome (or system default browser) to play the iconic YouTube clip.
    """
    print("\n[SERENADE] Cueing up The Dude's opinion on the matter...")
    try:
        # Attempts to explicitly open in Chrome; falls back to default browser if not found
        chrome_path = "google-chrome"
        if sys.platform == "darwin":  # macOS
            chrome_path = "open -a /Applications/Google\\ Chrome.app %s"
        elif sys.platform == "win32":  # Windows
            chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

        webbrowser.get(chrome_path).open(DUDE_YOUTUBE_URL)
    except Exception:
        # Fallback to default browser
        webbrowser.open(DUDE_YOUTUBE_URL)


def check_metadata(file_path):
    """
    Inspects internal metadata tags (artist, album artist, composer)
    for target keywords.
    """
    try:
        audio = mutagen.File(file_path)
        if audio is None:
            return False

        # Convert all metadata text values into a single lowercased string
        metadata_text = []
        for key, value in audio.items():
            if isinstance(value, list):
                metadata_text.extend([str(v).lower() for v in value])
            else:
                metadata_text.append(str(value).lower())

        full_metadata = " ".join(metadata_text)
        return any(keyword in full_metadata for keyword in TARGET_KEYWORDS)
    except Exception:
        # If metadata reading fails, fall back gracefully
        return False


def is_eagles_file(file_path):
    """
    Evaluates both file path and internal metadata tags.
    """
    path_lower = file_path.lower()

    # 1. Check filename/path
    if any(keyword in path_lower for keyword in TARGET_KEYWORDS):
        return True, "Filename/Path match"

    # 2. Check internal ID3/Metadata tags
    if check_metadata(file_path):
        return True, "Metadata/ID3 Tag match"

    return False, ""


def confirm_deletion(file_path, reason):
    """
    Prompts the user directly in the terminal before taking destructive action.
    """
    print("\n" + "-" * 50)
    print(f"🚨 TARGET ACQUIRED: {file_path}")
    print(f"   Reason Flagged: {reason}")
    print("-" * 50)

    while True:
        choice = (
            input(
                "Do you want to permanently delete this file? (y/n/all/quit): "
            )
            .strip()
            .lower()
        )
        if choice in ["y", "yes"]:
            return "yes"
        elif choice in ["n", "no"]:
            return "no"
        elif choice == "all":
            return "all"
        elif choice in ["q", "quit"]:
            return "quit"
        print(
            "Invalid input. Please enter 'y' (yes), 'n' (no), 'all' (delete rest without asking), or 'quit'."
        )


def hotel_california_checkout():
    """
    Runs the scanner with interactive deletion prompts and browser trigger.
    """
    print("=" * 60)
    print(" 🦅 HOTEL CALIFORNIA EVICTION NOTICE PROTOCOL 🦅")
    print("   'You can check out any time you like, but you can never stay.'")
    print("=" * 60)

    # Launch YouTube video in Chrome
    play_dude_clip()

    files_found = 0
    files_deleted = 0
    auto_delete_all = False

    for directory in SEARCH_DIRECTORIES:
        if not os.path.exists(directory):
            print(f"\nSkipping missing directory: {directory}")
            continue

        print(f"\nScanning directory: {directory}...")

        for root, _, files in os.walk(directory):
            for file in files:
                _, ext = os.path.splitext(file)

                if ext.lower() in AUDIO_EXTENSIONS:
                    file_path = os.path.join(root, file)
                    is_target, reason = is_eagles_file(file_path)

                    if is_target:
                        files_found += 1

                        # Determine if we should delete or prompt
                        if auto_delete_all:
                            action = "yes"
                        else:
                            action = confirm_deletion(file_path, reason)

                        if action == "quit":
                            print("\n[ABORTED] Scan interrupted by user.")
                            sys.exit(0)
                        elif action == "all":
                            auto_delete_all = True
                            action = "yes"

                        if action == "yes":
                            try:
                                os.remove(file_path)
                                print(f"[EVICTED] Deleted: {file}")
                                files_deleted += 1
                            except Exception as e:
                                print(f"[ERROR] Failed to delete {file}: {e}")
                        else:
                            print(f"[SKIPPED] Kept file: {file}")

    print("\n" + "=" * 60)
    print(f"Scan complete. Found: {files_found} target file(s).")
    print(f"Total deleted: {files_deleted} file(s). Take it easy!")
    print("=" * 60)


if __name__ == "__main__":
    hotel_california_checkout()