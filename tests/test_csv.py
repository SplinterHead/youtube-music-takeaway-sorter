from dataclasses import dataclass, field
from io import StringIO
from unittest.mock import patch

import pytest

from src.csv import CSVTrack, load_file, parse_row, search_for_title_matches

MOCK_CSV_PATH = "/tmp/test.csv"
CSV_HEADER = "Song Title,Album Title,Artist Names,Duration Seconds"


def test_parse_csv_row():
    csv_content = {
        "Song Title": "song 1",
        "Album Title": "album 1",
        "Artist Names": "artist 1",
        "Duration Seconds": 123.45,
    }

    expected = CSVTrack(
        title="song 1", album="album 1", artist="artist 1", duration=123.45
    )

    actual = parse_row(csv_content)
    assert actual == expected


@dataclass
class CsvLoadTestCase:
    description: str
    csv_content: str
    expected_output: list[CSVTrack]


csv_load_test_cases = [
    CsvLoadTestCase(
        description="Single line CSV file",
        csv_content=f"{CSV_HEADER}\nsong 1,album 1,artist 1,123.45",
        expected_output=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            )
        ],
    ),
    CsvLoadTestCase(
        description="Multiple line CSV file",
        csv_content=f"{CSV_HEADER}\nsong 1,album 1,artist 1,123.45\nsong 2,album 2,artist 2,12.345",
        expected_output=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 2", album="album 2", artist="artist 2", duration=12.345
            ),
        ],
    ),
]


@patch("builtins.open")
@pytest.mark.parametrize(
    "testcase", csv_load_test_cases, ids=[x.description for x in csv_load_test_cases]
)
def test_csv_load(file_open_mock, testcase):
    csv_content = StringIO(testcase.csv_content)
    file_open_mock.return_value = csv_content

    actual = load_file(MOCK_CSV_PATH)
    expected = testcase.expected_output

    assert actual == expected


@dataclass
class CsvSearchTestCase:
    description: str
    search_term: str
    csv_records: list[CSVTrack]
    filesystem_files: list[list[str]]
    expected_output: list[CSVTrack]


csv_search_test_cases = [
    CsvSearchTestCase(
        description="Single entries in CSV, does not match the search term",
        search_term="song 1",
        csv_records=[
            CSVTrack(
                title="song 2", album="album 1", artist="artist 1", duration=123.45
            )
        ],
        filesystem_files=[],
        expected_output=[],
    ),
    CsvSearchTestCase(
        description="Single entries in CSV, matches the search term",
        search_term="song 1",
        csv_records=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            )
        ],
        filesystem_files=[],
        expected_output=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            )
        ],
    ),
    CsvSearchTestCase(
        description="Multiple entries in CSV, all matching the search term",
        search_term="song 1",
        csv_records=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
        filesystem_files=[],
        expected_output=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
    ),
    CsvSearchTestCase(
        description="Multiple entries in CSV, some matching the search term",
        search_term="song 1",
        csv_records=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
            CSVTrack(
                title="song 2", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
        filesystem_files=[],
        expected_output=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
    ),
    CsvSearchTestCase(
        description="Multiple entries in CSV, all matching the search term, one album's version exists already",
        search_term="song 1",
        csv_records=[
            CSVTrack(
                title="song 1", album="album 1", artist="artist 1", duration=123.45
            ),
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
        filesystem_files=[["01 - song 1.mp3"], []],
        expected_output=[
            CSVTrack(
                title="song 1", album="album 2", artist="artist 2", duration=123.45
            ),
        ],
    ),
]


@patch("os.listdir")
@pytest.mark.parametrize(
    "testcase",
    csv_search_test_cases,
    ids=[x.description for x in csv_search_test_cases],
)
def test_csv_search(list_dir_mock, testcase):
    if len(testcase.filesystem_files) == 0:
        list_dir_mock.return_value = testcase.filesystem_files
    else:
        list_dir_mock.side_effect = testcase.filesystem_files

    actual = search_for_title_matches(testcase.search_term, testcase.csv_records)
    expected = testcase.expected_output

    assert actual == expected
