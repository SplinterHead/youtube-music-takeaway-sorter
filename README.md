# YouTube Music Takeout Sorter

**YouTube Music Google Takeout is shit.** 
It leaves you with a disappointing flat structure of files

This sorter will hopefully be the one-shot tool to give your tracks some order.
It will scan the big list of files for MP3 metadata first, 
then it will work it's way through the provided CSV file and make educated guesses for where to place things

## Goal

This sorter should leave your music in such a way that another tool, such as Plex or Lidarr should be able to
recognise the music and display it in all its wonderful glory

**Features**
* Uses embedded metadata tags to organise what it can
* Dry Run mode to check the inner workings
* Adds metadata tags to the tracks without any

**Limitations**:
* Depending on how featuring artists have been stored, they may create a new artist directory.
* Unless in the metadata, the track numbers are unable to be added.
* Assumes all files were MP3s.

## How To Use

### Prerequisites
* Python3.9
* Poetry

### Dependencies
Once the prerequisites are installed, install the dependencies with either the `make` or `poetry` commands
```bash
# Make command
make install
# Poetry command
poetry install
```

### Configure
Next, check the configuration at `src/config.py`.
This file should represent the relevant paths to the existing music files, 
the CSV of metadata, and the desired directory for the music to end up in. 

There are also options for running the sorter in dry run mode to output what would be done 
without changing anything, and whether to copy or move the original file.

### Run
With all that in place, run either the `make` or `poetry` commands to execute the sorter
```bash
# Make command
make run
# Poetry command
poetry run python src/yt-sorter.py
```