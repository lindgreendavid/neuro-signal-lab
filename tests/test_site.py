import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class InteractiveSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
        cls.javascript = (ROOT / "site" / "app.js").read_text(encoding="utf-8")

    def test_site_exposes_the_frozen_endpoint(self):
        self.assertIn("Pz", self.html)
        self.assertIn("300–600 ms", self.html)
        self.assertIn("target-minus-standard", self.html)

    def test_site_keeps_scientific_boundary_visible(self):
        self.assertIn("not a medical device", self.html)
        self.assertIn("does not show", self.html)

    def test_all_participant_results_are_embedded(self):
        for participant in range(1, 14):
            self.assertIn(f"sub-{participant:03d}", self.javascript)

    def test_confirmatory_and_sensitivity_thresholds_are_available(self):
        for threshold in (100, 150, 200):
            self.assertIn(f"{threshold}:{{mean:", self.javascript)


if __name__ == "__main__":
    unittest.main()
