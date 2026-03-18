"""Multi-step survey with validation.

Demonstrates:
- Tabs container with nested child components
- TextField with various validation functions (required, length, email, regex)
- ChoicePicker with multiple options
- CheckBox for boolean inputs
- Slider for numeric range
- CheckRule for per-field validation
"""

from py_a2ui import (
    Button,
    CheckBox,
    CheckRule,
    ChoiceOption,
    ChoicePicker,
    Column,
    EventAction,
    Slider,
    Tab,
    Tabs,
    Text,
    TextField,
    UpdateComponentsMessage,
    email,
    length,
    regex,
    required,
)

msg = UpdateComponentsMessage(
    surface_id="survey",
    components=[
        Tabs(
            id="survey_tabs",
            tabs=[
                Tab(
                    title="Personal Info",
                    child=Column(
                        children=[
                            TextField(
                                label="Your Name",
                                checks=[
                                    CheckRule(condition=required(), message="Name is required"),
                                    CheckRule(condition=length(min=2, max=50), message="2-50 characters"),
                                ],
                            ),
                            TextField(
                                label="Email Address",
                                checks=[
                                    CheckRule(condition=required(), message="Email is required"),
                                    CheckRule(condition=email(), message="Must be a valid email"),
                                ],
                            ),
                            TextField(
                                label="Phone (optional)",
                                checks=[
                                    CheckRule(
                                        condition=regex(r"^\+?[\d\s\-()]{7,15}$"),
                                        message="Invalid phone format",
                                    ),
                                ],
                            ),
                        ]
                    ),
                ),
                Tab(
                    title="Preferences",
                    child=Column(
                        children=[
                            ChoicePicker(
                                label="Experience Level",
                                options=[
                                    ChoiceOption(label="Beginner", value="beginner"),
                                    ChoiceOption(label="Intermediate", value="intermediate"),
                                    ChoiceOption(label="Advanced", value="advanced"),
                                    ChoiceOption(label="Expert", value="expert"),
                                ],
                                value=[],
                            ),
                            Slider(min=0, max=10, value=5),
                            CheckBox(label="Subscribe to newsletter", value=False),
                        ]
                    ),
                ),
                Tab(
                    title="Feedback",
                    child=Column(
                        children=[
                            TextField(
                                label="Additional feedback",
                                variant="longText",
                                checks=[CheckRule(condition=length(max=500), message="Max 500 characters")],
                            ),
                            Button(
                                child=Text(text="Submit Survey"),
                                variant="primary",
                                action=EventAction(event_name="submit_survey"),
                            ),
                        ]
                    ),
                ),
            ],
        ),
    ],
)

if __name__ == "__main__":
    msg.print_tree()
    print()
    print(msg.export_json(indent=2))
