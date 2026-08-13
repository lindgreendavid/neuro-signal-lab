import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from neuro_signal_lab.analysis import p3_contrast, summarize_contrasts, window_mean


class P3EndpointTests(unittest.TestCase):
    def test_window_mean_includes_both_preregistered_boundaries(self):
        times = [299.0, 300.0, 450.0, 600.0, 601.0]
        amplitudes = [99.0, 2.0, 4.0, 6.0, 99.0]

        self.assertEqual(window_mean(times, amplitudes), 4.0)

    def test_window_mean_rejects_a_window_without_samples(self):
        with self.assertRaisesRegex(ValueError, "contains no samples"):
            window_mean([0.0, 100.0], [1.0, 2.0])

    def test_window_mean_accepts_array_like_scientific_inputs(self):
        class ArrayLike(list):
            def __bool__(self):
                raise ValueError("array truth is ambiguous")

        self.assertEqual(window_mean(ArrayLike([300.0, 600.0]), [2.0, 4.0]), 3.0)

    def test_contrast_direction_is_target_minus_standard(self):
        self.assertEqual(p3_contrast(target_mean_uv=8.5, standard_mean_uv=2.0), 6.5)

    def test_summary_preserves_participant_level_sample_size(self):
        summary = summarize_contrasts([-1.0, 1.0, 3.0, 5.0])

        self.assertEqual(summary.participants, 4)
        self.assertEqual(summary.mean_uv, 2.0)
        self.assertEqual(summary.median_uv, 2.0)
        self.assertEqual(summary.positive_fraction, 0.75)
        self.assertTrue(math.isfinite(summary.cohen_dz))


if __name__ == "__main__":
    unittest.main()
