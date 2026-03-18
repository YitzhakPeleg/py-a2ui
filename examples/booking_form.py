"""Restaurant booking form.

Demonstrates:
- Nested component composition (no manual string-ID wiring)
- EventAction for form submission
- Validation with required() and length()
- CheckRule for inline validation
- export_json() for A2UI wire format
- print_tree() for visual debugging
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
        Column(
            id="root",
            children=[
                Text(text="Reserve a Table", variant="h1"),
                Card(
                    child=Column(
                        children=[
                            TextField(
                                label="Full Name",
                                checks=[CheckRule(condition=required(), message="Name is required")],
                            ),
                            TextField(
                                label="Email",
                                checks=[
                                    CheckRule(condition=required(), message="Email is required"),
                                    CheckRule(condition=length(min=5, max=100), message="Must be 5-100 characters"),
                                ],
                            ),
                            DateTimeInput(value="", enable_date=True, enable_time=True, label="Date & Time"),
                            TextField(label="Number of guests", variant="number"),
                            Button(
                                child=Text(text="Reserve"),
                                variant="primary",
                                action=EventAction(event_name="submit_booking"),
                            ),
                        ]
                    )
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    msg.print_tree()
    print()
    print(msg.export_json(indent=2))
