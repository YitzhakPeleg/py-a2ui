"""Flatten nested component trees to A2UI wire format."""

from typing import Any

from py_a2ui._registry import CHILD_FIELDS, generate_id
from py_a2ui.types.base import ComponentCommon


def flatten(components: list[ComponentCommon]) -> list[dict[str, Any]]:
    """Flatten nested component trees into A2UI wire-format dicts.

    Top-level components must have an explicit ``id``. Inner components
    get auto-generated IDs of the form ``{type}_{counter}`` when ``id``
    is ``None``.

    Output order: children are emitted before their parent (DFS post-order,
    left-to-right). This ensures that when a client processes the list
    sequentially, every referenced child ID already exists.

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
        cid, self.counter = generate_id(component, self.counter)
        if cid in self.seen_ids:
            msg = f"Duplicate component id: {cid!r}"
            raise ValueError(msg)
        self.seen_ids.add(cid)
        return cid


def _flatten_component(component: ComponentCommon, ctx: _FlattenContext) -> str:
    """Flatten a component and its children recursively. Returns the assigned ID."""
    cid = ctx.assign_id(component)

    # Build the wire-format dict. model_dump(by_alias=True) produces alias-keyed
    # dicts for the full nested tree; we then overwrite child fields with flattened
    # string IDs. This is acceptable because:
    # 1. UI component trees are small in practice (hundreds, not millions of nodes).
    # 2. All child-bearing fields (children, child, trigger, content, tabs) have no
    #    alias, so field_name == JSON key. If a child field gains an alias, the
    #    CHILD_FIELDS registry and this loop must be updated to use the alias.
    data = component.model_dump(by_alias=True, exclude_none=True)
    data["id"] = cid

    comp_type = component.component  # e.g., "Column", "Button"
    child_fields = CHILD_FIELDS.get(comp_type, [])

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
            new_tabs: list[dict[str, Any]] = []
            for tab in value:
                tab_data = tab.model_dump(by_alias=True, exclude_none=True)
                if isinstance(tab.child, ComponentCommon):
                    child_id = _flatten_component(tab.child, ctx)
                    tab_data["child"] = child_id
                new_tabs.append(tab_data)
            data[field_name] = new_tabs

    ctx.collected.append(data)
    return cid
