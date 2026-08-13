# Neuro Signal Lab

<p><a href="https://github.com/lindgreendavid/lindgreendavid/tree/main/brand"><img src="https://raw.githubusercontent.com/lindgreendavid/lindgreendavid/main/brand/lab-notes-mark.svg" width="52" align="right" alt="Lab Notes research-cycle mark"></a></p>

**Part of the [Lab Notes Research Portfolio](https://blog-interactive.lindgreendavid.workers.dev/)** · Neuroscience · Question → evidence → finding → boundary

An inspectable neuroscience program for asking a narrow question: **does the classic P3b
target-minus-standard effect remain visible when the measurement is fixed in advance and applied
to an independent public EEG dataset?**

**[Open the interactive Neuro Signal Lab](https://lindgreendavid.github.io/neuro-signal-lab/)**

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
- The first confirmatory result is complete: mean participant-level P3b contrast **+5.65 µV**,
  95% CI **[+4.83, +6.48]**, with all 13 participant contrasts positive. Read the
  [research report](docs/research-report.md) for the exact inference and boundaries.

## Interactive experience

The static laboratory in [`site/`](site/) lets a visitor:

1. inspect the fixed Pz, 300–600 ms endpoint without changing it;
2. explore every participant-level contrast rather than seeing only a group mean;
3. compare the confirmatory artifact threshold with both prespecified sensitivity analyses;
4. keep the visual ERP CORE anchor and independent auditory dataset conceptually distinct;
5. trace each displayed value back to data version, preprocessing decision, and code.

Open [`site/index.html`](site/index.html) directly or serve the repository root with any static web
server. The interface is dependency-free, responsive, keyboard-accessible, and uses only committed
machine-readable results. Its waveform graphic is explicitly labelled as an illustration because
the repository does not publish a time-series aggregate.

## Development

Requires Python 3.10 or newer. The small analysis contract has no runtime dependency; the real EEG
pipeline uses the pinned MNE-Python analysis extra.

```bash
python -m unittest discover -s tests
python -m pip install -e '.[analysis]'
neuro-signal-fetch --subject sub-001
neuro-signal-analyze --data-root data/raw --output data/derived/confirmatory.json
```

Fetching and analysis are deliberately separate. The fetch command verifies every included `.set`
file against the MD5 identifier stored in OpenNeuro's pinned DataLad metadata. It explicitly skips
the frozen `sub-012/run-1` metadata exclusion; that run's current 8 MB S3 object conflicts with its
63 MB DataLad pointer and both its event table and signal file are truncated. The analysis command
writes the fixed confirmatory result to its own namespace.

Read [the research scope](docs/research-scope.md) and [the draft protocol](docs/protocol.md) before
adding a data pipeline or user interface.

## Scientific boundary

Scalp EEG is not a direct readout of a single brain region, and a positive P3b contrast is not a
diagnosis, a mind-reading result, or proof of one unique cognitive mechanism. This project is an
educational reproducibility study, not a clinical device.

Code is MIT-licensed. Upstream data and materials retain their own licenses and must be cited
separately.
