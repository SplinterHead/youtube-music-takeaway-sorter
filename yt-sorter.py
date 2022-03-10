import logging
import os

from src import csv, metadata, mover, progress_bar, sorter, track_files
from src.config import CSV_PATH, MUSIC_ROOT
from src.lib.logging import get_logger

log = get_logger("main")

if __name__ == "__main__":
    # Check that the MUSIC_ROOT env var is set
    if not MUSIC_ROOT:
        raise "MUSIC_ROOT is not set"

    # First sort through using the embedded ID3 tags
    # metadata.sort_by_metadata()
    # Parse the CSV file into records
    csv_records = csv.load_file(CSV_PATH)
    unique_csv_records = set(csv_record.title for csv_record in csv_records)

    # Get a list of all files in the music root
    os_files_list = os.listdir(MUSIC_ROOT)

    # Create a list of all combined CSV records and the filenames of matching files
    track_data = []

    progress_bar_total = len(csv_records)
    print("Matching the CSV entries to the files in the root directory")
    for idx, title in enumerate(unique_csv_records):
        log.info(f"Processing {title}")
        if logging.root.level > logging.INFO:
            progress_bar.progress_bar(idx, progress_bar_total)
        matching_csv_records = csv.search_for_title_matches(title, csv_records)
        matching_files = track_files.search_names(title, os_files_list)
        for match_record in sorter.sort_lists(matching_csv_records, matching_files):
            track_data.append(match_record)
    progress_bar.progress_bar(progress_bar_total, progress_bar_total)
    print("")

    if len(track_data) > 0:
        print("Moving the matching files into their new homes")
        progress_bar_total = len(track_data)
        for idx, track in enumerate(track_data):
            if logging.root.level > logging.INFO:
                progress_bar.progress_bar(idx, progress_bar_total)
            if track.filename is not None:
                mover.move_csv_track(track)
        progress_bar.progress_bar(progress_bar_total, progress_bar_total)
        print("")
    else:
        print("No new files discovered")
