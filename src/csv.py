import csv
from dataclasses import dataclass
from typing import Any, List

from .lib.logging import get_logger

log = get_logger("csv")


@dataclass
class CSVTrack:
    title: str
    album: str
    artist: str
    duration: float
    filename: str = ""


def parse_row(csv_row: Any) -> Any:
    return CSVTrack(
        title=csv_row["Song Title"],
        album=csv_row["Album Title"],
        artist=csv_row["Artist Names"],
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
    return list(filter(lambda x: x.title == search_title, csv_records))
