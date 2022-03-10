# import os
#
# import pytest
#
# from src.config import (
#     get_csv_path,
#     get_dry_run,
#     get_move_source,
#     get_music_destination,
#     get_music_root,
# )
#
# FAKE_MUSIC_ROOT = "/music/root"
# FAKE_MUSIC_DEST = "music.destination"
# FAKE_CSV_PATH = "not-the-default.csv"
#
#
# def test_get_music_root_exits_when_not_set(monkeypatch):
#     monkeypatch.delenv("MUSIC_ROOT")
#     with pytest.raises(SystemExit) as pytest_wrapped_e:
#         get_music_root()
#     assert pytest_wrapped_e.type == SystemExit
#     assert pytest_wrapped_e.value.code == 1
#
#
# def test_get_music_root_returns_env_var_when_set(monkeypatch):
#     monkeypatch.setenv("MUSIC_ROOT", FAKE_MUSIC_ROOT)
#     expected = FAKE_MUSIC_ROOT
#     actual = get_music_root()
#
#     assert actual == expected
#
#
# def test_get_music_destination_returns_default_when_env_not_set(monkeypatch):
#     monkeypatch.setenv("MUSIC_ROOT", FAKE_MUSIC_ROOT)
#     if "DESTINATION" in os.environ:
#         monkeypatch.delenv("DESTINATION")
#     expected = f"{FAKE_MUSIC_ROOT}/Structured"
#     actual = get_music_destination()
#
#     assert actual == expected
#
#
# def test_get_music_destination_returns_env_var_when_set(monkeypatch):
#     monkeypatch.setenv("DESTINATION", FAKE_MUSIC_DEST)
#     expected = FAKE_MUSIC_DEST
#     actual = get_music_destination()
#
#     assert actual == expected
#
#
# def test_get_csv_path_returns_default_when_env_not_set(monkeypatch):
#     monkeypatch.setenv("MUSIC_ROOT", FAKE_MUSIC_ROOT)
#     if "CSV_PATH" in os.environ:
#         monkeypatch.delenv("CSV_PATH")
#     expected = f"{FAKE_MUSIC_ROOT}/music-uploads-metadata.csv"
#     actual = get_csv_path()
#
#     assert actual == expected
#
#
# def test_get_csv_path_returns_env_var_when_set(monkeypatch):
#     monkeypatch.setenv("CSV_PATH", FAKE_CSV_PATH)
#     expected = FAKE_CSV_PATH
#     actual = get_csv_path()
#
#     assert actual == expected
#
#
# def test_get_move_source_returns_default_when_env_not_set(monkeypatch):
#     if "MOVE_SOURCE" in os.environ:
#         monkeypatch.delenv("MOVE_SOURCE")
#     expected = False
#     actual = get_move_source()
#
#     assert actual == expected
#
#
# def test_get_move_source_returns_env_var_when_set(monkeypatch):
#     monkeypatch.setenv("MOVE_SOURCE", "true")
#     expected = True
#     actual = get_move_source()
#
#     assert actual == expected
#
#
# def test_get_dry_run_returns_default_when_env_not_set(monkeypatch):
#     if "DRY_RUN" in os.environ:
#         monkeypatch.delenv("DRY_RUN")
#     expected = False
#     actual = get_dry_run()
#
#     assert actual == expected
#
#
# def test_get_dry_run_returns_env_var_when_set(monkeypatch):
#     monkeypatch.setenv("DRY_RUN", "true")
#     expected = True
#     actual = get_dry_run()
#
#     assert actual == expected
