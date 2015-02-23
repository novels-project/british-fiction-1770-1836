#!/usr/bin/env python3

import collections
import json
import logging
import os
import re

import bs4

BASE_DIR = os.path.abspath(__file__ + '/../../')
INPUT_DIR = os.path.join(BASE_DIR, 'data', 'www.british-fiction.cf.ac.uk')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data')
OUTPUT_FN = os.path.join(OUTPUT_DIR, 'british-fiction-1800-1829.json')

if __name__ == '__main__':
    index_fn = os.path.join(INPUT_DIR, 'titleIndex.asp')
    if not os.path.exists(index_fn):
        msg = "Mirror of british-fiction.cf.ac.uk not found."
        raise RuntimeError(msg)
    soup = bs4.BeautifulSoup(open(index_fn, 'r', encoding='utf-8'))
    record_filenames = set()
    records = []
    for rec in soup('tr', valign="top"):
        title_hrefs = [a.attrs['href'] for a in rec('a') if 'TitleDetails' in a.attrs['href']]
        # skip header and separators
        if len(title_hrefs) != 1:
            continue
        title_href = title_hrefs.pop()
        # get unique title_id
        try:
            title_id = re.search(r'title=([0-9A-Z]+)&', title_href).group(1)
        except AttributeError:
            msg = "Did not find title id for record in href: {}".format(title_href)
            raise RuntimeError(msg)

        # get details from the index page
        title_short = rec.em.string
        # author_short is typically last name
        author_or_translator_short = rec('td')[2].a.string.split(',')[0].strip('.')
        year_check = int(rec('td')[3].string)

        # get remaining information from full title record
        record_fn = os.path.join(INPUT_DIR, 'TitleDetails.asp?title={:s}&browse=y'.format(title_id))
        if record_fn in record_filenames:
            raise RuntimeError("Encountered duplicate record: ".format(record_fn))
        record_filenames.add(record_fn)

        details_soup = bs4.BeautifulSoup(open(record_fn, encoding='utf-8'))
        rows = details_soup("tr", align="left", valign="top")
        rows.reverse()
        record = collections.OrderedDict()

        ######################################################################
        # short title
        ######################################################################
        record['title_short'] = title_short

        ######################################################################
        # year
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if field != "Year:":
            raise RuntimeError("Expected 'Year:', found: {:s}".format(field))
        value = row('td')[1].string
        value = value.strip('.')
        year = int(value)
        if year != year_check:
            raise RuntimeError("Year from index doesn't match year on detail page.")
        record['year'] = year

        ######################################################################
        # author (or translator)
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Author(s)" in field:
            author = row('td')[1].a.b.string.strip().strip('.')
            if not author:
                raise RuntimeError("Expecting author: {:s}".format(row))
            if author_or_translator_short not in author:
                raise RuntimeError("Author from index doesn't match author: {}".format(row))
            record['author'] = author
        elif "Translator" in field:
            translator = row('td')[1].a.b.string.strip().strip('.')
            if not translator:
                raise RuntimeError("Expecting translator: {:s}".format(row))
            if author_or_translator_short not in translator:
                raise RuntimeError("Author from index doesn't match author: {}".format(row))
            record['translator'] = translator
        else:
            raise RuntimeError("Found neither author nor translator: {}".format(row))
        record['author_or_translator_short'] = author_or_translator_short

        ######################################################################
        # translator field, if present
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Translator" in field and 'translator' not in record:
            translator = row('td')[1].a.b.string.strip().strip('.')
            record['translator'] = translator
            if not translator:
                raise RuntimeError("Expecting translator: {:s}".format(row))
            # advance row
            row = rows.pop()
        elif "Translator" in field and 'translator' in record:
            raise RuntimeError("Found duplicate translator field in row: {}".format(row))

        ######################################################################
        # gender
        ######################################################################
        field = row('td')[0].strong.string
        if "Gender" not in field:
            raise RuntimeError("Expected Gender, found: {}".format(row))
        gender = row('td')[1].string.strip('.')
        if not gender:
            raise RuntimeError("Expecting gender: {:s}".format(row))
        record['gender'] = gender

        ######################################################################
        # full title
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        assert "Title" in field, "Expected Title, found: '%s'" % field
        title = row('td')[1].i.string.strip().strip('.')
        if not title:
            raise RuntimeError("Expecting title, found: {:s}".format(row))
        record['title'] = title

        ######################################################################
        # publication
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Publication" not in field:
            raise RuntimeError("Expected publication, found: {}".format(row))
        valuelst = row('td')[1].contents
        publication = ''.join(str(v) for v in valuelst).replace('\r\n','').strip().strip('.')
        publication = re.sub(r': \s+', ': ', publication)
        if not publication:
            raise RuntimeError("Expecting publication, found: {:s}".format(row))
        record['publication'] = publication

        ######################################################################
        # publication
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Format" not in field:
            raise RuntimeError("Expected Format, found: {}".format(row))
        format = row('td')[1].string.strip().strip('.')
        if not format:
            raise RuntimeError("Expecting format, found: {:s}".format(row))
        record['format'] = format

        ######################################################################
        # Catalog numbers
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Cat. nos" not in field:
            raise RuntimeError("Expected Cat. nos, found: {}".format(row))
        valuelst = row('td')[1].contents
        catalogue_numbers = ''.join(str(v) for v in valuelst).strip().strip('.')
        if not catalogue_numbers:
            raise RuntimeError("Expecting catalog numbers, found: {:s}".format(row))
        record['catalogue_numbers'] = catalogue_numbers


        ######################################################################
        # Notes
        ######################################################################
        row = rows.pop()
        field = row('td')[0].strong.string
        if "Notes" in field:
            valuelst = row('td')[1].contents
            # don't strip off the trailing period in this case
            notes = ''.join(str(v) for v in valuelst).strip()
            if not notes:
                raise RuntimeError("Expecting notes, found: {:s}".format(row))
            record['notes'] = notes
            row = rows.pop()

        ######################################################################
        # Further editions
        ######################################################################
        # if further editions fields present
        field = row('td')[0].strong.string
        if "Further" in field:
            valuelst = row('td')[1].contents
            further_eds = ''.join(str(v) for v in valuelst).strip().strip('.')
            if not further_eds:
                raise RuntimeError("Expecting further eds., found: {:s}".format(row))
            record['further_eds'] = further_eds
            row = rows.pop()

        ######################################################################
        # Skip empty row
        ######################################################################
        if len(row('td')) == 0:
            row = rows.pop()

        ######################################################################
        # Garside ID
        ######################################################################
        field = row('td')[0].strong.string
        if "DBF" not in field:
            raise RuntimeError("Expected DBF id, found: {}".format(row))
        id_check = row('td')[1].string.strip().strip('.')
        if title_id != id_check:
            raise RuntimeError("Garside id from index does not match detail: ".format(row))
        record['id'] = title_id
        records.append(record)

    ######################################################################
    # reorganize results, sorting by Garside ID
    ######################################################################
    records = collections.OrderedDict(sorted((record['id'], record) for record in records))

    ######################################################################
    # rudimentary tests
    ######################################################################
    id = '1822A005'
    r = records[id]
    assert len(r) == 12  # 10 fields + title_short from index
    fields_expected = set('id year author author_or_translator_short gender title publication '
                          'format catalogue_numbers notes further_eds title_short'.split())
    missing_fields = fields_expected.symmetric_difference(r.keys())
    assert len(missing_fields) == 0, "Problem with fields in {}, missing: {}".format(id, missing_fields)
    assert r['title'] == """THE COURT OF HOLYROOD; FRAGMENTS OF AN OLD STORY"""

    id = '1812A064'
    r = records[id]
    assert len(r) == 11  # 9 fields + title_short from index
    fields_expected = set('id year author author_or_translator_short gender title publication '
                          'format catalogue_numbers notes title_short'.split())
    missing_fields = fields_expected.symmetric_difference(r.keys())
    assert len(missing_fields) == 0, "Problem with fields in {}, missing: {}".format(id, missing_fields)
    assert r['title'] == """ROSAMUND, COUNTESS OF CLARENSTEIN. IN THREE VOLUMES"""

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
        f.write(s)
