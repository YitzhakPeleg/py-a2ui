"""Multi-step survey with validation.

Demonstrates:
- Tabs container for multi-page forms
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
        # -- Tabs layout --
        Tabs(
            id="survey_tabs",
            tabs=[
                Tab(title="Personal Info", child="tab_personal"),
                Tab(title="Preferences", child="tab_preferences"),
                Tab(title="Feedback", child="tab_feedback"),
            ],
        ),
        # === Tab 1: Personal Info ===
        Column(id="tab_personal", children=["name_input", "email_input", "phone_input"]),
        TextField(
            id="name_input",
            label="Your Name",
            checks=[
                CheckRule(condition=required(), message="Name is required"),
                CheckRule(condition=length(min=2, max=50), message="2-50 characters"),
            ],
        ),
        TextField(
            id="email_input",
            label="Email Address",
            checks=[
                CheckRule(condition=required(), message="Email is required"),
                CheckRule(condition=email(), message="Must be a valid email"),
            ],
        ),
        TextField(
            id="phone_input",
            label="Phone (optional)",
            checks=[
                CheckRule(condition=regex(r"^\+?[\d\s\-()]{7,15}$"), message="Invalid phone format"),
            ],
        ),
        # === Tab 2: Preferences ===
        Column(id="tab_preferences", children=["experience_picker", "satisfaction_slider", "newsletter_check"]),
        ChoicePicker(
            id="experience_picker",
            label="Experience Level",
            options=[
                ChoiceOption(label="Beginner", value="beginner"),
                ChoiceOption(label="Intermediate", value="intermediate"),
                ChoiceOption(label="Advanced", value="advanced"),
                ChoiceOption(label="Expert", value="expert"),
            ],
            value=[],
        ),
        Slider(id="satisfaction_slider", min=0, max=10, value=5),
        CheckBox(id="newsletter_check", label="Subscribe to newsletter", value=False),
        # === Tab 3: Feedback ===
        Column(id="tab_feedback", children=["feedback_text", "submit_btn"]),
        TextField(
            id="feedback_text",
            label="Additional feedback",
            variant="longText",
            checks=[
                CheckRule(condition=length(max=500), message="Max 500 characters"),
            ],
        ),
        Button(
            id="submit_btn",
            child="submit_label",
            variant="primary",
            action=EventAction(event_name="submit_survey"),
        ),
        Text(id="submit_label", text="Submit Survey"),
    ],
)

if __name__ == "__main__":
    print(msg.model_dump_json(by_alias=True, exclude_none=True, indent=2))
