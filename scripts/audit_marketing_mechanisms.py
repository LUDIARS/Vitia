#!/usr/bin/env python3
"""Route a marketing artifact to evidence-aware mechanism audits.

The scores are transparent relevance and readiness heuristics. They do not
estimate persuasion effects, diagnose people, or validate the Vitia taxonomy.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from score_vitia import BLOCKING_FLAGS, RISK_PENALTIES
except ImportError:  # Support importing this file as scripts.audit_marketing_mechanisms.
    from scripts.score_vitia import BLOCKING_FLAGS, RISK_PENALTIES


CANDIDATE_THRESHOLD = 0.45
COVERAGE_THRESHOLD = 0.50
READINESS_THRESHOLD = 0.55

MODULES: dict[str, dict[str, Any]] = {
    "color_context": {
        "domains": ["luxuria", "superbia", "acedia"],
        "opportunity": {
            "visual_channel": 0.35,
            "color_decision_relevance": 0.25,
            "brand_personality_relevance": 0.20,
            "affective_tone_relevance": 0.20,
        },
        "readiness": {
            "context_specific_color_hypothesis": 0.20,
            "audience_color_validation": 0.15,
            "brand_color_consistency": 0.15,
            "contrast_legibility": 0.20,
            "noncolor_redundancy": 0.15,
            "behavioral_measure_available": 0.15,
        },
        "hypothesis": (
            "A context-matched color treatment may change attention or meaning "
            "without changing the offer."
        ),
        "test": (
            "Randomize the color treatment while holding copy, layout, and offer "
            "constant; measure behavior, comprehension, and accessibility."
        ),
        "caution": (
            "Hue meanings vary by task, surrounding colors, culture, and learned "
            "association; do not use universal color-emotion tables."
        ),
    },
    "behavioral_contingency": {
        "domains": ["gula", "acedia", "avaritia"],
        "opportunity": {
            "repeat_or_target_behavior": 0.25,
            "environmental_cue_available": 0.20,
            "consequence_timing_relevant": 0.20,
            "response_effort_relevant": 0.15,
            "utilitarian_outcome_relevant": 0.10,
            "informational_outcome_relevant": 0.10,
        },
        "readiness": {
            "target_behavior_observable": 0.20,
            "baseline_rate_known": 0.15,
            "antecedent_documented": 0.15,
            "consequence_documented": 0.15,
            "feedback_timing_measurable": 0.15,
            "agency_preserved": 0.10,
            "harm_guardrail_defined": 0.10,
        },
        "hypothesis": (
            "Changing an observable cue, response cost, or consequence timing may "
            "change a defined customer behavior."
        ),
        "test": (
            "Measure the baseline rate, change one contingency, and compare the "
            "same behavioral outcome with agency and harm guardrails."
        ),
        "caution": (
            "Describe observable settings and consequences, not hidden motives; "
            "reject coercive or compulsive reinforcement schedules."
        ),
    },
    "processing_fluency": {
        "domains": ["acedia", "luxuria"],
        "opportunity": {
            "comprehension_bottleneck": 0.30,
            "dense_information": 0.20,
            "unfamiliar_terms": 0.15,
            "visual_complexity": 0.20,
            "rapid_decision_context": 0.15,
        },
        "readiness": {
            "readability_baseline": 0.15,
            "message_hierarchy_defined": 0.20,
            "figure_ground_legible": 0.15,
            "semantic_coherence": 0.20,
            "comprehension_measure": 0.20,
            "accuracy_preserved": 0.10,
        },
        "hypothesis": (
            "Reducing avoidable processing difficulty may improve comprehension "
            "and task completion."
        ),
        "test": (
            "Compare a clearer treatment with the original while measuring "
            "comprehension, completion, decision quality, and misplaced trust."
        ),
        "caution": (
            "Ease is not truth. Preserve qualifications and test comprehension "
            "instead of assuming that liking or familiarity proves understanding."
        ),
    },
    "choice_architecture": {
        "domains": ["acedia", "avaritia"],
        "opportunity": {
            "choice_set_complexity": 0.20,
            "decision_task_difficulty": 0.20,
            "preference_uncertainty": 0.20,
            "effort_minimizing_goal": 0.20,
            "choice_deferral_observed": 0.20,
        },
        "readiness": {
            "default_disclosed": 0.20,
            "choice_reversible": 0.20,
            "option_parity_preserved": 0.15,
            "complexity_measure": 0.15,
            "choice_deferral_measure": 0.15,
            "regret_guardrail": 0.15,
        },
        "hypothesis": (
            "A simpler, transparent choice environment may reduce deferral when "
            "complexity, task difficulty, and preference uncertainty are high."
        ),
        "test": (
            "Change one choice-structure feature and measure qualified choice, "
            "deferral, switching, regret, and accidental action."
        ),
        "caution": (
            "Assortment size alone does not establish overload, and average nudge "
            "effects are contested; preserve disclosure, parity, and reversibility."
        ),
    },
    "mental_simulation": {
        "domains": ["luxuria", "superbia"],
        "opportunity": {
            "experiential_offer": 0.25,
            "sensory_attributes": 0.20,
            "use_context_important": 0.20,
            "psychological_distance": 0.15,
            "demo_possible": 0.20,
        },
        "readiness": {
            "scenario_truthful": 0.25,
            "feature_outcome_traceable": 0.20,
            "audience_self_relevance": 0.15,
            "analytical_information_preserved": 0.15,
            "trial_or_demo_matches": 0.15,
            "regret_guardrail": 0.10,
        },
        "hypothesis": (
            "A concrete, truthful use episode may help the audience evaluate an "
            "experience that is otherwise psychologically distant."
        ),
        "test": (
            "Compare a process-focused scenario with a factual control while "
            "holding claims constant; measure qualified trial, recall, and regret."
        ),
        "caution": (
            "Narrative transportation can reduce critical scrutiny; retain material "
            "facts and do not simulate outcomes the product cannot deliver."
        ),
    },
    "social_norms": {
        "domains": ["invidia", "superbia"],
        "opportunity": {
            "peer_behavior_relevant": 0.25,
            "uncertainty_about_others": 0.20,
            "reference_group_salient": 0.20,
            "behavior_public_or_observable": 0.15,
            "aspirational_pathway": 0.20,
        },
        "readiness": {
            "norm_data_verified": 0.25,
            "denominator_disclosed": 0.15,
            "reference_group_relevant": 0.20,
            "injunctive_alignment": 0.15,
            "boomerang_segment_checked": 0.15,
            "no_shaming": 0.10,
        },
        "hypothesis": (
            "A truthful norm from a relevant reference group may reduce uncertainty "
            "or make an attainable pathway legible."
        ),
        "test": (
            "Compare verified norm information with a non-normative control and "
            "measure behavior by baseline segment, trust, and boomerang effects."
        ),
        "caution": (
            "Descriptive norms can normalize undesirable behavior; disclose the "
            "denominator and never fabricate popularity or use shame."
        ),
    },
    "attention_hierarchy": {
        "domains": ["luxuria", "acedia"],
        "opportunity": {
            "visual_ad": 0.25,
            "competing_elements": 0.20,
            "low_exposure_time": 0.20,
            "brand_recall_bottleneck": 0.20,
            "cta_detection_bottleneck": 0.15,
        },
        "readiness": {
            "element_roles_defined": 0.15,
            "clutter_measured": 0.15,
            "brand_message_linked": 0.20,
            "legibility_preserved": 0.15,
            "attention_measure_available": 0.20,
            "behavioral_outcome_available": 0.15,
        },
        "hypothesis": (
            "A goal-relevant visual hierarchy may improve detection and transfer "
            "attention among the brand, message, and action."
        ),
        "test": (
            "Vary one hierarchy feature and measure detection or attention together "
            "with recall, comprehension, and qualified action."
        ),
        "caution": (
            "Attention is not persuasion or welfare; avoid salience that hides terms "
            "or diverts attention from material information."
        ),
    },
}

EXAMPLE = {
    "signals": {
        "visual_channel": 0.9,
        "color_decision_relevance": 0.7,
        "brand_personality_relevance": 0.8,
        "affective_tone_relevance": 0.6,
        "context_specific_color_hypothesis": 0.8,
        "audience_color_validation": 0.6,
        "brand_color_consistency": 0.9,
        "contrast_legibility": 0.9,
        "noncolor_redundancy": 0.8,
        "behavioral_measure_available": 0.8,
        "comprehension_bottleneck": 0.7,
        "dense_information": 0.8,
        "visual_complexity": 0.7,
        "readability_baseline": 0.6,
        "message_hierarchy_defined": 0.8,
        "figure_ground_legible": 0.8,
        "semantic_coherence": 0.7,
        "comprehension_measure": 0.8,
        "accuracy_preserved": 1.0,
    },
    "confidence": {"global": 0.7, "color_context": 0.8},
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

    known_signals = {
        signal
        for module in MODULES.values()
        for dimension in ("opportunity", "readiness")
        for signal in module[dimension]
    }
    unknown_signals = sorted(set(raw_signals) - known_signals)
    if unknown_signals:
        raise InputError(f"unknown signals: {', '.join(unknown_signals)}")

    allowed_confidence = {"global", *MODULES}
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
    return signals, confidence, set(raw_flags)


def _score_dimension(
    signals: dict[str, float],
    weights: dict[str, float],
    confidence: float,
) -> dict[str, Any] | None:
    observed = {key: signals[key] for key in weights if key in signals}
    if not observed:
        return None

    total_weight = sum(weights.values())
    observed_weight = sum(weights[key] for key in observed)
    raw = sum(observed[key] * weights[key] for key in observed) / observed_weight
    coverage = observed_weight / total_weight
    coverage_factor = 0.5 + 0.5 * coverage
    adjusted = raw * (0.6 + 0.4 * confidence) * coverage_factor
    return {
        "score": round(max(0.0, min(1.0, adjusted)), 3),
        "raw_score": round(raw, 3),
        "signal_coverage": round(coverage, 3),
        "observed_signals": observed,
    }


def _status(
    opportunity: dict[str, Any] | None,
    readiness: dict[str, Any] | None,
) -> str:
    if opportunity is None:
        return "not_observed"
    if opportunity["signal_coverage"] < COVERAGE_THRESHOLD:
        return "exploratory"
    if opportunity["score"] < CANDIDATE_THRESHOLD:
        return "low_priority"
    if (
        readiness is None
        or readiness["signal_coverage"] < COVERAGE_THRESHOLD
        or readiness["score"] < READINESS_THRESHOLD
    ):
        return "needs_evidence"
    return "testable"


def audit(payload: Any) -> dict[str, Any]:
    signals, confidence, risk_flags = validate(payload)
    blocked = sorted(risk_flags & BLOCKING_FLAGS)
    if blocked:
        return {
            "status": "blocked",
            "blocked_by": blocked,
            "recommendation": (
                "Do not optimize persuasion; provide neutral information or a "
                "user-protective alternative."
            ),
        }

    results: list[dict[str, Any]] = []
    for module_id, specification in MODULES.items():
        module_confidence = confidence.get(module_id, confidence["global"])
        module_domains = set(specification["domains"])
        applicable_risks = sorted(
            flag
            for flag, (affected_domains, _) in RISK_PENALTIES.items()
            if flag in risk_flags and module_domains & affected_domains
        )
        opportunity = _score_dimension(
            signals,
            specification["opportunity"],
            module_confidence,
        )
        readiness = _score_dimension(
            signals,
            specification["readiness"],
            module_confidence,
        )
        results.append(
            {
                "module": module_id,
                "domains": specification["domains"],
                "status": _status(opportunity, readiness),
                "ethics_review_required": bool(applicable_risks),
                "risk_flags": applicable_risks,
                "confidence": round(module_confidence, 3),
                "opportunity": opportunity,
                "readiness": readiness,
                "hypothesis": specification["hypothesis"],
                "recommended_test": specification["test"],
                "caution": specification["caution"],
            }
        )

    results.sort(
        key=lambda item: (
            -(item["opportunity"] or {}).get("score", -1.0),
            item["module"],
        )
    )
    candidates = [
        item["module"]
        for item in results
        if item["status"] in {"testable", "needs_evidence"}
    ]
    overall_status = (
        "ok"
        if any(item["status"] == "testable" for item in results)
        else "exploratory"
        if candidates
        else "no_candidates"
    )
    return {
        "status": overall_status,
        "candidate_modules": candidates,
        "modules": results,
        "unknown_risk_flags": sorted(
            risk_flags - BLOCKING_FLAGS - set(RISK_PENALTIES)
        ),
        "note": (
            "Module scores route audits and experiments; they do not estimate "
            "effect size or alter Vitia domain scores. A testable status does not "
            "waive any reported ethics review."
        ),
    }


def describe_modules() -> dict[str, Any]:
    return {
        module_id: {
            "domains": specification["domains"],
            "opportunity_signals": specification["opportunity"],
            "readiness_signals": specification["readiness"],
        }
        for module_id, specification in MODULES.items()
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
        help="print module mappings and accepted signals",
    )
    args = parser.parse_args()

    if args.example and args.list_signals:
        parser.error("choose only one of --example or --list-signals")
    if args.example:
        print(json.dumps(EXAMPLE, ensure_ascii=False, indent=2))
        return 0
    if args.list_signals:
        print(json.dumps(describe_modules(), ensure_ascii=False, indent=2))
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
