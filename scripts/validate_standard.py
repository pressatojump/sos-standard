#!/usr/bin/env python3
"""Validate SCREEN_OBSOLESCENCE_SCORE_STANDARD.md, embedded formulas, fixtures, and negative cases.

Performs:
1. Structural and normative inventory checks on SCREEN_OBSOLESCENCE_SCORE_STANDARD.md
   (including Section 1.3 "Why This Standard Is Important", H-SEALED-SCREEN, 4 SFE codes,
   4 Pillars, 16 Sub-Dimensions, 6 Maturity Tiers, RULE-TIER-CAP, 5 Scenarios, and
   4 Normative Evaluation Rules).
2. Byte-parity verification with ~/SCREEN_OBSOLESCENCE_SCORE_STANDARD.md when present.
3. Mathematical property checks (bounds, monotonicity, BBF formula, RULE-TIER-CAP).
4. 18 negative/adversarial rejection checks on sos_engine and sos_sfe_harness.
5. Validation of fixtures/magiclab_sos_evaluation.json and fixtures/sample_sfe_traces.json.
6. Execution of the full unittest suite in tests/test_sos_suite.py.

Python 3.11 stdlib only; deterministic; no network.
"""

from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sos_engine import (
    ALL_SUBDIMENSIONS,
    MATURITY_TIERS,
    PILLARS,
    SCENARIO_IDS,
    SFE_CODES,
    SOSEngineError,
    compute_scores,
    decode_strict_json,
    validate_evaluation_record,
)
from sos_sfe_harness import audit_suite_traces

ROOT = SCRIPTS_DIR.parent
DOCUMENT = ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md"
HOME_DOCUMENT = Path.home() / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md"
MAGICLAB_FIXTURE = ROOT / "fixtures" / "magiclab_sos_evaluation.json"
TRACES_FIXTURE = ROOT / "fixtures" / "sample_sfe_traces.json"

REQUIRED_NORMATIVE_RULES: tuple[str, ...] = (
    "RULE-TIER-CAP",
    "RULE-SEQ-01",
    "RULE-SCOPE-02",
    "RULE-EVID-03",
    "RULE-TABLE-04",
)

