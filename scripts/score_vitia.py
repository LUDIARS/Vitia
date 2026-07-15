#!/usr/bin/env python3
"""Deterministically route a marketing problem to Vitia domains.

The weights are transparent product heuristics, not psychological diagnostics.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


DOMAIN_WEIGHTS: dict[str, dict[str, float]] = {
    "superbia": {
        "identity_relevance": 0.25,
        "status_visibility": 0.25,
        "aspiration": 0.20,
        "public_consumption": 0.15,
        "proof_strength": 0.15,
    },
    "avaritia": {
        "economic_stakes": 0.25,
        "measurable_value": 0.25,
        "loss_salience": 0.15,
        "price_sensitivity": 0.15,
        "ownership_potential": 0.10,
        "proof_strength": 0.10,
    },
    "luxuria": {
        "sensory_vividness": 0.25,
        "affect_intensity": 0.20,
        "immediacy": 0.20,
        "trialability": 0.15,
        "novelty": 0.10,
        "reward_clarity": 0.10,
    },
    "invidia": {
        "social_comparison": 0.25,
        "reference_group_visibility": 0.20,
        "aspiration": 0.20,
        "attainability": 0.15,
        "deservingness": 0.10,
        "proof_strength": 0.10,
    },
    "gula": {
        "repeat_frequency": 0.25,
        "reward_clarity": 0.20,
        "variety_potential": 0.20,
        "habit_opportunity": 0.15,
        "satiation_risk": 0.10,
        "feedback_speed": 0.10,
    },
    "ira": {
        "frustration": 0.25,
        "perceived_injustice": 0.20,
        "blocked_goal": 0.20,
        "autonomy_threat": 0.15,
        "repairability": 0.10,
        "evidence_of_problem": 0.10,
    },
    "acedia": {
        "decision_friction": 0.25,
        "effort": 0.20,
        "delay": 0.15,
        "choice_complexity": 0.15,
        "present_bias": 0.10,
        "reversibility": 0.10,
        "feedback_speed": 0.05,
    },
}

BLOCKING_FLAGS = {
    "children_targeting",
    "acute_vulnerability",
    "fabricated_claims",
    "deceptive_scarcity",
    "hidden_default",
    "discriminatory_targeting",
    "addiction_exploitation",
    "incitement",
    "nonconsensual_surveillance",
}

RISK_PENALTIES: dict[str, tuple[set[str], float]] = {
    "unverified_scarcity": ({"avaritia"}, 0.40),
    "status_shaming": ({"superbia", "invidia"}, 0.40),
    "sexual_exploitation": ({"luxuria"}, 0.50),
    "compulsive_loop": ({"luxuria", "gula"}, 0.50),
    "anger_escalation": ({"ira"}, 0.50),
    "coercive_default": ({"acedia"}, 0.50),
    "privacy_intrusion": (set(DOMAIN_WEIGHTS), 0.30),
}

PROHIBITED_PAIRS = {frozenset(("ira", "invidia"))}
CAUTION_PAIRS = {frozenset(("luxuria", "gula")): "mandatory compulsion audit"}

EXAMPLE = {
    "signals": {
        "identity_relevance": 0.4,
        "economic_stakes": 0.9,
        "measurable_value": 0.9,
        "loss_salience": 0.6,
        "price_sensitivity": 0.7,
        "proof_strength": 0.8,
        "decision_friction": 0.7,
        "effort": 0.5,
        "choice_complexity": 0.6,
        "reversibility": 0.8,
        "feedback_speed": 0.6,
    },
    "confidence": {"global": 0.75, "avaritia": 0.9},
    "risk_flags": [],
}


class InputError(ValueError):
    pass


def _unit_interval(name: str, value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{name} must be a number from 0 to 1")
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise InputError(f"{name} must be between 0 and 1")
    return number


def validate(payload: Any) -> tuple[dict[str, float], dict[str, float], set[str]]:
    if not isinstance(payload, dict):
        raise InputError("input must be a JSON object")

    raw_signals = payload.get("signals", {})
    raw_confidence = payload.get("confidence", {"global": 0.5})
    raw_flags = payload.get("risk_flags", [])
    if not isinstance(raw_signals, dict):
        raise InputError("signals must be an object")
    if not isinstance(raw_confidence, dict):
        raise InputError("confidence must be an object")
    if not isinstance(raw_flags, list) or not all(isinstance(x, str) for x in raw_flags):
        raise InputError("risk_flags must be an array of strings")

    known_signals = {key for weights in DOMAIN_WEIGHTS.values() for key in weights}
    unknown_signals = sorted(set(raw_signals) - known_signals)
    if unknown_signals:
        raise InputError(f"unknown signals: {', '.join(unknown_signals)}")

    allowed_confidence = {"global", *DOMAIN_WEIGHTS}
    unknown_confidence = sorted(set(raw_confidence) - allowed_confidence)
    if unknown_confidence:
        raise InputError(f"unknown confidence keys: {', '.join(unknown_confidence)}")

    signals = {key: _unit_interval(f"signals.{key}", value) for key, value in raw_signals.items()}
    confidence = {
        key: _unit_interval(f"confidence.{key}", value)
        for key, value in raw_confidence.items()
    }
    confidence.setdefault("global", 0.5)
    return signals, confidence, set(raw_flags)


def score(payload: Any) -> dict[str, Any]:
    signals, confidence, risk_flags = validate(payload)
    blocked = sorted(risk_flags & BLOCKING_FLAGS)
    if blocked:
        return {
            "status": "blocked",
            "blocked_by": blocked,
            "recommendation": "Do not optimize persuasion; provide neutral information or a user-protective alternative.",
        }

    results: list[dict[str, Any]] = []
    for domain, weights in DOMAIN_WEIGHTS.items():
        observed = {key: signals[key] for key in weights if key in signals}
        observed_weight = sum(weights[key] for key in observed)
        raw = (
            sum(observed[key] * weights[key] for key in observed) / observed_weight
            if observed_weight
            else 0.0
        )
        domain_confidence = confidence.get(domain, confidence["global"])
        penalty_items = [
            (flag, amount)
            for flag, (domains, amount) in RISK_PENALTIES.items()
            if flag in risk_flags and domain in domains
        ]
        penalty = sum(amount for _, amount in penalty_items)
        coverage = observed_weight / sum(weights.values())
        coverage_factor = 0.5 + 0.5 * coverage
        adjusted = max(
            0.0,
            min(
                1.0,
                raw * (0.6 + 0.4 * domain_confidence) * coverage_factor - penalty,
            ),
        )
        results.append(
            {
                "domain": domain,
                "score": round(adjusted, 3),
                "raw_score": round(raw, 3),
                "confidence": round(domain_confidence, 3),
                "signal_coverage": round(coverage, 3),
                "observed_signals": observed,
                "penalties": [flag for flag, _ in penalty_items],
            }
        )

    results.sort(key=lambda item: (-item["score"], item["domain"]))
    primary = next(
        (
            item
            for item in results
            if item["score"] >= 0.45 and item["signal_coverage"] >= 0.50
        ),
        None,
    )
    secondary = None
    cautions: list[str] = []
    if primary:
        for candidate in results[1:]:
            pair = frozenset((primary["domain"], candidate["domain"]))
            if (
                candidate["score"] < 0.50
                or candidate["signal_coverage"] < 0.50
                or primary["score"] - candidate["score"] > 0.15
            ):
                continue
            if pair in PROHIBITED_PAIRS:
                cautions.append(f"prohibited pair excluded: {primary['domain']} + {candidate['domain']}")
                continue
            secondary = candidate
            if pair in CAUTION_PAIRS:
                cautions.append(CAUTION_PAIRS[pair])
            break

    exploratory = primary is None or (
        primary
        and (
            primary["confidence"] < 0.50
            or primary["signal_coverage"] < 0.50
        )
    )
    return {
        "status": "exploratory" if exploratory else "ok",
        "primary": primary["domain"] if primary else None,
        "secondary": secondary["domain"] if secondary else None,
        "cautions": cautions,
        "scores": results,
        "unknown_risk_flags": sorted(
            risk_flags - BLOCKING_FLAGS - set(RISK_PENALTIES)
        ),
        "note": "Scores route strategy work; they do not diagnose people or prove causal effects.",
    }


def load_payload(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="JSON input path, or - for stdin")
    parser.add_argument("--example", action="store_true", help="print an example input")
    args = parser.parse_args()

    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return 0
    if not args.input:
        parser.error("input is required unless --example is used")

    try:
        result = score(load_payload(args.input))
    except (InputError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
