from dataclasses import dataclass
from unittest.mock import patch

import pytest

from src.csv import CSVTrack
from src.track_files import search_names, target_file_exists


@dataclass
class FileSearchTestCase:
    description: str
    file_names: list[str]
    search_term: str
    expected: list[tuple]


file_search_test_cases = [
    FileSearchTestCase(
        description="Multiple filenames, matches the search term",
        file_names=["Song 1.mp3", "Song 2.mp3"],
        search_term="Song 1",
        expected=[("Song 1.mp3", 10.0)],
    ),
    FileSearchTestCase(
        description="Multiple filename, no matches to the search term",
        file_names=["Song 1.mp3", "Song 2.mp3"],
        search_term="Song 3",
        expected=[],
    ),
    FileSearchTestCase(
        description="Multiple duplicate filenames, all match the search term",
        file_names=["Song 1.mp3", "Song 1(1).mp3"],
        search_term="Song 1",
        expected=[("Song 1.mp3", 10.0), ("Song 1(1).mp3", 10.0)],
    ),
    FileSearchTestCase(
        description="Multiple duplicate filenames with multiple digits, all match the search term",
        file_names=["Song 1.mp3", "Song 1(11).mp3", "Song 1(111).mp3"],
        search_term="Song 1",
        expected=[
            ("Song 1.mp3", 10.0),
            ("Song 1(11).mp3", 10.0),
            ("Song 1(111).mp3", 10.0),
        ],
    ),
]


@patch("os.listdir")
@patch("src.track_files.find_track_duration")
@pytest.mark.parametrize(
    "testcase",
    file_search_test_cases,
    ids=[x.description for x in file_search_test_cases],
)
def test_search_by_title(duration_mock, listdir_mock, testcase):
    duration_mock.return_value = 10.0
    listdir_mock.return_value = testcase.file_names
    actual = search_names(testcase.search_term)
    expected = testcase.expected

    assert actual == expected


@dataclass
class FileExistTestCase:
    description: str
    file_names: list[str]
    track_data: CSVTrack
    expected: bool


file_exists_test_cases = [
    FileExistTestCase(
        description="Return False if the directory is empty",
        file_names=[],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        expected=False,
    ),
    FileExistTestCase(
        description="Return False if the directory has no matching file",
        file_names=["Song 2.mp3, Song 3.mp3"],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        expected=False,
    ),
    FileExistTestCase(
        description="Return True if the directory has matching file",
        file_names=["Song 1.mp3, Song 2.mp3, Song 3.mp3"],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        expected=True,
    ),
    FileExistTestCase(
        description="Return True if the directory has matching file with track number",
        file_names=["01 - Song 1.mp3, 02 - Song 2.mp3, Song 3.mp3"],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        expected=True,
    ),
]


@patch("os.listdir")
@pytest.mark.parametrize(
    "testcase",
    file_exists_test_cases,
    ids=[x.description for x in file_exists_test_cases],
)
def test_track_file_exists(list_dir_mock, testcase):
    list_dir_mock.return_value = testcase.file_names

    actual = target_file_exists(testcase.track_data)
    expected = testcase.expected

    assert actual == expected
