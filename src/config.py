import os

# Current directory for all files
MUSIC_ROOT = None
if "MUSIC_ROOT" in os:
    MUSIC_ROOT = os.getenv("MUSIC_ROOT")
else:
    print("MUSIC_ROOT not set but is essential, quitting...")
    exit(1)

# Where the organised music should end up
MUSIC_DESTINATION = os.getenv("DESTINATION", f"{MUSIC_ROOT}/Structured")

# Path to the provided CSV file
CSV_PATH = os.getenv("CSV_PATH", f"{MUSIC_ROOT}/music-uploads-metadata.csv")

# Whether to move the file from ROOT to DESTINATION (True), or just copy it (False)
MOVE_SOURCE = os.getenv("MOVE_SOURCE", False)

# Run in dry run mode to not affect the files, but output the logs
DRY_RUN = os.getenv("DRY_RUN", False)
