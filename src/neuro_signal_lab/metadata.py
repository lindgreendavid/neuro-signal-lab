"""Metadata-only contracts for the pinned OpenNeuro snapshot."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

TARGET_LABEL = "oddball_with_reponse"
STANDARD_LABEL = "standard"
MIN_TARGET_TRIALS = 20
MIN_STANDARD_TRIALS = 100


@dataclass(frozen=True)
class RunAudit:
    path: str
    target_trials: int
    standard_trials: int

    @property
    def eligible_before_artifact_rejection(self) -> bool:
        return (
            self.target_trials >= MIN_TARGET_TRIALS and self.standard_trials >= MIN_STANDARD_TRIALS
        )


def audit_event_file(path: Path) -> RunAudit:
    """Count only the two frozen correct-trial labels in one BIDS event table."""

    counts = {TARGET_LABEL: 0, STANDARD_LABEL: 0}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if "value" not in (reader.fieldnames or []):
            raise ValueError(f"{path} has no value column")
        for row in reader:
            value = row["value"]
            if value in counts:
                counts[value] += 1
    return RunAudit(str(path), counts[TARGET_LABEL], counts[STANDARD_LABEL])


def pz_is_eeg_channel(path: Path) -> bool:
    """Return whether a BIDS channel table contains Pz as an EEG channel."""

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        return any(row.get("name") == "Pz" and row.get("type") == "EEG" for row in reader)


def load_frozen_audit(path: Path) -> dict[str, object]:
    """Load the committed audit and refuse any audit that inspected signal."""

    audit = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    if audit.get("signal_inspected_during_audit") is not False:
        raise ValueError("metadata audit must explicitly record that signal was not inspected")
    return audit
