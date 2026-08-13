"""Fetch pinned OpenNeuro files and verify their DataLad MD5 identities."""

from __future__ import annotations

import argparse
import hashlib
import re
import urllib.request
from pathlib import Path

DATASET = "ds003061"
VERSION_COMMIT = "223a18423a57d00dd1fb1fc3ac088b9d54c1e1e6"
RAW_GITHUB = f"https://raw.githubusercontent.com/OpenNeuroDatasets/{DATASET}/{VERSION_COMMIT}"
OPENNEURO_S3 = f"https://s3.amazonaws.com/openneuro.org/{DATASET}"
SIDECAR_SUFFIXES = ("channels.tsv", "events.tsv", "eeg.json")
EXCLUDED_RECORDINGS = {"sub-012_task-P300_run-1"}


def md5_file(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_annex_pointer(pointer: str) -> tuple[int, str]:
    """Extract the byte size and MD5 from one Git-annex pointer target."""

    match = re.search(r"MD5E-s(\d+)--([0-9a-f]{32})\.set", pointer)
    if not match:
        raise ValueError("could not parse pinned annex identity")
    return int(match.group(1)), match.group(2)


def expected_annex_identity(relative_set_path: str) -> tuple[int, str]:
    """Read the pinned Git-annex byte size and MD5 without downloading EEG signal data."""

    pointer_url = f"{RAW_GITHUB}/{relative_set_path}"
    with urllib.request.urlopen(pointer_url) as response:
        pointer = response.read().decode("utf-8").strip()
    return parse_annex_pointer(pointer)


def download(url: str, destination: Path, expected_bytes: int | None = None) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".partial")
    with urllib.request.urlopen(url) as response, temporary.open("wb") as handle:
        while chunk := response.read(1024 * 1024):
            handle.write(chunk)
    observed_bytes = temporary.stat().st_size
    if expected_bytes is not None and observed_bytes != expected_bytes:
        temporary.unlink()
        raise ValueError(
            f"incomplete download for {destination.name}: "
            f"expected {expected_bytes} bytes, got {observed_bytes}"
        )
    temporary.replace(destination)


def fetch_recording(subject: str, run: int, root: Path) -> Path:
    stem = f"{subject}_task-P300_run-{run}"
    relative_directory = f"{subject}/eeg"
    relative_set = f"{relative_directory}/{stem}_eeg.set"
    destination_directory = root / relative_directory

    for suffix in SIDECAR_SUFFIXES:
        relative = f"{relative_directory}/{stem}_{suffix}"
        destination = root / relative
        if not destination.exists():
            download(f"{RAW_GITHUB}/{relative}", destination)

    set_destination = destination_directory / f"{stem}_eeg.set"
    expected_bytes, expected_md5 = expected_annex_identity(relative_set)
    if not set_destination.exists():
        download(f"{OPENNEURO_S3}/{relative_set}", set_destination, expected_bytes)
    observed_bytes = set_destination.stat().st_size
    if observed_bytes != expected_bytes:
        raise ValueError(
            f"size mismatch for {relative_set}: expected {expected_bytes}, got {observed_bytes}"
        )
    observed_md5 = md5_file(set_destination)
    if observed_md5 != expected_md5:
        raise ValueError(
            f"checksum mismatch for {relative_set}: expected {expected_md5}, got {observed_md5}"
        )
    return set_destination


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subject", action="append", help="BIDS subject such as sub-001")
    parser.add_argument("--data-root", type=Path, default=Path("data/raw"))
    args = parser.parse_args()

    subjects = args.subject or [f"sub-{number:03d}" for number in range(1, 14)]
    for subject in subjects:
        if not re.fullmatch(r"sub-\d{3}", subject):
            parser.error(f"invalid subject label: {subject}")
        for run in range(1, 4):
            stem = f"{subject}_task-P300_run-{run}"
            if stem in EXCLUDED_RECORDINGS:
                print(f"skipped frozen metadata exclusion {stem}")
                continue
            path = fetch_recording(subject, run, args.data_root)
            print(f"verified {path}")


if __name__ == "__main__":
    main()
