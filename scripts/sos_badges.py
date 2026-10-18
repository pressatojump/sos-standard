#!/usr/bin/env python3
"""Custom SVG & ASCII Design Badge Generator and Validator for SOS-1.0 Levels 0..8."""

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
        "horizon_tag": "H0 · HUMAN SCREEN OPERATOR",
        "subtitle": "Primary reading, writing, navigation & QA performed on human screen",
        "ascii_badge": "⟦ L0 ▣ MANUAL SCREEN LABOR · 0–19.99 ⟧",
        "bg_start": "#0f172a",
        "bg_end": "#1e293b",
        "accent": "#94a3b8",
        "accent_bright": "#cbd5e1",
        "emblem_id": "crt-cursor",
    },
    {
        "level": 1,
        "id": "Level 1",
        "slug": "level-1-assisted-screen-scribe",
        "filename": "level-1-assisted-screen-scribe.svg",
        "name": "Assisted Screen Scribe",
        "range_label": "20.00 – 39.99",
        "horizon_tag": "H0 · SCREEN-TETHERED SCRIBE",
        "subtitle": "LLM accelerates drafting/code; human tethered to CLI/IDE/viewer",
        "ascii_badge": "⟦ L1 ✒ ASSISTED SCREEN SCRIBE · 20–39.99 ⟧",
        "bg_start": "#0f172a",
        "bg_end": "#1e3a8a",
        "accent": "#3b82f6",
        "accent_bright": "#93c5fd",
        "emblem_id": "scribe-chevron",
    },
    {
        "level": 2,
        "id": "Level 2",
        "slug": "level-2-headless-cognitive-engine",
        "filename": "level-2-headless-cognitive-engine.svg",
        "name": "Headless Cognitive Engine",
        "range_label": "40.00 – 59.99",
        "horizon_tag": "H1 · TETHERED I/O BOUNDARY",
        "subtitle": "Strong internal CTX/CRE/JDG; human screen required for I/O or QA",
        "ascii_badge": "⟦ L2 ⚙ HEADLESS COGNITIVE ENGINE · 40–59.99 ⟧",
        "bg_start": "#111827",
        "bg_end": "#312e81",
        "accent": "#38bdf8",
        "accent_bright": "#7dd3fc",
        "emblem_id": "neural-bezel",
    },
    {
        "level": 3,
        "id": "Level 3",
        "slug": "level-3-supervised-screen-free-delegation",
        "filename": "level-3-supervised-screen-free-delegation.svg",
        "name": "Supervised Screen-Free Delegation",
        "range_label": "60.00 – 79.99",
        "horizon_tag": "H1 · HANDS-FREE DIGITAL LOOP",
        "subtitle": "Bidirectional audio + LLM virtual screen with occasional SFE",
        "ascii_badge": "⟦ L3 ≋ SUPERVISED SCREEN-FREE · 60–79.99 ⟧",
        "bg_start": "#042f2e",
        "bg_end": "#065f46",
        "accent": "#10b981",
        "accent_bright": "#6ee7b7",
        "emblem_id": "acoustic-wave",
    },
    {
        "level": 4,
        "id": "Level 4",
        "slug": "level-4-autonomous-screen-stewardship",
        "filename": "level-4-autonomous-screen-stewardship.svg",
        "name": "Autonomous Screen Stewardship",
        "range_label": "80.00 – 94.99",
        "horizon_tag": "H1 · LLM-OWNED SCREEN LOOP",
        "subtitle": "Closed-loop vision critics & full-duplex audio across all artifacts",
        "ascii_badge": "⟦ L4 ◉ AUTONOMOUS SCREEN STEWARD · 80–94.99 ⟧",
        "bg_start": "#1e1b4b",
        "bg_end": "#4c1d95",
        "accent": "#a855f7",
        "accent_bright": "#d8b4fe",
        "emblem_id": "vision-iris",
    },
    {
        "level": 5,
        "id": "Level 5",
        "slug": "level-5-post-screen-digital-sovereign",
        "filename": "level-5-post-screen-digital-sovereign.svg",
        "name": "Post-Screen Digital Sovereign",
        "range_label": "95.00 – 119.99",
        "horizon_tag": "H1 · IDEATION-ON-MACHINE CLOSURE",
        "subtitle": "0-nit human screen; 100% autonomous digital papers, art, code & QA",
        "ascii_badge": "⟦ L5 ★ POST-SCREEN DIGITAL SOVEREIGN · 95–119.99 ⟧",
        "bg_start": "#271505",
        "bg_end": "#78350f",
        "accent": "#f59e0b",
        "accent_bright": "#fde68a",
        "emblem_id": "sovereign-star",
    },
    {
        "level": 6,
        "id": "Level 6",
        "slug": "level-6-autonomous-value-accrual-sovereign",
        "filename": "level-6-autonomous-value-accrual-sovereign.svg",
        "name": "Autonomous Value Accrual Sovereign",
        "range_label": "120.00 – 159.99",
        "horizon_tag": "H2 · IDEATION → VALUE ACCRUAL (VAL)",
        "subtitle": "Solves from machine ideation to autonomous deployment & value capture",
        "ascii_badge": "⟦ L6 ◈ VALUE ACCRUAL SOVEREIGN · 120–159.99 ⟧",
        "bg_start": "#2a0808",
        "bg_end": "#7f1d1d",
        "accent": "#fbbf24",
        "accent_bright": "#fef08a",
        "emblem_id": "value-lattice",
    },
    {
        "level": 7,
        "id": "Level 7",
        "slug": "level-7-robotic-wetlab-sovereign",
        "filename": "level-7-robotic-wetlab-sovereign.svg",
        "name": "Robotic & Wet-Lab Sovereign",
        "range_label": "160.00 – 219.99",
        "horizon_tag": "H3 · ROBOTICS & WET-LAB CLOSURE (ROB/WET)",
        "subtitle": "Embodied actuation, mechatronic synthesis & closed-loop wet-lab assays",
        "ascii_badge": "⟦ L7 ⬡ ROBOTIC & WET-LAB SOVEREIGN · 160–219.99 ⟧",
        "bg_start": "#090d16",
        "bg_end": "#164e63",
        "accent": "#22d3ee",
        "accent_bright": "#f472b6",
        "emblem_id": "robotic-wetlab",
    },
    {
        "level": 8,
        "id": "Level 8",
        "slug": "level-8-unbounded-matter-reality-foundry",
        "filename": "level-8-unbounded-matter-reality-foundry.svg",
        "name": "Unbounded Matter & Reality Foundry",
        "range_label": "220.00 – ∞",
        "horizon_tag": "H4 · IDEATION → VALUE → ROB/WET → MATERIAL DESIGN",
        "subtitle": "No upper ceiling [220, ∞): inverse material design & physical synthesis",
        "ascii_badge": "⟦ L8 ∞ UNBOUNDED MATTER & REALITY FOUNDRY · 220–∞ ⟧",
        "bg_start": "#05070e",
        "bg_end": "#3b0764",
        "accent": "#fde047",
        "accent_bright": "#e879f9",
        "emblem_id": "matter-infinity",
    },
)


