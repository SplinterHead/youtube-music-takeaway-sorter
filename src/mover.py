import os
import re
import shutil

from .config import DRY_RUN, MOVE_SOURCE, MUSIC_DESTINATION, MUSIC_ROOT
from .lib.logging import get_logger

log = get_logger("mover")


def move(source_file: str, destination_dir: str, destination_file: str) -> None:
    target_dir = f"{MUSIC_DESTINATION}/{destination_dir}"
    if not os.path.isdir(target_dir):
        log.debug(f"Creating new directory for {target_dir}")
        os.makedirs(target_dir)
    if not os.path.isfile(re.escape(destination_file)):
        destination_file = destination_file.replace("/", "\\/")

    log.debug(
        f"{'DRY_RUN: ' if DRY_RUN else ''}{'Mov' if MOVE_SOURCE else 'Copy'}ing {source_file} to {target_dir}/{destination_file}"
    )
    if not DRY_RUN and not MOVE_SOURCE:
        shutil.copy(f"{MUSIC_ROOT}/{source_file}", f"{target_dir}/{destination_file}")
    if not DRY_RUN and MOVE_SOURCE:
        shutil.move(f"{MUSIC_ROOT}/{source_file}", f"{target_dir}/{destination_file}")
