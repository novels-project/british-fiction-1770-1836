Machine-readable version of *Bibliographical Survey of Prose Fiction Published in the British Isles*
====================================================================================================

Scripts and copies of original data required to generate machine-readable versions
of the following sources:

* "British Fiction 1800-1829," ed. Garside et al. http://www.british-fiction.cf.ac.uk
* "The English Novel, 1830-1836," ed. Garside et al. http://www.cardiff.ac.uk/encap/journals/corvey/1830s/index.html
* Updates 1-6. http://www.romtext.cf.ac.uk/reports/index.html

The following files contain machine-readable versions of these sources:

- `data/british-fiction-1800-1829.json`

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

Correcting errors
-----------------

**Do not edit the `data/british-fiction-1800-1829.json` directly.** If there is
an error that is the result of parsing the mirror of
`http://www.british-fiction.cf.ac.uk` the errors need to be corrected in the
parsing scripts.

TODO
----

- Add "updates" from updates 1-6 that are not included (e.g., update 6 has a text by ANON with title De Courcy...)
- Add 1770-99 (not yet trivially machine readable)
