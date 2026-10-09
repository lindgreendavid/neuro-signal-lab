"""POST-HOC (not preregistered): recompute the confirmatory result from participant contrasts.

The confirmatory endpoint is one number per participant (the Pz 300-600 ms correct target minus
correct standard contrast), so every reported statistic can be recomputed exactly from the 13
stored contrasts without the raw EEG. This module does that, as an independent check of the
report, and adds quantities suited to n = 13: an exact sign-flip permutation test, leave-one-out
sensitivity, a small-sample (Hedges) effect size with a noncentral-t interval, and a 95%
prediction interval for the contrast of a new participant from the same population.

scipy is imported lazily, as in `pipeline.py` (it belongs to the `analysis` extra).
"""

from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
from statistics import mean, stdev
from typing import Any


def recompute(contrasts: list[float]) -> dict[str, Any]:
    from scipy import optimize, stats

    n = len(contrasts)
    m, sd = mean(contrasts), stdev(contrasts)
    se = sd / math.sqrt(n)
    df = n - 1
    t = m / se
    p = float(2 * stats.t.sf(abs(t), df))
    t_crit = float(stats.t.ppf(0.975, df))
    dz = m / sd

    # Exact sign-flip permutation test on the mean (2^n sign patterns).
    observed = abs(m)
    extreme = sum(
        1
        for signs in itertools.product((1, -1), repeat=n)
        if abs(sum(s * c for s, c in zip(signs, contrasts, strict=True)) / n) >= observed - 1e-12
    )
    sign_flip_p = extreme / 2**n

    wilcoxon = stats.wilcoxon(contrasts)

    # Noncentral-t 95% interval for dz: noncentrality t * sqrt(n) / sqrt(n) -> dz * sqrt(n).
    ncp = dz * math.sqrt(n)

    def bound(prob: float) -> float:
        root = optimize.brentq(lambda x: stats.nct.cdf(t, df, x) - prob, ncp - 40, ncp + 40)
        return float(root / math.sqrt(n))

    try:
        dz_low, dz_high = bound(0.975), bound(0.025)
    except ValueError:  # scipy's noncentral t is numerically unavailable for extreme effect sizes
        dz_low = dz_high = float("nan")
    hedges_correction = 1 - 3 / (4 * df - 1)

    loo = []
    for i in range(n):
        rest = contrasts[:i] + contrasts[i + 1 :]
        loo_t = mean(rest) / (stdev(rest) / math.sqrt(len(rest)))
        loo.append(
            {
                "mean_uv": mean(rest),
                "t": loo_t,
                "p": float(2 * stats.t.sf(abs(loo_t), len(rest) - 1)),
            }
        )

    pred_half = t_crit * sd * math.sqrt(1 + 1 / n)
    return {
        "n": n,
        "mean_uv": m,
        "sd_uv": sd,
        "t": t,
        "df": df,
        "p_two_sided": p,
        "mean_95_ci_uv": [m - t_crit * se, m + t_crit * se],
        "cohen_dz": dz,
        "cohen_dz_95_ci_noncentral_t": [dz_low, dz_high],
        "hedges_gz": dz * hedges_correction,
        "sign_flip_exact_p_two_sided": sign_flip_p,
        "wilcoxon_statistic": float(wilcoxon.statistic),
        "wilcoxon_p": float(wilcoxon.pvalue),
        "prediction_interval_95_new_participant_uv": [m - pred_half, m + pred_half],
        "leave_one_out": {
            "largest_p": max(x["p"] for x in loo),
            "smallest_mean_uv": min(x["mean_uv"] for x in loo),
            "largest_mean_uv": max(x["mean_uv"] for x in loo),
            "smallest_t": min(x["t"] for x in loo),
        },
    }


def build_audit(summary_path: Path) -> dict[str, Any]:
    summary = json.loads(Path(summary_path).read_text(encoding="utf-8"))
    contrasts = list(summary["participant_contrasts_uv"].values())
    out = recompute(contrasts)
    reported = {
        "mean_uv": summary["mean_contrast_uv"],
        "t": summary["t_statistic"],
        "p_two_sided": summary["two_sided_p_value"],
        "cohen_dz": summary["cohen_dz"],
        "mean_95_ci_uv": summary["mean_95_ci_uv"],
    }
    return {
        "schema_version": 1,
        "label": "POST-HOC (not preregistered): recomputation from participant-level contrasts",
        "reported": reported,
        "recomputed": out,
        "max_abs_difference_from_reported": max(
            abs(out["mean_uv"] - reported["mean_uv"]),
            abs(out["t"] - reported["t"]),
            abs(out["cohen_dz"] - reported["cohen_dz"]),
            abs(out["mean_95_ci_uv"][0] - reported["mean_95_ci_uv"][0]),
            abs(out["mean_95_ci_uv"][1] - reported["mean_95_ci_uv"][1]),
        ),
    }
