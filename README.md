Machine-readable version of *Bibliographical Survey of Prose Fiction Published in the British Isles*
====================================================================================================

Scripts and copies of original data required to generate machine-readable versions
of the following sources:

* "British Fiction 1800-1829," ed. Garside et al. http://www.british-fiction.cf.ac.uk
* "The English Novel, 1830-1836," ed. Garside et al. http://www.cardiff.ac.uk/encap/journals/corvey/1830s/index.html
* Updates 1-6. http://www.romtext.cf.ac.uk/reports/index.html

The following files contain machine-readable versions of these sources:

- `data/british-fiction-1800-1829.json`
- `data/british-fiction-1830-1836.json`
- `data/british-fiction-1800-1829-updates.json`

Recreating the dataset (1800-1829)
----------------------------------

1.  Retrieve the index and detail pages from  `http://www.british-fiction.cf.ac.uk` using `scripts/download-british-fiction-1800-1836.py`.
2.  Process the downloaded pages with `scripts/process-british-fiction-1800-1829.py`.

The partial mirror of `www.british-fiction.cf.ac.uk` created by
`downloaded-british-fiction-1800-1836.py` was retrieved January 30th, 2015.

Recreating the dataset (1830-1836)
----------------------------------

1.  Retrieve the file `1830-36.html` from `http://www.cf.ac.uk/encap/journals/corvey/1830s/1830-36.html` and
    place it in `data/www.cf.ac.uk/`.
2.  Process the html with `scripts/process-british-fiction-1830-1836.py`.

A copy of `1830-36.html` is stored in this repository. The server at
`http://www.cf.ac.uk/` reports its last modification date as: Tue, 22 May 2012
12:40:26 GMT

Recreating the dataset (Updates 1-6)
------------------------------------

There are 4 novels given in the "New Titles for Inclusion" sections of Updates
4 through 6. These have been entered manually into
`data/british-fiction-1800-1829-updates.json`. Copies of Updates 1-6 are stored
in the repository.

The section "C: New Titles for Inclusion" in
[Updates 1-6](http://www.romtext.cf.ac.uk/reports/index.html) lists a small number of
novels that have been discovered since the publication of British Fiction,
1800-1829.

Some of these new entries are in the `http://www.british-fiction.cf.ac.uk` database.

- "New Titles for Inclusion" in [Update 1](http://www.romtext.cf.ac.uk/reports/engnov1.html) are included in 1800-1829.
- "New Titles for Inclusion" in [Update 2](http://www.romtext.cf.ac.uk/reports/engnov2.html) are included in 1800-1829.
- "New Titles for Inclusion" in [Update 3](http://www.romtext.cf.ac.uk/reports/engnov3.html) are included in 1800-1829.

Some of these new entires **are not** in the `http://www.british-fiction.cf.ac.uk` database.

- "New Titles for Inclusion" in [Update 4](http://www.romtext.cf.ac.uk/reports/engnov4.html) *are not* included in 1800-1829.
- "New Titles for Inclusion" in [Update 5](http://www.romtext.cf.ac.uk/reports/engnov5.html) *are not* included in 1800-1829.
- "New Titles for Inclusion" in [Update 6](http://www.romtext.cf.ac.uk/reports/engnov6.html) *are not* included in 1800-1829.

The novel referenced in Update 5 and Update 6 is the same one: ANON. DE COURCY: A TALE. Isle of Wight: The Author, 1825.

Correcting errors
-----------------

**Do not edit the `british-fiction-1800-1829.json` or `british-fiction-1830-1836.json` directly.** If there is an error that is the
result of parsing the mirror of `http://www.british-fiction.cf.ac.uk` the
errors need to be corrected in the parsing scripts.

TODO
----
- Add 1770-99 (not yet trivially machine readable)
