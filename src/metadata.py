# import logging
# import os
# from dataclasses import dataclass
# from typing import Any
#
# import eyed3
#
# from .config import get_music_root
# from .lib.logging import get_logger
# from .mover import move
# from .progress_bar import progress_bar
#
# log = get_logger("metadata")
#
# eyed3.log.setLevel("ERROR")
#
#
# MUSIC_ROOT = get_music_root()
#
#
# @dataclass
# class TrackTags:
#     artist: str = None
#     album: str = None
#     title: str = None
#     track_no: tuple = (None, None)
#     duration: int = -1
#
#     def __repr__(self):
#         return f"{self.title} from the album {self.album} by {self.artist}"
#
#
# def sort_by_metadata() -> None:
#     print("Automatically sorting tracks by their MP3 metadata, if present")
#     progress_bar_total = len(os.listdir(MUSIC_ROOT))
#     for idx, filename in enumerate(os.listdir(MUSIC_ROOT)):
#         if logging.root.level > logging.INFO:
#             progress_bar(idx, progress_bar_total)
#         log.info(f"Attempting to read metadata tags for {filename}")
#         try:
#             tags = read_metadata_tags(filename)
#             if (
#                 tags.artist is not None
#                 and tags.album is not None
#                 and tags.title is not None
#             ):
#                 log.info("- Found all necessary metadata")
#                 log.debug(f"Metadata tags read for {filename} are:")
#                 log.debug(tags)
#                 output_filename_track_no = f"{tags.track_no[0]:02} - "
#                 output_filename = f"{output_filename_track_no if tags.track_no[0] is not None else ''}{tags.title}.mp3"
#                 output_dir = f"{tags.artist}/{tags.album}"
#                 move(filename, output_dir, output_filename)
#         except Exception:
#             log.info("- Could not read metadata")
#             pass
#     # Close off the progress bar cleanly
#     progress_bar(progress_bar_total, progress_bar_total)
#     print("")
#
#
# def read_metadata_tags(filename: str) -> Any:
#     full_path = f"{MUSIC_ROOT}/{filename}"
#     log.debug(f"Reading metadata tags for {filename}")
#
#     try:
#         audio_file = eyed3.load(full_path)
#         tag = audio_file.tag
#
#         if tag.album_artist:
#             log.debug(f"Album Artist tag found, {tag.album_artist}")
#         else:
#             log.debug(f"Artist tag fallen back on, {tag.artist}")
#
#         return TrackTags(
#             artist=tag.album_artist or tag.artist,
#             album=tag.album or None,
#             title=tag.title or None,
#             track_no=tag.track_num or None,
#             duration=audio_file.info.time_secs,
#         )
#     except Exception:
#         log.debug(
#             f"Couldn't load {filename} to find the tags, likely not a valid audio file"
#         )
#         return TrackTags()
