#!/bin/python

import argparse
from sys import stderr
from urllib.request import urlopen
from urllib.error import URLError
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser('BLiSS WEb Scraper')
parser.add_argument('-w', '--site', type=str, required=True, 
        help='Specifies a URL to scrape')
args = parser.parse_args()

try:
    with urlopen(args.site) as response:
        from .osdir import get_storage_dir
        soup = BeautifulSoup(response.read(), 'html.parser')
        print(soup.prettify())
except URLError:
    print('There was an error finding the web page.', file=stderr) 
except ValueError:
    print('Did you forget to add http:// or https:// to the URL?', file=stderr)

