#!/usr/bin/env python3
"""Academic Metrological SVG & Notation Badge Generator for SOS-1.0 Levels 0..8.

Follows a restrained, institutional IEEE/ISO/SIAM specification aesthetic:
- Archival paper/slate monochrome & muted ink palette (#f8fafc, #e2e8f0, #334155, #0f172a).
- 1.2px orthographic & mathematical schematic glyphs (zero decorative or dramatic ornaments).
- Classical serif & tabular monospace typography.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import sys
from typing import Any, Mapping
import xml.etree.ElementTree as ET


LEVEL_BADGE_SPECS: tuple[dict[str, Any], ...] = (
    {
        "level": 0,
        "id": "Level 0",
        "slug": "level-0-manual-screen-labor",
        "filename": "level-0-manual-screen-labor.svg",
        "name": "Manual Screen Labor",
        "range_label": "0.00 – 19.99",
        "horizon_tag": "DOMAIN H0 · DIRECT 2D VIEWPORT OPERATION",
        "subtitle": "Primary reading, writing, navigation, and verification performed on human screen",
        "ascii_badge": "[SOS-1.0 | Level 0 | 0.00–19.99 | Manual Screen Labor]",
        "ink": "#334155",
        "accent": "#64748b",
        "emblem_id": "cartesian-viewport",
    },
    {
        "level": 1,
        "id": "Level 1",
        "slug": "level-1-assisted-screen-scribe",
        "filename": "level-1-assisted-screen-scribe.svg",
        "name": "Assisted Screen Scribe",
        "range_label": "20.00 – 39.99",
        "horizon_tag": "DOMAIN H0 · ASSISTED TEXT/CODE INSCRIPTION",
        "subtitle": "Model accelerates drafting or code; human remains tethered to CLI, IDE, or viewer",
        "ascii_badge": "[SOS-1.0 | Level 1 | 20.00–39.99 | Assisted Screen Scribe]",
        "ink": "#1e3a5f",
        "accent": "#475569",
        "emblem_id": "baseline-register",
    },
    {
        "level": 2,
        "id": "Level 2",
        "slug": "level-2-headless-cognitive-engine",
        "filename": "level-2-headless-cognitive-engine.svg",
        "name": "Headless Cognitive Engine (Screen-Tethered Boundary)",
        "range_label": "40.00 – 59.99",
        "horizon_tag": "DOMAIN H1 · PARTITIONED INTERNAL COMPUTATION",
        "subtitle": "Substantial internal CTX/CRE/JDG; human screen required for I/O or visual QA",
        "ascii_badge": "[SOS-1.0 | Level 2 | 40.00–59.99 | Headless Cognitive Engine]",
        "ink": "#1e293b",
        "accent": "#334155",
        "emblem_id": "partitioned-dag",
    },
    {
        "level": 3,
        "id": "Level 3",
        "slug": "level-3-supervised-screen-free-delegation",
        "filename": "level-3-supervised-screen-free-delegation.svg",
        "name": "Supervised Screen-Free Delegation",
        "range_label": "60.00 – 79.99",
        "horizon_tag": "DOMAIN H1 · BIDIRECTIONAL 1D ACOUSTIC CHANNEL",
        "subtitle": "Primary interaction via spoken audio; machine manages virtual screens with bounded SFE",
        "ascii_badge": "[SOS-1.0 | Level 3 | 60.00–79.99 | Supervised Screen-Free Delegation]",
        "ink": "#134e4a",
        "accent": "#2d6a64",
        "emblem_id": "harmonic-axis",
    },
    {
        "level": 4,
        "id": "Level 4",
        "slug": "level-4-autonomous-screen-stewardship",
        "filename": "level-4-autonomous-screen-stewardship.svg",
        "name": "Autonomous Screen Stewardship",
        "range_label": "80.00 – 94.99",
        "horizon_tag": "DOMAIN H1 · CLOSED-LOOP VISUAL VERIFICATION",
        "subtitle": "Offscreen rendering verified by machine vision and structural critics prior to report",
        "ascii_badge": "[SOS-1.0 | Level 4 | 80.00–94.99 | Autonomous Screen Stewardship]",
        "ink": "#1e3a5f",
        "accent": "#3b5980",
        "emblem_id": "feedback-loop",
    },
    {
        "level": 5,
        "id": "Level 5",
        "slug": "level-5-post-screen-digital-sovereign",
        "filename": "level-5-post-screen-digital-sovereign.svg",
        "name": "Post-Screen Liberation (Ideation-on-Machine Closure)",
        "range_label": "95.00 – 119.99",
        "horizon_tag": "DOMAIN H1 · COMPLETE IDEATION-ON-MACHINE CLOSURE",
        "subtitle": "Zero human screen dependency across digital ideation, papers, art, code, and verification",
        "ascii_badge": "[SOS-1.0 | Level 5 | 95.00–119.99 | Post-Screen Liberation]",
        "ink": "#0f172a",
        "accent": "#334155",
        "emblem_id": "commutative-square",
    },
    {
        "level": 6,
        "id": "Level 6",
        "slug": "level-6-autonomous-value-accrual-sovereign",
        "filename": "level-6-autonomous-value-accrual-sovereign.svg",
        "name": "Autonomous Value Accrual",
        "range_label": "120.00 – 159.99",
        "horizon_tag": "DOMAIN H2 · ECONOMIC & OPERATIONAL VALUE ACCRUAL (VAL)",
        "subtitle": "Closed-loop execution from machine ideation to deployment and measurable value accrual",
        "ascii_badge": "[SOS-1.0 | Level 6 | 120.00–159.99 | Autonomous Value Accrual]",
        "ink": "#27272a",
        "accent": "#52525b",
        "emblem_id": "utility-integral",
    },
    {
        "level": 7,
        "id": "Level 7",
        "slug": "level-7-robotic-wetlab-sovereign",
        "filename": "level-7-robotic-wetlab-sovereign.svg",
        "name": "Robotic and Wet-Lab Execution",
        "range_label": "160.00 – 219.99",
        "horizon_tag": "DOMAIN H3 · PHYSICAL ACTUATION & EXPERIMENTAL ASSAY (ROB/WET)",
        "subtitle": "Closed-loop sensorimotor robotics, hardware bring-up, and wet-lab protocol execution",
        "ascii_badge": "[SOS-1.0 | Level 7 | 160.00–219.99 | Robotic and Wet-Lab Execution]",
        "ink": "#18181b",
        "accent": "#3f3f46",
        "emblem_id": "orthogonal-triad",
    },
    {
        "level": 8,
        "id": "Level 8",
        "slug": "level-8-unbounded-matter-reality-foundry",
        "filename": "level-8-unbounded-matter-reality-foundry.svg",
        "name": "Open-Ended Material and Physical Synthesis",
        "range_label": "220.00 – ∞",
        "horizon_tag": "DOMAIN H4 · INVERSE MATERIAL DESIGN & SYNTHESIS [220, ∞)",
        "subtitle": "Unbounded horizon: ideation to value accrual, robotics/wet-lab, and material design",
        "ascii_badge": "[SOS-1.0 | Level 8 | 220.00–∞ | Open-Ended Material and Physical Synthesis]",
        "ink": "#090d16",
        "accent": "#1e293b",
        "emblem_id": "unit-cell-ray",
    },
)


def get_badge_spec(level: int) -> dict[str, Any]:
    """Return the badge specification dictionary for a given level (0..8)."""
    for spec in LEVEL_BADGE_SPECS:
        if spec["level"] == level:
            return dict(spec)
    raise ValueError(f"Unknown SOS maturity level: {level}")


def _emblem_svg_group(emblem_id: str, ink: str, accent: str) -> str:
    """Return restrained 1.2px technical schematic line geometry (center=34,34)."""
    # Subtle coordinate reticle common to all technical diagrams
    reticle = (
        f'<line x1="14" y1="34" x2="54" y2="34" stroke="#cbd5e1" stroke-width="0.75"/>'
        f'<line x1="34" y1="14" x2="34" y2="54" stroke="#cbd5e1" stroke-width="0.75"/>'
    )
    if emblem_id == "cartesian-viewport":
        return (
            reticle
            + f"""
        <rect x="18" y="20" width="32" height="24" fill="none" stroke="{ink}" stroke-width="1.25"/>
        <line x1="18" y1="26" x2="50" y2="26" stroke="{accent}" stroke-width="0.9"/>
        <line x1="26" y1="26" x2="26" y2="44" stroke="{accent}" stroke-width="0.9"/>
        <circle cx="38" cy="35" r="2" fill="none" stroke="{ink}" stroke-width="1.2"/>
        """
        )
    if emblem_id == "baseline-register":
        return (
            reticle
            + f"""
        <rect x="19" y="17" width="30" height="34" fill="none" stroke="{ink}" stroke-width="1.25"/>
        <line x1="23" y1="24" x2="45" y2="24" stroke="{ink}" stroke-width="1.2"/>
        <line x1="23" y1="30" x2="41" y2="30" stroke="{accent}" stroke-width="1.1"/>
        <line x1="23" y1="36" x2="45" y2="36" stroke="{accent}" stroke-width="1.1"/>
        <line x1="23" y1="42" x2="36" y2="42" stroke="{accent}" stroke-width="1.1"/>
        """
        )
    if emblem_id == "partitioned-dag":
        return (
            reticle
            + f"""
        <line x1="42" y1="16" x2="42" y2="52" stroke="{accent}" stroke-width="1.1" stroke-dasharray="2.5,2.5"/>
        <circle cx="22" cy="34" r="3" fill="#ffffff" stroke="{ink}" stroke-width="1.25"/>
        <circle cx="33" cy="24" r="3" fill="#ffffff" stroke="{ink}" stroke-width="1.25"/>
        <circle cx="33" cy="44" r="3" fill="#ffffff" stroke="{ink}" stroke-width="1.25"/>
        <line x1="24.5" y1="32" x2="30.5" y2="26" stroke="{ink}" stroke-width="1.15"/>
        <line x1="24.5" y1="36" x2="30.5" y2="42" stroke="{ink}" stroke-width="1.15"/>
        <line x1="33" y1="27" x2="33" y2="41" stroke="{accent}" stroke-width="1"/>
        """
        )
    if emblem_id == "harmonic-axis":
        return (
            reticle
            + f"""
        <path d="M 16 34 C 20 22, 24 22, 28 34 C 32 46, 36 46, 40 34 C 44 22, 48 22, 52 34" fill="none" stroke="{ink}" stroke-width="1.35"/>
        <circle cx="16" cy="34" r="1.6" fill="{ink}"/>
        <circle cx="52" cy="34" r="1.6" fill="{ink}"/>
        """
        )
    if emblem_id == "feedback-loop":
        return (
            reticle
            + f"""
        <rect x="25" y="21" width="18" height="10" fill="#ffffff" stroke="{ink}" stroke-width="1.2"/>
        <rect x="25" y="37" width="18" height="10" fill="#ffffff" stroke="{accent}" stroke-width="1.2"/>
        <path d="M 43 26 L 49 26 L 49 42 L 43 42" fill="none" stroke="{ink}" stroke-width="1.15"/>
        <path d="M 25 42 L 19 42 L 19 26 L 25 26" fill="none" stroke="{ink}" stroke-width="1.15"/>
        """
        )
    if emblem_id == "commutative-square":
        return (
            reticle
            + f"""
        <rect x="21" y="21" width="26" height="26" fill="none" stroke="{ink}" stroke-width="1.25"/>
        <line x1="21" y1="21" x2="47" y2="47" stroke="{accent}" stroke-width="1.05" stroke-dasharray="2,2"/>
        <circle cx="21" cy="21" r="2.2" fill="#ffffff" stroke="{ink}" stroke-width="1.2"/>
        <circle cx="47" cy="21" r="2.2" fill="#ffffff" stroke="{ink}" stroke-width="1.2"/>
        <circle cx="21" cy="47" r="2.2" fill="#ffffff" stroke="{ink}" stroke-width="1.2"/>
        <circle cx="47" cy="47" r="2.2" fill="{ink}"/>
        """
        )
    if emblem_id == "utility-integral":
        return (
            reticle
            + f"""
        <polyline points="18,18 18,48 50,48" fill="none" stroke="{ink}" stroke-width="1.25"/>
        <path d="M 18 46 L 26 46 L 26 39 L 34 39 L 34 30 L 42 30 L 42 21 L 49 21" fill="none" stroke="{ink}" stroke-width="1.3"/>
        <circle cx="49" cy="21" r="1.8" fill="{ink}"/>
        """
        )
    if emblem_id == "orthogonal-triad":
        return (
            reticle
            + f"""
        <line x1="30" y1="36" x2="30" y2="18" stroke="{ink}" stroke-width="1.3"/>
        <line x1="30" y1="36" x2="48" y2="36" stroke="{ink}" stroke-width="1.3"/>
        <line x1="30" y1="36" x2="19" y2="47" stroke="{ink}" stroke-width="1.3"/>
        <circle cx="30" cy="36" r="2" fill="{ink}"/>
        <rect x="36" y="22" width="10" height="10" fill="none" stroke="{accent}" stroke-width="1.15"/>
        """
        )
    # Default / Level 8: unit-cell-ray (isometric cubic unit cell + open ray [0, inf))
    return (
        reticle
        + f"""
    <rect x="19" y="25" width="18" height="18" fill="none" stroke="{ink}" stroke-width="1.2"/>
    <rect x="25" y="19" width="18" height="18" fill="none" stroke="{accent}" stroke-width="1.1"/>
    <line x1="19" y1="25" x2="25" y2="19" stroke="{ink}" stroke-width="1.1"/>
    <line x1="37" y1="25" x2="43" y2="19" stroke="{ink}" stroke-width="1.1"/>
    <line x1="19" y1="43" x2="25" y2="37" stroke="{ink}" stroke-width="1.1"/>
    <line x1="37" y1="43" x2="43" y2="37" stroke="{ink}" stroke-width="1.1"/>
    <line x1="43" y1="28" x2="53" y2="28" stroke="{ink}" stroke-width="1.25"/>
    <polyline points="49.5,25 53,28 49.5,31" fill="none" stroke="{ink}" stroke-width="1.2"/>
    """
    )


def render_level_badge_svg(
    level: int,
    *,
    score_override: float | None = None,
    scope_label: str | None = None,
) -> str:
    """Render an academic specification-plate SVG badge for an SOS-1.0 level or evaluated score."""
    spec = get_badge_spec(level)
    emblem = _emblem_svg_group(spec["emblem_id"], spec["ink"], spec["accent"])

    header_left = (
        f"SOS-STD-1.0 ({scope_label.upper()}) · {spec['horizon_tag']}"
        if scope_label
        else f"SOS-STD-1.0 · {spec['horizon_tag']}"
    )
    metric_label = "MEASURED" if score_override is not None else "INTERVAL"
    pill_text = (
        f"{score_override:.2f} [0, ∞)"
        if score_override is not None
        else f"{spec['range_label']}"
    )
    title_text = f"LEVEL {spec['level']} · {spec['name'].upper()}"
    subtitle_text = spec["subtitle"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="540" height="68" viewBox="0 0 540 68" role="img" aria-label="{escape(title_text)} ({escape(pill_text)})">
  <title>{escape(title_text)} — {escape(pill_text)}</title>
  <rect x="0.5" y="0.5" width="539" height="67" rx="3" fill="#fcfcfd" stroke="#cbd5e1" stroke-width="1"/>
  <rect x="1" y="1" width="66" height="66" fill="#f1f5f9"/>
  <rect x="1" y="1" width="3.5" height="66" fill="{spec['ink']}"/>
  <line x1="67.5" y1="1" x2="67.5" y2="67" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="67.5" y1="24" x2="539" y2="24" stroke="#e2e8f0" stroke-width="1"/>
  <line x1="420" y1="1" x2="420" y2="24" stroke="#e2e8f0" stroke-width="1"/>
  <g id="emblem-{escape(spec['emblem_id'])}">
    {emblem.strip()}
  </g>
  <text x="78" y="16" fill="#475569" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="8.8" font-weight="600" letter-spacing="0.5">{escape(header_left)}</text>
  <text x="480" y="16" fill="{spec['ink']}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="8.8" font-weight="700" text-anchor="middle">{escape(metric_label)}: {escape(pill_text)}</text>
  <text x="78" y="42.5" fill="#0f172a" font-family="Georgia, 'Times New Roman', STIXGeneral, serif" font-size="13.2" font-weight="700" letter-spacing="0.15">{escape(title_text)}</text>
  <text x="78" y="57.5" fill="#475569" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="10.0" font-weight="400">{escape(subtitle_text)}</text>
</svg>
"""
    return svg


