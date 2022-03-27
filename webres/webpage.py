""" For manipulating webpages
@author Kyle Guarco
"""

from __future__ import annotations
from typing import List, final
from urllib.error import URLError

from bs4 import BeautifulSoup, Tag

from util import flatmap
from webres.parse import validate_url
from webres.request import urlopen

from . import *

@final
class Webpage(WebResource):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        try:
            with urlopen(url) as response:
                self._bs = BeautifulSoup(response.read(), 'html.parser')
        except (URLError, ValueError):
            raise WebResourceError

    def acquire_resources(self):
        """ Enables resource acquisition for this webpage.
        When this function is called, all tags with the 'src' attribute
        are collected, transformed into WebResources and saved.
        @returns Self.
        """
        def change_tag_src(wtag: Tag) -> WebResource:
            link: str = str(wtag['src'])
            res: WebResource = WebResource(validate_url(self.get_url(), link))
            wtag['src'] = res.get_path().as_uri()
            return res
        
        tags: List[Tag] = self.get_soup().find_all(src=True)

        # Make a list over a mapped element...
        weblist: List[WebResource] = list(map(change_tag_src, tags))

        # Save each resource
        for res in weblist:
            res.save()

        return self
    
    def spider(self) -> List[Webpage]:
        """ Crawls through a webpage and retrieves 'href' tags.
        @returns A list of Webpages.
        """
        def change_tag_href(wtag: Tag) -> Webpage:
            link: str = str(wtag['href'])
            print(link)
            return Webpage(validate_url(self.get_url(), link))

        tags: List[Tag] = self.get_soup().find_all(href=True)
        return list(map(change_tag_href, tags))

    def save(self) -> bool:
        page_encoding = str(self.get_soup().original_encoding) or 'utf-8'
        super().provide_bytes(self.get_soup().prettify().encode(page_encoding))
        return super().save()

    def get_soup(self) -> BeautifulSoup:
        return self._bs

