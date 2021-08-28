import os
import re
from typing import List

import eyed3

from .config import MUSIC_ROOT


def search_names(track_title: str) -> List[tuple]:
    matching_files = []
    title_quote = re.escape(track_title).replace("'", "_")
    # Should search through '(1)..(x)' for extracted duplicates
    filename_regex = f"^{title_quote}(\\([0-9]+\\))?.(mp3|vid)"
    for filename in os.listdir(MUSIC_ROOT):
        if re.search(filename_regex, filename):
            match_tuple = (filename, find_track_duration(filename))
            matching_files.append(match_tuple)
    return matching_files


def find_track_duration(filename: str) -> float:
    try:
        full_path = f"{MUSIC_ROOT}/{filename}"
        audio_file = eyed3.load(full_path)
        return audio_file.info.time_secs
    except Exception:
        pass
