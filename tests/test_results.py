import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))


class PublishedResultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = json.loads((ROOT / "results" / "summary.json").read_text(encoding="utf-8"))

    def test_result_keeps_participants_as_the_sample_size(self):
        self.assertEqual(self.result["participants"], 13)
        self.assertEqual(len(self.result["participant_contrasts_uv"]), 13)

    def test_every_participant_contrast_is_positive(self):
        contrasts = self.result["participant_contrasts_uv"].values()

        self.assertTrue(all(contrast > 0 for contrast in contrasts))
        self.assertEqual(self.result["positive_participant_fraction"], 1.0)

    def test_confirmatory_interval_excludes_zero(self):
        lower, upper = self.result["mean_95_ci_uv"]

        self.assertGreater(lower, 0)
        self.assertGreater(upper, lower)

    def test_sensitivity_intervals_exclude_zero(self):
        for sensitivity in self.result["artifact_sensitivity"].values():
            self.assertGreater(sensitivity["mean_95_ci_uv"][0], 0)


if __name__ == "__main__":
    unittest.main()
