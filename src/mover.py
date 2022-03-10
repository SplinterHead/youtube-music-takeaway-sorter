import os
import shutil

from .config import DIR_UNSAFE_CHARS, DRY_RUN, MOVE_SOURCE, MUSIC_DEST, MUSIC_ROOT
from .csv import CSVTrack
from .lib.logging import get_logger

log = get_logger("mover")


def _path_safe(dir_part: str) -> str:
    # Chars replaced by underscore
    for char in DIR_UNSAFE_CHARS:
        dir_part = dir_part.replace(char, "_")
    return dir_part


def move_csv_track(csv_track: CSVTrack) -> None:
    source_file = os.path.join(MUSIC_ROOT, csv_track.filename)
    target_dir = os.path.join(
        MUSIC_DEST, _path_safe(csv_track.artist), _path_safe(csv_track.album)
    )
    target_file = os.path.join(target_dir, r"%s.mp3" % _path_safe(csv_track.title))
    if not os.path.isdir(target_dir):
        log.debug(f"Creating new directory for {target_dir}")
        os.makedirs(target_dir)

    log.debug(f"{'Mov' if MOVE_SOURCE else 'Copy'}ing {source_file} to {target_file}")
    if not DRY_RUN:
        if MOVE_SOURCE:
            shutil.move(source_file, target_file)
        else:
            shutil.copy(source_file, target_file)
