import os
import re
from typing import Any, List

import eyed3

from .config import get_music_destination, get_music_root
from .lib.logging import get_logger

log = get_logger("track_files")

MUSIC_ROOT = get_music_root()
MUSIC_DEST = get_music_destination()


def safe_name(track_title: str) -> str:
    # Chars replaced by underscore
    for char in ":?'\"":
        track_title = track_title.replace(char, "_")
    return re.escape(track_title[0:47])


def search_names(track_title: str, os_files_list: List[str]) -> List[tuple]:
    matching_files = []
    # Should search through '(1)..(x)' for extracted duplicates
    filename_regex = f"^{safe_name(track_title)}(\\([0-9]+\\))?.(mp3|vid)$"
    log.debug(f"Searching with the expression: {filename_regex}")
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
    target_file_regex = f"([0-9]+ - )?{safe_name(track_data.title)}\\.mp3"

    if os.path.isdir(output_dir):
        for filename in os.listdir(output_dir):
            if re.search(target_file_regex, filename):
                exists = True

    return exists
