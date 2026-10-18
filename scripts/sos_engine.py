#!/usr/bin/env python3
"""Core scoring, rubric validation, tier gating, and sensitivity engine for SOS-1.0.

Implements the normative mathematical and evidence rules defined in
SCREEN_OBSOLESCENCE_SCORE_STANDARD.md (SOS-STD-1.0):
- Four pillars (AIO, CTX, CRE, JDG), each [0, 100] from four [0, 25] sub-dimensions.
- Latent Post-Screen Capability Score (SOS_latent).
- Bottleneck Balance Factor (BBF) with smoothing constant epsilon = 10, gamma = 0.5.
- Effective Screen-Free Liberation Score (SOS_effective).
- Scribe-to-Post-Screen Maturity Tiers (Level 0 .. Level 5) and RULE-TIER-CAP.
- ASDAI-aligned evidence binding verification (RULE-SEQ-01 .. RULE-TABLE-04).

Python 3.11 stdlib only; deterministic; no network.
"""

from __future__ import annotations

import argparse
from collections.abc import Mapping
import json
import math
from pathlib import Path
import sys
from typing import Any

__all__ = [
    "EPSILON",
    "EVIDENCE_KINDS",
    "GAMMA",
    "MATURITY_TIERS",
    "PILLARS",
    "SCENARIO_IDS",
    "SCHEMA_VERSION",
    "SFE_CODES",
    "SOSEngineError",
    "STANDARD_VERSION",
    "SUBDIMENSIONS",
    "SUBDIMENSION_TITLES",
    "compute_scores",
    "compute_upgrade_sensitivity",
    "decode_strict_json",
    "render_markdown_report",
    "rubric_band",
    "validate_evaluation_record",
]

SCHEMA_VERSION = "sos-evaluation/1.0"
STANDARD_VERSION = "1.0.0"
EPSILON = 10.0
GAMMA = 0.5

PILLARS: tuple[str, ...] = ("AIO", "CTX", "CRE", "JDG")

SUBDIMENSIONS: dict[str, tuple[str, ...]] = {
    "AIO": ("AIO-1", "AIO-2", "AIO-3", "AIO-4"),
    "CTX": ("CTX-1", "CTX-2", "CTX-3", "CTX-4"),
    "CRE": ("CRE-1", "CRE-2", "CRE-3", "CRE-4"),
    "JDG": ("JDG-1", "JDG-2", "JDG-3", "JDG-4"),
}

SUBDIMENSION_TITLES: dict[str, str] = {
    "AIO-1": "Audible Input Capture, Duplex Flow, and Paralinguistic Fidelity",
    "AIO-2": "2D-to-1D Semantic Audio Transduction",
    "AIO-3": "Progressive Audible Zoom and Background Sonification",
    "AIO-4": "Zero-Screen Lifecycle Bootstrap and Operational Control",
    "CTX-1": "Passive Ambient and Cross-Session Context Assembly",
    "CTX-2": "Active Multi-Source Epistemic Hunting",
    "CTX-3": "Source Provenance, Freshness, and Drift Invalidation",
    "CTX-4": "Zero-Copy, Zero-Pointer Context Ergonomics",
    "CRE-1": "Paper, Manuscript, and Formal Document Generation",
    "CRE-2": "Art, Image, and Visual Media Synthesis",
    "CRE-3": "LLM-Owned Screen Loop (Machine Rendering & Visual Self-Inspection)",
    "CRE-4": "Cross-Modal Synthesis and Deliverable Packaging",
    "JDG-1": "Epistemic, Empirical, and Adversarial Self-Verification",
    "JDG-2": "Autonomous Aesthetic, Rhetorical, and Compositional Judgment",
    "JDG-3": "Long-Horizon Tactical Autonomy and Self-Healing",
    "JDG-4": "Calibrated Principal Escalation Boundary",
}

ALL_SUBDIMENSIONS: tuple[str, ...] = tuple(
    sub_id for pillar in PILLARS for sub_id in SUBDIMENSIONS[pillar]
)