def validate_badge_svg(svg_text: str, expected_level: int | None = None) -> dict[str, Any]:
    """Validate that an SVG badge is well-formed XML with required SOS-1.0 visual elements."""
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as exc:
        raise ValueError(f"Malformed SVG XML: {exc}") from exc

    if not root.tag.endswith("svg"):
        raise ValueError(f"Expected <svg> root element, got {root.tag!r}")
    if root.attrib.get("width") != "540" or root.attrib.get("height") != "68":
        raise ValueError("Badge SVG must have width=540 and height=68")

    all_text = " ".join(root.itertext())
    if expected_level is not None:
        spec = get_badge_spec(expected_level)
        expected_title = f"LEVEL {expected_level} · {spec['name'].upper()}"
        if expected_title not in all_text:
            raise ValueError(f"Badge missing expected title {expected_title!r}")

    return {"valid": True, "byte_length": len(svg_text.encode("utf-8"))}


def generate_all_badges(output_dir: Path, evaluation_bundle: Mapping[str, Any] | None = None) -> list[Path]:
    """Write all 9 level badges (and optional system evaluation badges) to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for spec in LEVEL_BADGE_SPECS:
        svg = render_level_badge_svg(spec["level"])
        validate_badge_svg(svg, expected_level=spec["level"])
        target = output_dir / spec["filename"]
        target.write_text(svg, encoding="utf-8")
        written.append(target)

    if evaluation_bundle and "evaluations" in evaluation_bundle:
        evals = evaluation_bundle["evaluations"]
        if isinstance(evals, Mapping):
            for scope_key, rec in evals.items():
                summary = rec.get("summary", {})
                tier_id = str(summary.get("effective_tier_id", "Level 0"))
                level_num = int(tier_id.split()[-1])
                eff_score = float(summary.get("sos_effective", 0.0))
                svg = render_level_badge_svg(
                    level_num,
                    score_override=eff_score,
                    scope_label=str(scope_key),
                )
                validate_badge_svg(svg, expected_level=level_num)
                target = output_dir / f"magiclab-{scope_key}.svg"
                target.write_text(svg, encoding="utf-8")
                written.append(target)

    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate and validate academic metrological SOS-1.0 SVG badges for Levels 0..8"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "badges",
        help="Target directory for generated SVG badges",
    )
    parser.add_argument(
        "--bundle",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "fixtures" / "magiclab_sos_evaluation.json",
        help="Optional evaluation bundle JSON to generate system score badges",
    )
    args = parser.parse_args(argv)

    import json

    bundle_data = None
    if args.bundle and args.bundle.is_file():
        bundle_data = json.loads(args.bundle.read_text(encoding="utf-8"))

    paths = generate_all_badges(args.output_dir, evaluation_bundle=bundle_data)
    print(
        json.dumps(
            {
                "status": "generated",
                "badge_count": len(paths),
                "badges": [str(p.name) for p in paths],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
