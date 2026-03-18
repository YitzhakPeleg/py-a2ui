"""Test that py-a2ui export() produces the official A2UI v0.9 envelope format."""

import json

from py_a2ui import (
    Button,
    Card,
    CheckBox,
    Column,
    CreateSurfaceMessage,
    DeleteSurfaceMessage,
    EventAction,
    Row,
    Text,
    TextField,
    UpdateComponentsMessage,
    UpdateDataModelMessage,
)


class TestExportMatchesSpec:
    """Verify py-a2ui export() output matches the official A2UI v0.9 wire format."""

    def test_create_surface_envelope(self):
        """createSurface wraps payload under key, no 'type' field."""
        msg = CreateSurfaceMessage(surface_id="contact_form_1", catalog_id="basic")
        data = msg.export()

        assert data["version"] == "v0.9"
        assert "createSurface" in data
        assert "type" not in data
        assert data["createSurface"]["surfaceId"] == "contact_form_1"
        assert data["createSurface"]["catalogId"] == "basic"

    def test_update_components_envelope(self):
        """updateComponents wraps payload under key with flattened components."""
        msg = UpdateComponentsMessage(
            surface_id="test",
            components=[
                Column(
                    id="root",
                    children=[Text(text="Hello", variant="h1")],
                ),
            ],
        )
        data = msg.export()

        assert data["version"] == "v0.9"
        assert "updateComponents" in data
        assert "type" not in data
        payload = data["updateComponents"]
        assert payload["surfaceId"] == "test"
        assert isinstance(payload["components"], list)
        # Components are flattened (string IDs, not nested objects)
        for comp in payload["components"]:
            assert isinstance(comp, dict)
            assert "id" in comp
            assert "component" in comp

    def test_update_data_model_envelope(self):
        """updateDataModel wraps payload under key."""
        msg = UpdateDataModelMessage(
            surface_id="contact_form_1",
            path="/contact",
            value={"firstName": "John", "lastName": "Doe"},
        )
        data = msg.export()

        assert data["version"] == "v0.9"
        assert "updateDataModel" in data
        assert "type" not in data
        payload = data["updateDataModel"]
        assert payload["surfaceId"] == "contact_form_1"
        assert payload["path"] == "/contact"
        assert payload["value"]["firstName"] == "John"

    def test_delete_surface_envelope(self):
        """deleteSurface wraps payload under key."""
        msg = DeleteSurfaceMessage(surface_id="contact_form_1")
        data = msg.export()

        assert data["version"] == "v0.9"
        assert "deleteSurface" in data
        assert "type" not in data
        assert data["deleteSurface"]["surfaceId"] == "contact_form_1"

    def test_export_json_is_valid_json(self):
        """export_json() produces parseable JSON matching export()."""
        msg = CreateSurfaceMessage(surface_id="s1", catalog_id="cat")
        json_str = msg.export_json(indent=2)
        parsed = json.loads(json_str)
        assert parsed == msg.export()

    def test_contact_form_like_output(self):
        """Build a mini contact form and verify structure matches spec examples."""
        msg = UpdateComponentsMessage(
            surface_id="contact_form_1",
            components=[
                Card(
                    id="root",
                    child=Column(
                        children=[
                            Row(
                                children=[
                                    Text(text="Contact Us", variant="h2"),
                                ]
                            ),
                            TextField(id="email_field", label="Email", value={"path": "/contact/email"}),
                            CheckBox(id="newsletter", label="Subscribe", value={"path": "/contact/subscribe"}),
                            Button(
                                id="submit",
                                child=Text(text="Send"),
                                variant="primary",
                                action=EventAction(event_name="submitContactForm"),
                            ),
                        ]
                    ),
                ),
            ],
        )
        data = msg.export()

        # Envelope check
        assert data["version"] == "v0.9"
        assert "updateComponents" in data
        assert "type" not in data

        payload = data["updateComponents"]
        assert payload["surfaceId"] == "contact_form_1"

        comps = payload["components"]
        # All components should be flat dicts with string IDs
        comp_map = {c["id"]: c for c in comps}

        # Root card references its child by string ID
        assert "root" in comp_map
        assert isinstance(comp_map["root"]["child"], str)

        # Button references its text child by string ID
        assert "submit" in comp_map
        assert isinstance(comp_map["submit"]["child"], str)
        assert comp_map["submit"]["variant"] == "primary"
