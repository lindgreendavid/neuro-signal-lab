# P3b target enhancement survives a fixed cross-dataset test

## Result in one sentence

Using a measurement fixed from ERP CORE before inspecting the external EEG signal, all 13
participants in OpenNeuro `ds003061` showed a positive correct-target-minus-correct-standard P3b
contrast at Pz from 300 to 600 ms; the participant-level mean was **+5.65 µV**, 95% CI
**[+4.83, +6.48]**, *t*(12) = 15.00, two-sided *p* = 3.88 × 10⁻⁹, Cohen's *dz* = 4.16.

This is best described as a **cross-paradigm robustness confirmation**, not a literal direct
replication: ERP CORE used an active visual oddball task, whereas the external dataset used an
active auditory three-stimulus oddball task.

## What was tested

ERP CORE recommends measuring P3 at Pz as the mean voltage from 300 to 600 ms after stimulus onset.
That electrode, window, contrast direction, participant-level unit of inference, artifact threshold,
and stopping rule were frozen before any EEG amplitude was inspected. The external test asked
whether correct auditory targets (`oddball_with_reponse`, the upstream spelling) were more positive
than correct standards (`standard`) under that unchanged endpoint.

## Evidence flow

1. The OpenNeuro `ds003061` version 1.1.0 metadata was audited at Git commit
   `223a18423a57d00dd1fb1fc3ac088b9d54c1e1e6` without inspecting signal amplitudes.
2. All 39 channel tables contained Pz; all recordings used 256 Hz sampling and documented 50 Hz
   line frequency.
3. The dataset described three identical runs per participant. Correct trials were pooled within
   participant, never treated as independent people.
4. One visibly truncated recording, `sub-012/run-1`, failed the frozen pre-signal minimum of 20
   correct targets and 100 correct standards. Its S3 object also conflicts with its DataLad pointer.
   It was excluded; the participant remained through runs 2 and 3.
5. The 38 eligible runs contributed 3,606 accepted target epochs and 19,481 accepted standard
   epochs after the 150 µV Pz peak-to-peak rule.

## Confirmatory result

| Quantity | Estimate |
| --- | ---: |
| Participants | 13 |
| Mean target-minus-standard contrast | +5.654 µV |
| Median contrast | +5.570 µV |
| 95% confidence interval for the mean | [+4.833, +6.476] µV |
| Two-sided one-sample test | *t*(12) = 15.004, *p* = 3.88 × 10⁻⁹ |
| Standardized effect | Cohen's *dz* = 4.161 |
| Positive participant contrasts | 13/13 |
| Wilcoxon sensitivity | *W* = 0, *p* = 0.000244 |

The result is not driven by a single participant: every participant-level contrast is positive,
ranging from +3.22 to +8.72 µV.

## Prespecified artifact-threshold sensitivity

| Pz peak-to-peak threshold | Mean contrast | 95% CI | Participants |
| --- | ---: | ---: | ---: |
| 100 µV | +5.827 µV | [+4.893, +6.761] | 13 |
| **150 µV (confirmatory)** | **+5.654 µV** | **[+4.833, +6.476]** | **13** |
| 200 µV | +5.738 µV | [+4.825, +6.652] | 13 |

The substantive conclusion is unchanged across all three thresholds.

## What this supports

The result supports the narrow claim that the fixed posterior 300–600 ms target enhancement is
robust enough to appear in an independent, small auditory-oddball dataset despite a modality and
paradigm change. It also demonstrates why fixing the electrode and time window before looking at
the external effect is useful: the result does not depend on searching the scalp or waveform for a
favorable region.

## What this does not support

- It does not show that visual and auditory oddball tasks engage identical processes.
- It does not uniquely localize a brain generator; scalp voltage is a mixed field measurement.
- It does not establish a diagnostic, therapeutic, or individual prediction tool.
- It does not generalize beyond this small sample of 13 people without further evidence.
- It does not prove that every preprocessing choice is harmless. The fixed analysis deliberately
  favors inspectability over a large, adaptive artifact-correction pipeline.
- The external dataset has no publication describing a purpose-built replication of ERP CORE; its
  role here is an independently hosted robustness sample.

## Reproducibility

The committed [protocol](protocol.md), [metadata audit](../data/metadata-audit.json), downloader,
analysis code, and [machine-readable result](../results/summary.json) provide the complete disclosed
path. Raw EEG is fetched from the pinned public source, checksum-verified for every included file,
and never committed. The reported run used Python 3.12.13, MNE-Python 1.12.1, NumPy 2.5.2, and
SciPy 1.18.0.

## Primary sources

1. Kappenman ES, Farrens JL, Zhang W, Stewart AX, Luck SJ. *ERP CORE: An open resource for human
   event-related potential research.* NeuroImage 225 (2021), 117465.
   <https://doi.org/10.1016/j.neuroimage.2020.117465>
2. Delorme A. *EEG data from an auditory oddball task.* OpenNeuro `ds003061`, version 1.1.0.
   <https://doi.org/10.18112/openneuro.ds003061.v1.1.0>
3. Pernet CR et al. *EEG-BIDS, an extension to the brain imaging data structure for
   electroencephalography.* Scientific Data 6 (2019), 103.
   <https://doi.org/10.1038/s41597-019-0104-8>