REQUIRED_SECTIONS: tuple[str, ...] = (
    "## 1. Executive Summary and Foundational Premise",
    "### 1.1 Leaving Behind a Single Base Skill",
    "### 1.2 Beyond the Scribe: Why the Screen Is the True Boundary",
    "### 1.3 Why This Standard Is Important",
    "## 2. The Necessary Hypothetical Scenario: The Sealed-Screen Protocol (`H-SEALED-SCREEN`)",
    "### 2.1 Definition of a Screen Fallback Event (`SFE`)",
    "## 3. Normative Architecture of the Score: The Four Critical Factors",
    "### Pillar I: Audible Inputs and Outputs (`AIO` — 0 to 100 Points)",
    "### Pillar II: Passive and Active Context Assembly (`CTX` — 0 to 100 Points)",
    "### Pillar III: Creation Across Modalities and LLM-Managed Screen Stewardship (`CRE` — 0 to 100 Points)",
    "### Pillar IV: Independent Judgment (`JDG` — 0 to 100 Points)",
    "## 4. Mathematical Formulation of the Score",
    "## 5. Reference Benchmark Scenarios (`SOS-BENCH-5`)",
    "## 6. Normative Evaluation Procedure and Reporting Contract",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def expect_rejected(fn: Any, label: str) -> None:
    try:
        fn()
    except (SOSEngineError, ValueError):
        return
    raise ValueError(f"Invalid case was erroneously accepted: {label}")


def validate_markdown_document(doc_path: Path = DOCUMENT) -> dict[str, Any]:
    require(doc_path.is_file(), f"Standard file missing: {doc_path}")
    raw_bytes = doc_path.read_bytes()
    text = raw_bytes.decode("utf-8")

    # Verify balanced code fences
    blocks = re.findall(r"^```([^\n]*)\n(.*?)^```[ \t]*$", text, re.M | re.S)
    require(text.count("\n```") == 2 * len(blocks), "Unbalanced Markdown code fences")

    # Verify all required section headers exist in order
    last_pos = -1
    for header in REQUIRED_SECTIONS:
        pos = text.find(header)
        require(pos != -1, f"Missing required section header: {header}")
        require(pos > last_pos, f"Section header out of order: {header}")
        last_pos = pos

    # Verify all 4 SFE codes
    for code in SFE_CODES:
        require(f"`{code}`" in text, f"Missing SFE code in standard: {code}")

    # Verify all 16 sub-dimensions and their 4 rubric bands (0–5, 6–12, 13–19, 20–25)
    for sub_id in ALL_SUBDIMENSIONS:
        require(f"#### `{sub_id}`:" in text, f"Missing sub-dimension heading: {sub_id}")
    for band in ("**0–5", "**6–12", "**13–19", "**20–25"):
        count = text.count(band)
        require(
            count == 16,
            f"Expected 16 occurrences of rubric band prefix {band!r}, found {count}",
        )

    # Verify all 6 Maturity Tiers
    for tier in MATURITY_TIERS:
        require(f"**{tier['id']}**" in text, f"Missing tier in standard: {tier['id']}")
        require(f"**{tier['name']}**" in text, f"Missing tier name in standard: {tier['name']}")

    # Verify all 5 Reference Benchmark Scenarios
    for scn_id in SCENARIO_IDS:
        require(f"`{scn_id}`" in text, f"Missing scenario ID in standard: {scn_id}")

    # Verify all 5 Normative Rules
    for rule_id in REQUIRED_NORMATIVE_RULES:
        require(f"`{rule_id}`" in text, f"Missing normative rule ID in standard: {rule_id}")

    # Check home directory sync if ~/SCREEN_OBSOLESCENCE_SCORE_STANDARD.md exists
    home_synced = False
    if HOME_DOCUMENT.is_file():
        home_digest = sha256(HOME_DOCUMENT.read_bytes()).hexdigest()
        repo_digest = sha256(raw_bytes).hexdigest()
        require(
            home_digest == repo_digest,
            f"Home standard {HOME_DOCUMENT} ({home_digest[:12]}) differs from repo copy ({repo_digest[:12]})",
        )
        home_synced = True

    return {
        "document_bytes": len(raw_bytes),
        "document_sha256": sha256(raw_bytes).hexdigest(),
        "home_synced": home_synced,
        "sections_verified": len(REQUIRED_SECTIONS),
        "subdimensions_verified": len(ALL_SUBDIMENSIONS),
        "rules_verified": len(REQUIRED_NORMATIVE_RULES),
    }


def check_mathematical_invariants() -> int:
    checks = 0

    # 1. Zero vector -> Level 0, SOS_latent = 0, BBF = 1.0, SOS_effective = 0.0
    zero_scores = {k: 0 for k in ALL_SUBDIMENSIONS}
    z_res = compute_scores(zero_scores)
    require(z_res["sos_latent"] == 0.0, "Zero latent mismatch")
    require(z_res["bbf"] == 1.0, "Zero BBF mismatch")
    require(z_res["sos_effective"] == 0.0, "Zero effective mismatch")
    require(z_res["effective_tier_level"] == 0, "Zero tier mismatch")
    checks += 1

    # 2. Perfect vector -> Level 5, SOS_latent = 100.0, BBF = 1.0, SOS_effective = 100.0
    max_scores = {k: 25 for k in ALL_SUBDIMENSIONS}
    m_res = compute_scores(max_scores)
    require(m_res["sos_latent"] == 100.0, "Max latent mismatch")
    require(m_res["bbf"] == 1.0, "Max BBF mismatch")
    require(m_res["sos_effective"] == 100.0, "Max effective mismatch")
    require(m_res["effective_tier_level"] == 5, "Max tier mismatch")
    require(not m_res["tier_capped"], "Max should not be capped")
    checks += 1

    # 3. Monotonicity across all 16 sub-dimensions from a mid-point state
    base_map = {
        "AIO-1": 8, "AIO-2": 9, "AIO-3": 7, "AIO-4": 8,
        "CTX-1": 18, "CTX-2": 18, "CTX-3": 19, "CTX-4": 17,
        "CRE-1": 16, "CRE-2": 15, "CRE-3": 14, "CRE-4": 17,
        "JDG-1": 20, "JDG-2": 18, "JDG-3": 19, "JDG-4": 19,
    }
    base_res = compute_scores(base_map)
    max_pillar_id = base_res["max_pillar"]["pillar"]
    for sub_id in ALL_SUBDIMENSIONS:
        bumped = dict(base_map)
        bumped[sub_id] += 1
        b_res = compute_scores(bumped)
        require(
            b_res["sos_latent"] > base_res["sos_latent"],
            f"Non-monotonic latent on {sub_id}",
        )
        if not sub_id.startswith(max_pillar_id + "-"):
            require(
                b_res["sos_effective"] > base_res["sos_effective"],
                f"Non-monotonic effective on non-max pillar sub-dimension {sub_id}",
            )
        checks += 1

    # 4. RULE-TIER-CAP: high CTX/CRE/JDG (96 each) with AIO = 48 (< 50) must cap at Level 2
    aio_capped_map = {k: 24 for k in ALL_SUBDIMENSIONS}
    for k in ("AIO-1", "AIO-2", "AIO-3", "AIO-4"):
        aio_capped_map[k] = 12  # AIO = 48
    cap_res = compute_scores(aio_capped_map)
    require(cap_res["sos_effective"] >= 60.0, "Expected raw effective >= 60")
    require(cap_res["tier_capped"] is True, "Expected RULE-TIER-CAP to trigger on AIO=48")
    require(cap_res["effective_tier_level"] == 2, f"Expected Level 2 cap, got {cap_res['effective_tier_level']}")
    checks += 1

    # 5. RULE-TIER-CAP: all pillars >= 75, but CRE-3 = 12 (< 13) must cap at Level 2
    cre3_capped_map = {k: 22 for k in ALL_SUBDIMENSIONS}
    cre3_capped_map["CRE-1"] = 25
    cre3_capped_map["CRE-2"] = 25
    cre3_capped_map["CRE-3"] = 12
    cre3_capped_map["CRE-4"] = 25
    cre3_res = compute_scores(cre3_capped_map)
    require(cre3_res["sos_effective"] >= 80.0, "Expected raw effective >= 80")
    require(cre3_res["tier_capped"] is True, "Expected RULE-TIER-CAP to trigger on CRE-3=12")
    require(cre3_res["effective_tier_level"] == 2, f"Expected Level 2 cap on CRE-3=12, got {cre3_res['effective_tier_level']}")
    checks += 1

    return checks


def check_negative_cases(sample_record: dict[str, Any]) -> int:
    mutations: list[tuple[str, Any]] = [
        ("missing subdimension AIO-1", lambda r: r["subdimensions"].pop("AIO-1")),
        ("unknown subdimension AIO-5", lambda r: r["subdimensions"].update({"AIO-5": deepcopy(r["subdimensions"]["AIO-1"])})),
        ("negative subdimension score", lambda r: r["subdimensions"]["AIO-1"].update(score=-1)),
        ("subdimension score > 25", lambda r: r["subdimensions"]["CTX-3"].update(score=25.1)),
        ("boolean subdimension score", lambda r: r["subdimensions"]["JDG-1"].update(score=True)),
        ("invalid evidence_kind", lambda r: r["subdimensions"]["CRE-1"].update(evidence_kind="rumor")),
        ("empty source locator", lambda r: r["subdimensions"]["CRE-2"].update(locator="   ")),
        ("empty rationale", lambda r: r["subdimensions"]["JDG-4"].update(rationale="")),
        ("unsupported schema", lambda r: r.update(schema="sos-evaluation/99.0")),
        ("unsupported standard_version", lambda r: r.update(standard_version="9.9.9")),
        ("invalid evaluation_scope", lambda r: r.update(evaluation_scope="hybrid_unknown")),
        ("missing target_system.name", lambda r: r["target_system"].update(name="")),
        ("tampered pillar total", lambda r: r["summary"]["pillar_totals"].update(AIO=99)),
        ("tampered sos_latent", lambda r: r["summary"].update(sos_latent=99.99)),
        ("tampered bbf", lambda r: r["summary"].update(bbf=0.9999)),
        ("tampered sos_effective", lambda r: r["summary"].update(sos_effective=88.88)),
        ("forged uncapped tier ID", lambda r: r["summary"].update(effective_tier_id="Level 5")),
        ("invalid SFE code in scenario", lambda r: r["scenarios"]["SCN-1"].update(sfe_events=["SFE-BOGUS"])),
    ]

    for label, mutate in mutations:
        candidate = deepcopy(sample_record)
        mutate(candidate)
        expect_rejected(lambda: validate_evaluation_record(candidate, canonical_std_path=DOCUMENT), label)

    expect_rejected(lambda: decode_strict_json('{"a": 1, "a": 2}'), "duplicate JSON key")
    expect_rejected(lambda: decode_strict_json('{"a": NaN}'), "NaN constant in JSON")
    return len(mutations) + 2


def main() -> int:
    doc_stats = validate_markdown_document(DOCUMENT)
    math_checks = check_mathematical_invariants()

    bundle = decode_strict_json(MAGICLAB_FIXTURE.read_text(encoding="utf-8"))
    native_rec = bundle["evaluations"]["native"]
    coupled_rec = bundle["evaluations"]["coupled"]

    val_native = validate_evaluation_record(native_rec, canonical_std_path=DOCUMENT)
    val_coupled = validate_evaluation_record(coupled_rec, canonical_std_path=DOCUMENT)
    require(val_native["computed"]["sos_effective"] == 33.93, "Native Magic Lab score drift")
    require(val_coupled["computed"]["sos_effective"] == 57.06, "Coupled Magic Lab score drift")

    neg_checks = check_negative_cases(native_rec)

    traces_bundle = decode_strict_json(TRACES_FIXTURE.read_text(encoding="utf-8"))["traces"]
    sovereign_audit = audit_suite_traces(traces_bundle["post_screen_sovereign_reference"])
    require(sovereign_audit["screen_fallback_rate_sfr"] == 0.0, "Sovereign reference trace must have SFR == 0.0")
    require(sovereign_audit["passed_scenarios"] == 5, "Sovereign reference trace must pass all 5 scenarios")

    failure_audit = audit_suite_traces(traces_bundle["screen_tethered_failure_showcase"])
    require(failure_audit["screen_fallback_rate_sfr"] == 1.0, "Failure showcase trace must have SFR == 1.0")
    require(all(failure_audit["sfe_counts_by_code"][c] >= 1 for c in SFE_CODES), "All 4 SFE codes must be exercised")

    # Run unittest suite
    test_run = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "tests"), "-v"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    require(test_run.returncode == 0, f"Unittest suite failed:\n{test_run.stdout}\n{test_run.stderr}")
    m = re.search(r"Ran (\d+) tests?", test_run.stderr)
    unit_count = int(m.group(1)) if m else 0

    summary = {
        "status": "passed",
        "standard": doc_stats,
        "mathematical_invariant_checks": math_checks,
        "negative_rejection_checks": neg_checks,
        "magiclab_native_effective": val_native["computed"]["sos_effective"],
        "magiclab_coupled_effective": val_coupled["computed"]["sos_effective"],
        "sfe_trace_suites_verified": 2,
        "unit_tests_passed": unit_count,
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
