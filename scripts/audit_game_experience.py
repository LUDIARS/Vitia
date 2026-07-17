#!/usr/bin/env python3
"""Audit game-experience integrity from label-neutral observed evidence.

The lens scores are transparent coverage heuristics. They do not measure fun,
diagnose players, predict sales, or alter the seven Vitia domain scores.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from score_vitia import BLOCKING_FLAGS
except ImportError:  # Support importing as scripts.audit_game_experience.
    from scripts.score_vitia import BLOCKING_FLAGS


COVERAGE_THRESHOLD = 0.50
CONFIDENCE_THRESHOLD = 0.50
SUPPORT_THRESHOLD = 0.55

LABEL_CONTEXT_KEYS = {
    "artifact_name",
    "category_name",
    "declared_domain",
    "reputation_label",
    "source_frame",
}

LENSES: dict[str, dict[str, Any]] = {
    "play_promise": {
        "domains": ["luxuria", "superbia"],
        "signals": {
            "experience_promise_observable": 0.15,
            "player_goal_clear": 0.15,
            "core_action_available": 0.15,
            "rule_obstacle_coherent": 0.20,
            "action_feedback_traceable": 0.15,
            "measurable_outcome_clear": 0.10,
            "first_peak_continuity": 0.10,
        },
        "question": (
            "Do the goal, available action, rule-created obstacle, feedback, and "
            "outcome truthfully demonstrate the promised experience?"
        ),
        "next_step": (
            "Trace one representative play episode and compare the first "
            "meaningful stage with the peak-value stage."
        ),
    },
    "challenge_learning": {
        "domains": ["superbia", "ira", "acedia"],
        "signals": {
            "prerequisite_knowledge_matched": 0.10,
            "challenge_skill_adjustable": 0.15,
            "goal_and_feedback_clear": 0.15,
            "safe_initial_attempt": 0.10,
            "failure_informs_next_strategy": 0.20,
            "recovery_path_available": 0.15,
            "later_transfer_observed": 0.15,
        },
        "question": (
            "Can a representative player form, test, and improve a strategy, "
            "then recover from failure without avoidable punishment?"
        ),
        "next_step": (
            "Observe an unaided attempt, diagnostic feedback, recovery, and a "
            "later transfer task after prompts fade."
        ),
    },
    "player_agency_fairness": {
        "domains": ["invidia", "ira", "superbia"],
        "signals": {
            "participation_voluntary": 0.15,
            "meaningful_choice_preserved": 0.15,
            "rule_parity_or_handicap_disclosed": 0.20,
            "anti_cheat_and_enforcement_credible": 0.10,
            "social_roles_and_expectations_clear": 0.10,
            "contribution_noncoercive": 0.15,
            "role_change_or_exit_proportionate": 0.15,
        },
        "question": (
            "Can players, teammates, opponents, and spectators understand their "
            "roles and participate without coercion or hidden rule asymmetry?"
        ),
        "next_step": (
            "Audit rule parity, social obligation, harassment, paid advantage, "
            "role change, and exit with each affected role."
        ),
    },
    "repeat_value": {
        "domains": ["gula", "superbia"],
        "signals": {
            "strategic_variety_present": 0.20,
            "choices_change_future_state": 0.15,
            "opponent_or_system_variation_meaningful": 0.15,
            "counterplay_or_alternative_paths": 0.15,
            "repeat_value_without_obligation": 0.15,
            "satiation_recovery_available": 0.10,
            "stopping_cues_and_exit_easy": 0.10,
        },
        "question": (
            "Does repetition create new decisions, mastery, expression, or social "
            "situations without relying on obligation or compulsive pressure?"
        ),
        "next_step": (
            "Identify what changes across repetitions and run the trigger-to-exit "
            "pressure-stack audit."
        ),
    },
}

LENS_RISK_PENALTIES: dict[str, tuple[set[str], float]] = {
    "bait_and_switch": ({"play_promise"}, 0.50),
    "rule_ambiguity": ({"play_promise", "challenge_learning"}, 0.30),
    "punitive_failure": ({"challenge_learning"}, 0.35),
    "social_spend_pressure": ({"player_agency_fairness"}, 0.50),
    "pay_to_keep_up": ({"player_agency_fairness"}, 0.40),
    "status_shaming": ({"player_agency_fairness"}, 0.35),
    "anger_escalation": ({"player_agency_fairness"}, 0.25),
    "privacy_intrusion": ({"player_agency_fairness"}, 0.30),
    "compulsive_loop": ({"repeat_value"}, 0.50),
    "near_miss_monetization": ({"repeat_value"}, 0.50),
    "unskippable_obligation": ({"repeat_value"}, 0.35),
}

EXAMPLE = {
    "signals": {
        "experience_promise_observable": 0.9,
        "player_goal_clear": 0.9,
        "core_action_available": 1.0,
        "rule_obstacle_coherent": 0.8,
        "action_feedback_traceable": 0.9,
        "measurable_outcome_clear": 0.8,
        "first_peak_continuity": 0.8,
        "prerequisite_knowledge_matched": 0.8,
        "challenge_skill_adjustable": 0.8,
        "goal_and_feedback_clear": 0.9,
        "safe_initial_attempt": 0.9,
        "failure_informs_next_strategy": 0.8,
        "recovery_path_available": 0.9,
        "later_transfer_observed": 0.8,
        "participation_voluntary": 0.9,
        "meaningful_choice_preserved": 0.8,
        "rule_parity_or_handicap_disclosed": 0.9,
        "anti_cheat_and_enforcement_credible": 0.7,
        "social_roles_and_expectations_clear": 0.8,
        "contribution_noncoercive": 0.9,
        "role_change_or_exit_proportionate": 0.9,
        "strategic_variety_present": 0.8,
        "choices_change_future_state": 0.8,
        "opponent_or_system_variation_meaningful": 0.8,
        "counterplay_or_alternative_paths": 0.8,
        "repeat_value_without_obligation": 0.9,
        "satiation_recovery_available": 0.8,
        "stopping_cues_and_exit_easy": 0.9,
    },
    "confidence": {"global": 0.8},
    "risk_flags": [],
    "label_context": {
        "artifact_name": "Example game",
        "category_name": "competitive puzzle",
        "declared_domain": "gula",
    },
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


def validate(
    payload: Any,
) -> tuple[dict[str, float], dict[str, float], set[str], dict[str, str]]:
    if not isinstance(payload, dict):
        raise InputError("input must be a JSON object")

    raw_signals = payload.get("signals", {})
    raw_confidence = payload.get("confidence", {"global": 0.5})
    raw_flags = payload.get("risk_flags", [])
    raw_label_context = payload.get("label_context", {})
    if not isinstance(raw_signals, dict):
        raise InputError("signals must be an object")
    if not isinstance(raw_confidence, dict):
        raise InputError("confidence must be an object")
    if not isinstance(raw_flags, list) or not all(
        isinstance(item, str) for item in raw_flags
    ):
        raise InputError("risk_flags must be an array of strings")
    if not isinstance(raw_label_context, dict):
        raise InputError("label_context must be an object")

    unknown_label_keys = sorted(set(raw_label_context) - LABEL_CONTEXT_KEYS)
    if unknown_label_keys:
        raise InputError(
            f"unknown label_context keys: {', '.join(unknown_label_keys)}"
        )
    if not all(isinstance(value, str) for value in raw_label_context.values()):
        raise InputError("label_context values must be strings")

    known_signals = {
        signal for specification in LENSES.values() for signal in specification["signals"]
    }
    unknown_signals = sorted(set(raw_signals) - known_signals)
    if unknown_signals:
        raise InputError(f"unknown signals: {', '.join(unknown_signals)}")

    allowed_confidence = {"global", *LENSES}
    unknown_confidence = sorted(set(raw_confidence) - allowed_confidence)
    if unknown_confidence:
        raise InputError(f"unknown confidence keys: {', '.join(unknown_confidence)}")

    signals = {
        key: _unit_interval(f"signals.{key}", value)
        for key, value in raw_signals.items()
    }
    confidence = {
        key: _unit_interval(f"confidence.{key}", value)
        for key, value in raw_confidence.items()
    }
    confidence.setdefault("global", 0.5)
    return signals, confidence, set(raw_flags), dict(raw_label_context)


def _score_lens(
    lens_id: str,
    specification: dict[str, Any],
    signals: dict[str, float],
    confidence: float,
    risk_flags: set[str],
) -> dict[str, Any]:
    weights = specification["signals"]
    observed = {key: signals[key] for key in weights if key in signals}
    if not observed:
        return {
            "lens": lens_id,
            "domains": specification["domains"],
            "status": "not_observed",
            "confidence": round(confidence, 3),
            "score": None,
            "raw_score": None,
            "signal_coverage": 0.0,
            "observed_signals": {},
            "weak_signals": [],
            "risk_flags": [],
            "question": specification["question"],
            "next_step": specification["next_step"],
        }

    observed_weight = sum(weights[key] for key in observed)
    total_weight = sum(weights.values())
    raw = sum(observed[key] * weights[key] for key in observed) / observed_weight
    coverage = observed_weight / total_weight
    penalties = [
        (flag, amount)
        for flag, (affected_lenses, amount) in LENS_RISK_PENALTIES.items()
        if flag in risk_flags and lens_id in affected_lenses
    ]
    coverage_factor = 0.5 + 0.5 * coverage
    adjusted = max(
        0.0,
        min(
            1.0,
            raw * (0.6 + 0.4 * confidence) * coverage_factor
            - sum(amount for _, amount in penalties),
        ),
    )
    if coverage < COVERAGE_THRESHOLD or confidence < CONFIDENCE_THRESHOLD:
        status = "exploratory"
    elif adjusted < SUPPORT_THRESHOLD:
        status = "needs_work"
    else:
        status = "supported"

    return {
        "lens": lens_id,
        "domains": specification["domains"],
        "status": status,
        "confidence": round(confidence, 3),
        "score": round(adjusted, 3),
        "raw_score": round(raw, 3),
        "signal_coverage": round(coverage, 3),
        "observed_signals": observed,
        "weak_signals": sorted(key for key, value in observed.items() if value < 0.5),
        "risk_flags": [flag for flag, _ in penalties],
        "question": specification["question"],
        "next_step": specification["next_step"],
    }


def audit(payload: Any) -> dict[str, Any]:
    signals, confidence, risk_flags, label_context = validate(payload)
    neutrality = {
        "status": "enforced",
        "ignored_context_keys": sorted(label_context),
        "rule": "Names, genres, reputations, and declared domains do not affect lens scores.",
    }
    blocked = sorted(risk_flags & BLOCKING_FLAGS)
    if blocked:
        return {
            "status": "blocked",
            "blocked_by": blocked,
            "recommendation": (
                "Do not optimize engagement; provide a user-protective redesign "
                "and re-audit the observed mechanics."
            ),
            "label_neutrality": neutrality,
        }

    results = [
        _score_lens(
            lens_id,
            specification,
            signals,
            confidence.get(lens_id, confidence["global"]),
            risk_flags,
        )
        for lens_id, specification in LENSES.items()
    ]
    statuses = {item["status"] for item in results}
    if "needs_work" in statuses:
        overall_status = "needs_work"
    elif statuses == {"supported"}:
        overall_status = "supported"
    elif statuses == {"not_observed"}:
        overall_status = "no_evidence"
    else:
        overall_status = "exploratory"

    priority = sorted(
        (
            item
            for item in results
            if item["status"] in {"needs_work", "exploratory"}
        ),
        key=lambda item: (
            0 if item["status"] == "needs_work" else 1,
            item["score"] if item["score"] is not None else 1.0,
            item["lens"],
        ),
    )
    known_risks = BLOCKING_FLAGS | set(LENS_RISK_PENALTIES)
    return {
        "status": overall_status,
        "priority_lenses": [item["lens"] for item in priority],
        "lenses": results,
        "unknown_risk_flags": sorted(risk_flags - known_risks),
        "label_neutrality": neutrality,
        "note": (
            "Lens scores summarize observed integrity and evidence coverage. They "
            "do not measure fun, diagnose players, predict revenue, or alter Vitia "
            "domain scores."
        ),
    }


def describe_lenses() -> dict[str, Any]:
    return {
        lens_id: {
            "domains": specification["domains"],
            "signals": specification["signals"],
            "risk_flags": sorted(
                flag
                for flag, (affected_lenses, _) in LENS_RISK_PENALTIES.items()
                if lens_id in affected_lenses
            ),
        }
        for lens_id, specification in LENSES.items()
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
    parser.add_argument(
        "--list-signals",
        action="store_true",
        help="print lens mappings and accepted signals",
    )
    args = parser.parse_args()

    if args.example and args.list_signals:
        parser.error("choose only one of --example or --list-signals")
    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return 0
    if args.list_signals:
        print(json.dumps(describe_lenses(), ensure_ascii=False, indent=2))
        return 0
    if not args.input:
        parser.error("input is required unless --example or --list-signals is used")

    try:
        result = audit(load_payload(args.input))
    except (InputError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
