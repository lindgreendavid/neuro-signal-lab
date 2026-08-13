# Draft confirmatory protocol

This document is deliberately marked **draft**. It becomes frozen only after a metadata-only audit
of OpenNeuro `ds003061` version `1.1.0` confirms event labels, run meanings, channel availability,
and usable participant count. The audit must not inspect target-minus-standard amplitudes.

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

## Pending metadata-only decisions

1. Which run is baseline and eligible for the confirmatory analysis.
2. Exact BIDS event values corresponding to target and standard stimuli.
3. Whether Pz is present under that exact channel name in every eligible recording.
4. Bad-channel, bad-epoch, eye-artifact, filtering, and rereferencing rules compatible with the
   source format.
5. Deterministic participant exclusions based only on missingness and prespecified data quality.

If any of these cannot be resolved without looking at the effect, the confirmatory study stops and
the project reports the dataset as unsuitable rather than silently changing the question.

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

## Interactive boundary

The published interface may offer exploratory electrodes and windows, but it must keep the fixed
confirmatory result visible, label every changed analysis as exploratory, and provide a one-click
reset to the protocol settings.
