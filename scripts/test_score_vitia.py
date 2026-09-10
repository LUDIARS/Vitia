#!/usr/bin/env python3
"""Regression contracts for Vitia 2.0.0 value/performance assessments."""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

from score_vitia import BLOCKING_FLAGS, InputError, RISK_PENALTIES, score

ROOT = Path(__file__).resolve().parent.parent


def axis(value: float, **overrides: object) -> dict:
    return {
        "score": value, "basis": "observed", "rationale": "Synthetic evidence for this axis.",
        "evidence_refs": ["fixture:audience-review"], "confidence": 0.8, **overrides,
    }


def assessment(value: float = 0.9, performance: float = 0.8) -> dict:
    return {
        "schema_version": 2, "audience": "Specified adult audience",
        "context": "Synthetic product assessment",
        "domains": {"superbia": {"value": axis(value), "performance": axis(performance)}},
        "neutrality_check": {"status": "passed", "evidence_refs": ["fixture:rename-check"]},
    }


class ScoreVitiaTest(unittest.TestCase):
    def test_audience_peak_survives_other_low_or_unknown_domains(self) -> None:
        payload = assessment(0.95, 0.3)
        payload["domains"]["gula"] = {"value": axis(0), "performance": axis(0)}
        result = score(payload)
        self.assertEqual(result["vitia_version"], "2.0.0")
        self.assertEqual(result["domains"][0]["value"]["score"], 0.95)
        self.assertEqual(result["domains"][0]["performance"]["score"], 0.3)
        self.assertEqual(result["domains"][0]["interpretation"], "delivery_gap")
        self.assertEqual({row["domain"] for row in result["domains"]}, {
            "superbia", "avaritia", "luxuria", "invidia", "gula", "ira", "acedia",
        })
        for removed in ("score", "scores", "primary", "secondary"):
            self.assertNotIn(removed, result)

    def test_axes_and_confidence_remain_independent(self) -> None:
        payload = assessment()
        original = copy.deepcopy(payload)
        changed = copy.deepcopy(payload)
        changed["domains"]["superbia"]["performance"]["score"] = 0.2
        changed["domains"]["superbia"]["value"]["confidence"] = 0.1
        changed["domains"]["gula"] = {"value": axis(1), "performance": axis(1)}
        first, second = score(payload)["domains"][0], score(changed)["domains"][0]
        self.assertEqual(first["value"]["score"], second["value"]["score"])
        self.assertEqual(second["value"]["confidence"], 0.1)
        self.assertEqual(payload, original)

    def test_known_pairs_have_distinct_interpretations(self) -> None:
        for value, performance, expected in (
            (0.75, 0.75, "strength"),
            (0.9, 0.2, "delivery_gap"),
            (0.2, 0.9, "value_or_audience_review"),
            (0.2, 0.2, "reconsider_focus"),
        ):
            with self.subTest(value=value, performance=performance):
                self.assertEqual(score(assessment(value, performance))["domains"][0]["interpretation"], expected)

    def test_unknown_is_not_zero_and_preserves_the_known_axis(self) -> None:
        payload = assessment()
        payload["domains"]["superbia"]["performance"] = None
        result = score(payload)
        self.assertEqual(result["status"], "partial")
        self.assertEqual(result["domains"][0]["value"]["score"], 0.9)
        self.assertIsNone(result["domains"][0]["performance"]["score"])
        self.assertEqual(result["domains"][0]["interpretation"], "unconfirmed")
        self.assertTrue(all(row["value"]["score"] is None for row in result["domains"][1:]))
        self.assertEqual(score(assessment(0, 0))["domains"][0]["value"]["score"], 0)

    def test_hypothesis_and_unspecified_confidence_stay_provisional(self) -> None:
        for update in ({"basis": "hypothesis"}, {"confidence": None}):
            with self.subTest(update=update):
                payload = assessment()
                payload["domains"]["superbia"]["performance"].update(update)
                row = score(payload)["domains"][0]
                self.assertEqual(row["performance"]["score"], 0.8)
                self.assertEqual(row["evidence_status"], "provisional")

    def test_relabeling_does_not_change_scores_or_guards(self) -> None:
        first, second = assessment(), assessment()
        first["label_context"] = {"artifact_name": "Generous gift", "declared_domain": "superbia"}
        second["label_context"] = {"artifact_name": "Greedy trap", "declared_domain": "avaritia"}
        self.assertEqual(score(first), score(second))
        first["domains"] = {}
        self.assertTrue(all(row["value"]["score"] is None for row in score(first)["domains"]))

    def test_incomplete_or_failed_neutrality_withholds_pair_conclusions(self) -> None:
        for check, expected_status in (
            ({}, "partial"),
            ({"status": "failed", "evidence_refs": ["fixture:failed-check"]}, "review_required"),
        ):
            with self.subTest(check=check):
                payload = assessment()
                payload["neutrality_check"] = check
                result = score(payload)
                self.assertEqual(result["status"], expected_status)
                self.assertEqual(result["domains"][0]["interpretation"], "neutrality_unconfirmed")

    def test_guards_cannot_be_offset_by_high_scores(self) -> None:
        for flags, expected in (
            (["price_obfuscation"], "blocked"),
            (["status_shaming"], "review_required"),
            (["unrecognized_harm"], "review_required"),
        ):
            with self.subTest(flags=flags):
                payload = assessment(1, 1)
                payload["risk_flags"] = flags
                result = score(payload)
                self.assertEqual(result["status"], expected)
                self.assertEqual(result["domains"][0]["value"]["score"], 1)
                self.assertEqual(result["domains"][0]["performance"]["score"], 1)
                if flags == ["unrecognized_harm"]:
                    self.assertEqual(result["guardrails"]["unknown_risk_flags"], flags)

    def test_invalid_numbers_fail_at_the_input_boundary(self) -> None:
        for field in ("score", "confidence"):
            for invalid in (True, "0.8", -0.01, 1.01, float("nan"), float("inf")):
                with self.subTest(field=field, invalid=invalid):
                    payload = assessment()
                    payload["domains"]["superbia"]["value"][field] = invalid
                    with self.assertRaises(InputError):
                        score(payload)
        for invalid in (0, True, float("nan"), 1.1):
            with self.subTest(threshold=invalid):
                with self.assertRaises(InputError):
                    score({**assessment(), "high_threshold": invalid})

    def test_known_scores_require_evidence_and_unknowns_cannot_claim_it(self) -> None:
        for update in (
            {"rationale": ""}, {"evidence_refs": []}, {"basis": "unknown"},
            {"score": None}, {"score": None, "basis": "unknown", "confidence": 0.8},
        ):
            with self.subTest(update=update):
                payload = assessment()
                payload["domains"]["superbia"]["value"].update(update)
                with self.assertRaises(InputError):
                    score(payload)

    def test_legacy_and_misspelled_contracts_fail_explicitly(self) -> None:
        for payload in (
            {"signals": {"frustration": 1}},
            {**assessment(), "schema_version": 2.0},
            {**assessment(), "schema_version": True},
            {**assessment(), "signals": {}},
            {**assessment(), "audience": ""},
            {**assessment(), "domains": {"superbai": {}}},
            {**assessment(), "domains": {"superbia": {"performace": axis(0.5)}}},
            {**assessment(), "label_context": {"artifact_name": 7}},
            {**assessment(), "neutrality_check": {"status": "passed"}},
        ):
            with self.subTest(payload=payload):
                with self.assertRaises(InputError):
                    score(payload)

    def test_existing_audits_retain_public_safety_imports(self) -> None:
        import audit_game_experience
        import audit_marketing_mechanisms
        self.assertIs(audit_game_experience.BLOCKING_FLAGS, BLOCKING_FLAGS)
        self.assertIs(audit_marketing_mechanisms.BLOCKING_FLAGS, BLOCKING_FLAGS)
        self.assertIs(audit_marketing_mechanisms.RISK_PENALTIES, RISK_PENALTIES)

    def test_example_and_release_declarations_match(self) -> None:
        payload = json.loads((ROOT / "references/assessment.example.json").read_text(encoding="utf-8"))
        self.assertEqual(score(payload)["vitia_version"], "2.0.0")
        self.assertIn('version: "2.0.0"', (ROOT / "SKILL.md").read_text(encoding="utf-8"))


