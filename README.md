# Neuro Signal Lab

An inspectable neuroscience program for asking a narrow question: **does the classic P3b
target-minus-standard effect remain visible when the measurement is fixed in advance and applied
to an independent public EEG dataset?**

The first study is deliberately staged. ERP CORE supplies the literature-anchored measurement
definition (Pz, mean voltage from 300–600 ms after stimulus onset). OpenNeuro `ds003061` is the
candidate external auditory-oddball dataset. No external result has been calculated yet, and the
protocol will not be frozen until its BIDS event labels and run semantics have been audited without
looking at the confirmatory contrast.

## Current status

- Research question selected from primary sources.
- Analysis contract implemented and tested independently of the research data.
- Draft protocol records the confirmatory endpoint, sensitivity analyses, exclusions, and stopping
  boundary.
- Raw data are never committed; the planned pipeline will fetch a pinned dataset snapshot.
- No scientific result is claimed at this stage.

## Planned interactive experience

The public laboratory will let a visitor:

1. compare target and standard waveforms without changing the preregistered endpoint;
2. move a *clearly labelled exploratory* time window and see why analytic flexibility matters;
3. inspect every participant-level contrast and uncertainty interval;
4. compare the visual ERP CORE anchor with the independent auditory dataset while keeping the
   paradigm difference visible;
5. trace each displayed value back to data version, preprocessing decision, and code.

## Development

Requires Python 3.9 or newer.

```bash
python -m unittest discover -s tests
```

Read [the research scope](docs/research-scope.md) and [the draft protocol](docs/protocol.md) before
adding a data pipeline or user interface.

## Scientific boundary

Scalp EEG is not a direct readout of a single brain region, and a positive P3b contrast is not a
diagnosis, a mind-reading result, or proof of one unique cognitive mechanism. This project is an
educational reproducibility study, not a clinical device.

Code is MIT-licensed. Upstream data and materials retain their own licenses and must be cited
separately.
