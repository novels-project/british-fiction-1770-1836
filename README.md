# Machine-readable version of Bibliographical Survey of Prose Fiction Published in the British Isles

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

## TODO

- Updates 1830-1836
- Add 1770-99
