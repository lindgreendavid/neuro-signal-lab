import json
import math
import tempfile
import unittest
from pathlib import Path

from neuro_signal_lab.summary_audit import build_audit, recompute


class RecomputeTests(unittest.TestCase):
    def test_matches_hand_calculation(self) -> None:
        out = recompute([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(out["mean_uv"], 3.0)
        self.assertAlmostEqual(out["sd_uv"], math.sqrt(2.5))
        self.assertAlmostEqual(out["t"], 3.0 / (math.sqrt(2.5) / math.sqrt(5)))
        self.assertEqual(out["df"], 4)

    def test_sign_flip_and_wilcoxon_agree_for_all_positive_data(self) -> None:
        out = recompute([1.0, 2.0, 3.0, 4.0, 5.0])
        self.assertAlmostEqual(out["sign_flip_exact_p_two_sided"], 2 / 32)
        self.assertAlmostEqual(out["wilcoxon_p"], 2 / 32)

    def test_effect_size_interval_brackets_the_point_estimate(self) -> None:
        out = recompute([5.0, 6.0, 7.0, 5.5, 6.5, 6.2, 5.8, 6.1])
        low, high = out["cohen_dz_95_ci_noncentral_t"]
        self.assertLess(low, out["cohen_dz"])
        self.assertGreater(high, out["cohen_dz"])
        self.assertLess(out["hedges_gz"], out["cohen_dz"])

    def test_effect_size_interval_is_nan_beyond_the_numerical_limit(self) -> None:
        out = recompute([5.0 + 0.001 * i for i in range(8)])
        self.assertTrue(math.isnan(out["cohen_dz_95_ci_noncentral_t"][0]))

    def test_prediction_interval_is_wider_than_the_mean_interval(self) -> None:
        out = recompute([5.0, 6.0, 7.0, 5.5, 6.5, 6.2, 5.8, 6.1])
        lo_m, hi_m = out["mean_95_ci_uv"]
        lo_p, hi_p = out["prediction_interval_95_new_participant_uv"]
        self.assertLess(lo_p, lo_m)
        self.assertGreater(hi_p, hi_m)

    def test_leave_one_out_bounds_contain_the_overall_mean(self) -> None:
        out = recompute([5.0, 6.0, 7.0, 5.5, 6.5, 6.2, 5.8, 6.1])
        loo = out["leave_one_out"]
        self.assertLessEqual(loo["smallest_mean_uv"], out["mean_uv"])
        self.assertGreaterEqual(loo["largest_mean_uv"], out["mean_uv"])


class BuildAuditTests(unittest.TestCase):
    def test_recomputation_reproduces_a_consistent_summary(self) -> None:
        contrasts = {f"sub-{i:03d}": 5.0 + 0.3 * i + (i % 3) for i in range(1, 9)}
        values = list(contrasts.values())
        recomputed = recompute(values)
        summary = {
            "participant_contrasts_uv": contrasts,
            "mean_contrast_uv": recomputed["mean_uv"],
            "t_statistic": recomputed["t"],
            "two_sided_p_value": recomputed["p_two_sided"],
            "cohen_dz": recomputed["cohen_dz"],
            "mean_95_ci_uv": recomputed["mean_95_ci_uv"],
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "summary.json"
            path.write_text(json.dumps(summary), encoding="utf-8")
            audit = build_audit(path)
        self.assertLess(audit["max_abs_difference_from_reported"], 1e-9)
        self.assertTrue(audit["label"].startswith("POST-HOC"))

    def test_the_stored_confirmatory_summary_is_reproduced(self) -> None:
        root = Path(__file__).resolve().parent.parent
        audit = build_audit(root / "results" / "summary.json")
        self.assertLess(audit["max_abs_difference_from_reported"], 1e-9)
        self.assertEqual(audit["recomputed"]["n"], 13)


if __name__ == "__main__":
    unittest.main()
