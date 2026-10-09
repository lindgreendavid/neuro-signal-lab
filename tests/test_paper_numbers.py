import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEX = (ROOT / "paper" / "paper.tex").read_text(encoding="utf-8")
AUDIT = json.loads(
    (ROOT / "results" / "post-release-summary-audit.json").read_text(encoding="utf-8")
)
SUMMARY = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))


class PaperNumbers(unittest.TestCase):
    def test_confirmatory_numbers_in_paper(self) -> None:
        self.assertIn(f"{SUMMARY['mean_contrast_uv']:.3f}", TEX)
        self.assertIn(f"{SUMMARY['cohen_dz']:.3f}", TEX)
        self.assertIn(f"{SUMMARY['t_statistic']:.3f}", TEX)
        low, high = SUMMARY["mean_95_ci_uv"]
        self.assertIn(f"{low:.3f}", TEX)
        self.assertIn(f"{high:.3f}", TEX)

    def test_recomputation_numbers_in_paper(self) -> None:
        r = AUDIT["recomputed"]
        self.assertEqual(AUDIT["max_abs_difference_from_reported"], 0.0)
        self.assertIn(f"{r['hedges_gz']:.3f}", TEX)
        low, high = r["cohen_dz_95_ci_noncentral_t"]
        self.assertIn(f"{low:.3f}", TEX)
        self.assertIn(f"{high:.3f}", TEX)
        loo = r["leave_one_out"]
        self.assertIn(f"{loo['smallest_mean_uv']:.3f}", TEX)
        self.assertIn(f"{loo['largest_mean_uv']:.3f}", TEX)
        plow, phigh = r["prediction_interval_95_new_participant_uv"]
        self.assertIn(f"{plow:.2f}", TEX)
        self.assertIn(f"{phigh:.2f}", TEX)


if __name__ == "__main__":
    unittest.main()
