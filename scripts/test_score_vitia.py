#!/usr/bin/env python3
"""Unit tests for label-neutral Vitia domain scoring."""

from __future__ import annotations

import unittest

from score_vitia import DOMAIN_WEIGHTS, EXAMPLE, InputError, score


class ScoreVitiaTest(unittest.TestCase):
    def test_example_scores_from_signals(self) -> None:
        result = score(EXAMPLE)

        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["primary"], "avaritia")
        self.assertEqual(result["label_neutrality"]["status"], "enforced")

    def test_relabeling_does_not_change_domain_result(self) -> None:
        common = {
            "signals": {
                "economic_stakes": 0.9,
                "measurable_value": 0.8,
                "price_sensitivity": 0.7,
                "proof_strength": 0.8,
            },
            "confidence": {"global": 0.8},
            "risk_flags": [],
        }
        first = score(
            {
                **common,
                "label_context": {
                    "artifact_name": "Generous Starter Pack",
                    "category_name": "player support",
                    "declared_domain": "luxuria",
                    "reputation_label": "fair",
                    "source_frame": "delight",
                },
            }
        )
        relabeled = score(
            {
                **common,
                "label_context": {
                    "artifact_name": "Greedy Cash Grab",
                    "category_name": "exploitative monetization",
                    "declared_domain": "avaritia",
                    "reputation_label": "predatory",
                    "source_frame": "human bug",
                },
            }
        )

        for key in ("status", "primary", "secondary", "cautions", "scores"):
            self.assertEqual(first[key], relabeled[key])

    def test_labels_without_evidence_cannot_create_a_candidate(self) -> None:
        result = score(
            {
                "label_context": {
                    "artifact_name": "Ultimate Pride Edition",
                    "declared_domain": "superbia",
                }
            }
        )

        self.assertEqual(result["status"], "exploratory")
        self.assertIsNone(result["primary"])
        self.assertTrue(all(item["score"] == 0.0 for item in result["scores"]))

    def test_invalid_label_context_fails_fast(self) -> None:
        with self.assertRaisesRegex(InputError, "label_context values"):
            score({"label_context": {"artifact_name": 7}})

    def test_observed_monetization_harm_blocks_scoring(self) -> None:
        result = score(
            {
                "signals": {"economic_stakes": 1.0},
                "risk_flags": ["price_obfuscation"],
                "label_context": {"category_name": "premium"},
            }
        )

        self.assertEqual(result["status"], "blocked")
        self.assertEqual(result["blocked_by"], ["price_obfuscation"])
        self.assertEqual(result["label_neutrality"]["status"], "enforced")

    def test_domain_weights_are_normalized(self) -> None:
        for domain, weights in DOMAIN_WEIGHTS.items():
            with self.subTest(domain=domain):
                self.assertAlmostEqual(sum(weights.values()), 1.0)


if __name__ == "__main__":
    unittest.main()
