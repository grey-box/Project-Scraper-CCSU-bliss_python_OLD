#!/bin/python

import argparse
from sys import stderr

import webres
import webres.webpage

parser = argparse.ArgumentParser('BLiSS WEb Scraper')
parser.add_argument('-w', '--site', type=str, required=True, 
        help='Specifies a URL to scrape')
args = parser.parse_args()

try:
    page = webres.webpage.Webpage(args.site)
    page.save()
except webres.types.WebResourceError:
    print('There was an error finding the web page.', file=stderr) 
except ValueError:
    print('Did you forget to add http:// or https:// to the URL?', file=stderr)

