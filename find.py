import os
import re
from collections import defaultdict

# Folder containing subtitle folders
BASE_DIR = r"C:\Users\User\Downloads\ST Subtitles"

# Map folder names to series codes
SERIES_LABELS = {
    "01_TOS": "01 TOS",
    "02_TAS": "02 TAS",
    "03_TNG": "03 TNG",
    "04_DS9": "04 DS9",
    "05_VOY": "05 VOY",
    "06_ENT": "06 ENT",
    "07_STD": "07 DIS",
    "08_PIC": "08 PIC",
    "09_LD": "09 LD",
    "10_PRO": "10 PRO",
    "11_SNW": "11 SNW",
}

def extract_season_episode(filename):
    match = re.search(r"[Ss](\d{1,2})[Ee](\d{1,2})", filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def search_word(word):
    result = defaultdict(lambda: defaultdict(int))
    word = word.lower()

    for folder in os.listdir(BASE_DIR):
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.isdir(folder_path):
            continue

        series = SERIES_LABELS.get(folder, folder)

        for file in os.listdir(folder_path):
            if not file.endswith(".srt"):
                continue

            season, _ = extract_season_episode(file)
            if season is None:
                continue

            file_path = os.path.join(folder_path, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read().lower()
                    count = content.count(word)
                    result[series][season] += count
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

    return result

def print_result(result, word):
    total = 0
    print(f"\nOccurrences of the word: '{word}'\n")
    print("{:<8} {:<8} {:<12}".format("Series", "Season", "Occurrences"))
    print("-" * 30)
    for series in sorted(result):
        for season in sorted(result[series]):
            count = result[series][season]
            total += count
            print(f"{series:<8} {season:<8} {count:<12}")
    print("-" * 30)
    print(f"{'Total':<16} {total:<12}")

if __name__ == "__main__":
    search_term = input("Enter a word to search for: ").strip()
    results = search_word(search_term)
    print_result(results, search_term)
