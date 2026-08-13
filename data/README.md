# Data boundary

Raw and derived EEG files are intentionally excluded from Git.

The future fetch step must pin OpenNeuro `ds003061` version `1.1.0`, record file checksums, and
download only the preregistered recordings. A metadata-only manifest may be committed after the
event/run audit. Every derived table must retain participant, run, condition, dataset version, and
pipeline-version provenance without containing direct identifiers.
