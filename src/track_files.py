import os
import re
from typing import Any, List

import eyed3

from .config import get_music_root, get_music_destination

MUSIC_ROOT = get_music_root()
MUSIC_DEST = get_music_destination()


def search_names(track_title: str, os_files_list: List[str]) -> List[tuple]:
    matching_files = []
    title_quote = re.escape(track_title).replace("'", "[\'_]")
    # Should search through '(1)..(x)' for extracted duplicates
    filename_regex = f"^{title_quote}(\\([0-9]+\\))?.(mp3|vid)$"
    for filename in os_files_list:
        if re.search(filename_regex, filename):
            match_tuple = (filename, find_track_duration(filename))
            if match_tuple[1] != 0.0:
                matching_files.append(match_tuple)
    return matching_files


def find_track_duration(filename: str) -> float:
    try:
        full_path = f"{MUSIC_ROOT}/{filename}"
        audio_file = eyed3.load(full_path)
        if audio_file is not None:
            return audio_file.info.time_secs
        else:
            return 0.0
    except Exception:
        pass


def target_file_exists(track_data: Any) -> bool:
    exists = False
    output_dir = f"{MUSIC_DEST}/{track_data.artist}/{track_data.album}"
    for char in "`*_{}[]()>#+-.!$":
        track_data.title = track_data.title.replace(char, '.')
    target_file_regex = f"([0-9]+ - )?{track_data.title}\\.mp3"

    if os.path.isdir(output_dir):
        for filename in os.listdir(output_dir):
            if re.search(target_file_regex, filename):
                exists = True

    return exists
