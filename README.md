# py-a2ui

Pythonic [Pydantic v2](https://docs.pydantic.dev/) wrapper for [A2UI](https://a2ui.org/) components.

Build type-safe A2UI component trees in Python and serialize them to the A2UI JSON wire format.

## Installation

```bash
pip install py-a2ui
```

> **Requires Python 3.14+**

## Quick Start

```python
from py_a2ui import (
    Text, Card, Column, Button,
    UpdateComponentsMessage, EventAction,
)

msg = UpdateComponentsMessage(
    surface_id="booking",
    components=[
        Column(id="root", children=["title", "card1"]),
        Text(id="title", text="Book Your Table", variant="h1"),
        Card(id="card1", child="form"),
        Column(id="form", children=["submit_btn"]),
        Button(
            id="submit_btn",
            child="submit_label",
            variant="primary",
            action=EventAction(event_name="submit"),
        ),
        Text(id="submit_label", text="Reserve"),
    ],
)

# camelCase JSON matching the A2UI wire format
print(msg.model_dump_json(by_alias=True, exclude_none=True, indent=2))
```

## Features

- **Pydantic v2 models** for all 17 A2UI v0.10 components
- **Server-to-client messages**: `CreateSurface`, `UpdateComponents`, `UpdateDataModel`, `DeleteSurface`, `CallFunction`
- **Type-safe enums** for variants, alignment, justification, etc.
- **Data binding** via `DataBinding(path="/some/path")`
- **Built-in function helpers** with input validation:
  - Validation: `required()`, `regex()`, `length()`, `numeric()`, `email()`
  - Formatting: `format_string()`, `format_number()`, `format_currency()`, `format_date()`, `pluralize()`
  - Navigation: `open_url()` (validates URL structure)
  - Logic: `and_()`, `or_()`, `not_()`
- **camelCase JSON** output via Pydantic aliases
- **Discriminated unions** for polymorphic deserialization (`AnyComponent`, `ServerMessage`)

## Components

| Component | Description |
|-----------|-------------|
| `Text` | Text display with Markdown support |
| `Image` | Image display with fit/variant options |
| `Icon` | Built-in or custom icons |
| `Video` | Video player |
| `AudioPlayer` | Audio player |
| `Row` | Horizontal layout |
| `Column` | Vertical layout |
| `List` | List layout |
| `Card` | Card container |
| `Tabs` | Tabbed container |
| `Modal` | Modal dialog |
| `Divider` | Visual divider |
| `Button` | Interactive button |
| `TextField` | Text input |
| `CheckBox` | Checkbox input |
| `ChoicePicker` | Selection input |
| `Slider` | Numeric slider |
| `DateTimeInput` | Date/time input |

## License

MIT