def get_badge_spec(level: int) -> dict[str, Any]:
    """Return the badge specification dictionary for a given level (0..8)."""
    for spec in LEVEL_BADGE_SPECS:
        if spec["level"] == level:
            return dict(spec)
    raise ValueError(f"Unknown SOS maturity level: {level}")


def _emblem_svg_group(emblem_id: str, accent: str, accent_bright: str) -> str:
    """Return bespoke vector artwork inside the 68x68 left emblem chamber (center=34,34)."""
    if emblem_id == "crt-cursor":
        return f"""
        <rect x="16" y="16" width="36" height="28" rx="3" fill="none" stroke="{accent}" stroke-width="2"/>
        <line x1="20" y1="22" x2="48" y2="22" stroke="{accent}" stroke-width="1" stroke-dasharray="2,2"/>
        <line x1="20" y1="28" x2="48" y2="28" stroke="{accent}" stroke-width="1" stroke-dasharray="2,2"/>
        <line x1="20" y1="34" x2="48" y2="34" stroke="{accent}" stroke-width="1" stroke-dasharray="2,2"/>
        <path d="M26 44 L42 44 M34 44 L34 50 M24 50 L44 50" stroke="{accent}" stroke-width="2" stroke-linecap="round"/>
        <polygon points="31,24 31,37 35,34 38,40 40,39 37,33 42,33" fill="{accent_bright}"/>
        """
    if emblem_id == "scribe-chevron":
        return f"""
        <rect x="15" y="15" width="38" height="38" rx="6" fill="none" stroke="{accent}" stroke-width="1.75"/>
        <path d="M21 27 L28 33 L21 39" fill="none" stroke="{accent_bright}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        <line x1="30" y1="39" x2="37" y2="39" stroke="{accent_bright}" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M45 20 L36 35 L39 38 L48 23 Z" fill="none" stroke="{accent}" stroke-width="1.8"/>
        <circle cx="38" cy="36" r="1.5" fill="{accent_bright}"/>
        """
    if emblem_id == "neural-bezel":
        return f"""
        <rect x="15" y="15" width="38" height="38" rx="5" fill="none" stroke="{accent}" stroke-width="1.6" stroke-dasharray="4,3"/>
        <polygon points="34,20 46,27 46,41 34,48 22,41 22,27" fill="none" stroke="{accent_bright}" stroke-width="1.8"/>
        <circle cx="34" cy="34" r="4.5" fill="{accent_bright}"/>
        <line x1="34" y1="20" x2="34" y2="29.5" stroke="{accent}" stroke-width="1.4"/>
        <line x1="46" y1="27" x2="38" y2="31.5" stroke="{accent}" stroke-width="1.4"/>
        <line x1="22" y1="41" x2="30" y2="36.5" stroke="{accent}" stroke-width="1.4"/>
        """
    if emblem_id == "acoustic-wave":
        return f"""
        <path d="M22 17 L16 17 L16 51 L22 51" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M46 17 L52 17 L52 51 L46 51" fill="none" stroke="{accent}" stroke-width="1.8" stroke-linecap="round"/>
        <path d="M13 34 L20 34 L24 22 L29 46 L34 16 L39 50 L44 25 L48 34 L55 34" fill="none" stroke="{accent_bright}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        """
    if emblem_id == "vision-iris":
        return f"""
        <ellipse cx="34" cy="34" rx="20" ry="12" fill="none" stroke="{accent}" stroke-width="1.8"/>
        <circle cx="34" cy="34" r="8" fill="none" stroke="{accent_bright}" stroke-width="2"/>
        <circle cx="34" cy="34" r="3.5" fill="{accent_bright}"/>
        <ellipse cx="34" cy="34" rx="14" ry="20" fill="none" stroke="{accent}" stroke-width="1.1" stroke-dasharray="3,3"/>
        """
    if emblem_id == "sovereign-star":
        return f"""
        <rect x="17" y="17" width="34" height="34" rx="5" fill="#090d16" stroke="{accent}" stroke-width="1.6"/>
        <polygon points="34,13 37.5,27.5 52,31 37.5,34.5 34,49 30.5,34.5 16,31 30.5,27.5" fill="{accent_bright}"/>
        <circle cx="34" cy="31" r="3.2" fill="#090d16"/>
        """
    if emblem_id == "value-lattice":
        return f"""
        <polygon points="34,14 50,30 34,46 18,30" fill="none" stroke="{accent}" stroke-width="1.8"/>
        <polyline points="18,46 28,36 35,40 48,22" fill="none" stroke="{accent_bright}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>
        <polyline points="41,22 48,22 48,29" fill="none" stroke="{accent_bright}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="28" cy="36" r="2.2" fill="{accent_bright}"/>
        <circle cx="35" cy="40" r="2.2" fill="{accent_bright}"/>
        """
    if emblem_id == "robotic-wetlab":
        return f"""
        <path d="M18 48 L28 48 M23 48 L23 36 L33 24 L43 28" fill="none" stroke="{accent}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>
        <circle cx="23" cy="36" r="2.8" fill="{accent_bright}"/>
        <circle cx="33" cy="24" r="2.8" fill="{accent_bright}"/>
        <path d="M43 24 L48 26 M43 32 L48 30" stroke="{accent_bright}" stroke-width="2" stroke-linecap="round"/>
        <path d="M40 36 L44 36 L49 48 L35 48 Z" fill="none" stroke="{accent_bright}" stroke-width="1.8" stroke-linejoin="round"/>
        <line x1="37" y1="44" x2="47" y2="44" stroke="{accent}" stroke-width="1.5"/>
        """
    # Default / Level 8: matter-infinity (atomic crystal lattice + infinity loop)
    return f"""
    <polygon points="34,13 51,23 51,45 34,55 17,45 17,23" fill="none" stroke="{accent}" stroke-width="1.6"/>
    <line x1="34" y1="13" x2="34" y2="55" stroke="{accent}" stroke-width="1" stroke-opacity="0.55"/>
    <line x1="17" y1="23" x2="51" y2="45" stroke="{accent}" stroke-width="1" stroke-opacity="0.55"/>
    <line x1="51" y1="23" x2="17" y2="45" stroke="{accent}" stroke-width="1" stroke-opacity="0.55"/>
    <path d="M25 34 C20 27, 15 34, 20 41 C25 45, 43 23, 48 27 C53 34, 48 41, 43 34 C38 27, 30 41, 25 34 Z" fill="none" stroke="{accent_bright}" stroke-width="2.4"/>
    <circle cx="34" cy="13" r="2.3" fill="{accent}"/>
    <circle cx="51" cy="23" r="2.3" fill="{accent_bright}"/>
    <circle cx="51" cy="45" r="2.3" fill="{accent}"/>
    <circle cx="34" cy="55" r="2.3" fill="{accent_bright}"/>
    <circle cx="17" cy="45" r="2.3" fill="{accent}"/>
    <circle cx="17" cy="23" r="2.3" fill="{accent_bright}"/>
    """


