"""Validate the versioned Vitia value/performance assessment contract."""

from __future__ import annotations

import math
from typing import Any

if __package__:
    from .vitia_guardrails import DOMAINS
else:
    from vitia_guardrails import DOMAINS

VERSION = "2.0.0"
LABEL_CONTEXT_KEYS = {
    "artifact_name", "category_name", "declared_domain", "reputation_label",
    "source_frame",
}
BASES = {"observed", "measured", "documented", "hypothesis", "unknown"}


class InputError(ValueError):
    pass


def _object(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{name} must be an object")
    return value


def _keys(value: dict[str, Any], allowed: set[str], name: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise InputError(f"unknown {name} keys: {', '.join(unknown)}")


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{name} must be a non-empty string")
    return value.strip()


def _texts(value: Any, name: str) -> list[str]:
    if not isinstance(value, list):
        raise InputError(f"{name} must be an array of strings")
    return [_text(item, f"{name}[{index}]") for index, item in enumerate(value)]


def _unit(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InputError(f"{name} must be a number from 0 to 1")
    if not 0 <= value <= 1 or not math.isfinite(value):
        raise InputError(f"{name} must be a finite number from 0 to 1")
    return float(value)


def _axis(value: Any, name: str) -> dict[str, Any]:
    raw = _object({} if value is None else value, name)
    _keys(raw, {"score", "basis", "rationale", "evidence_refs", "confidence"}, name)
    basis = raw.get("basis", "unknown")
    if not isinstance(basis, str) or basis not in BASES:
        raise InputError(f"{name}.basis must be one of {', '.join(sorted(BASES))}")
    axis_score = raw.get("score")
    confidence = raw.get("confidence")
    rationale = raw.get("rationale", "")
    if not isinstance(rationale, str):
        raise InputError(f"{name}.rationale must be a string")
    evidence = _texts(raw.get("evidence_refs", []), f"{name}.evidence_refs")
    if axis_score is None:
        if basis != "unknown" or confidence is not None:
            raise InputError(f"{name}: an unknown score requires unknown basis and null confidence")
    else:
        axis_score = _unit(axis_score, f"{name}.score")
        if basis == "unknown":
            raise InputError(f"{name}: a score requires an explicit evidence basis")
        rationale = _text(rationale, f"{name}.rationale")
        if not evidence:
            raise InputError(f"{name}: a score requires evidence_refs (hypotheses may cite design evidence)")
        if confidence is not None:
            confidence = _unit(confidence, f"{name}.confidence")
    return {
        "score": axis_score, "basis": basis, "rationale": rationale.strip(),
        "evidence_refs": evidence, "confidence": confidence,
    }


def validate(payload: Any) -> dict[str, Any]:
    raw = _object(payload, "input")
    if type(raw.get("schema_version")) is not int or raw["schema_version"] != 2:
        raise InputError("schema_version must be 2; v1 signals cannot be converted automatically. See references/algorithm.md")
    _keys(raw, {"schema_version", "audience", "context", "domains", "risk_flags",
                "label_context", "high_threshold", "neutrality_check"}, "input")
    audience = _text(raw.get("audience"), "audience")
    context = _text(raw.get("context"), "context")
    domains = _object(raw.get("domains", {}), "domains")
    _keys(domains, set(DOMAINS), "domains")
    normalized = {}
    for domain in DOMAINS:
        item = _object(domains.get(domain, {}), f"domains.{domain}")
        _keys(item, {"value", "performance"}, f"domains.{domain}")
        normalized[domain] = {
            axis: _axis(item.get(axis), f"domains.{domain}.{axis}")
            for axis in ("value", "performance")
        }
    labels = _object(raw.get("label_context", {}), "label_context")
    _keys(labels, LABEL_CONTEXT_KEYS, "label_context")
    if not all(isinstance(value, str) for value in labels.values()):
        raise InputError("label_context values must be strings")
    threshold = _unit(raw.get("high_threshold", 0.75), "high_threshold")
    if threshold == 0:
        raise InputError("high_threshold must be greater than zero")
    neutrality = _object(raw.get("neutrality_check", {}), "neutrality_check")
    _keys(neutrality, {"status", "evidence_refs"}, "neutrality_check")
    status = neutrality.get("status", "not_checked")
    if not isinstance(status, str) or status not in {"passed", "failed", "not_checked"}:
        raise InputError("neutrality_check.status must be passed, failed, or not_checked")
    evidence = _texts(neutrality.get("evidence_refs", []), "neutrality_check.evidence_refs")
    if status in {"passed", "failed"} and not evidence:
        raise InputError("neutrality_check requires evidence_refs for a checked result")
    return {
        "schema_version": 2, "audience": audience, "context": context,
        "domains": normalized, "high_threshold": threshold,
        "risk_flags": sorted(set(_texts(raw.get("risk_flags", []), "risk_flags"))),
        "label_context": dict(labels),
        "neutrality_check": {"status": status, "evidence_refs": evidence},
    }
