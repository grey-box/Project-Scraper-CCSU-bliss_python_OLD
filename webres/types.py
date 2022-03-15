""" Classes for parsing webpage resources. 
@author Kyle Guarco
"""

from pathlib import Path
from urllib.parse import ParseResult, urlparse

from osdir import get_storage_dir

class WebResourceError(Exception):
    """ Raised when a WebResource cannot aquire a remote resource. """
    pass

class WebResource():
    """ Blanket implementation for a remote resource. """
    def __init__(self, url: str, ext: str):
        self._url: ParseResult = urlparse(url)
        self._ext: str = ext
        self._genpath: Path = self._filepath()

    def _filepath(self) -> Path:
        """ Builds a folder path to the resource. 
        @returns A filepath
        """
        filepath = get_storage_dir() / self._url.netloc

        pathsplit = self._url.path.split('/')
        for path in pathsplit[:-1]:
            filepath /= path
        
        lastpath = pathsplit[-1:][0] 
        if not lastpath:
            lastpath = "index"

        if self._url.query or self._url.fragment:
            filepath /= lastpath
            filepath /= self._url.query
            filepath /= self._url.fragment

        if not filepath.exists():
            filepath.mkdir(parents=True)
        
        filepath /= lastpath + self.getextension()

        return filepath

    def filename(self) -> str:
        """ Builds and returns the expected local resource name. """
        return self._genpath.name

    def save(self, contents: bytes) -> bool:
        """ Saves this resource to the local filesystem. 
        if self._genpath.exists():
        """
        if self.exists():
            return False
        
        with self._genpath.open(mode='wb') as file:
            file.write(contents)

        return True

    def getextension(self) -> str:
        """ Returns the expected file extension of this resource. """
        return self._ext

    def getsite(self) -> str:
        """ Returns the URL this resource was obtained from. """
        return self._url.geturl()

    def exists(self) -> bool:
        return self._genpath.exists()

