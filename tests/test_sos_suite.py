"""Comprehensive unit and integration test suite for the SOS-1.0 Standard testing tools."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sos_badges import LEVEL_BADGE_SPECS, render_level_badge_svg, validate_badge_svg
from sos_engine import (
    ALL_SUBDIMENSIONS,
    SOSEngineError,
    compute_scores,
    compute_upgrade_sensitivity,
    decode_strict_json,
    render_markdown_report,
    rubric_band,
    validate_evaluation_record,
)
from sos_repo_probe import probe_repository
from sos_sfe_harness import audit_scenario_trace, audit_suite_traces, detect_turn_sfes
from validate_standard import validate_markdown_document


class TestSOSEngine(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture_path = ROOT / "fixtures" / "magiclab_sos_evaluation.json"
        self.bundle = decode_strict_json(self.fixture_path.read_text(encoding="utf-8"))
        self.native_rec = self.bundle["evaluations"]["native"]
        self.coupled_rec = self.bundle["evaluations"]["coupled"]

    def test_standard_document_conformance(self) -> None:
        stats = validate_markdown_document(ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md")
        self.assertEqual(stats["subdimensions_verified"], 16)
        self.assertEqual(stats["frontier_horizons_verified"], 4)
        self.assertEqual(stats["tiers_verified"], 9)
        self.assertEqual(stats["rules_verified"], 5)
        self.assertGreaterEqual(stats["sections_verified"], 15)

    def test_magiclab_native_and_coupled_scores(self) -> None:
        val_native = validate_evaluation_record(
            self.native_rec,
            canonical_std_path=ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md",
        )
        self.assertEqual(
            val_native["computed"]["pillar_totals"],
            {"AIO": 18, "CTX": 74, "CRE": 72, "JDG": 82},
        )
        self.assertEqual(val_native["computed"]["sos_latent"], 61.50)
        self.assertEqual(val_native["computed"]["bbf"], 0.5517)
        self.assertEqual(val_native["computed"]["sos_effective"], 33.93)
        self.assertEqual(val_native["computed"]["effective_tier_id"], "Level 1")
        self.assertIsNone(val_native["computed"]["score_ceiling"])
        self.assertEqual(val_native["computed"]["badge_svg"], "badges/level-1-assisted-screen-scribe.svg")

        val_coupled = validate_evaluation_record(
            self.coupled_rec,
            canonical_std_path=ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md",
        )
        self.assertEqual(
            val_coupled["computed"]["pillar_totals"],
            {"AIO": 46, "CTX": 86, "CRE": 83, "JDG": 90},
        )
        self.assertEqual(val_coupled["computed"]["sos_latent"], 76.25)
        self.assertEqual(val_coupled["computed"]["bbf"], 0.7483)
        self.assertEqual(val_coupled["computed"]["sos_effective"], 57.06)
        self.assertEqual(val_coupled["computed"]["effective_tier_id"], "Level 2")
        self.assertEqual(val_coupled["computed"]["badge_svg"], "badges/level-2-headless-cognitive-engine.svg")

    def test_unbounded_frontier_horizons_levels_6_7_8(self) -> None:
        base_sovereign = {sub_id: 25 for sub_id in ALL_SUBDIMENSIONS}

        # Level 6: Autonomous Value Accrual Sovereign
        res_l6 = compute_scores(
            base_sovereign,
            frontier_horizons={"VAL": 30, "ROB": 0, "WET": 0, "MAT": 0},
        )
        self.assertEqual(res_l6["sos_effective"], 130.0)
        self.assertEqual(res_l6["effective_tier_level"], 6)
        self.assertEqual(res_l6["badge_svg"], "badges/level-6-autonomous-value-accrual-sovereign.svg")

        # Level 7: Robotic & Wet-Lab Development Sovereign
        res_l7 = compute_scores(
            base_sovereign,
            frontier_horizons={"VAL": 35, "ROB": 30, "WET": 25, "MAT": 0},
        )
        self.assertEqual(res_l7["sos_effective"], 190.0)
        self.assertEqual(res_l7["effective_tier_level"], 7)
        self.assertEqual(res_l7["badge_svg"], "badges/level-7-robotic-wetlab-sovereign.svg")

        # Level 8: Unbounded Matter & Reality Foundry ([220, inf) with no ceiling)
        open_sub = {sub_id: 40 for sub_id in ALL_SUBDIMENSIONS}  # 160 per pillar
        res_l8 = compute_scores(
            open_sub,
            frontier_horizons={"VAL": 120, "ROB": 150, "WET": 140, "MAT": 180},
        )
        self.assertEqual(res_l8["sos_effective"], 750.0)
        self.assertEqual(res_l8["effective_tier_level"], 8)
        self.assertEqual(res_l8["badge_svg"], "badges/level-8-unbounded-matter-reality-foundry.svg")

    def test_custom_design_badges_for_all_nine_levels(self) -> None:
        self.assertEqual(len(LEVEL_BADGE_SPECS), 9)
        for spec in LEVEL_BADGE_SPECS:
            svg = render_level_badge_svg(spec["level"])
            meta = validate_badge_svg(svg, expected_level=spec["level"])
            self.assertTrue(meta["valid"])
            self.assertGreater(meta["byte_length"], 500)

    def test_rule_tier_cap_enforced_when_aio_below_50(self) -> None:
        scores = {sub_id: 24 for sub_id in ALL_SUBDIMENSIONS}
        for aio_sub in ("AIO-1", "AIO-2", "AIO-3", "AIO-4"):
            scores[aio_sub] = 12  # AIO = 48 < 50
        res = compute_scores(scores)
        self.assertGreaterEqual(res["sos_effective"], 60.0)
        self.assertTrue(res["tier_capped"])
        self.assertEqual(res["effective_tier_level"], 2)
        self.assertTrue(any("RULE-TIER-CAP: AIO" in r for r in res["cap_reasons"]))

    def test_rule_tier_cap_enforced_when_cre3_below_13(self) -> None:
        scores = {sub_id: 22 for sub_id in ALL_SUBDIMENSIONS}
        scores["CRE-1"] = 25
        scores["CRE-2"] = 25
        scores["CRE-3"] = 12  # CRE-3 < 13
        scores["CRE-4"] = 25
        res = compute_scores(scores)
        self.assertGreaterEqual(res["sos_effective"], 80.0)
        self.assertTrue(res["tier_capped"])
        self.assertEqual(res["effective_tier_level"], 2)
        self.assertTrue(any("RULE-TIER-CAP: CRE-3" in r for r in res["cap_reasons"]))

    def test_rubric_bands_including_open_ended_above_25(self) -> None:
        self.assertIn("0-5", rubric_band(0))
        self.assertIn("0-5", rubric_band(5))
        self.assertIn("6-12", rubric_band(6))
        self.assertIn("13-19", rubric_band(13))
        self.assertIn("20-25", rubric_band(20))
        self.assertIn("20-25", rubric_band(25))
        self.assertIn("25+ (Open-Ended Frontier Mastery)", rubric_band(42.5))

    def test_upgrade_sensitivity_identifies_aio_bottleneck(self) -> None:
        raw_scores = {
            sub_id: self.native_rec["subdimensions"][sub_id]["score"]
            for sub_id in ALL_SUBDIMENSIONS
        }
        sens = compute_upgrade_sensitivity(raw_scores)
        self.assertEqual(sens["bottleneck_pillar"]["pillar"], "AIO")
        top_four_pillars = {
            item["pillar"] for item in sens["ranked_subdimension_levers"][:4]
        }
        self.assertEqual(top_four_pillars, {"AIO"})

    def test_markdown_report_rendering(self) -> None:
        md = render_markdown_report(self.native_rec)
        self.assertIn("# SOS-1.0 Evaluation Report: Magic Lab (Native Repository Scope)", md)
        self.assertIn("`33.93 / ∞`", md)
        self.assertIn("`Level 1: Assisted Screen Scribe`", md)
        self.assertIn("badges/level-1-assisted-screen-scribe.svg", md)

    def test_rule_seq_01_rejects_missing_standard_file(self) -> None:
        with self.assertRaises(SOSEngineError) as ctx:
            validate_evaluation_record(
                self.native_rec,
                canonical_std_path=ROOT / "NON_EXISTENT_STANDARD.md",
            )
        self.assertIn("RULE-SEQ-01", str(ctx.exception))

    def test_strict_json_rejects_duplicates_and_nan(self) -> None:
        with self.assertRaises(SOSEngineError):
            decode_strict_json('{"x": 1, "x": 2}')
        with self.assertRaises(SOSEngineError):
            decode_strict_json('{"x": NaN}')


class TestSOSSFEHarness(unittest.TestCase):
    def setUp(self) -> None:
        traces_path = ROOT / "fixtures" / "sample_sfe_traces.json"
        self.traces = decode_strict_json(traces_path.read_text(encoding="utf-8"))["traces"]

    def test_post_screen_sovereign_reference_passes_all_scenarios(self) -> None:
        report = audit_suite_traces(self.traces["post_screen_sovereign_reference"])
        self.assertEqual(report["passed_scenarios"], 5)
        self.assertEqual(report["screen_fallback_rate_sfr"], 0.0)
        self.assertEqual(report["screen_free_survival_rate_sfsr"], 1.0)

    def test_screen_tethered_failure_showcase_triggers_all_four_sfe_classes(self) -> None:
        report = audit_suite_traces(self.traces["screen_tethered_failure_showcase"])
        self.assertEqual(report["passed_scenarios"], 0)
        self.assertEqual(report["screen_fallback_rate_sfr"], 1.0)
        counts = report["sfe_counts_by_code"]
        self.assertGreaterEqual(counts["SFE-IO"], 1)
        self.assertGreaterEqual(counts["SFE-CTX"], 1)
        self.assertGreaterEqual(counts["SFE-VIS"], 1)
        self.assertGreaterEqual(counts["SFE-JDG"], 1)

    def test_detect_turn_sfes_catches_uninspected_visual_artifact(self) -> None:
        turn = {
            "input_modality": "voice",
            "audible_output": "I created the figure.",
            "created_artifacts": [{"id": "fig1", "kind": "plot"}],
            "claims_completion": False,
        }
        events = detect_turn_sfes(turn)
        self.assertEqual([e["code"] for e in events], ["SFE-VIS"])

    def test_scenario_missing_required_visual_artifact_fails_sfe_vis(self) -> None:
        trace = {
            "turns": [
                {
                    "input_modality": "voice",
                    "audible_output": "I finished the research paper verbally without generating a manuscript.",
                    "created_artifacts": [],
                    "claims_completion": True,
                    "independent_judgment": {
                        "verdict": "celebrate",
                        "evidence_digests": 2,
                        "simulated_only": False,
                    },
                }
            ]
        }
        res = audit_scenario_trace("SCN-1", trace)
        self.assertFalse(res["screen_free_pass"])
        self.assertIn("SFE-VIS", res["sfe_codes"])


class TestSOSRepoProbeAndCLI(unittest.TestCase):
    def test_probe_synthetic_repository(self) -> None:
        with TemporaryDirectory(prefix="sos-probe-test-") as tmp:
            tmp_root = Path(tmp)
            scripts_dir = tmp_root / "scripts"
            scripts_dir.mkdir()
            (scripts_dir / "engine.py").write_text(
                "class JudgeExecutor:\n"
                "    MIN_EVIDENCE_DIGESTS = 2\n"
                "    def run(self):\n"
                "        return 'StaleSourceError'\n",
                encoding="utf-8",
            )
            record = probe_repository(
                tmp_root,
                canonical_std_path=ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md",
            )
            self.assertEqual(record["schema"], "sos-evaluation/1.0")
            self.assertEqual(record["evaluation_scope"], "native")
            self.assertGreater(record["subdimensions"]["JDG-1"]["score"], 6)
            self.assertIn("scripts/engine.py:", record["subdimensions"]["JDG-1"]["locator"])

    def test_cli_entrypoints(self) -> None:
        res_val = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "sos_engine.py"),
                "validate",
                str(ROOT / "fixtures" / "magiclab_sos_evaluation.json"),
                "--standard",
                str(ROOT / "SCREEN_OBSOLESCENCE_SCORE_STANDARD.md"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertEqual(res_val.returncode, 0, res_val.stderr)
        payload = json.loads(res_val.stdout)
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["validated_count"], 2)


if __name__ == "__main__":
    unittest.main()
