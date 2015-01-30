#!/usr/bin/env python3

import os
import re
import time

import bs4
import requests


BASE_URL = 'http://www.british-fiction.cf.ac.uk/'
BASE_DIR = os.path.abspath(__file__ + '/../../')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'www.british-fiction.cf.ac.uk')


if __name__ == '__main__':
    index_url = BASE_URL + 'titleIndex.asp'
    index_fn = os.path.join(OUTPUT_DIR, os.path.basename(index_url))
    if not os.path.exists(index_fn):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        index_html = requests.get(index_url).text
        with open(index_fn, 'w', encoding='utf-8') as f:
            f.write(index_html)
    soup = bs4.BeautifulSoup(open(index_fn, 'r', encoding='utf-8'))
    records = soup('tr', valign="top")
    record_filenames = set()
    for i, rec in enumerate(records):
        title_href = rec.a.attrs['href']

        # skip header and separators
        if 'TitleDetails' not in title_href:
            continue
        # get unique title_id
        try:
            title_id = re.search(r'title=([0-9A-Z]+)&', title_href).group(1)
        except AttributeError:
            msg = "Did not find title id for record in href: {}".format(title_href)
            raise RuntimeError(msg)
        record_url = BASE_URL + 'TitleDetails.asp?title={:s}&browse=y'.format(title_id)
        record_fn = os.path.join(OUTPUT_DIR, os.path.basename(record_url))
        if record_fn in record_filenames:
            raise RuntimeError("Encountered duplicate record: ".format(record_fn))
        record_filenames.add(record_fn)
        print("Fetching {}".format(title_id))
        record_html = requests.get(record_url).text
        if not re.search('Title\s+details\s+for', record_html):
            msg = "Failed to retrieve record, url: {}".format(record_url)
            print(record_html)
            raise RuntimeError(msg)
        with open(record_fn, 'w', encoding='utf-8') as f:
            f.write(record_html)