EVIDENCE_KINDS: frozenset[str] = frozenset(
    {"observation", "inference", "assumption", "decision", "requirement", "question"}
)

SFE_CODES: tuple[str, ...] = ("SFE-IO", "SFE-CTX", "SFE-VIS", "SFE-JDG")
SCENARIO_IDS: tuple[str, ...] = ("SCN-1", "SCN-2", "SCN-3", "SCN-4", "SCN-5")

MATURITY_TIERS: tuple[dict[str, Any], ...] = (
    {
        "level": 0,
        "id": "Level 0",
        "name": "Manual Screen Labor",
        "min_effective": 0.0,
        "max_effective": 19.99,
        "min_all_pillars": 0.0,
        "min_two_pillars": 0.0,
    },
    {
        "level": 1,
        "id": "Level 1",
        "name": "Assisted Screen Scribe",
        "min_effective": 20.0,
        "max_effective": 39.99,
        "min_all_pillars": 0.0,
        "min_two_pillars": 0.0,
    },
    {
        "level": 2,
        "id": "Level 2",
        "name": "Headless Cognitive Engine (Screen-Tethered Boundary)",
        "min_effective": 40.0,
        "max_effective": 59.99,
        "min_all_pillars": 0.0,
        "min_two_pillars": 50.0,
    },
    {
        "level": 3,
        "id": "Level 3",
        "name": "Supervised Screen-Free Delegation",
        "min_effective": 60.0,
        "max_effective": 79.99,
        "min_all_pillars": 50.0,
        "min_two_pillars": 50.0,
    },
    {
        "level": 4,
        "id": "Level 4",
        "name": "Autonomous Screen Stewardship",
        "min_effective": 80.0,
        "max_effective": 94.99,
        "min_all_pillars": 75.0,
        "min_two_pillars": 75.0,
    },
    {
        "level": 5,
        "id": "Level 5",
        "name": "Post-Screen Liberation",
        "min_effective": 95.0,
        "max_effective": 100.0,
        "min_all_pillars": 90.0,
        "min_two_pillars": 90.0,
    },
)


class SOSEngineError(ValueError):
    """Raised when an SOS-1.0 score input, receipt, or constraint is invalid."""


