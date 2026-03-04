"""Tests for Emulation Playbook schema and validation."""

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
EP_DIR = REPO_ROOT / "EmulationPlaybooks"
TEMPLATE_PATH = REPO_ROOT / "Templates" / "emulation-playbook-template.json"

REQUIRED_TOP_LEVEL_FIELDS = [
    "id", "title", "description", "author", "date",
    "target_threat_paths", "cfpf_phases", "fraud_types",
    "sectors", "prerequisites", "steps", "expected_outcomes",
]

VALID_CFPF_PHASES = {"P1", "P2", "P3", "P4", "P5"}


class TestEPTemplate:
    def test_template_exists(self) -> None:
        assert TEMPLATE_PATH.exists()

    def test_template_is_valid_json(self) -> None:
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        assert isinstance(data, dict)

    def test_template_has_required_fields(self) -> None:
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        for field in REQUIRED_TOP_LEVEL_FIELDS:
            assert field in data, f"Template missing required field: {field}"

    def test_template_has_steps_array(self) -> None:
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        assert isinstance(data["steps"], list)
        assert len(data["steps"]) >= 1

    def test_template_step_has_required_fields(self) -> None:
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        step = data["steps"][0]
        for field in ["step_number", "cfpf_phase", "title", "action", "expected_result"]:
            assert field in step, f"Step missing required field: {field}"


class TestEPValidation:
    """Test the validator can handle EP files."""

    def test_validate_template_passes(self) -> None:
        from scripts.validate_submission import validate_file
        result = validate_file(TEMPLATE_PATH)
        # Template uses TP-0001 which exists, and DL-0012 which exists
        assert result.passed, f"Template validation failed: {result.errors}"

    def test_validate_invalid_json(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        result = validate_file(bad)
        assert not result.passed

    def test_validate_missing_fields(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        ep = tmp_path / "test.json"
        ep.write_text(json.dumps({"id": "EP-0099"}), encoding="utf-8")
        result = validate_file(ep)
        assert not result.passed
        assert any("Missing" in e for e in result.errors)

    def test_validate_bad_id_prefix(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        data["id"] = "XX-0001"
        ep = tmp_path / "test.json"
        ep.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(ep)
        assert not result.passed

    def test_validate_invalid_cfpf_phase(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        data["cfpf_phases"] = ["P1", "P99"]
        ep = tmp_path / "test.json"
        ep.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(ep)
        assert not result.passed

    def test_validate_empty_steps(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        data["steps"] = []
        ep = tmp_path / "test.json"
        ep.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(ep)
        assert not result.passed

    def test_validate_non_sequential_steps(self, tmp_path: Path) -> None:
        from scripts.validate_submission import validate_file
        data = json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))
        data["steps"][0]["step_number"] = 5
        ep = tmp_path / "test.json"
        ep.write_text(json.dumps(data), encoding="utf-8")
        result = validate_file(ep)
        assert not result.passed


class TestEPFiles:
    """Test all EP files in EmulationPlaybooks/ if directory exists."""

    def _get_ep_files(self) -> list[Path]:
        if not EP_DIR.exists():
            return []
        return sorted(EP_DIR.glob("EP-*.json"))

    def test_all_eps_are_valid_json(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            assert isinstance(data, dict), f"{ep_file.name} is not a JSON object"

    def test_all_eps_have_required_fields(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            for field in REQUIRED_TOP_LEVEL_FIELDS:
                assert field in data, f"{ep_file.name} missing field: {field}"

    def test_all_eps_have_valid_id_format(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            assert data["id"].startswith("EP-"), f"{ep_file.name} id must start with EP-"

    def test_all_eps_reference_existing_tps(self) -> None:
        tp_dir = REPO_ROOT / "ThreatPaths"
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            for tp_id in data.get("target_threat_paths", []):
                matches = list(tp_dir.glob(f"{tp_id}-*.md"))
                assert len(matches) > 0, f"{ep_file.name} references {tp_id} which doesn't exist"

    def test_all_eps_have_valid_cfpf_phases(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            for phase in data.get("cfpf_phases", []):
                assert phase in VALID_CFPF_PHASES, f"{ep_file.name} invalid phase: {phase}"

    def test_all_ep_steps_have_sequential_numbers(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            steps = data.get("steps", [])
            for i, step in enumerate(steps):
                assert step["step_number"] == i + 1, \
                    f"{ep_file.name} step {i} has step_number {step['step_number']}, expected {i + 1}"

    def test_all_ep_steps_have_valid_cfpf_phase(self) -> None:
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            for step in data.get("steps", []):
                assert step["cfpf_phase"] in VALID_CFPF_PHASES, \
                    f"{ep_file.name} step {step['step_number']} invalid phase: {step['cfpf_phase']}"

    def test_all_ep_dl_refs_exist(self) -> None:
        dl_dir = REPO_ROOT / "DetectionLogic"
        for ep_file in self._get_ep_files():
            data = json.loads(ep_file.read_text(encoding="utf-8"))
            for step in data.get("steps", []):
                dl_ref = step.get("detection_rule_ref")
                if dl_ref:
                    matches = list(dl_dir.glob(f"{dl_ref}-*.yml"))
                    assert len(matches) > 0, \
                        f"{ep_file.name} step {step['step_number']} references {dl_ref} which doesn't exist"
