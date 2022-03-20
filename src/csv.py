import csv
from dataclasses import dataclass
from typing import Any, List

from .lib.logging import get_logger
from .track_files import target_file_exists

log = get_logger("csv")


@dataclass
class CSVTrack:
    title: str
    trunc_title: str
    album: str
    artist: str
    duration: float
    filename: str = ""

    def to_csv(self):
        return ",".join([self.title, self.album, self.artist, str(self.duration)])


def parse_row(csv_row: Any) -> Any:
    extracted_title = csv_row["Song Title"].strip()
    return CSVTrack(
        title=extracted_title,
        trunc_title=extracted_title[:47],
        album=csv_row["Album Title"].strip(),
        artist=csv_row["Artist Names"].strip(),
        duration=float(csv_row["Duration Seconds"]),
    )


def load_file(csv_filename: str) -> List[Any]:
    uploaded_tracks = []
    # Read the CSV
    log.debug(f"Loading the CSV contents from {csv_filename}")
    with open(csv_filename) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=",")

        # Parse each row of the CSV
        row_count = 0
        for row in reader:
            row_count += 1
            uploaded_tracks.append(parse_row(row))
    log.debug(f"All {row_count} rows loaded from the CSV")
    return uploaded_tracks


def search_for_title_matches(search_title: str, csv_records: List[Any]) -> List[Any]:
    csv_matches = list(filter(lambda x: x.trunc_title == search_title, csv_records))
    # Strip out the matches where the files have already been created by the metadata sorting
    valid_csv_matches = []
    for match in csv_matches:
        if not target_file_exists(match):
            valid_csv_matches.append(match)

    return valid_csv_matches
