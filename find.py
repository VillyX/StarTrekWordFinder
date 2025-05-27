import os
import re
from collections import defaultdict

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SERIES_LABELS = {
    "01_TOS": "01 TOS",
    "02_TAS": "02 TAS",
    "03_TNG": "03 TNG",
    "04_DS9": "04 DS9",
    "05_VOY": "05 VOY",
    "06_ENT": "06 ENT",
    "07_DIS": "07 DIS",
    "08_SHO": "07 SHO",
    "09_PIC": "08 PIC",
    "10_LD":  "09 LD",
    "11_PRO": "10 PRO",
    "12_SNW": "11 SNW",
}

def extract_season_episode(filename):
    match = re.search(r"[Ss](\d{1,2})[Ee](\d{1,2})", filename)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def search_word(word, use_regex=False):
    result = defaultdict(lambda: defaultdict(int))

    if use_regex:
        pattern = re.compile(word, re.IGNORECASE)
    else:
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
                    content = f.read()
                    count = len(pattern.findall(content)) if use_regex else content.lower().count(word)
                    result[series][season] += count
            except Exception as e:
                print(f"Failed to read {file_path}: {e}")

    return result

def print_result(result, word):
    print(f"\nOccurrences of the word: '{word}'\n")
    print("{:<8} {:<8} {:<12}".format("Series", "Season", "Occurrences"))
    print("-" * 30)
    total = 0
    for series in sorted(result):
        for season in sorted(result[series]):
            count = result[series][season]
            print(f"{series:<8} {season:<8} {count:<12}")
            total += count
    print("-" * 30)
    print(f"{'TOTAL':<16} {total:<12}")

if __name__ == "__main__":
    search_term = input("Enter a word or regex pattern to search for: ").strip()
    use_regex = input("Use regex matching? (y/n): ").strip().lower() == 'y'
    results = search_word(search_term, use_regex=use_regex)
    print_result(results, search_term)
