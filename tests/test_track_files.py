import os
from dataclasses import dataclass
from unittest.mock import PropertyMock, patch

import pytest

from src.csv import CSVTrack
from src.track_files import find_track_duration, search_names, target_file_exists


@dataclass
class FileSearchTestCase:
    description: str
    file_names: list[str]
    durations: list[float]
    search_term: str
    expected: list[tuple]


file_search_test_cases = [
    FileSearchTestCase(
        description="Multiple filenames, matches the search term",
        file_names=["Song 1.mp3", "Song 2.mp3"],
        durations=[10.0, 10.0],
        search_term="Song 1",
        expected=[("Song 1.mp3", 10.0)],
    ),
    FileSearchTestCase(
        description="Multiple filename, no matches to the search term",
        file_names=["Song 1.mp3", "Song 2.mp3"],
        durations=[10.0, 10.0],
        search_term="Song 3",
        expected=[],
    ),
    FileSearchTestCase(
        description="Multiple duplicate filenames, all match the search term",
        file_names=["Song 1.mp3", "Song 1(1).mp3"],
        durations=[10.0, 10.0],
        search_term="Song 1",
        expected=[("Song 1.mp3", 10.0), ("Song 1(1).mp3", 10.0)],
    ),
    FileSearchTestCase(
        description="Multiple duplicate filenames with multiple digits, all match the search term",
        file_names=["Song 1.mp3", "Song 1(11).mp3", "Song 1(111).mp3"],
        durations=[10.0, 10.0, 10.0],
        search_term="Song 1",
        expected=[
            ("Song 1.mp3", 10.0),
            ("Song 1(11).mp3", 10.0),
            ("Song 1(111).mp3", 10.0),
        ],
    ),
    FileSearchTestCase(
        description="Multiple duplicate filenames, all match the search term, one has duration None",
        file_names=["Song 1.mp3", "Song 1(1).mp3"],
        durations=[10.0, 0.0],
        search_term="Song 1",
        expected=[("Song 1.mp3", 10.0)],
    ),
]


@patch("src.track_files.find_track_duration")
@patch.dict(os.environ, {"MUSIC_ROOT": "/music/root"})
@pytest.mark.parametrize(
    "testcase",
    file_search_test_cases,
    ids=[x.description for x in file_search_test_cases],
)
def test_search_by_title(duration_mock, testcase):
    duration_mock.side_effect = testcase.durations
    actual = search_names(testcase.search_term, testcase.file_names)
    expected = testcase.expected

    assert actual == expected


@dataclass
class TrackDurationTestCase:
    description: str
    file_duration: any
    expected_duration: float


track_duration_test_case = [
    TrackDurationTestCase(
        description="File with valid duration returns duration",
        file_duration=10.0,
        expected_duration=10.0,
    ),
    TrackDurationTestCase(
        description="Invalid audio file returns zero duration",
        file_duration=None,
        expected_duration=0.0,
    ),
]


@patch("eyed3.load", new_callable=PropertyMock)
@pytest.mark.parametrize(
    "testcase",
    track_duration_test_case,
    ids=[x.description for x in track_duration_test_case],
)
def test_find_track_duration(eyed3_load_mock, testcase):
    if testcase.file_duration:
        eyed3_load_mock.return_value.info.time_secs = testcase.file_duration
    else:
        eyed3_load_mock.return_value = None
    actual = find_track_duration("not_a_file.vid")
    assert actual == testcase.expected_duration


@dataclass
class FileExistTestCase:
    description: str
    file_names: list[str]
    track_data: CSVTrack
    expected: bool
    artist_album_exists: bool = True


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
        file_names=["Song 2.mp3", "Song 3.mp3"],
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
        file_names=["Song 1.mp3", "Song 2.mp3", "Song 3.mp3"],
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
        file_names=["01 - Song 1.mp3", "02 - Song 2.mp3", "Song 3.mp3"],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        expected=True,
    ),
    FileExistTestCase(
        description="Return False if the artist/album directory does not exist",
        file_names=["01 - Song 1.mp3"],
        track_data=CSVTrack(
            title="Song 1",
            album="Album 1",
            artist="Artist 1",
            duration=123,
        ),
        artist_album_exists=False,
        expected=False,
    ),
]


@patch("os.listdir")
@patch("os.path.isdir")
@pytest.mark.parametrize(
    "testcase",
    file_exists_test_cases,
    ids=[x.description for x in file_exists_test_cases],
)
def test_track_file_exists(is_dir_mock, list_dir_mock, testcase):
    is_dir_mock.return_value = testcase.artist_album_exists
    list_dir_mock.return_value = testcase.file_names

    actual = target_file_exists(testcase.track_data)
    expected = testcase.expected

    assert actual == expected
