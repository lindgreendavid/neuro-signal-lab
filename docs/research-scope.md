# Research scope

Status: **external metadata audited; confirmatory protocol frozen before EEG inspection**
Date: 2026-08-13

## Bounded question

Does a fixed P3b endpoint — participant-level target-minus-standard mean voltage at Pz from 300 to
600 ms after stimulus onset — remain positive in an independent public auditory-oddball EEG
dataset?

This is a cross-dataset robustness check, not a claim that visual and auditory oddball paradigms
are interchangeable.

## Why this endpoint

Kappenman et al. created ERP CORE from 40 neurotypical young adults and six optimized paradigms.
For its active visual oddball task, the paper recommends Pz and a 300–600 ms mean-amplitude window
for P3. Those choices are adopted *before* inspecting the candidate external contrast, preventing
the site and time window from being selected for a favorable result.

## Candidate external evidence

OpenNeuro snapshot `ds003061` version `1.1.0` is a CC0, BIDS-formatted auditory oddball EEG dataset
with 13 participants, three documented identical runs per participant, 64 EEG channels (79 recorded
channels including auxiliary signals), and a 256 Hz sampling rate. It is small, so uncertainty and
participant-level results must remain prominent.

The metadata-only audit used the version tag `1.1.0` at Git commit
`223a18423a57d00dd1fb1fc3ac088b9d54c1e1e6`. Pz exists in all 39 channel tables. The dataset's own
HED definitions identify `oddball_with_reponse` as a correct target event and `standard` as a
correct non-target event. The misspelling of “response” is part of the upstream label and is kept
verbatim. Across all runs, the sidecars contain 3,667 correct target events and 19,855 correct
standard events. `sub-012/run-1` is visibly truncated in metadata (9 correct targets and 64 correct
standards), which motivated the run-level minimum trial rule before EEG amplitudes were inspected.
The later fetch validation also found that its 8,025,984-byte S3 object conflicts with the
63,026,728-byte Git-annex pointer; this strengthens the exclusion but did not create it.

## Primary sources

1. Kappenman ES, Farrens JL, Zhang W, Stewart AX, Luck SJ. *ERP CORE: An open resource for human
   event-related potential research.* NeuroImage 225 (2021), 117465.
   <https://doi.org/10.1016/j.neuroimage.2020.117465>
2. ERP CORE resource and materials. <https://erpinfo.org/erp-core>
3. Delorme A. *EEG data from an auditory oddball task*, OpenNeuro `ds003061`, version 1.1.0.
   <https://doi.org/10.18112/openneuro.ds003061.v1.1.0>
4. Pernet CR et al. *EEG-BIDS, an extension to the brain imaging data structure for
   electroencephalography.* Scientific Data 6 (2019), 103.
   <https://doi.org/10.1038/s41597-019-0104-8>

## Interpretation boundary

- The external sample is small and contains repeated recordings.
- A positive scalp voltage does not uniquely localize a neural generator.
- Cross-paradigm agreement would support robustness of the measurement, not equivalence of the
  underlying cognitive operations.
- Failure to reject zero would not prove absence of P3b; data quality and power must be reported.
- The study is non-clinical and must not be framed as diagnostic or therapeutic.
