import os

# Current directory for all files
from distutils.util import strtobool

# Environment Setup
MUSIC_ROOT = os.getenv("MUSIC_ROOT", None)
MUSIC_DEST = os.getenv("DESTINATION", f"{MUSIC_ROOT}/Structured")
CSV_PATH = os.getenv("CSV_PATH", f"{MUSIC_ROOT}/music-uploads-metadata.csv")
MOVE_SOURCE = strtobool(os.getenv("MOVE_SOURCE", "False"))
DRY_RUN = strtobool(os.getenv("DRY_RUN", "False"))

# Constants
DIR_UNSAFE_CHARS = "/"
TAKEOUT_UNSAFE_CHARS = ":?'\"&*/;<>%"
