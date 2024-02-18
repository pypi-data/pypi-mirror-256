# MusicChecker

Application that provides a series of functions to retrieve tag information from media files.

## Features

-   Define libraries by familiar name
-   Pulls all tags from supported media files
-   Stored in a SQLite DB for fast retrieval

# Requirements

Python 3+

# Usage

# Supported Formats

-   MP3
-   FLAC

# Caching

Cached data is stored in the standard XDG directory

```txt
$HOME/$XDG_CACHE/MusicCheckerMicro/<library_name>
```

Usually /home/username/.cache/MusicChecker

# Testing

Run pytest in root directory passing in tests directory. Sample audio files are also contained within tests path

# TODO

-   ~Generate list of media files~
-   ~Extract from Music Manager Micro~
-   ~Put media files in DB~
-   ~for each entry find file~
-   ~extract tags from file~
    -   define tags in program
-   dynamic placement of cache dir
-   update on mtime

# Build

```python
python -m build
python -m twine upload dist/*
```