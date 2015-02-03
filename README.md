# Dataset for Bibliographical Survey of Prose Fiction Published in the British Isles

Scripts and original data required to generate a merged dataset (CSV) with a
list of novels described in the following sources:

* "British Fiction 1800-1829," ed. Garside et al. http://www.british-fiction.cf.ac.uk
* "The English Novel, 1830-1836," ed. Garside et al. http://www.cardiff.ac.uk/encap/journals/corvey/1830s/index.html
* Updates 1-6. http://www.romtext.cf.ac.uk/reports/index.html

## Data

Data `http://www.british-fiction.cf.ac.uk` was retrieved using `scripts/download-british-fiction-1800-1836.py`.

## Processing

The downloaded pages are processed with `scripts/process-british-fiction-1800-1829.py`, resulting
in the utf-8 encoded file `data/british-fiction-1800-1829.json` which contains a JSON-encoded dictionary.

## TODO

- Add 1770–99