def render_level_badge_svg(
    level: int,
    *,
    score_override: float | None = None,
    scope_label: str | None = None,
) -> str:
    """Render a custom SVG design badge for an SOS-1.0 level (or evaluated system score)."""
    spec = get_badge_spec(level)
    emblem = _emblem_svg_group(spec["emblem_id"], spec["accent"], spec["accent_bright"])

    header_left = (
        f"SOS-1.0 ({scope_label.upper()}) · {spec['horizon_tag']}"
        if scope_label
        else f"SOS-1.0 STANDARD · {spec['horizon_tag']}"
    )
    pill_text = (
        f"SCORE {score_override:.2f} / ∞"
        if score_override is not None
        else f"SOS {spec['range_label']}"
    )
    title_text = f"LEVEL {spec['level']} · {spec['name'].upper()}"
    subtitle_text = spec["subtitle"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="540" height="68" viewBox="0 0 540 68" role="img" aria-label="{escape(title_text)} ({escape(pill_text)})">
  <title>{escape(title_text)} — {escape(pill_text)}</title>
  <defs>
    <linearGradient id="bg-l{spec['level']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{spec['bg_start']}"/>
      <stop offset="100%" stop-color="{spec['bg_end']}"/>
    </linearGradient>
    <linearGradient id="emblem-l{spec['level']}" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16"/>
      <stop offset="100%" stop-color="{spec['bg_start']}"/>
    </linearGradient>
  </defs>
  <rect x="1" y="1" width="538" height="66" rx="10" fill="url(#bg-l{spec['level']})" stroke="{spec['accent']}" stroke-width="1.5"/>
  <rect x="1" y="1" width="68" height="66" rx="10" fill="url(#emblem-l{spec['level']})"/>
  <line x1="69" y1="2" x2="69" y2="66" stroke="{spec['accent']}" stroke-width="1.2" stroke-opacity="0.65"/>
  <g id="emblem-{escape(spec['emblem_id'])}">
    {emblem.strip()}
  </g>
  <text x="82" y="21" fill="{spec['accent_bright']}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="9.5" font-weight="700" letter-spacing="0.8">{escape(header_left)}</text>
  <rect x="412" y="9" width="116" height="17" rx="8.5" fill="#090d16" fill-opacity="0.72" stroke="{spec['accent']}" stroke-width="1"/>
  <text x="470" y="20.5" fill="{spec['accent_bright']}" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace" font-size="9.5" font-weight="700" text-anchor="middle">{escape(pill_text)}</text>
  <text x="82" y="42" fill="#f8fafc" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="14.5" font-weight="800" letter-spacing="0.3">{escape(title_text)}</text>
  <text x="82" y="57.5" fill="#cbd5e1" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="10.5" font-weight="500">{escape(subtitle_text)}</text>
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
        description="Generate and validate custom SOS-1.0 SVG design badges for Levels 0..8"
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
