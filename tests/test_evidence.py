import io
import tempfile
import unittest
from unittest.mock import patch
from scripts.run_benchmarks import ZWCADTestHarness
from scripts.score_results import score_results

class EvidenceTests(unittest.TestCase):
    def test_no_host_or_screenshot_and_no_measured_fields(self):
        with tempfile.TemporaryDirectory() as d, patch.object(ZWCADTestHarness, "_init_com", side_effect=AssertionError), patch.object(ZWCADTestHarness, "capture_screenshot", side_effect=AssertionError):
            h = ZWCADTestHarness(d)
            for provider in ("multicad", "dalingo_zwcad", "unknown"):
                r = h._run_test_case(provider, "T01", "connection", io.StringIO())
                self.assertEqual(r["status"], "UNVERIFIED")
                self.assertEqual(r["verification_kind"], "LEGACY_SYNTHETIC")
                self.assertIsNone(r["correctness_score"])
                self.assertIsNone(r["latency_ms"])
                self.assertEqual(r["evidence_path"], "")
                self.assertFalse(r["measured_export_allowed"])
            self.assertEqual(h._compute_summary([])["capability_rankings"], {})
    def test_measured_export_rejected(self):
        with self.assertRaises(ValueError):
            score_results(measured=True)
        self.assertEqual(score_results()["provider_summary"], {})

    def test_full_generation_is_synthetic(self):
        import contextlib
        with tempfile.TemporaryDirectory() as d, contextlib.redirect_stdout(io.StringIO()):
            h = ZWCADTestHarness(d)
            records, summary = h.run_all_benchmarks()
            self.assertEqual(len(records), 306)
            self.assertTrue(all(r["status"] == "UNVERIFIED" for r in records))
            self.assertTrue(all(r["latency_ms"] is None for r in records))
            self.assertEqual(summary["provider_summary"], {})
