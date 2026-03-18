"""Conformance tests using official A2UI v0.9 test cases.

These test cases are downloaded from:
https://github.com/google/A2UI/tree/main/specification/v0_9/test/cases

They validate that py-a2ui can parse valid wire-format data and that
the envelope structure matches the official spec.
"""

import json
from pathlib import Path

import pytest
from pydantic import TypeAdapter, ValidationError

from py_a2ui.components import AnyComponent

CASES_DIR = Path(__file__).parent / "cases"

# Map of component type names to their py-a2ui models
_component_adapter = TypeAdapter(AnyComponent)


def _load_json_tests(filename: str) -> list[dict]:
    """Load test cases from a JSON test file."""
    path = CASES_DIR / filename
    data = json.loads(path.read_text())
    return data["tests"]


def _load_jsonl_messages(filename: str) -> list[dict]:
    """Load messages from a JSONL file."""
    path = CASES_DIR / filename
    return [json.loads(line) for line in path.read_text().strip().splitlines()]


def _extract_components(data: dict) -> list[dict]:
    """Extract component dicts from a wire-format message."""
    uc = data.get("updateComponents")
    if uc and "components" in uc:
        return uc["components"]
    return []


# --------------------------------------------------------------------------
# Envelope structure tests
# --------------------------------------------------------------------------


class TestEnvelopeFormat:
    """Verify wire-format envelope uses type-as-key, not a type field."""

    def test_contact_form_lifecycle(self):
        """Full lifecycle JSONL uses correct envelope format."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        assert len(messages) == 4

        # createSurface
        assert "createSurface" in messages[0]
        assert "type" not in messages[0]
        assert messages[0]["version"] == "v0.9"

        # updateComponents
        assert "updateComponents" in messages[1]
        assert "type" not in messages[1]

        # updateDataModel
        assert "updateDataModel" in messages[2]
        assert "type" not in messages[2]

        # deleteSurface
        assert "deleteSurface" in messages[3]
        assert "type" not in messages[3]

    def test_create_surface_structure(self):
        """createSurface has surfaceId and catalogId nested under key."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        cs = messages[0]["createSurface"]
        assert "surfaceId" in cs
        assert "catalogId" in cs

    def test_update_components_structure(self):
        """updateComponents has surfaceId and components nested under key."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        uc = messages[1]["updateComponents"]
        assert "surfaceId" in uc
        assert "components" in uc
        assert len(uc["components"]) > 0

    def test_update_data_model_structure(self):
        """updateDataModel has surfaceId, path, value nested under key."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        udm = messages[2]["updateDataModel"]
        assert "surfaceId" in udm
        assert "path" in udm
        assert "value" in udm

    def test_delete_surface_structure(self):
        """deleteSurface has surfaceId nested under key."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        ds = messages[3]["deleteSurface"]
        assert "surfaceId" in ds


# --------------------------------------------------------------------------
# Component parsing tests — valid cases
# --------------------------------------------------------------------------


def _valid_component_cases() -> list[tuple[str, str, dict]]:
    """Collect all valid test cases that contain components."""
    cases = []
    for filename in sorted(CASES_DIR.glob("*.json")):
        data = json.loads(filename.read_text())
        for test in data.get("tests", []):
            if not test.get("valid", False):
                continue
            components = _extract_components(test["data"])
            for comp in components:
                cases.append((filename.stem, test["description"], comp))
    return cases


_VALID_CASES = _valid_component_cases()


@pytest.mark.parametrize(
    ("source", "description", "comp_data"),
    _VALID_CASES,
    ids=[f"{s}::{d}::{c.get('id', '?')}" for s, d, c in _VALID_CASES],
)
def test_parse_valid_component(source: str, description: str, comp_data: dict):
    """Valid component data from official test cases should parse through py-a2ui."""
    parsed = _component_adapter.validate_python(comp_data)
    assert parsed.component == comp_data["component"]
    assert parsed.id == comp_data["id"]


# --------------------------------------------------------------------------
# Component rejection tests — invalid cases
# --------------------------------------------------------------------------

# Some invalid cases test JSON Schema constraints that Pydantic doesn't enforce
# (e.g., additionalProperties:false, deprecated fields). We skip those and focus
# on cases where py-a2ui should also reject the data.
_PYDANTIC_REJECTABLE = {
    "Text with invalid variant (should fail)",
    "Tabs with empty tabs array (should fail)",
}


def _invalid_component_cases() -> list[tuple[str, str, list[dict]]]:
    """Collect invalid test cases that Pydantic should reject."""
    cases = []
    for filename in sorted(CASES_DIR.glob("*.json")):
        data = json.loads(filename.read_text())
        for test in data.get("tests", []):
            if test.get("valid", True):
                continue
            if test["description"] not in _PYDANTIC_REJECTABLE:
                continue
            components = _extract_components(test["data"])
            if components:
                cases.append((filename.stem, test["description"], components))
    return cases


_INVALID_CASES = _invalid_component_cases()


@pytest.mark.parametrize(
    ("source", "description", "comp_list"),
    _INVALID_CASES,
    ids=[f"{s}::{d}" for s, d, _ in _INVALID_CASES],
)
def test_reject_invalid_components(source: str, description: str, comp_list: list[dict]):
    """Invalid component data from official test cases should be rejected by py-a2ui."""
    with pytest.raises(ValidationError):
        for comp in comp_list:
            _component_adapter.validate_python(comp)


# --------------------------------------------------------------------------
# Contact form lifecycle test
# --------------------------------------------------------------------------


class TestContactFormLifecycle:
    """Parse the full contact_form_example.jsonl through py-a2ui models."""

    def test_all_components_parseable(self):
        """Every component in the contact form example should parse."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        uc = messages[1]["updateComponents"]
        components = uc["components"]
        assert len(components) > 20  # contact form has ~28 components

        for comp_data in components:
            parsed = _component_adapter.validate_python(comp_data)
            assert parsed.component == comp_data["component"]

    def test_component_types_present(self):
        """Contact form uses diverse component types."""
        messages = _load_jsonl_messages("contact_form_example.jsonl")
        components = messages[1]["updateComponents"]["components"]
        types = {c["component"] for c in components}
        expected = {
            "Card",
            "Column",
            "Row",
            "Text",
            "TextField",
            "Button",
            "Icon",
            "CheckBox",
            "ChoicePicker",
            "Divider",
        }
        assert types >= expected
