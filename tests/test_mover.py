from dataclasses import dataclass
from unittest.mock import patch

import pytest

from src.config import MUSIC_DEST, MUSIC_ROOT
from src.csv import CSVTrack
from src.mover import move_csv_track


@dataclass
class FileCsvMoverTestCase:
    description: str
    csv_track: CSVTrack
    exp_destination: str


csv_file_mover_test_cases = [
    FileCsvMoverTestCase(
        description="Track containing no special characters",
        csv_track=CSVTrack(
            title="Song 1",
            trunc_title="Song 1",
            artist="Artist 1",
            album="Album 1",
            duration=10,
            filename="Song 1.mp3",
        ),
        exp_destination="Artist 1/Album 1",
    ),
    FileCsvMoverTestCase(
        description="Track with album and title containing forward slashes",
        csv_track=CSVTrack(
            title="Song 1",
            trunc_title="Song 1",
            artist="Artist/1",
            album="Album / 1",
            duration=10,
            filename="Song 1.mp3",
        ),
        exp_destination="Artist_1/Album _ 1",
    ),
]


@pytest.fixture(scope="function")
def move_source_true(monkeypatch):
    monkeypatch.setenv("MOVE_SOURCE", "true")


@pytest.fixture(scope="function")
def move_source_false(monkeypatch):
    monkeypatch.setenv("MOVE_SOURCE", "false")


@patch("os.path.isdir")
@patch("os.makedirs")
@patch("shutil.copy")
@pytest.mark.parametrize(
    "testcase",
    csv_file_mover_test_cases,
    ids=[x.description for x in csv_file_mover_test_cases],
)
def test_mover_creates_directory_if_not_exists_for_csv_track(
    mock_copy, mock_makedirs, mock_isdir, testcase
):
    mock_isdir.return_value = False
    move_csv_track(testcase.csv_track)

    assert mock_makedirs.called
    mock_makedirs.assert_called_with(f"{MUSIC_DEST}/{testcase.exp_destination}")


@patch("os.path.isdir")
@patch("os.makedirs")
@patch("shutil.copy")
@pytest.mark.parametrize(
    "testcase",
    csv_file_mover_test_cases,
    ids=[x.description for x in csv_file_mover_test_cases],
)
def test_mover_does_not_create_directory_if_exists_for_csv_mover(
    mock_copy, mock_makedirs, mock_isdir, testcase
):
    mock_isdir.return_value = True
    move_csv_track(testcase.csv_track)
    assert not mock_makedirs.called


@patch("os.path.isdir")
@patch("shutil.copy")
@patch("shutil.move")
@pytest.mark.parametrize(
    "testcase",
    csv_file_mover_test_cases,
    ids=[x.description for x in csv_file_mover_test_cases],
)
def test_move_with_copy(mock_move, mock_copy, mock_isdir, testcase, move_source_false):
    mock_isdir.return_value = True

    source_path = f"{MUSIC_ROOT}/{testcase.csv_track.filename}"
    destination_path = (
        f"{MUSIC_DEST}/{testcase.exp_destination}/{testcase.csv_track.filename}"
    )
    move_csv_track(testcase.csv_track)

    mock_copy.assert_called_with(source_path, destination_path)
    assert not mock_move.called
