# Draft confirmatory protocol

Status: **frozen 2026-08-13 before any EEG amplitude or target-minus-standard result was inspected.**

The metadata-only audit of OpenNeuro `ds003061` version `1.1.0` confirmed event labels, run
semantics, channel availability, and the nominal participant count. Amendments must be timestamped,
justified without reference to a favorable result, and never silently replace this protocol.

## Confirmatory estimand

For each participant, calculate the mean Pz amplitude from 300 through 600 ms for target epochs and
standard epochs, then subtract standard from target. The group estimand is the mean of those
participant-level differences in microvolts. Participants, not trials, are the unit of inference.

## Hypothesis

- H0: the population mean target-minus-standard contrast is zero.
- H1: the population mean target-minus-standard contrast is not zero.

The expected direction is positive, but the confirmatory test is two-sided. Direction, interval,
and standardized effect size will be reported even when the test is not significant.

## Fixed choices inherited from the anchor paper

- Electrode: Pz.
- Time lock: stimulus onset.
- Epoch display range: -200 to 800 ms.
- Baseline: -200 to 0 ms, unless the external dataset's recording constraints make this impossible;
  any change must be made before contrast inspection and recorded as a protocol amendment.
- Measurement: arithmetic mean from 300 to 600 ms, inclusive.
- Contrast: target minus standard.

## Frozen external-dataset decisions

- Use all three runs, which the dataset README describes as identical sessions. Pool accepted
  epochs within condition and participant; never treat runs or trials as independent participants.
- Target events are `oddball_with_reponse`; standard events are `standard`. These are the upstream
  labels for correct target and correct non-target trials. Incorrect or ambiguous events are not
  reclassified.
- Require Pz in every included run; the audit found it in all 39 channel tables.
- Keep EEG channels only, apply a 50 Hz notch, a zero-phase 0.1–30 Hz band-pass filter, and an
  average EEG reference. Epoch from -200 through 800 ms and baseline-correct from -200 through 0 ms.
- Reject an epoch if its Pz peak-to-peak range exceeds 150 microvolts. Report sensitivity analyses
  at 100 and 200 microvolts; these do not replace the confirmatory result.
- A run must retain at least 20 correct target epochs and 100 correct standard epochs after artifact
  rejection. A participant must contribute at least one eligible run. The same thresholds apply
  before and after artifact rejection. This metadata rule excludes the visibly truncated
  `sub-012/run-1` before signal inspection.
- If fewer than eight participants remain, stop the confirmatory test and publish only a data-
  suitability report.

## Planned inference and reporting

- Two-sided one-sample t test of participant contrasts against zero, alpha 0.05.
- 95% confidence interval for the mean contrast and Cohen's dz.
- Sensitivity analyses: Wilcoxon signed-rank test, leave-one-participant-out estimates, and results
  across eligible runs kept separate from the confirmatory baseline analysis.
- Participant-level dot plot, target and standard grand-average waveforms, target-minus-standard
  difference waveform, and an explicit missing/excluded-participant table.
- Exact software environment, dataset DOI/version, checksum manifest, and random seeds.

No optional stopping is allowed. The available eligible participants in the pinned dataset form the
sample; no power-based claim will be made after seeing the result.

The primary test is run once at the frozen settings. Exploratory analyses and sensitivity checks
must be generated in a separate output namespace so they cannot overwrite the confirmatory result.

## Interactive boundary

The published interface may offer exploratory electrodes and windows, but it must keep the fixed
confirmatory result visible, label every changed analysis as exploratory, and provide a one-click
reset to the protocol settings.
