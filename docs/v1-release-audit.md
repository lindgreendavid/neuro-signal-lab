# v1.0.0 release audit

Audit date: 2026-08-13. Scientific baseline: `2fde5c853c9f3b29f7b10c5c171057369ec6347f`.
The exact product-release commit is the commit resolved by annotated tag `v1.0.0`.

## Evidence checked

- ERP CORE fixes the P3b measurement anchor; OpenNeuro `ds003061` version 1.1.0 is the independent
  auditory-oddball dataset. Primary identifiers: DOI
  [10.1016/j.neuroimage.2020.117465](https://doi.org/10.1016/j.neuroimage.2020.117465) and
  [10.18112/openneuro.ds003061.v1.1.0](https://doi.org/10.18112/openneuro.ds003061.v1.1.0).
- Dataset identity, downloaded-file checksums, participant/run eligibility, event labels and
  exclusions were rechecked by the frozen pipeline tests.
- The committed result contains 13 participants, 38 eligible runs, 3,606 accepted target trials,
  19,481 accepted standard trials, and the fixed Pz 300–600 ms target-minus-standard endpoint.
- Mean participant contrast: +5.6544 µV; 95% CI [+4.8334, +6.4755]; all 13 contrasts positive.
  Artifact-threshold sensitivity outputs remain machine-readable in `results/summary.json`.

## Reproduction and integrity

`python -m unittest discover -s tests -v` and the real-data pipeline contract are the release
gates. SHA-256 of `results/summary.json` before the v1 product release:
`3f9ed3a4d86d3035793891ec4e2085813d74917519b4295ff937710fdd4eb58f`.

## Boundary

v1.0.0 marks stable software, documentation and interaction design. It does not create a new
preregistration, alter the frozen endpoint, or generalize beyond this dataset and preprocessing
pipeline.
