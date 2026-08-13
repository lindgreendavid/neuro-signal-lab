"""Small, dependency-free functions that define the confirmatory P3 endpoint.

Signal preprocessing and file access intentionally live outside this module. Keeping the endpoint
pure makes it possible to test the scientific contract before any research data are inspected.
"""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean, median, stdev
from typing import Sequence


P3_WINDOW_MS = (300.0, 600.0)


@dataclass(frozen=True)
class P3Summary:
    """Participant-level summary of target-minus-standard P3 mean amplitudes."""

    participants: int
    mean_uv: float
    median_uv: float
    standard_deviation_uv: float
    cohen_dz: float
    positive_fraction: float


def window_mean(
    times_ms: Sequence[float],
    amplitudes_uv: Sequence[float],
    window_ms: tuple[float, float] = P3_WINDOW_MS,
) -> float:
    """Return the inclusive mean amplitude inside a fixed time window."""

    if len(times_ms) != len(amplitudes_uv):
        raise ValueError("times and amplitudes must have the same length")
    if len(times_ms) == 0:
        raise ValueError("at least one sample is required")

    start_ms, end_ms = window_ms
    if start_ms > end_ms:
        raise ValueError("window start must not exceed window end")

    selected = [
        amplitude
        for time, amplitude in zip(times_ms, amplitudes_uv)
        if start_ms <= time <= end_ms
    ]
    if not selected:
        raise ValueError("the requested window contains no samples")
    return mean(selected)


def p3_contrast(target_mean_uv: float, standard_mean_uv: float) -> float:
    """Return the preregistered direction: target minus standard, in microvolts."""

    return target_mean_uv - standard_mean_uv


def summarize_contrasts(contrasts_uv: Sequence[float]) -> P3Summary:
    """Summarize participant-level contrasts without silently dropping observations."""

    if len(contrasts_uv) < 2:
        raise ValueError("at least two participant contrasts are required")

    values = [float(value) for value in contrasts_uv]
    spread = stdev(values)
    effect = mean(values) / spread if spread else float("inf")
    positive = sum(value > 0 for value in values) / len(values)

    return P3Summary(
        participants=len(values),
        mean_uv=mean(values),
        median_uv=median(values),
        standard_deviation_uv=spread,
        cohen_dz=effect,
        positive_fraction=positive,
    )
