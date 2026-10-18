#!/usr/bin/env python3
"""Sealed-Screen Protocol (H-SEALED-SCREEN) Scenario Simulator & SFE Detector.

Evaluates interaction traces across the 5 reference benchmark scenarios
(SCN-1 .. SCN-5) defined in SCREEN_OBSOLESCENCE_SCORE_STANDARD.md §2.1 and §5,
automatically detecting Screen Fallback Events (SFE):
- SFE-IO:  Acoustic Mediation Failure (typed-only input, raw 2D code/table/JSON/path dump on audio).
- SFE-CTX: Manual Context Assembly Failure (asking human to locate paths, copy-paste, or browse).
- SFE-VIS: Uninspected Visual Creation Failure (delivering PDF/SVG/PNG/CAD/render/UI without
           an LLM-side virtual screen render + pixel/layout critic inspection receipt).
- SFE-JDG: Judgment Abdication Failure (claiming completion without verification/judge receipts
           or bombarding the human with tactical micro-confirmations).

Python 3.11 stdlib only; deterministic; no network.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
import json
from pathlib import Path
import re
import sys
from typing import Any

from sos_engine import SCENARIO_IDS, SFE_CODES, SOSEngineError, decode_strict_json

__all__ = [
    "SCENARIO_SPECS",
    "audit_scenario_trace",
    "audit_suite_traces",
    "detect_turn_sfes",
]

SCENARIO_SPECS: dict[str, dict[str, Any]] = {
    "SCN-1": {
        "name": "Spoken Research Loop to Camera-Ready Paper",
        "requires_visual_artifact": True,
        "requires_independent_judge": True,
        "max_tactical_confirmations": 0,
    },
    "SCN-2": {
        "name": "Blind Direction of Art, Image, and Visual Experience",
        "requires_visual_artifact": True,
        "requires_independent_judge": True,
        "max_tactical_confirmations": 0,
    },
    "SCN-3": {
        "name": "Zero-Hint Ambient Resumption",
        "requires_visual_artifact": False,
        "requires_independent_judge": True,
        "max_tactical_confirmations": 0,
    },
    "SCN-4": {
        "name": "Multi-Hour Autonomous Engineering Under Fault Injection",
        "requires_visual_artifact": False,
        "requires_independent_judge": True,
        "max_tactical_confirmations": 0,
    },
    "SCN-5": {
        "name": "Epistemic & Aesthetic Trap Resistance",
        "requires_visual_artifact": True,
        "requires_independent_judge": True,
        "max_tactical_confirmations": 0,
    },
}

# Patterns that violate 2D-to-1D acoustic transduction when spoken to a human (SFE-IO)
_RAW_2D_AUDIO_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("fenced_code_block", re.compile(r"```")),
    ("markdown_table", re.compile(r"\|[ \t]*:?-+:?[ \t]*\|")),
    ("raw_traceback", re.compile(r"Traceback \(most recent call last\):")),
    ("raw_json_object", re.compile(r"^\s*\{\s*\"[A-Za-z0-9_]+\"\s*:", re.M)),
    ("unix_path_dump", re.compile(r"(?:/Users/|/home/|/var/|/etc/)[A-Za-z0-9_./-]{12,}")),
)

# Patterns where the system offloads context assembly onto the human (SFE-CTX)
_MANUAL_CONTEXT_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("ask_for_file_path", re.compile(r"(?i)\b(?:please\s+)?(?:provide|specify|paste|enter|give\s+me)\s+(?:the\s+)?(?:exact\s+)?(?:file\s*path|directory\s*path|task\s*id|sha256)\b")),
    ("ask_to_copy_paste", re.compile(r"(?i)\b(?:copy\s+and\s+paste|paste\s+the\s+(?:error|logs?|output|snippet|contents?))\b")),
    ("ask_to_check_screen", re.compile(r"(?i)\b(?:look\s+at|check|open|inspect)\s+(?:the\s+|your\s+)?(?:screen|browser|terminal|viewer|dashboard|window|pdf|image)\b")),
)

VISUAL_ARTIFACT_KINDS: frozenset[str] = frozenset(
    {"paper", "pdf", "svg", "image", "art", "render", "plot", "cad_model", "drawing", "ui", "video"}
)


def detect_turn_sfes(turn: Mapping[str, Any]) -> list[dict[str, str]]:
    """Inspect a single interaction turn under H-SEALED-SCREEN and return triggered SFEs."""
    if not isinstance(turn, Mapping):
        raise SOSEngineError("Turn must be a mapping")

    events: list[dict[str, str]] = []
    modality = str(turn.get("input_modality") or "voice").lower()
    if modality in {"keyboard_screen", "gui_click", "cli_typed", "screen_picker"}:
        events.append(
            {
                "code": "SFE-IO",
                "reason": f"Human input required screen-tethered modality {modality!r}",
            }
        )

    audible_reply = str(turn.get("audible_output") or "")
    if turn.get("emits_to_human", True) and not audible_reply.strip():
        events.append(
            {
                "code": "SFE-IO",
                "reason": "System emitted no audible output on a human-facing turn",
            }
        )

    for label, pattern in _RAW_2D_AUDIO_PATTERNS:
        if pattern.search(audible_reply):
            events.append(
                {
                    "code": "SFE-IO",
                    "reason": f"Audible output contains raw 2D screen construct ({label})",
                }
            )

    for label, pattern in _MANUAL_CONTEXT_PATTERNS:
        if pattern.search(audible_reply):
            events.append(
                {
                    "code": "SFE-CTX",
                    "reason": f"System offloaded context assembly or screen inspection to human ({label})",
                }
            )

    if turn.get("requires_human_path_hint") is True or turn.get("requires_human_copy_paste") is True:
        events.append(
            {
                "code": "SFE-CTX",
                "reason": "Turn explicitly required human path specification or copy-paste",
            }
        )

    # Check visual artifacts created in this turn
    artifacts = turn.get("created_artifacts") or ()
    if not isinstance(artifacts, Sequence) or isinstance(artifacts, (str, bytes)):
        raise SOSEngineError("created_artifacts must be a list of artifact objects")

    for art in artifacts:
        if not isinstance(art, Mapping):
            raise SOSEngineError("Artifact entry must be a mapping")
        kind = str(art.get("kind") or "").lower()
        if kind in VISUAL_ARTIFACT_KINDS:
            inspection = art.get("llm_screen_inspection")
            if not isinstance(inspection, Mapping):
                events.append(
                    {
                        "code": "SFE-VIS",
                        "reason": f"Visual artifact {art.get('id', kind)!r} ({kind}) delivered without llm_screen_inspection receipt",
                    }
                )
            else:
                rendered = inspection.get("rendered_on_llm_screen") is True
                critiqued = inspection.get("vision_critic_passed") is True
                defects = inspection.get("unresolved_visual_defects", 1)
                if not (rendered and critiqued and defects == 0):
                    events.append(
                        {
                            "code": "SFE-VIS",
                            "reason": (
                                f"Visual artifact {art.get('id', kind)!r} failed closed-loop LLM screen inspection "
                                f"(rendered={rendered}, critic={critiqued}, defects={defects})"
                            ),
                        }
                    )

    # Check judgment / verification on completion claims
    if turn.get("claims_completion") is True:
        judgment = turn.get("independent_judgment")
        if not isinstance(judgment, Mapping):
            events.append(
                {
                    "code": "SFE-JDG",
                    "reason": "System claimed task completion without an independent_judgment receipt",
                }
            )
        else:
            verdict = str(judgment.get("verdict") or "")
            digests = int(judgment.get("evidence_digests") or 0)
            sim_only = judgment.get("simulated_only") is True
            if verdict not in {"celebrate", "pass", "form-conformant"} or digests < 2 or sim_only:
                events.append(
                    {
                        "code": "SFE-JDG",
                        "reason": (
                            f"Completion claimed with insufficient independent judgment "
                            f"(verdict={verdict!r}, digests={digests}, simulated_only={sim_only})"
                        ),
                    }
                )

    return events


def audit_scenario_trace(scenario_id: str, trace: Mapping[str, Any]) -> dict[str, Any]:
    """Audit a multi-turn scenario trace under H-SEALED-SCREEN."""
    if scenario_id not in SCENARIO_SPECS:
        raise SOSEngineError(f"Unknown scenario_id {scenario_id!r}; expected one of {SCENARIO_IDS}")
    if not isinstance(trace, Mapping):
        raise SOSEngineError("Scenario trace must be a mapping")

    spec = SCENARIO_SPECS[scenario_id]
    turns = trace.get("turns")
    if not isinstance(turns, list) or not turns:
        raise SOSEngineError(f"Scenario {scenario_id} must contain a non-empty list of turns")

    all_events: list[dict[str, Any]] = []
    tactical_confirmations = 0
    visual_artifacts_seen = 0

    for idx, turn in enumerate(turns, start=1):
        if not isinstance(turn, Mapping):
            raise SOSEngineError(f"Turn {idx} in {scenario_id} must be a mapping")
        if turn.get("asks_tactical_confirmation") is True:
            tactical_confirmations += 1
        for art in turn.get("created_artifacts") or ():
            if isinstance(art, Mapping) and str(art.get("kind") or "").lower() in VISUAL_ARTIFACT_KINDS:
                visual_artifacts_seen += 1
        turn_events = detect_turn_sfes(turn)
        for ev in turn_events:
            all_events.append({"turn": idx, **ev})

    if tactical_confirmations > spec["max_tactical_confirmations"]:
        all_events.append(
            {
                "turn": len(turns),
                "code": "SFE-JDG",
                "reason": (
                    f"Scenario exceeded allowed tactical confirmation prompts "
                    f"({tactical_confirmations} > {spec['max_tactical_confirmations']})"
                ),
            }
        )

    if spec["requires_visual_artifact"] and visual_artifacts_seen == 0:
        all_events.append(
            {
                "turn": len(turns),
                "code": "SFE-VIS",
                "reason": f"Scenario {scenario_id} requires a visual/paper artifact but none was created",
            }
        )

    distinct_codes = sorted({e["code"] for e in all_events})
    for code in distinct_codes:
        if code not in SFE_CODES:
            raise SOSEngineError(f"Internal error: invalid SFE code {code!r}")

    return {
        "scenario_id": scenario_id,
        "scenario_name": spec["name"],
        "turn_count": len(turns),
        "sfe_count": len(all_events),
        "sfe_codes": distinct_codes,
        "sfe_events": all_events,
        "screen_free_pass": len(all_events) == 0,
    }


def audit_suite_traces(suite: Mapping[str, Any]) -> dict[str, Any]:
    """Audit a complete 5-scenario SOS-BENCH-5 trace suite."""
    if not isinstance(suite, Mapping):
        raise SOSEngineError("Suite payload must be a JSON object")
    scenarios = suite.get("scenarios")
    if not isinstance(scenarios, Mapping):
        raise SOSEngineError("Suite payload must contain a 'scenarios' mapping")

    missing = [s for s in SCENARIO_IDS if s not in scenarios]
    if missing:
        raise SOSEngineError(f"Missing required benchmark scenarios: {', '.join(missing)}")

    results: dict[str, Any] = {}
    total_turns = 0
    sfe_turns = 0
    passed_scenarios = 0
    code_counts: dict[str, int] = {code: 0 for code in SFE_CODES}

    for scn_id in SCENARIO_IDS:
        res = audit_scenario_trace(scn_id, scenarios[scn_id])
        results[scn_id] = res
        total_turns += res["turn_count"]
        turns_with_sfe = len({e["turn"] for e in res["sfe_events"]})
        sfe_turns += turns_with_sfe
        if res["screen_free_pass"]:
            passed_scenarios += 1
        for ev in res["sfe_events"]:
            code_counts[ev["code"]] += 1

    sfr = round(sfe_turns / total_turns, 4) if total_turns > 0 else 1.0
    sfsr = round(1.0 - sfr, 4)

    return {
        "suite_schema": "sos-bench-5/1.0",
        "total_scenarios": len(SCENARIO_IDS),
        "passed_scenarios": passed_scenarios,
        "total_turns": total_turns,
        "turns_with_sfe": sfe_turns,
        "screen_fallback_rate_sfr": sfr,
        "screen_free_survival_rate_sfsr": sfsr,
        "sfe_counts_by_code": code_counts,
        "scenarios": results,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SOS-1.0 Sealed-Screen Scenario Simulator & SFE Detector"
    )
    parser.add_argument("trace_file", type=Path, help="Path to SOS-BENCH-5 trace JSON file")
    parser.add_argument(
        "--trace",
        default=None,
        help="Optional trace key when trace_file contains a 'traces' bundle",
    )
    args = parser.parse_args(argv)

    payload = decode_strict_json(args.trace_file.read_text(encoding="utf-8"))
    if isinstance(payload, Mapping) and "traces" in payload and "scenarios" not in payload:
        traces_map = payload["traces"]
        if not isinstance(traces_map, Mapping):
            raise SOSEngineError("'traces' field must be a mapping")
        if args.trace:
            if args.trace not in traces_map:
                raise SOSEngineError(f"Requested trace {args.trace!r} not in bundle")
            report: Any = audit_suite_traces(traces_map[args.trace])
        else:
            report = {
                name: audit_suite_traces(suite)
                for name, suite in traces_map.items()
            }
    else:
        report = audit_suite_traces(payload)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
