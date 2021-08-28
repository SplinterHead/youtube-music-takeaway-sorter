# from dataclasses import dataclass
# from src.config import MUSIC_PATH, MUSIC_ROOT
# from unittest.mock import patch
# from src.mover import move
# import pytest
#
#
# @dataclass
# class FileMoverTestCase:
#     description: str
#     source_filename: str
#     target_destination: str
#     target_filename: str
#
#
# file_mover_test_cases = [
#     FileMoverTestCase(
#         description="Directory and Filenames with no special characters",
#         source_filename="What I Go To School For.vid",
#         target_destination="Busted/Busted",
#         target_filename="What I Go To School For.mp3",
#     ),
#     FileMoverTestCase(
#         description="Directory with forward slash and Filenames with no special characters",
#         source_filename="What I Go To School For.vid",
#         target_destination="Busted/Busted",
#         target_filename="What I Go To School For.mp3",
#     )
# ]
#
#
# @patch("os.path.isdir")
# @patch("os.makedirs")
# @patch("shutil.copy")
# @pytest.mark.parametrize("testcase", file_mover_test_cases)
# def test_mover_creates_directory_if_not_exists(mock_copy, mock_makedirs, mock_isdir, testcase):
#     mock_isdir.return_value = False
#     move(testcase.source_filename, testcase.target_destination, testcase.target_filename)
#
#     assert mock_makedirs.called
#     mock_makedirs.assert_called_with(f"{MUSIC_ROOT}/{testcase.target_destination}")
#
#
# # @patch("os.path.isdir")
# # @patch("os.makedirs")
# # @patch("shutil.copy")
# # def test_mover_does_not_create_directory_exists(mock_copy, mock_makedirs, mock_isdir):
# #     source_path = f"{MUSIC_PATH}/{source_filename}"
# #     destination_path = f"{target_destination}/{target_filename}"
# #
# #     mock_isdir.return_value = True
# #     move(source_filename, target_destination, target_filename)
# #     assert not mock_makedirs.called
# #
# #
# # @patch("os.path.isdir")
# # @patch("shutil.copy")
# # def test_move_with_copy(mock_copy, mock_isdir):
# #     mock_isdir.return_value = True
# #     move(source_filename, target_destination, target_filename)
# #     assert mock_copy.called_with(source_path, destination_path)
