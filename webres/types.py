""" Classes for parsing webpage resources. 
@author Kyle Guarco
"""

from http.client import HTTPResponse
from io import BufferedWriter
from pathlib import Path
from typing import Optional
from urllib.parse import ParseResult, urlparse

from webres.request import urlopen
from webres.parse import url2filepath

class WebResourceError(Exception):
    """ Raised when a WebResource cannot aquire a remote resource. """
    pass

class WebResource():
    """ Blanket implementation for a remote resource. """
    def __init__(self, url: str):
        self._url: ParseResult = urlparse(url)
        self._genpath: Path = url2filepath(self._url)
        self._savebytes: Optional[bytes] = None

    def filename(self) -> str:
        """ Builds and returns the expected local resource name. """
        return self._genpath.name

    def provide_bytes(self, content: bytes):
        """ Provide the bytes for saving the file instead. 
        This is used if the data has already been obtained, so the
        programmer doesn't have to make another web request for the data.
        @returns Self.
        """
        self._savebytes = content
        return self

    def save(self) -> bool:
        """ Saves this resource to the local filesystem. """
        if self.exists():
            return False
        
        with self._genpath.open(mode='wb') as file:
            file: BufferedWriter
            if not self._savebytes:
                with urlopen(self.get_url()) as content:
                    content: HTTPResponse
                    data = content.read()
            else:
                data = self._savebytes
            file.write(data)

        return True

    def get_path(self) -> Path:
        """ Returns the expected file extension of this resource. """
        return self._genpath

    def get_url(self) -> str:
        """ Returns the URL this resource was obtained from. """
        return self._url.geturl()

    def exists(self) -> bool:
        return self._genpath.exists()

