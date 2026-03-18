"""Restaurant booking form.

Demonstrates:
- Basic component composition (Column, Card, Text, Button, TextField, DateTimeInput)
- EventAction for form submission
- Validation with required() and length()
- CheckRule for inline validation
- TextVariant and ButtonVariant enums
"""

from py_a2ui import (
    Button,
    Card,
    CheckRule,
    Column,
    DateTimeInput,
    EventAction,
    Text,
    TextField,
    UpdateComponentsMessage,
    length,
    required,
)

msg = UpdateComponentsMessage(
    surface_id="booking",
    components=[
        # -- Layout --
        Column(id="root", children=["header", "card"]),
        Text(id="header", text="Reserve a Table", variant="h1"),
        Card(id="card", child="form"),
        Column(id="form", children=["name_field", "email_field", "date_field", "guests_field", "submit_btn"]),
        # -- Inputs --
        TextField(
            id="name_field",
            label="Full Name",
            checks=[CheckRule(condition=required(), message="Name is required")],
        ),
        TextField(
            id="email_field",
            label="Email",
            checks=[
                CheckRule(condition=required(), message="Email is required"),
                CheckRule(condition=length(min=5, max=100), message="Must be 5-100 characters"),
            ],
        ),
        DateTimeInput(id="date_field", value="", enable_date=True, enable_time=True, label="Date & Time"),
        TextField(id="guests_field", label="Number of guests", variant="number"),
        # -- Actions --
        Button(
            id="submit_btn",
            child="submit_label",
            variant="primary",
            action=EventAction(event_name="submit_booking"),
        ),
        Text(id="submit_label", text="Reserve"),
    ],
)

if __name__ == "__main__":
    print(msg.model_dump_json(by_alias=True, exclude_none=True, indent=2))
