"""Shared registry and utilities for component tree processing.

Used by both ``export.py`` (flattening) and ``tree.py`` (visualization)
to ensure a single source of truth.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from py_a2ui.types.base import ComponentCommon

# Registry of child-bearing fields per component type.
# Each entry maps a component name to a list of (field_name, field_type) tuples.
# All child-bearing fields currently use unaliased names (the JSON key matches
# the Python field name). If a child field gains an alias in the future, the
# field_name here is the *Python* name; callers that need the JSON key should
# resolve the alias via model_fields.
CHILD_FIELDS: dict[str, list[tuple[str, Literal["single", "list", "tab_list"]]]] = {
    "Column": [("children", "list")],
    "Row": [("children", "list")],
    "List": [("children", "list")],
    "Card": [("child", "single")],
    "Button": [("child", "single")],
    "Modal": [("trigger", "single"), ("content", "single")],
    "Tabs": [("tabs", "tab_list")],
}


def generate_id(component: ComponentCommon, counter: int) -> tuple[str, int]:
    """Generate an ID for a component, returning (id, next_counter).

    If the component has an explicit ID, returns it unchanged.
    Otherwise generates ``{type}_{counter}`` and increments the counter.
    """
    if component.id is not None:
        return component.id, counter
    cid = f"{component.component.lower()}_{counter}"
    return cid, counter + 1