def _unique_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise SOSEngineError(f"Duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> Any:
    raise SOSEngineError(f"Invalid non-finite JSON constant: {value!r}")


def decode_strict_json(raw_text: str) -> Any:
    """Parse JSON while rejecting duplicate keys and NaN/Infinity constants."""
    if not isinstance(raw_text, str) or not raw_text.strip():
        raise SOSEngineError("JSON input must be a non-empty string")
    try:
        return json.loads(
            raw_text,
            object_pairs_hook=_unique_object_pairs,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise SOSEngineError(f"Malformed JSON: {exc}") from exc


def _validate_subscore(value: Any, sub_id: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise SOSEngineError(
            f"Sub-dimension {sub_id!r} score must be an int or float, got {type(value).__name__}"
        )
    numeric = float(value)
    if not math.isfinite(numeric):
        raise SOSEngineError(f"Sub-dimension {sub_id!r} score must be finite")
    if numeric < 0.0 or numeric > 25.0:
        raise SOSEngineError(
            f"Sub-dimension {sub_id!r} score {numeric} out of bounds [0, 25]"
        )
    return numeric


def rubric_band(score: float) -> str:
    """Return the normative SOS-1.0 rubric band for a [0, 25] sub-dimension score."""
    val = _validate_subscore(score, "rubric_probe")
    if val < 6.0:
        return "0-5 (Absent / Screen-Bound)"
    if val < 13.0:
        return "6-12 (Partial / Assisted)"
    if val < 20.0:
        return "13-19 (Operational / Autonomous Loop)"
    return "20-25 (Sovereign / Post-Screen Grade)"


def _tier_by_level(level: int) -> dict[str, Any]:
    for tier in MATURITY_TIERS:
        if tier["level"] == level:
            return dict(tier)
    raise SOSEngineError(f"Unknown tier level: {level}")


def _numerical_tier_level(sos_effective: float) -> int:
    if sos_effective >= 95.0:
        return 5
    if sos_effective >= 80.0:
        return 4
    if sos_effective >= 60.0:
        return 3
    if sos_effective >= 40.0:
        return 2
    if sos_effective >= 20.0:
        return 1
    return 0


def _satisfies_tier_floors(
    level: int,
    pillar_totals: Mapping[str, float],
    cre3_score: float,
) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    values = list(pillar_totals.values())
    min_pillar = min(values)
    count_ge_50 = sum(1 for v in values if v >= 50.0)

    if level >= 3:
        # RULE-TIER-CAP check
        if pillar_totals["AIO"] < 50.0:
            reasons.append(
                f"RULE-TIER-CAP: AIO ({pillar_totals['AIO']:.2f}) < 50.0 required for Level >= 3"
            )
        if cre3_score < 13.0:
            reasons.append(
                f"RULE-TIER-CAP: CRE-3 ({cre3_score:.2f}) < 13.0 required for Level >= 3"
            )

    if level == 5 and min_pillar < 90.0:
        reasons.append(f"Level 5 floor requires all pillars >= 90.0 (min={min_pillar:.2f})")
    elif level == 4 and min_pillar < 75.0:
        reasons.append(f"Level 4 floor requires all pillars >= 75.0 (min={min_pillar:.2f})")
    elif level == 3 and min_pillar < 50.0:
        reasons.append(f"Level 3 floor requires all pillars >= 50.0 (min={min_pillar:.2f})")
    elif level == 2 and count_ge_50 < 2:
        reasons.append(
            f"Level 2 floor requires at least two pillars >= 50.0 (count={count_ge_50})"
        )

    return (len(reasons) == 0, reasons)


def compute_scores(subscores: Mapping[str, int | float]) -> dict[str, Any]:
    """Compute pillar totals, SOS_latent, BBF, SOS_effective, and Maturity Tier."""
    if not isinstance(subscores, Mapping):
        raise SOSEngineError("subscores must be a mapping of 16 sub-dimension IDs")

    missing = [k for k in ALL_SUBDIMENSIONS if k not in subscores]
    extra = [k for k in subscores if k not in ALL_SUBDIMENSIONS]
    if missing:
        raise SOSEngineError(f"Missing sub-dimension scores: {', '.join(missing)}")
    if extra:
        raise SOSEngineError(f"Unknown sub-dimension keys: {', '.join(sorted(extra))}")

    validated_sub: dict[str, float] = {
        sub_id: _validate_subscore(subscores[sub_id], sub_id)
        for sub_id in ALL_SUBDIMENSIONS
    }

    pillar_totals: dict[str, float] = {}
    for pillar in PILLARS:
        pillar_totals[pillar] = round(
            sum(validated_sub[sub_id] for sub_id in SUBDIMENSIONS[pillar]), 4
        )

    min_pillar_name = min(PILLARS, key=lambda p: pillar_totals[p])
    max_pillar_name = max(PILLARS, key=lambda p: pillar_totals[p])
    min_pillar_val = pillar_totals[min_pillar_name]
    max_pillar_val = pillar_totals[max_pillar_name]

    sos_latent = round(sum(pillar_totals.values()) / 4.0, 2)
    bbf_raw = math.pow(
        (min_pillar_val + EPSILON) / (max_pillar_val + EPSILON), GAMMA
    )
    bbf = round(bbf_raw, 4)
    sos_effective = round(sos_latent * bbf_raw, 2)

    raw_level = _numerical_tier_level(sos_effective)
    effective_level = raw_level
    cap_reasons: list[str] = []

    while effective_level > 0:
        ok, reasons = _satisfies_tier_floors(
            effective_level, pillar_totals, validated_sub["CRE-3"]
        )
        if ok:
            break
        for r in reasons:
            if r not in cap_reasons:
                cap_reasons.append(r)
        effective_level -= 1

    tier_info = _tier_by_level(effective_level)
    raw_tier_info = _tier_by_level(raw_level)

    return {
        "subscores": {
            k: int(v) if v.is_integer() else v for k, v in validated_sub.items()
        },
        "pillar_totals": {
            k: int(v) if v.is_integer() else v for k, v in pillar_totals.items()
        },
        "min_pillar": {"pillar": min_pillar_name, "score": min_pillar_val},
        "max_pillar": {"pillar": max_pillar_name, "score": max_pillar_val},
        "sos_latent": sos_latent,
        "bbf": bbf,
        "bbf_exact": bbf_raw,
        "sos_effective": sos_effective,
        "raw_tier": f"{raw_tier_info['id']}: {raw_tier_info['name']}",
        "effective_tier_level": effective_level,
        "effective_tier_id": tier_info["id"],
        "effective_tier_name": tier_info["name"],
        "effective_tier": f"{tier_info['id']}: {tier_info['name']}",
        "tier_capped": effective_level < raw_level,
        "cap_reasons": cap_reasons,
    }


def compute_upgrade_sensitivity(subscores: Mapping[str, int | float]) -> dict[str, Any]:
    """Rank sub-dimensions by marginal SOS_effective gain (+1 pt and to max=25)."""
    base = compute_scores(subscores)
    base_eff = base["sos_effective"]

    marginal_gains: list[dict[str, Any]] = []
    for sub_id in ALL_SUBDIMENSIONS:
        current_val = float(subscores[sub_id])
        pillar = sub_id.split("-")[0]
        if current_val >= 25.0:
            marginal_gains.append(
                {
                    "subdimension": sub_id,
                    "pillar": pillar,
                    "current_score": current_val,
                    "headroom": 0.0,
                    "delta_plus_1": 0.0,
                    "delta_to_max_25": 0.0,
                }
            )
            continue

        plus_one_map = dict(subscores)
        plus_one_map[sub_id] = min(25.0, current_val + 1.0)
        plus_one_res = compute_scores(plus_one_map)

        to_max_map = dict(subscores)
        to_max_map[sub_id] = 25.0
        to_max_res = compute_scores(to_max_map)

        marginal_gains.append(
            {
                "subdimension": sub_id,
                "pillar": pillar,
                "title": SUBDIMENSION_TITLES[sub_id],
                "current_score": current_val,
                "headroom": round(25.0 - current_val, 2),
                "delta_plus_1": round(plus_one_res["sos_effective"] - base_eff, 2),
                "delta_to_max_25": round(to_max_res["sos_effective"] - base_eff, 2),
                "new_effective_at_25": to_max_res["sos_effective"],
            }
        )

    marginal_gains.sort(
        key=lambda item: (-item["delta_to_max_25"], -item["delta_plus_1"], item["subdimension"])
    )

    current_level = base["effective_tier_level"]
    next_level = min(5, current_level + 1)
    next_tier = _tier_by_level(next_level)

    return {
        "baseline_effective": base_eff,
        "baseline_latent": base["sos_latent"],
        "baseline_tier": base["effective_tier"],
        "bottleneck_pillar": base["min_pillar"],
        "next_target_tier": f"{next_tier['id']}: {next_tier['name']}",
        "next_target_min_effective": next_tier["min_effective"],
        "next_target_min_all_pillars": next_tier["min_all_pillars"],
        "ranked_subdimension_levers": marginal_gains,
    }


def validate_evaluation_record(
    record: Mapping[str, Any],
    *,
    canonical_std_path: Path | None = None,
) -> dict[str, Any]:
    """Validate an SOS-1.0 evaluation record against RULE-SEQ-01 .. RULE-TABLE-04."""
    if not isinstance(record, Mapping):
        raise SOSEngineError("Evaluation record must be a JSON object")

    # RULE-SEQ-01: Standard document must exist before scoring
    if canonical_std_path is not None:
        if not Path(canonical_std_path).is_file():
            raise SOSEngineError(
                f"RULE-SEQ-01 violation: standard file missing at {canonical_std_path}"
            )

    if record.get("schema") != SCHEMA_VERSION:
        raise SOSEngineError(
            f"Unsupported or missing schema: expected {SCHEMA_VERSION!r}, got {record.get('schema')!r}"
        )
    if record.get("standard_version") != STANDARD_VERSION:
        raise SOSEngineError(
            f"Unsupported standard_version: expected {STANDARD_VERSION!r}, got {record.get('standard_version')!r}"
        )

    target = record.get("target_system")
    if not isinstance(target, Mapping) or not str(target.get("name") or "").strip():
        raise SOSEngineError("target_system.name is required")

    # RULE-SCOPE-02: Scope separation
    scope = record.get("evaluation_scope")
    if scope not in ("native", "coupled"):
        raise SOSEngineError(
            f"RULE-SCOPE-02 violation: evaluation_scope must be 'native' or 'coupled', got {scope!r}"
        )

    # RULE-EVID-03: Evidence binding per sub-dimension
    raw_sub = record.get("subdimensions")
    if not isinstance(raw_sub, Mapping):
        raise SOSEngineError("subdimensions object is required")
    extra_sub = [k for k in raw_sub if k not in ALL_SUBDIMENSIONS]
    if extra_sub:
        raise SOSEngineError(
            f"RULE-EVID-03 violation: unknown sub-dimension keys: {', '.join(sorted(extra_sub))}"
        )

    extracted_scores: dict[str, float] = {}
    for sub_id in ALL_SUBDIMENSIONS:
        if sub_id not in raw_sub:
            raise SOSEngineError(f"RULE-EVID-03 violation: missing sub-dimension {sub_id!r}")
        entry = raw_sub[sub_id]
        if not isinstance(entry, Mapping):
            raise SOSEngineError(f"Sub-dimension {sub_id!r} entry must be an object")
        score = _validate_subscore(entry.get("score"), sub_id)
        ev_kind = entry.get("evidence_kind")
        if ev_kind not in EVIDENCE_KINDS:
            raise SOSEngineError(
                f"RULE-EVID-03 violation: {sub_id!r} evidence_kind {ev_kind!r} not in {sorted(EVIDENCE_KINDS)}"
            )
        locator = entry.get("locator")
        if not isinstance(locator, str) or not locator.strip():
            raise SOSEngineError(
                f"RULE-EVID-03 violation: {sub_id!r} requires a non-empty source locator"
            )
        rationale = entry.get("rationale")
        if not isinstance(rationale, str) or not rationale.strip():
            raise SOSEngineError(
                f"RULE-EVID-03 violation: {sub_id!r} requires a non-empty rationale"
            )
        extracted_scores[sub_id] = score

    computed = compute_scores(extracted_scores)

    # RULE-TABLE-04: Verify declared summary numbers if present
    declared_summary = record.get("summary")
    if declared_summary is not None:
        if not isinstance(declared_summary, Mapping):
            raise SOSEngineError("summary must be an object when present")
        declared_pillars = declared_summary.get("pillar_totals")
        if isinstance(declared_pillars, Mapping):
            for p in PILLARS:
                if p in declared_pillars and float(declared_pillars[p]) != float(
                    computed["pillar_totals"][p]
                ):
                    raise SOSEngineError(
                        f"RULE-TABLE-04 mismatch on pillar {p}: declared {declared_pillars[p]} != computed {computed['pillar_totals'][p]}"
                    )
        if "sos_latent" in declared_summary and round(
            float(declared_summary["sos_latent"]), 2
        ) != computed["sos_latent"]:
            raise SOSEngineError(
                f"RULE-TABLE-04 mismatch on sos_latent: declared {declared_summary['sos_latent']} != computed {computed['sos_latent']}"
            )
        if "bbf" in declared_summary and round(
            float(declared_summary["bbf"]), 4
        ) != computed["bbf"]:
            raise SOSEngineError(
                f"RULE-TABLE-04 mismatch on bbf: declared {declared_summary['bbf']} != computed {computed['bbf']}"
            )
        if "sos_effective" in declared_summary and round(
            float(declared_summary["sos_effective"]), 2
        ) != computed["sos_effective"]:
            raise SOSEngineError(
                f"RULE-TABLE-04 mismatch on sos_effective: declared {declared_summary['sos_effective']} != computed {computed['sos_effective']}"
            )
        if (
            "effective_tier_id" in declared_summary
            and declared_summary["effective_tier_id"] != computed["effective_tier_id"]
        ):
            raise SOSEngineError(
                f"RULE-TABLE-04 / RULE-TIER-CAP mismatch on effective_tier_id: declared {declared_summary['effective_tier_id']!r} != computed {computed['effective_tier_id']!r}"
            )

    # Validate scenarios if present
    scenarios = record.get("scenarios")
    if scenarios is not None:
        if not isinstance(scenarios, Mapping):
            raise SOSEngineError("scenarios must be a mapping when present")
        missing_scn = [s for s in SCENARIO_IDS if s not in scenarios]
        if missing_scn:
            raise SOSEngineError(
                f"RULE-TABLE-04 violation: missing scenarios {', '.join(missing_scn)}"
            )
        for scn_id in SCENARIO_IDS:
            scn = scenarios[scn_id]
            if not isinstance(scn, Mapping):
                raise SOSEngineError(f"Scenario {scn_id} must be an object")
            sfes = scn.get("sfe_events", [])
            if not isinstance(sfes, list) or any(c not in SFE_CODES for c in sfes):
                raise SOSEngineError(
                    f"Scenario {scn_id} sfe_events must be a list of valid SFE codes {SFE_CODES}"
                )

    return {
        "valid": True,
        "target_system": dict(target),
        "evaluation_scope": scope,
        "computed": computed,
        "sensitivity": compute_upgrade_sensitivity(extracted_scores),
    }


def render_markdown_report(record: Mapping[str, Any]) -> str:
    """Render a complete SOS-1.0 Markdown report from a validated evaluation record."""
    validated = validate_evaluation_record(record)
    computed = validated["computed"]
    target = validated["target_system"]
    scope = validated["evaluation_scope"]
    sub_map = record["subdimensions"]

    lines: list[str] = [
        f"# SOS-1.0 Evaluation Report: {target.get('name')} ({scope.upper()} Scope)",
        "",
        f"- **Target System:** `{target.get('name')}`",
        f"- **Repository / Path:** `{target.get('repository', 'N/A')}`",
        f"- **Commit / Revision:** `{target.get('revision', 'N/A')}`",
        f"- **Evaluation Scope (`RULE-SCOPE-02`):** `{scope}`",
        f"- **Standard Version:** `SOS-{STANDARD_VERSION}`",
        "",
        "## 1. Headline Composite Score (`RULE-TABLE-04`)",
        "",
        "| Metric | Value | Notes |",
        "| :--- | :---: | :--- |",
        f"| **Pillar I: `AIO`** (Audible I/O) | **`{computed['pillar_totals']['AIO']} / 100`** | Spoken input, 2D->1D audio, audio zoom, zero-GUI boot |",
        f"| **Pillar II: `CTX`** (Context Assembly) | **`{computed['pillar_totals']['CTX']} / 100`** | Passive continuity, active hunting, provenance, zero-copy |",
        f"| **Pillar III: `CRE`** (Creation & LLM Screen) | **`{computed['pillar_totals']['CRE']} / 100`** | Paper foundry, art/images, LLM screen loop, packaging |",
        f"| **Pillar IV: `JDG`** (Independent Judgment) | **`{computed['pillar_totals']['JDG']} / 100`** | Epistemic verification, aesthetic critique, self-healing, escalation |",
        f"| **`SOS_latent`** (Arithmetic Mean) | **`{computed['sos_latent']:.2f} / 100`** | Unweighted mean of the 4 pillars |",
        f"| **`BBF`** (Bottleneck Balance Factor) | **`{computed['bbf']:.4f}`** | $\\sqrt{{(\\min + 10) / (\\max + 10)}}$ (`min={computed['min_pillar']['pillar']}`, `max={computed['max_pillar']['pillar']}`) |",
        f"| **`SOS_effective`** (Headline Score) | **`{computed['sos_effective']:.2f} / 100`** | $\\text{{SOS}}_{{\\text{{latent}}}} \\times \\text{{BBF}}$ |",
        f"| **Normative Maturity Tier** | **`{computed['effective_tier']}`** | {'Capped by floor/RULE-TIER-CAP' if computed['tier_capped'] else 'Uncapped'} |",
        "",
        "## 2. Sub-Dimension Breakdown (`RULE-EVID-03`)",
        "",
        "| Sub-Dimension | Score (`/25`) | Band | Evidence Kind | Source Locator |",
        "| :--- | :---: | :--- | :---: | :--- |",
    ]

    for sub_id in ALL_SUBDIMENSIONS:
        entry = sub_map[sub_id]
        sc = computed["subscores"][sub_id]
        lines.append(
            f"| **`{sub_id}`** {SUBDIMENSION_TITLES[sub_id]} | **{sc} / 25** | {rubric_band(float(sc))} | `{entry['evidence_kind']}` | `{entry['locator']}` |"
        )

    if computed["cap_reasons"]:
        lines.extend(
            [
                "",
                "## 3. Active Tier Floor / Cap Constraints (`RULE-TIER-CAP`)",
                "",
            ]
        )
        for reason in computed["cap_reasons"]:
            lines.append(f"- `{reason}`")

    top_levers = validated["sensitivity"]["ranked_subdimension_levers"][:5]
    lines.extend(
        [
            "",
            "## 4. Top 5 Upgrade Levers by Marginal `SOS_effective` Gain",
            "",
            "| Rank | Sub-Dimension | Current | Gain (+1 pt) | Gain (to 25/25) | Projected `SOS_effective` |",
            "| :---: | :--- | :---: | :---: | :---: | :---: |",
        ]
    )
    for idx, lever in enumerate(top_levers, start=1):
        lines.append(
            f"| {idx} | **`{lever['subdimension']}`** ({lever.get('title', '')}) | `{lever['current_score']}/25` | `+{lever['delta_plus_1']:.2f}` | `+{lever['delta_to_max_25']:.2f}` | `{lever.get('new_effective_at_25', computed['sos_effective']):.2f}` |"
        )

    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="SOS-1.0 Scoring, Validation, and Sensitivity CLI"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_val = sub.add_parser("validate", help="Validate an SOS-1.0 evaluation JSON file")
    p_val.add_argument("path", type=Path, help="Path to evaluation JSON file")
    p_val.add_argument(
        "--standard",
        type=Path,
        default=None,
        help="Optional path to SCREEN_OBSOLESCENCE_SCORE_STANDARD.md for RULE-SEQ-01 check",
    )

    p_rep = sub.add_parser("report", help="Render Markdown or JSON report for an evaluation")
    p_rep.add_argument("path", type=Path, help="Path to evaluation JSON file")
    p_rep.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    p_rep.add_argument(
        "--scope",
        choices=("native", "coupled"),
        default=None,
        help="If the file contains a multi-scope bundle, select which scope to render",
    )

    args = parser.parse_args(argv)
    payload = decode_strict_json(args.path.read_text(encoding="utf-8"))

    # Support either a single evaluation record or a bundle {"evaluations": {"native": ..., "coupled": ...}}
    records: list[Mapping[str, Any]] = []
    if isinstance(payload, Mapping) and "evaluations" in payload:
        evals = payload["evaluations"]
        if not isinstance(evals, Mapping):
            raise SOSEngineError("evaluations field must be a mapping")
        if getattr(args, "scope", None):
            if args.scope not in evals:
                raise SOSEngineError(f"Requested scope {args.scope!r} not in evaluations")
            records.append(evals[args.scope])
        else:
            for k in sorted(evals):
                records.append(evals[k])
    else:
        records.append(payload)

    if args.command == "validate":
        results = [
            validate_evaluation_record(r, canonical_std_path=args.standard)
            for r in records
        ]
        print(json.dumps({"status": "ok", "validated_count": len(results), "results": results}, indent=2))
        return 0

    if args.command == "report":
        if args.format == "json":
            results = [validate_evaluation_record(r) for r in records]
            print(json.dumps(results if len(results) > 1 else results[0], indent=2))
        else:
            blocks = [render_markdown_report(r) for r in records]
            print("\n---\n\n".join(blocks), end="")
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
