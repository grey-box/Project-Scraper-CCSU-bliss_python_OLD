""" For manipulating websites
@author Kyle Guarco
"""

from typing import List
from urllib.request import urlopen
from urllib.error import URLError

from bs4 import BeautifulSoup, Tag

from .types import *

class Webpage(WebResource):
    def __init__(self, url: str, page_res: bool = False) -> None:
        super().__init__(url, '.html')
        self._page_res: bool = page_res
        try:
            with urlopen(url) as response:
                self._bs = BeautifulSoup(response.read(), 'html.parser')
        except (URLError, ValueError):
            raise WebResourceError

    def with_page_resources(self):
        self._page_res = True
        return self

    def links(self) -> List[Tag]:
        tags = self._bs.find_all(href=True)
        tags.extend(self._bs.find_all(src=True))
        return tags

    def save(self) -> bool:
        return super().save(self._bs.prettify().encode('utf-8'))

    def get_soup(self) -> BeautifulSoup:
        return self._bs
