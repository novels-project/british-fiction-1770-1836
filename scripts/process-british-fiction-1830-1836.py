#!/usr/bin/env python3

import collections
import json
import logging
import os
import re

import bs4

BASE_DIR = os.path.abspath(__file__ + '/../../')
INPUT_DIR = os.path.join(BASE_DIR, 'data', 'www.cf.ac.uk')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_FN = os.path.join(OUTPUT_DIR, 'british-fiction-1830-1836.json')

if __name__ == '__main__':
    index_fn = os.path.join(INPUT_DIR, '1830-36.html')
    if not os.path.exists(index_fn):
        msg = "Mirror of british-fiction.cf.ac.uk not found."
        raise RuntimeError(msg)
    html = open(index_fn, 'r', encoding='latin1').read()
    # \xa0 is non-breaking space in Latin1 (ISO 8859-1)
    html = html.replace(r'\xa0', ' ')
    soup = bs4.BeautifulSoup(html)
    title_ids = set()
    records = []
    for rec in soup('p', align="justify"):
        record = collections.OrderedDict()
        text = rec.text
        html = str(rec)
        title_id_matches = re.search(r'^\s*([0-9]{4}):\s*([0-9]+\s*[()a-z]*)', text)
        if title_id_matches is None:
            continue
        title_id = ':'.join(title_id_matches.groups())
        # strip all whitespace from title id
        title_id = re.sub(r'\s+', '', title_id)
        if title_id in title_ids:
            raise RuntimeError("Found duplicate id {}".format(title_id))
        title_ids.add(title_id)
        record['id'] = title_id
        record['year'] = int(title_id_matches.group(1))

        # extract author
        lines = html.split('<br/>')
        line_cleaned = re.sub(r'\s+', ' ', bs4.BeautifulSoup(lines[0]).text)
        author_match = re.search(r'[{[A-Z].*$', line_cleaned)
        if author_match is None:
            raise RuntimeError("Did not find author in title id {}".format(title_id))
        record['author'] = author_match.group()

        # extract title
        line_cleaned = re.sub(r'\s+', ' ', bs4.BeautifulSoup(lines[1]).text)
        if re.search(r'[A-Z]+', line_cleaned) is None:
            raise RuntimeError("Did not find title in title id {}".format(title_id))
        record['title'] = line_cleaned

        # extract publisher
        # first remove initial closing tags
        line = lines[2].replace(r'</', '<')
        line_cleaned = re.sub(r'\s+', ' ', bs4.BeautifulSoup(line).text)
        if re.search(r'18[0-9]+.*\.', line_cleaned) is None:
            raise RuntimeError("Did not find full publisher in title id {}".format(title_id))
        record['publisher'] = line_cleaned
        records.append(record)

    ######################################################################
    # reorganize results, sorting by Garside ID
    ######################################################################
    records = collections.OrderedDict((record['id'], record) for record in records)

    ######################################################################
    # store results
    ######################################################################
    # rearrange results
    with open(OUTPUT_FN, 'w', encoding='utf8') as f:
        s = json.dumps(records, f, ensure_ascii=False, indent=2)
        # for some reason 0x96 sneaks in to the HTML; it's invariably an en-dash, '–' \u2013
        s = s.replace('\x96', '\u2013')
        # for some reason 0x97 sneaks in to the HTML; it's invariably an em-dash, '–' \u2014
        s = s.replace('\x97', '\u2014')
        # for some reason 0x97 sneaks in to the HTML; it's an ellipsis \u2026
        s = s.replace('\x85', '\u2026')
        # for some reason 0x92 sneaks in to the HTML; it's ’ \u2019
        s = s.replace('\x92', '\u2019')
        # for some reason 0x91 sneaks in to the HTML; it's ‘ \u2018
        s = s.replace('\x91', '\u2018')
        # corrections for “ and ”
        s = s.replace('\x93', '\u201c')
        s = s.replace('\x94', '\u201d')
        f.write(s)