class ScoreVitiaCliTest(unittest.TestCase):
    def invoke(self, *args: str, input_data: bytes = b"") -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/score_vitia.py"), *args],
            input=input_data, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            cwd=ROOT, timeout=10, check=False,
        )

    def test_stdin_preserves_unicode_and_accepts_utf8_bom(self) -> None:
        payload = assessment()
        payload["audience"] = "短時間で達成感を得たい成人 🎮"
        result = self.invoke("-", input_data=json.dumps(payload, ensure_ascii=False).encode("utf-8-sig"))
        self.assertEqual(result.returncode, 0, result.stderr.decode("utf-8"))
        self.assertEqual(json.loads(result.stdout.decode("utf-8"))["audience"], payload["audience"])

    def test_legacy_cli_input_has_no_success_json(self) -> None:
        result = self.invoke("-", input_data=b'{"signals": {}}')
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertIn("schema_version must be 2", result.stderr.decode("utf-8"))

    def test_version_and_example_are_reusable_cli_outputs(self) -> None:
        version = self.invoke("--version")
        self.assertEqual(version.returncode, 0)
        self.assertEqual(version.stdout.decode("utf-8").strip(), "Vitia 2.0.0")
        example = self.invoke("--example")
        self.assertEqual(example.returncode, 0, example.stderr.decode("utf-8"))
        self.assertEqual(score(json.loads(example.stdout.decode("utf-8")))["schema_version"], 2)


if __name__ == "__main__":
    unittest.main()
