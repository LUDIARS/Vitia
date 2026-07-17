#!/usr/bin/env python3
"""Unit tests for the label-neutral game-experience integrity audit."""

from __future__ import annotations

import unittest

from audit_game_experience import EXAMPLE, LENSES, InputError, audit, describe_lenses


class AuditGameExperienceTest(unittest.TestCase):
    def test_example_supports_all_lenses(self) -> None:
        result = audit(EXAMPLE)

        self.assertEqual(result["status"], "supported")
        self.assertEqual(result["label_neutrality"]["status"], "enforced")
        self.assertTrue(
            all(item["status"] == "supported" for item in result["lenses"])
        )

    def test_relabeling_does_not_change_lens_results(self) -> None:
        common = {
            "signals": EXAMPLE["signals"],
            "confidence": EXAMPLE["confidence"],
            "risk_flags": [],
        }
        praised = audit(
            {
                **common,
                "label_context": {
                    "artifact_name": "Beloved masterpiece",
                    "category_name": "cozy game",
                    "declared_domain": "luxuria",
                    "reputation_label": "fair",
                    "source_frame": "wholesome",
                },
            }
        )
        condemned = audit(
            {
                **common,
                "label_context": {
                    "artifact_name": "Predatory grind",
                    "category_name": "cash grab",
                    "declared_domain": "gula",
                    "reputation_label": "exploitative",
                    "source_frame": "addiction",
                },
            }
        )

        for key in ("status", "priority_lenses", "lenses"):
            self.assertEqual(praised[key], condemned[key])

    def test_labels_without_evidence_do_not_support_a_lens(self) -> None:
        result = audit(
            {
                "label_context": {
                    "artifact_name": "Deep Strategy Game",
                    "category_name": "competitive",
                }
            }
        )

        self.assertEqual(result["status"], "no_evidence")
        self.assertTrue(
            all(item["status"] == "not_observed" for item in result["lenses"])
        )

    def test_incomplete_evidence_is_exploratory(self) -> None:
        result = audit(
            {
                "signals": {
                    "experience_promise_observable": 1.0,
                    "player_goal_clear": 1.0,
                },
                "confidence": {"play_promise": 0.9},
            }
        )

        promise = next(
            item for item in result["lenses"] if item["lens"] == "play_promise"
        )
        self.assertEqual(result["status"], "exploratory")
        self.assertEqual(promise["status"], "exploratory")

    def test_observed_weak_recovery_needs_work(self) -> None:
        result = audit(
            {
                "signals": {
                    signal: 0.2
                    for signal in LENSES["challenge_learning"]["signals"]
                },
                "confidence": {"challenge_learning": 0.9},
            }
        )

        challenge = next(
            item
            for item in result["lenses"]
            if item["lens"] == "challenge_learning"
        )
        self.assertEqual(result["status"], "needs_work")
        self.assertEqual(challenge["status"], "needs_work")
        self.assertIn("recovery_path_available", challenge["weak_signals"])

    def test_blocking_flag_stops_engagement_audit(self) -> None:
        result = audit(
            {
                "signals": {"strategic_variety_present": 1.0},
                "risk_flags": ["loss_chasing_design"],
            }
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["blocked_by"], ["loss_chasing_design"])

    def test_near_miss_monetization_penalizes_repeat_value(self) -> None:
        payload = {
            "signals": {
                signal: 1.0 for signal in LENSES["repeat_value"]["signals"]
            },
            "confidence": {"repeat_value": 1.0},
            "risk_flags": ["near_miss_monetization"],
        }

        result = audit(payload)
        repeat = next(
            item for item in result["lenses"] if item["lens"] == "repeat_value"
        )

        self.assertEqual(repeat["status"], "needs_work")
        self.assertEqual(repeat["risk_flags"], ["near_miss_monetization"])

    def test_unknown_signal_fails_fast(self) -> None:
        with self.assertRaisesRegex(InputError, "unknown signals"):
            audit({"signals": {"fun_factor": 1.0}})

    def test_lens_weights_are_normalized(self) -> None:
        for lens_id, specification in describe_lenses().items():
            with self.subTest(lens=lens_id):
                self.assertAlmostEqual(sum(specification["signals"].values()), 1.0)


if __name__ == "__main__":
    unittest.main()
