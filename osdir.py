""" Cross-platofrm storage support
Provides support for opening storage directories for
bliss-scraper across supported operating systems.
"""

from pathlib import Path, PosixPath, WindowsPath

_EXPECTED_STORAGE_DIR = 'bliss-web-scraper'

def get_storage_dir() -> Path:
    path: Path = Path().home()
    
    if isinstance(path, PosixPath):
        path = path.joinpath('.local/share/Greybox/' + _EXPECTED_STORAGE_DIR)
    elif isinstance(path, WindowsPath):
        path = path.joinpath('AppData/Roaming/Greybox/' + _EXPECTED_STORAGE_DIR)
    else: # Just point to a spot in their home folder
        path = path.joinpath(".greybox/" + _EXPECTED_STORAGE_DIR)
     
    if not path.exists():
        path.mkdir(parents=True)
    return path

