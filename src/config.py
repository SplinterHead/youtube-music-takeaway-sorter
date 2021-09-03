import os


# Current directory for all files
def get_music_root() -> str:
    return os.getenv("MUSIC_ROOT")


# Where the organised music should end up
def get_music_destination() -> str:
    return os.getenv("DESTINATION", f"{get_music_root()}/Structured")


# Path to the provided CSV file
def get_csv_path() -> str:
    return os.getenv("CSV_PATH", f"{get_music_root()}/music-uploads-metadata.csv")


# Whether to move the file from ROOT to DESTINATION (True), or just copy it (False)
def get_move_source() -> bool:
    return os.getenv("MOVE_SOURCE", False)


# Run in dry run mode to not affect the files, but output the logs
def get_dry_run() -> bool:
    return os.getenv("DRY_RUN", False)
