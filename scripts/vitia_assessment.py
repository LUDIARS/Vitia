"""Interpret seven independent value/performance pairs without a composite score."""

from __future__ import annotations

from typing import Any

if __package__:
    from .vitia_contract import VERSION, validate
    from .vitia_guardrails import BLOCKING_FLAGS, DOMAINS, RISK_PENALTIES
else:
    from vitia_contract import VERSION, validate
    from vitia_guardrails import BLOCKING_FLAGS, DOMAINS, RISK_PENALTIES


def _interpret(value: float | None, performance: float | None, threshold: float) -> str:
    if value is None or performance is None:
        return "unconfirmed"
    if value >= threshold:
        return "strength" if performance >= threshold else "delivery_gap"
    return "value_or_audience_review" if performance >= threshold else "reconsider_focus"


def score(payload: Any) -> dict[str, Any]:
    data = validate(payload)
    flags = set(data["risk_flags"])
    blocked = sorted(flags & BLOCKING_FLAGS)
    unknown_flags = sorted(flags - BLOCKING_FLAGS - set(RISK_PENALTIES))
    neutrality_passed = data["neutrality_check"]["status"] == "passed"
    domains = []
    for domain in DOMAINS:
        axes = data["domains"][domain]
        evidence_status = (
            "unconfirmed" if any(axis["score"] is None for axis in axes.values())
            else "provisional" if any(
                axis["basis"] == "hypothesis" or axis["confidence"] is None
                for axis in axes.values()
            ) else "evidence_recorded"
        )
        domains.append({
            "domain": domain, **axes,
            "interpretation": (
                _interpret(axes["value"]["score"], axes["performance"]["score"], data["high_threshold"])
                if neutrality_passed or evidence_status == "unconfirmed" else "neutrality_unconfirmed"
            ),
            "evidence_status": evidence_status,
            "risk_flags": sorted(
                flag for flag, (affected, _) in RISK_PENALTIES.items()
                if flag in flags and domain in affected
            ),
        })
    if blocked:
        status = "blocked"
    elif flags or data["neutrality_check"]["status"] == "failed":
        status = "review_required"
    elif not neutrality_passed or any(row["evidence_status"] != "evidence_recorded" for row in domains):
        status = "partial"
    else:
        status = "assessed"
    return {
        "vitia_version": VERSION, "schema_version": 2, "status": status,
        "audience": data["audience"], "context": data["context"],
        "high_threshold": data["high_threshold"],
        "domains": domains,
        "guardrails": {
            "status": "blocked" if blocked else "review_required" if flags else "no_flags_reported",
            "blocked_by": blocked, "unknown_risk_flags": unknown_flags,
            "note": "No reported flags is not proof that a safety review was completed.",
        },
        "label_neutrality": {
            "scoring": "labels_excluded", "ignored_context_keys": sorted(data["label_context"]),
            "extraction_check": data["neutrality_check"],
        },
        "note": "Value and performance are independent rubric judgments, not sales probabilities. Evidence and confidence do not change either score. Low or unconfirmed axes do not automatically require a product change.",
    }
