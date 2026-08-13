import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from neuro_signal_lab.fetch import EXCLUDED_RECORDINGS, parse_annex_pointer
from neuro_signal_lab.pipeline import ParticipantResult, RunResult, read_events, result_payload


class PipelineContractTests(unittest.TestCase):
    def test_known_truncated_recording_is_frozen_out_of_fetch(self):
        self.assertEqual(EXCLUDED_RECORDINGS, {"sub-012_task-P300_run-1"})

    def test_annex_pointer_provides_size_and_checksum(self):
        pointer = "../../MD5E-s63026728--ef8322e19b0c135246c91df8207f2bb0.set"

        self.assertEqual(
            parse_annex_pointer(pointer),
            (63026728, "ef8322e19b0c135246c91df8207f2bb0"),
        )

    def test_event_reader_keeps_only_correct_frozen_conditions(self):
        events, counts = read_events(ROOT / "tests" / "fixtures" / "events.tsv")

        self.assertEqual(counts, {"oddball_with_reponse": 1, "standard": 1})
        self.assertEqual([event[2] for event in events], [2, 1])

    def test_confirmatory_payload_requires_eight_participants(self):
        participant = ParticipantResult("sub-001", 1, 20, 100, 5.0, 1.0, 4.0)
        run = RunResult("sub-001_task-P300_run-1", 20, 100, True, None)

        with self.assertRaisesRegex(ValueError, "fewer than eight"):
            result_payload([participant] * 7, [run])

    def test_confirmatory_payload_keeps_participants_as_unit(self):
        participants = [
            ParticipantResult(f"sub-{index:03d}", 3, 60, 300, 5.0, 1.0, float(index))
            for index in range(1, 9)
        ]
        run = RunResult("recording", 20, 100, True, None)

        payload = result_payload(participants, [run])

        self.assertEqual(payload["summary"]["participants"], 8)
        self.assertEqual(payload["endpoint"]["window_ms"], [300.0, 600.0])


if __name__ == "__main__":
    unittest.main()
