"""Generate the POST-HOC participant-level recomputation (requires the `analysis` extra)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from neuro_signal_lab.summary_audit import build_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--summary", default="results/summary.json")
    args = parser.parse_args()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        json.dump(build_audit(Path(args.summary)), handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
