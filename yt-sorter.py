import logging
import os

from src import config, csv, metadata, mover, progress_bar, sorter, track_files


def check_music_root():
    if "MUSIC_ROOT" not in os:
        exit(1)


if __name__ == "__main__":
    # Check that the MUSIC_ROOT env var is set
    check_music_root()

    # First sort through using the embedded ID3 tags
    metadata.sort_by_metadata()
    # Parse the CSV file into records
    csv_records = csv.load_file(config.get_csv_path())

    # Create a list of all combined CSV records and the filenames of matching files
    track_data = []

    progress_bar_total = len(csv_records)
    print("Matching the CSV entries to the files in the root directory")
    for idx, record in enumerate(csv_records):
        if logging.root.level > logging.INFO:
            progress_bar.progress_bar(idx, progress_bar_total)
        matching_csv_records = csv.search_for_title_matches(record.title, csv_records)
        matching_files = track_files.search_names(record.title)
        for match_record in sorter.sort_lists(matching_csv_records, matching_files):
            track_data.append(match_record)
    print("")

    print("Moving the matching files into their new homes")
    progress_bar_total = len(track_data)
    for idx, track in enumerate(track_data):
        if logging.root.level > logging.INFO:
            progress_bar.progress_bar(idx, progress_bar_total)
        if track.filename is not None:
            mover.move(
                track.filename, f"{track.artist}/{track.album}", f"{track.title}.mp3"
            )
    print("")
