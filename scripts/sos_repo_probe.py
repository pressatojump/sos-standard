#!/usr/bin/env python3
"""Automated Repository & Architecture Probe for SOS-1.0.

Scans a target repository across the 16 sub-dimensions of SOS-1.0 using
deterministic lexical and structural evidence rules, recording concrete
file:line source locators (RULE-EVID-03) and emitting a schema-valid
sos-evaluation/1.0 JSON record.

Python 3.11 stdlib only; deterministic; no network.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
import json
from typing import Any

from sos_engine import (
    ALL_SUBDIMENSIONS,
    SCHEMA_VERSION,
    STANDARD_VERSION,
    SUBDIMENSION_TITLES,
    compute_scores,
    validate_evaluation_record,
)

__all__ = [
    "PROBE_RULES",
    "probe_repository",
]

_IGNORED_DIRS: frozenset[str] = frozenset(
    {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "dist",
        "build",
        ".claude",
        ".codex",
        ".astra",
        ".research",
        ".blade",
        ".wrangler",
        ".shortbreath",
        ".work",
        "work",
        "archive",
    }
)

_SCANNABLE_SUFFIXES: frozenset[str] = frozenset(
    {".py", ".md", ".js", ".ts", ".tsx", ".rs", ".go", ".swift"}
)

# Deterministic structural signals for each of the 16 sub-dimensions.
# Each tuple is: (base_score, max_score, points_per_hit, regex_pattern, description)
PROBE_RULES: dict[str, tuple[int, int, int, re.Pattern[str], str]] = {
    "AIO-1": (
        2,
        25,
        4,
        re.compile(r"\b(?:speech_to_text|whisper|microphone|barge_in|audio_input|voice_stream)\b", re.I),
        "Live speech-to-text, microphone capture, or full-duplex voice ingress",
    ),
    "AIO-2": (
        4,
        25,
        3,
        re.compile(r"\b(?:accessible_equivalent|tts|text_to_speech|audio_summary|spoken_brief|operator_report)\b", re.I),
        "2D-to-1D semantic transduction or accessible summary projection",
    ),
    "AIO-3": (
        2,
        25,
        3,
        re.compile(r"\b(?:CADENCE_PHASES|earcon|sonif|paired_preview|bounded_continuation|audio_zoom)\b"),
        "Progressive multi-resolution navigation or cadence/sonification timing",
    ),
    "AIO-4": (
        3,
        25,
        3,
        re.compile(r"\b(?:autonomy_supervisor|voice_bootstrap|daemon|uncle|service_install)\b", re.I),
        "Headless daemon supervision and lifecycle control",
    ),
    "CTX-1": (
        6,
        25,
        3,
        re.compile(r"\b(?:IntentProfile|memory_upkeep|CultivationArchive|self_memory|Uncle)\b"),
        "Passive cross-session profile, memory upkeep, and ambient workspace tracking",
    ),
    "CTX-2": (
        6,
        25,
        3,
        re.compile(r"\b(?:match_methods|retrieve_structural_analogies|embedding_retrieve|source_discovery|semantic_index)\b"),
        "Active multi-source epistemic retrieval and analogy matching",
    ),
    "CTX-3": (
        6,
        25,
        3,
        re.compile(r"\b(?:StaleSourceError|suspend_on_retraction|revoke_and_propagate|dirty_closure|SKILL_VERSION)\b"),
        "Cryptographic provenance, dirty-closure invalidation, and stale-source rejection",
    ),
    "CTX-4": (
        6,
        25,
        2,
        re.compile(r"\b(?:FORBIDDEN_WITHHOLD|planner_packet|acquire_context|ContextManager)\b"),
        "Automatic context packet assembly and zero-withhold worker handoffs",
    ),
    "CRE-1": (
        5,
        25,
        3,
        re.compile(r"\b(?:REQUIRED_SURFACES|pdf_company_pipeline|academic_report|enterprise_report|argument_notebook)\b"),
        "End-to-end PDF, manuscript, and formal report synthesis pipelines",
    ),
    "CRE-2": (
        5,
        25,
        3,
        re.compile(r"\b(?:generate_drawing|FRONT_BALLOON_PARTS|CLASS_ROW_COUNTS|causal_frontier|base_scene)\b"),
        "Vector engineering drawings, 3D/orthographic scenes, and PBR/CAD asset pipelines",
    ),
    "CRE-3": (
        4,
        25,
        3,
        re.compile(r"\b(?:cu007_screen_capture|cu009_screen_ocr|collision_report|GuiAgent|duo_consensus)\b"),
        "Machine-side screen capture, OCR, collision verification, and multi-brief UI consensus",
    ),
    "CRE-4": (
        5,
        25,
        3,
        re.compile(r"\b(?:front_facts|sj1_bom|reproduction_capsule|check_pdf_pipeline)\b"),
        "Cross-modal binding between specs, BOMs, geometry, figures, and packages",
    ),
    "JDG-1": (
        6,
        25,
        3,
        re.compile(r"\b(?:JudgeExecutor|MIN_EVIDENCE_DIGESTS|adversarial_checks|JUDGE_ACCEPTANCE|forced_abstain)\b"),
        "Independent adversarial judge execution, minimum evidence digests, and abstention law",
    ),
    "JDG-2": (
        5,
        25,
        3,
        re.compile(r"\b(?:DesignGatesError|evaluate_pack|FIXED_RULES|kappa_strong|chartjunk)\b", re.I),
        "Binary craft/aesthetic quality gates (G9) and multi-proposer design consensus",
    ),
    "JDG-3": (
        5,
        25,
        3,
        re.compile(r"\b(?:PHASE_ORDER|AttemptStore|EvaluationCustody|WORLD_FEATURE_MODULES|supervise)\b"),
        "Multi-phase RSI controller, generation-fenced worker supervision, and self-healing",
    ),
    "JDG-4": (
        5,
        25,
        3,
        re.compile(r"\b(?:ApprovalTiers|FOUR_EYES|AuthorityRequiredError|dispatch_authority_gate|injection_law)\b"),
        "Tiered spend/action approval gates, four-eyes verification, and authority separation",
    ),
}


def _iter_repo_files(root: Path, max_files: int = 600) -> list[Path]:
    found: list[Path] = []
    # Prioritize scripts/, references/, and top-level docs for deterministic scanning
    priority_roots = [
        root / "scripts",
        root / "references",
        root / "continuous",
        root,
    ]
    seen: set[Path] = set()

    for base in priority_roots:
        if not base.exists():
            continue
        candidates = [base] if base.is_file() else sorted(base.rglob("*"))
        for path in candidates:
            if len(found) >= max_files:
                return found
            if not path.is_file() or path in seen:
                continue
            rel_parts = path.relative_to(root).parts
            if any(part in _IGNORED_DIRS for part in rel_parts):
                continue
            if path.suffix not in _SCANNABLE_SUFFIXES:
                continue
            try:
                if path.stat().st_size > 512 * 1024:
                    continue
            except OSError:
                continue
            seen.add(path)
            found.append(path)
    return found


def _git_head(root: Path) -> str:
    try:
        res = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "unknown"


def probe_repository(
    repo_root: Path,
    *,
    canonical_std_path: Path | None = None,
) -> dict[str, Any]:
    """Scan repo_root and return a validated SOS-1.0 native evaluation record."""
    root = Path(repo_root).resolve()
    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {root}")

    files = _iter_repo_files(root)
    hits_by_sub: dict[str, list[str]] = {sub_id: [] for sub_id in ALL_SUBDIMENSIONS}

    for file_path in files:
        try:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = str(file_path.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), start=1):
            for sub_id, (_, _, _, pattern, _) in PROBE_RULES.items():
                if len(hits_by_sub[sub_id]) >= 8:
                    continue
                if pattern.search(line):
                    locator = f"{rel}:{line_no}"
                    if not any(h.startswith(rel + ":") for h in hits_by_sub[sub_id]):
                        hits_by_sub[sub_id].append(locator)

    subdimensions: dict[str, dict[str, Any]] = {}
    raw_scores: dict[str, float] = {}

    for sub_id in ALL_SUBDIMENSIONS:
        base_score, max_score, pts_per_hit, _, desc = PROBE_RULES[sub_id]
        locators = hits_by_sub[sub_id]
        computed_score = min(max_score, base_score + len(locators) * pts_per_hit)
        raw_scores[sub_id] = float(computed_score)
        locator_str = ", ".join(locators[:3]) if locators else f"{root.name} (no matching surface found)"
        subdimensions[sub_id] = {
            "score": computed_score,
            "title": SUBDIMENSION_TITLES[sub_id],
            "evidence_kind": "observation",
            "locator": locator_str,
            "matched_file_count": len(locators),
            "rationale": (
                f"Static repository probe for {desc}: matched {len(locators)} distinct module(s) "
                f"({locator_str})."
            ),
        }

    computed = compute_scores(raw_scores)
    record: dict[str, Any] = {
        "schema": SCHEMA_VERSION,
        "standard_version": STANDARD_VERSION,
        "target_system": {
            "name": root.name,
            "repository": str(root),
            "revision": _git_head(root),
        },
        "evaluation_scope": "native",
        "subdimensions": subdimensions,
        "summary": {
            "pillar_totals": computed["pillar_totals"],
            "sos_latent": computed["sos_latent"],
            "bbf": computed["bbf"],
            "sos_effective": computed["sos_effective"],
            "effective_tier_id": computed["effective_tier_id"],
            "effective_tier": computed["effective_tier"],
        },
    }

    validate_evaluation_record(record, canonical_std_path=canonical_std_path)
    return record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Automated Repository & Architecture Probe for SOS-1.0"
    )
    parser.add_argument("repo", type=Path, help="Path to target repository directory")
    parser.add_argument(
        "--standard",
        type=Path,
        default=None,
        help="Optional path to SCREEN_OBSOLESCENCE_SCORE_STANDARD.md for RULE-SEQ-01 verification",
    )
    args = parser.parse_args(argv)

    record = probe_repository(args.repo, canonical_std_path=args.standard)
    print(json.dumps(record, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
