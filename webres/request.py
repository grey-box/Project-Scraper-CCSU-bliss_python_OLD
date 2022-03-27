""" A module that allows one to manipulate HTTP requests.
@author Kyle Guarco
"""

from typing import Optional 
import urllib.request as urlreq
import http.client as client

DEFAULT_USER_AGENT = 'Mozilla/5.0'

def urlopen(url: str, user_agent: Optional[str] = None) -> client.HTTPResponse:
    """ urllib.request.urlopen, except with a user agent. 
    @returns An HTTPResponse.
    """
    return urlreq.urlopen(urlreq.Request(url, headers={'User-Agent': user_agent or DEFAULT_USER_AGENT}))

