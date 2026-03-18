"""Flatten nested component trees to A2UI wire format."""

from typing import Any, Literal

from py_a2ui.types.base import ComponentCommon

# Registry of child-bearing fields per component type.
# Each entry maps a component name to a list of (field_name, field_type) tuples.
_CHILD_FIELDS: dict[str, list[tuple[str, Literal["single", "list", "tab_list"]]]] = {
    "Column": [("children", "list")],
    "Row": [("children", "list")],
    "List": [("children", "list")],
    "Card": [("child", "single")],
    "Button": [("child", "single")],
    "Modal": [("trigger", "single"), ("content", "single")],
    "Tabs": [("tabs", "tab_list")],
}


def flatten(components: list[ComponentCommon]) -> list[dict[str, Any]]:
    """Flatten nested component trees into A2UI wire-format dicts.

    Top-level components must have an explicit ``id``. Inner components
    get auto-generated IDs of the form ``{type}_{counter}`` when ``id``
    is ``None``.

    Raises:
        ValueError: If a top-level component has no ``id``, or if
            duplicate IDs are detected.
    """
    for comp in components:
        if comp.id is None:
            msg = f"Top-level component {comp.component} must have an explicit id"
            raise ValueError(msg)

    ctx = _FlattenContext()
    for comp in components:
        _flatten_component(comp, ctx)
    return ctx.collected


class _FlattenContext:
    def __init__(self) -> None:
        self.collected: list[dict[str, Any]] = []
        self.counter: int = 1
        self.seen_ids: set[str] = set()

    def assign_id(self, component: ComponentCommon) -> str:
        if component.id is not None:
            cid = component.id
        else:
            cid = f"{component.component.lower()}_{self.counter}"
            self.counter += 1
        if cid in self.seen_ids:
            msg = f"Duplicate component id: {cid!r}"
            raise ValueError(msg)
        self.seen_ids.add(cid)
        return cid


def _flatten_component(component: ComponentCommon, ctx: _FlattenContext) -> str:
    """Flatten a component and its children recursively. Returns the assigned ID."""
    cid = ctx.assign_id(component)

    # Build the wire-format dict
    data = component.model_dump(by_alias=True, exclude_none=True)
    data["id"] = cid

    comp_type = component.component  # e.g., "Column", "Button"
    child_fields = _CHILD_FIELDS.get(comp_type, [])

    for field_name, field_type in child_fields:
        value = getattr(component, field_name, None)
        if value is None:
            continue

        if field_type == "single":
            if isinstance(value, ComponentCommon):
                child_id = _flatten_component(value, ctx)
                data[field_name] = child_id
            # else it's a string ID, already in data

        elif field_type == "list":
            if isinstance(value, list):
                new_children: list[str] = []
                for child in value:
                    if isinstance(child, ComponentCommon):
                        child_id = _flatten_component(child, ctx)
                        new_children.append(child_id)
                    else:
                        new_children.append(child)  # string ID
                data[field_name] = new_children
            # else it's DynamicChildTemplate, already dumped correctly

        elif field_type == "tab_list":
            from py_a2ui.components.tabs import Tab

            new_tabs: list[dict[str, Any]] = []
            for tab in value:
                if isinstance(tab, Tab):
                    tab_data = tab.model_dump(by_alias=True, exclude_none=True)
                    if isinstance(tab.child, ComponentCommon):
                        child_id = _flatten_component(tab.child, ctx)
                        tab_data["child"] = child_id
                else:
                    tab_data = tab
                new_tabs.append(tab_data)
            data["tabs"] = new_tabs

    ctx.collected.append(data)
    return cid
