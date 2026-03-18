"""Shared registry of child-bearing fields per component type.

Used by both ``export.py`` (flattening) and ``tree.py`` (visualization)
to ensure a single source of truth for which fields contain nested children.

Each entry maps a component name to a list of ``(field_name, field_type)``
tuples. All child-bearing fields currently use unaliased names (the JSON
key matches the Python field name). If a child field gains an alias in the
future, the ``field_name`` here is the *Python* name; callers that need
the JSON key should resolve the alias via ``model_fields``.
"""

from typing import Literal

CHILD_FIELDS: dict[str, list[tuple[str, Literal["single", "list", "tab_list"]]]] = {
    "Column": [("children", "list")],
    "Row": [("children", "list")],
    "List": [("children", "list")],
    "Card": [("child", "single")],
    "Button": [("child", "single")],
    "Modal": [("trigger", "single"), ("content", "single")],
    "Tabs": [("tabs", "tab_list")],
}
