#!/usr/bin/env python3
"""Validate and report Vitia 2.0.0 value/performance profiles."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if __package__:
    from .vitia_assessment import score
    from .vitia_contract import InputError, VERSION
    from .vitia_guardrails import BLOCKING_FLAGS, RISK_PENALTIES
else:
    from vitia_assessment import score
    from vitia_contract import InputError, VERSION
    from vitia_guardrails import BLOCKING_FLAGS, RISK_PENALTIES

# Keep the public imports used by the existing game and mechanism audits.
__all__ = ["score", "InputError", "BLOCKING_FLAGS", "RISK_PENALTIES", "VERSION"]


def load_payload(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> int:
    # JSON pipes must use the same encoding across Windows and Unix shells.
    sys.stdin.reconfigure(encoding="utf-8-sig")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Vitia v2 JSON input path, or - for stdin")
    parser.add_argument("--example", action="store_true", help="print a v2 example input")
    parser.add_argument("--version", action="version", version=f"Vitia {VERSION}")
    args = parser.parse_args()
    try:
        if args.example:
            example = Path(__file__).resolve().parent.parent / "references" / "assessment.example.json"
            payload = load_payload(str(example))
            score(payload)
            print(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False))
            return 0
        if not args.input:
            parser.error("input is required unless --example or --version is used")
        result = score(load_payload(args.input))
    except (InputError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
