#!/usr/bin/env python3
"""Unit tests for the evidence-aware marketing mechanism audit."""

from __future__ import annotations

import unittest

from audit_marketing_mechanisms import EXAMPLE, InputError, audit, describe_modules


class AuditMarketingMechanismsTest(unittest.TestCase):
    def test_example_selects_testable_color_and_fluency_modules(self) -> None:
        result = audit(EXAMPLE)

        self.assertEqual(result["status"], "ok")
        self.assertIn("color_context", result["candidate_modules"])
        self.assertIn("processing_fluency", result["candidate_modules"])
        statuses = {item["module"]: item["status"] for item in result["modules"]}
        self.assertEqual(statuses["color_context"], "testable")
        self.assertEqual(statuses["processing_fluency"], "testable")

    def test_candidate_without_readiness_needs_evidence(self) -> None:
        result = audit(
            {
                "signals": {
                    "experiential_offer": 1.0,
                    "sensory_attributes": 1.0,
                    "use_context_important": 1.0,
                },
                "confidence": {"global": 0.8},
            }
        )

        item = next(
            module for module in result["modules"] if module["module"] == "mental_simulation"
        )
        self.assertEqual(item["status"], "needs_evidence")

    def test_blocking_flag_stops_audit(self) -> None:
        result = audit(
            {
                "signals": {"visual_channel": 1.0},
                "risk_flags": ["children_targeting"],
            }
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["blocked_by"], ["children_targeting"])

    def test_unknown_signal_fails_fast(self) -> None:
        with self.assertRaisesRegex(InputError, "unknown signals"):
            audit({"signals": {"magic_color_effect": 1.0}})

    def test_nonblocking_risk_is_visible_on_affected_modules(self) -> None:
        payload = dict(EXAMPLE)
        payload["risk_flags"] = ["privacy_intrusion"]

        result = audit(payload)

        color = next(
            module for module in result["modules"] if module["module"] == "color_context"
        )
        self.assertTrue(color["ethics_review_required"])
        self.assertEqual(color["risk_flags"], ["privacy_intrusion"])
        self.assertEqual(result["unknown_risk_flags"], [])

    def test_signal_catalog_contains_both_dimensions(self) -> None:
        catalog = describe_modules()

        self.assertIn("opportunity_signals", catalog["behavioral_contingency"])
        self.assertIn("readiness_signals", catalog["behavioral_contingency"])


if __name__ == "__main__":
    unittest.main()
