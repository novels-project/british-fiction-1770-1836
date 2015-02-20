# Machine-readable version of *Bibliographical Survey of Prose Fiction Published in the British Isles*

Scripts and copies of original data required to generate machine-readable versions
of the following sources:

* "British Fiction 1800-1829," ed. Garside et al. http://www.british-fiction.cf.ac.uk
* "The English Novel, 1830-1836," ed. Garside et al. http://www.cardiff.ac.uk/encap/journals/corvey/1830s/index.html
* Updates 1-6. http://www.romtext.cf.ac.uk/reports/index.html

The following files contain machine-readable versions of these sources:

- `data/british-fiction-1800-1829.json`

## Recreating the dataset

1. Retrieve the index and detail pages from  `http://www.british-fiction.cf.ac.uk` using `scripts/download-british-fiction-1800-1836.py`.
2. Process the downloaded pages with `scripts/process-british-fiction-1800-1829.py`.

## Mirror of www.british-fiction.cf.ac.uk

The partial mirror of `www.british-fiction.cf.ac.uk` created by
`downloaded-british-fiction-1800-1836.py` was retrieved January 30th, 2015.

## Correcting errors

**Do not edit the `data/british-fiction-1800-1829.json` directly.** If there is
an error that is the result of parsing the mirror of
`http://www.british-fiction.cf.ac.uk` the errors need to be corrected in the
parsing scripts.

## TODO

- Add 1830-1836
- Add "updates" if not already included (a small number)
- Add 1770-99 (not yet trivially machine readable)
