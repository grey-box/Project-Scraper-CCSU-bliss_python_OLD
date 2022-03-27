#!/bin/python

import argparse
from sys import stderr

import webres
import webres.webpage

parser = argparse.ArgumentParser('BLiSS WEb Scraper')
parser.add_argument('-w', '--site', type=str, required=True, 
        help='Specifies a URL to scrape')
args = parser.parse_args()

page = webres.webpage.Webpage(args.site)
page.acquire_resources().save()
