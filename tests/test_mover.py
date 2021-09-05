from dataclasses import dataclass
from unittest.mock import patch

import pytest

from src.config import get_music_destination, get_music_root
from src.mover import move

MUSIC_ROOT = get_music_root()
MUSIC_DESTINATION = get_music_destination()


@dataclass
class FileMoverTestCase:
    description: str
    source_filename: str
    target_destination: str
    target_filename: str


file_mover_test_cases = [
    FileMoverTestCase(
        description="Directory and Filenames with no special characters",
        source_filename="Song 1.vid",
        target_destination="Artist 1/Album 1",
        target_filename="Song 1.mp3",
    )
]


@patch("os.path.isdir")
@patch("os.makedirs")
@patch("shutil.copy")
@pytest.mark.parametrize(
    "testcase",
    file_mover_test_cases,
    ids=[x.description for x in file_mover_test_cases],
)
def test_mover_creates_directory_if_not_exists(
    mock_copy, mock_makedirs, mock_isdir, testcase
):
    mock_isdir.return_value = False
    move(
        testcase.source_filename, testcase.target_destination, testcase.target_filename
    )

    assert mock_makedirs.called
    mock_makedirs.assert_called_with(
        f"{MUSIC_DESTINATION}/{testcase.target_destination}"
    )


@patch("os.path.isdir")
@patch("os.makedirs")
@patch("shutil.copy")
def test_mover_does_not_create_directory_if_exists(
    mock_copy, mock_makedirs, mock_isdir
):
    filename = "Song 1.mp3"
    destination_path = f"{MUSIC_DESTINATION}/{filename}"

    mock_isdir.return_value = True
    move(filename, destination_path, filename)
    assert not mock_makedirs.called


@patch("os.path.isdir")
@patch("shutil.copy")
@patch("shutil.move")
def test_move_with_copy(mock_move, mock_copy, mock_isdir, monkeypatch):
    monkeypatch.setenv("MOVE_SOURCE", "false")

    filename = "Song 1.mp3"
    source_path = MUSIC_ROOT
    destination_path = f"{MUSIC_DESTINATION}/{filename}"

    mock_isdir.return_value = True
    move(filename, destination_path, filename)
    assert mock_copy.called_with(source_path, destination_path)
    assert not mock_move.called
