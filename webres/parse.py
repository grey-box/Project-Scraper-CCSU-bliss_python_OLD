""" Contains tools for parsing a url into a filepath.
@author Kyle Guarco
"""

from pathlib import Path
from typing import List
from urllib.parse import ParseResult, urlparse

from osdir import get_storage_dir

def validate_url(parent: str, url: str) -> str:
    """ Fixes urls by assuring relative URLs become absolute URLs.
    Fixing the URL requires a valid netloc. 'parent' doesn't need
    to have an absolute path.
    @returns The URL, with scheme and netloc.
    """
    pres: ParseResult = urlparse(parent)
    ures: ParseResult = urlparse(url)

    if ures.scheme and ures.netloc:
        return url

    return ParseResult(scheme=pres.scheme, netloc=pres.netloc, path=ures.path, 
            params='', query='', fragment='').geturl()

def url2filepath(url) -> Path:
        """ Builds a folder path to the resource. 
        @returns A filepath
        """
        # Expected final type is ParseResult
        url = urlparse(url) if type(url) is str else url
    
        filepath: Path = get_storage_dir() / url.netloc

        pathsplit: List[str] = url.path.split('/')
        for path in pathsplit[:-1]:
            filepath /= path
        
        lastpath: str = pathsplit[-1:][0] 
        if not lastpath:
            lastpath = "index"

        if url.query or url.fragment:
            filepath /= lastpath
            filepath /= url.query
            filepath /= url.fragment

        if not filepath.exists():
            filepath.mkdir(parents=True)
        
        filepath /= lastpath

        return filepath


