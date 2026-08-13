"""Frozen participant-level P3b analysis for the pinned OpenNeuro dataset."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

from .analysis import P3_WINDOW_MS, p3_contrast, summarize_contrasts, window_mean
from .fetch import EXCLUDED_RECORDINGS
from .metadata import MIN_STANDARD_TRIALS, MIN_TARGET_TRIALS, STANDARD_LABEL, TARGET_LABEL


ARTIFACT_THRESHOLD_UV = 150.0
EVENT_IDS = {TARGET_LABEL: 1, STANDARD_LABEL: 2}


@dataclass(frozen=True)
class RunResult:
    recording: str
    accepted_target_trials: int
    accepted_standard_trials: int
    eligible: bool
    reason: str | None


@dataclass(frozen=True)
class ParticipantResult:
    participant: str
    included_runs: int
    target_trials: int
    standard_trials: int
    target_mean_uv: float
    standard_mean_uv: float
    contrast_uv: float


def read_events(path: Path) -> tuple[list[list[int]], dict[str, int]]:
    """Read frozen correct-trial events and return MNE-compatible sample rows."""

    events: list[list[int]] = []
    counts = {TARGET_LABEL: 0, STANDARD_LABEL: 0}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        for row in reader:
            label = row.get("value")
            if label in EVENT_IDS:
                events.append([int(row["sample"]), 0, EVENT_IDS[label]])
                counts[label] += 1
    return events, counts


def analyze_recording(set_path: Path, threshold_uv: float = ARTIFACT_THRESHOLD_UV):
    """Return accepted Pz epochs for one run; imports MNE only for real-data execution."""

    import mne
    import numpy as np

    stem = set_path.name.removesuffix("_eeg.set")
    event_path = set_path.with_name(f"{stem}_events.tsv")
    channel_path = set_path.with_name(f"{stem}_channels.tsv")
    events, pre_counts = read_events(event_path)
    if pre_counts[TARGET_LABEL] < MIN_TARGET_TRIALS or pre_counts[STANDARD_LABEL] < MIN_STANDARD_TRIALS:
        return None, None, None, RunResult(stem, 0, 0, False, "below pre-artifact trial minimum")

    with channel_path.open(newline="", encoding="utf-8") as handle:
        eeg_names = [
            row["name"] for row in csv.DictReader(handle, delimiter="\t") if row["type"] == "EEG"
        ]
    if "Pz" not in eeg_names:
        return None, None, None, RunResult(stem, 0, 0, False, "Pz is not an EEG channel")

    raw = mne.io.read_raw_eeglab(set_path, preload=True, verbose="ERROR")
    raw.pick(eeg_names)
    raw.filter(0.1, 30.0, phase="zero", verbose="ERROR")
    raw.set_eeg_reference("average", projection=False, verbose="ERROR")
    mne_events = np.asarray(events, dtype=int)
    mne_events[:, 0] += raw.first_samp

    epochs = mne.Epochs(
        raw,
        mne_events,
        event_id=EVENT_IDS,
        tmin=-0.2,
        tmax=0.8,
        baseline=(-0.2, 0.0),
        picks=["Pz"],
        reject={"eeg": threshold_uv * 1e-6},
        preload=True,
        verbose="ERROR",
    )
    target = epochs[TARGET_LABEL].get_data(copy=True)[:, 0, :] * 1e6
    standard = epochs[STANDARD_LABEL].get_data(copy=True)[:, 0, :] * 1e6
    eligible = len(target) >= MIN_TARGET_TRIALS and len(standard) >= MIN_STANDARD_TRIALS
    reason = None if eligible else "below post-artifact trial minimum"
    result = RunResult(stem, len(target), len(standard), eligible, reason)
    times_ms = epochs.times * 1000.0
    return (target if eligible else None), (standard if eligible else None), times_ms, result


def analyze_participant(
    subject_directory: Path,
    threshold_uv: float = ARTIFACT_THRESHOLD_UV,
) -> tuple[ParticipantResult | None, list[RunResult]]:
    import numpy as np

    target_epochs = []
    standard_epochs = []
    runs: list[RunResult] = []
    times_ms = None

    for set_path in sorted((subject_directory / "eeg").glob("*_eeg.set")):
        target, standard, run_times_ms, run = analyze_recording(set_path, threshold_uv)
        runs.append(run)
        if run.eligible:
            target_epochs.append(target)
            standard_epochs.append(standard)
            if times_ms is None:
                times_ms = run_times_ms
            elif not np.array_equal(times_ms, run_times_ms):
                raise ValueError("eligible runs do not share the same epoch time grid")

    if not target_epochs or times_ms is None:
        return None, runs

    target = np.concatenate(target_epochs)
    standard = np.concatenate(standard_epochs)
    target_wave = target.mean(axis=0)
    standard_wave = standard.mean(axis=0)
    target_mean = window_mean(times_ms, target_wave)
    standard_mean = window_mean(times_ms, standard_wave)
    result = ParticipantResult(
        participant=subject_directory.name,
        included_runs=len(target_epochs),
        target_trials=len(target),
        standard_trials=len(standard),
        target_mean_uv=target_mean,
        standard_mean_uv=standard_mean,
        contrast_uv=p3_contrast(target_mean, standard_mean),
    )
    return result, runs


def expected_recordings() -> set[str]:
    return {
        f"sub-{subject:03d}_task-P300_run-{run}"
        for subject in range(1, 14)
        for run in range(1, 4)
        if f"sub-{subject:03d}_task-P300_run-{run}" not in EXCLUDED_RECORDINGS
    }


def validate_recording_set(data_root: Path) -> None:
    observed = {
        path.name.removesuffix("_eeg.set") for path in data_root.glob("sub-*/eeg/*_eeg.set")
    }
    missing = sorted(expected_recordings() - observed)
    unexpected = sorted(observed - expected_recordings())
    if missing or unexpected:
        raise ValueError(f"recording set mismatch; missing={missing}, unexpected={unexpected}")


def result_payload(
    participants: Sequence[ParticipantResult],
    runs: Sequence[RunResult],
    analysis: str = "confirmatory",
    threshold_uv: float = ARTIFACT_THRESHOLD_UV,
) -> dict:
    import numpy as np
    from scipy import stats

    if len(participants) < 8:
        raise ValueError("fewer than eight participants remain; confirmatory inference must stop")
    contrasts = np.asarray([participant.contrast_uv for participant in participants], dtype=float)
    summary = summarize_contrasts(contrasts)
    test = stats.ttest_1samp(contrasts, popmean=0.0, alternative="two-sided")
    standard_error = stats.sem(contrasts)
    ci_low, ci_high = stats.t.interval(
        0.95,
        df=len(contrasts) - 1,
        loc=float(contrasts.mean()),
        scale=float(standard_error),
    )
    wilcoxon = stats.wilcoxon(contrasts, alternative="two-sided")
    return {
        "analysis": analysis,
        "dataset": "ds003061",
        "dataset_version": "1.1.0",
        "endpoint": {
            "electrode": "Pz",
            "window_ms": list(P3_WINDOW_MS),
            "contrast": "target_minus_standard",
            "artifact_threshold_uv_peak_to_peak": threshold_uv,
        },
        "summary": asdict(summary),
        "inference": {
            "test": "two_sided_one_sample_t",
            "null_mean_uv": 0.0,
            "t_statistic": float(test.statistic),
            "degrees_of_freedom": len(contrasts) - 1,
            "p_value": float(test.pvalue),
            "mean_95_ci_uv": [float(ci_low), float(ci_high)],
            "sensitivity_wilcoxon_statistic": float(wilcoxon.statistic),
            "sensitivity_wilcoxon_p_value": float(wilcoxon.pvalue),
        },
        "participants": [asdict(participant) for participant in participants],
        "runs": [asdict(run) for run in runs],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/derived/confirmatory.json"))
    parser.add_argument("--analysis", choices=("confirmatory", "sensitivity"), default="confirmatory")
    parser.add_argument("--artifact-threshold-uv", type=float, default=ARTIFACT_THRESHOLD_UV)
    args = parser.parse_args()

    if args.analysis == "confirmatory" and args.artifact_threshold_uv != ARTIFACT_THRESHOLD_UV:
        parser.error("confirmatory analysis requires the frozen 150 microvolt threshold")
    if args.analysis == "sensitivity" and args.artifact_threshold_uv not in (100.0, 200.0):
        parser.error("sensitivity threshold must be 100 or 200 microvolts")

    validate_recording_set(args.data_root)

    participants = []
    runs = [
        RunResult(recording, 0, 0, False, "frozen metadata exclusion")
        for recording in sorted(EXCLUDED_RECORDINGS)
    ]
    for subject_directory in sorted(args.data_root.glob("sub-*")):
        participant, subject_runs = analyze_participant(
            subject_directory,
            threshold_uv=args.artifact_threshold_uv,
        )
        runs.extend(subject_runs)
        if participant is not None:
            participants.append(participant)

    payload = result_payload(
        participants,
        runs,
        analysis=args.analysis,
        threshold_uv=args.artifact_threshold_uv,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote frozen {args.analysis} result to {args.output}")


if __name__ == "__main__":
    main()
