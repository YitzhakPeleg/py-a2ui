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

## Data Binding

Bind component values to a client-side data model using `DataBinding`:

```python
from py_a2ui import Text, TextField, DataBinding

# Display a value from the data model
greeting = Text(id="greeting", text=DataBinding(path="/user/greeting"))

# Two-way bind an input to the data model
name_field = TextField(id="name", label="Your Name", value=DataBinding(path="/user/name"))
```

Dynamic children iterate over a data model array:

```python
from py_a2ui import List, Row, Text, DynamicChildTemplate, DataBinding

items = List(
    id="item_list",
    children=DynamicChildTemplate(component_id="item_row", path="/items"),
)
item_row = Row(id="item_row", children=["item_name"])
item_name = Text(id="item_name", text=DataBinding(path="/name"))
```

## Function Helpers

Built-in functions return `FunctionCall` instances with **input validation at construction time**.

### Validation

```python
from py_a2ui import TextField, CheckRule, required, length, email, regex

field = TextField(
    id="email",
    label="Email",
    checks=[
        CheckRule(condition=required(), message="Required"),
        CheckRule(condition=email(), message="Invalid email"),
        CheckRule(condition=length(min=5, max=100), message="5-100 chars"),
    ],
)

# regex validates the pattern compiles
CheckRule(condition=regex(r"^\d{3}-\d{4}$"), message="Invalid format")
```

### Formatting

```python
from py_a2ui import Text, format_currency, format_number, format_date, pluralize

# Currency (validates ISO 4217 code)
price = Text(id="price", text=format_currency("USD", decimals=2))

# Number with grouping (e.g. "1,234")
count = Text(id="count", text=format_number(grouping=True))

# Date (validates strftime pattern)
date = Text(id="date", text=format_date("%b %d, %Y"))

# Pluralization
items = Text(id="items", text=pluralize(one="item", other="items"))
```

### Navigation

```python
from py_a2ui import Button, FunctionAction, open_url

# URL is validated as a well-formed HTTP(S) URL
btn = Button(
    id="link",
    child="label",
    action=FunctionAction(function_call=open_url("https://example.com")),
)
```

### Logic

```python
from py_a2ui import and_, or_, not_, required, length

# Combine validation conditions
both = and_(required(), length(min=1))
either = or_(required(), length(min=1))
negated = not_(required())
```

## Server Messages

```python
from py_a2ui import (
    CreateSurfaceMessage,
    UpdateComponentsMessage,
    UpdateDataModelMessage,
    DeleteSurfaceMessage,
    Text,
)

# 1. Create a surface
create = CreateSurfaceMessage(surface_id="app", catalog_id="my-catalog")

# 2. Send components
update = UpdateComponentsMessage(
    surface_id="app",
    components=[Text(id="hello", text="Hello, world!")],
)

# 3. Update the data model
data = UpdateDataModelMessage(
    surface_id="app",
    path="/user",
    value={"name": "Alice", "email": "alice@example.com"},
)

# 4. Remove the surface
delete = DeleteSurfaceMessage(surface_id="app")
```

## JSON Output

All models serialize to camelCase JSON matching the A2UI wire format:

```python
# As a dict
data = msg.model_dump(by_alias=True, exclude_none=True)

# As a JSON string
json_str = msg.model_dump_json(by_alias=True, exclude_none=True, indent=2)
```

Both `snake_case` (Python) and `camelCase` (JSON) field names are accepted as input:

```python
# These are equivalent
Text(id="t", text="hi", variant="h1")
Text(**{"id": "t", "text": "hi", "variant": "h1"})
```

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

## Examples

See the [`examples/`](examples/) directory for complete, runnable scripts:

- **[`booking_form.py`](examples/booking_form.py)** -- Restaurant reservation with validation
- **[`product_card.py`](examples/product_card.py)** -- E-commerce card with data binding and formatting
- **[`survey_form.py`](examples/survey_form.py)** -- Multi-step survey with tabs and input types
- **[`dashboard.py`](examples/dashboard.py)** -- Analytics dashboard with dynamic lists and multiple messages

```bash
uv run python examples/booking_form.py
```

## License

MIT
