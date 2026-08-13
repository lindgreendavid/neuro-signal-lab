import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from neuro_signal_lab.metadata import audit_event_file, load_frozen_audit, pz_is_eeg_channel


class MetadataContractTests(unittest.TestCase):
    def test_uses_only_frozen_correct_trial_labels(self):
        audit = audit_event_file(ROOT / "tests" / "fixtures" / "events.tsv")

        self.assertEqual(audit.target_trials, 1)
        self.assertEqual(audit.standard_trials, 1)
        self.assertFalse(audit.eligible_before_artifact_rejection)

    def test_identifies_pz_as_an_eeg_channel(self):
        self.assertTrue(pz_is_eeg_channel(ROOT / "tests" / "fixtures" / "channels.tsv"))

    def test_committed_audit_proves_signal_blinding(self):
        audit = load_frozen_audit(ROOT / "data" / "metadata-audit.json")

        self.assertEqual(audit["metadata_git_commit"], "223a18423a57d00dd1fb1fc3ac088b9d54c1e1e6")
        self.assertFalse(audit["signal_inspected_during_audit"])


if __name__ == "__main__":
    unittest.main()
