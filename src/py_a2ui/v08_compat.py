"""v0.8 compatibility layer for A2UI wire-format export.

Transforms v0.9 wire-format dicts into v0.8 format at export time.
No changes to Pydantic models — this operates purely on serialized dicts.
"""

from typing import Any

# ---------------------------------------------------------------------------
# Message envelope conversion
# ---------------------------------------------------------------------------

_ENVELOPE_KEY_MAP = {
    "createSurface": "beginRendering",
    "updateComponents": "surfaceUpdate",
    "updateDataModel": "dataModelUpdate",
    # deleteSurface stays the same
}


def convert_message(v09_msg: dict) -> dict:
    """Convert a v0.9 wire-format message dict to v0.8."""
    result: dict[str, Any] = {}

    for key, value in v09_msg.items():
        if key == "version":
            continue  # v0.8 has no version field

        v08_key = _ENVELOPE_KEY_MAP.get(key, key)

        if key == "createSurface":
            result[v08_key] = _convert_begin_rendering(value)
        elif key == "updateComponents":
            result[v08_key] = _convert_surface_update(value)
        elif key == "updateDataModel":
            result[v08_key] = _convert_data_model_update(value)
        else:
            result[v08_key] = value

    return result


def _convert_begin_rendering(payload: dict) -> dict:
    """Convert createSurface payload to beginRendering.

    v0.8 requires a ``root`` field and renames ``theme`` → ``styles``.
    """
    result: dict[str, Any] = {"surfaceId": payload["surfaceId"]}

    if "catalogId" in payload:
        result["catalogId"] = payload["catalogId"]

    # v0.8 requires root — default to "root" if not specified
    result["root"] = payload.get("root", "root")

    if "theme" in payload:
        result["styles"] = payload["theme"]
    if "styles" in payload:
        result["styles"] = payload["styles"]

    return result


def _convert_surface_update(payload: dict) -> dict:
    """Convert updateComponents payload to surfaceUpdate."""
    return {
        "surfaceId": payload["surfaceId"],
        "components": [_convert_component(c) for c in payload["components"]],
    }


def _convert_data_model_update(payload: dict) -> dict:
    """Convert updateDataModel payload to dataModelUpdate.

    v0.8 uses ``contents`` with typed key-value entries instead of ``value``.
    """
    result: dict[str, Any] = {"surfaceId": payload["surfaceId"]}

    if "path" in payload:
        result["path"] = payload["path"]

    if "value" in payload:
        result["contents"] = _convert_data_model_value(payload["value"])

    return result


def _convert_data_model_value(value: Any) -> list[dict]:
    """Convert a v0.9 data model value to v0.8 contents array."""
    if isinstance(value, dict):
        return [_make_data_entry(k, v) for k, v in value.items()]
    if isinstance(value, list):
        return value  # already in list format
    return []


def _make_data_entry(key: str, value: Any) -> dict:
    """Create a v0.8 typed data entry."""
    entry: dict[str, Any] = {"key": key}
    if isinstance(value, str):
        entry["valueString"] = value
    elif isinstance(value, bool):
        entry["valueBoolean"] = value
    elif isinstance(value, (int, float)):
        entry["valueNumber"] = value
    elif isinstance(value, dict):
        entry["valueMap"] = [_make_data_entry(k, v) for k, v in value.items()]
    return entry


# ---------------------------------------------------------------------------
# Component conversion
# ---------------------------------------------------------------------------

# Fields that are dynamic values (need literalString/literalNumber/literalBoolean wrapping)
_DYNAMIC_STRING_FIELDS = frozenset(
    {
        "text",
        "label",
        "url",
        "name",
        "value",
        "title",
    }
)

_DYNAMIC_NUMBER_FIELDS = frozenset(
    {
        "value",  # for Slider — but also DynamicString for TextField; handled per-component
    }
)

_DYNAMIC_BOOLEAN_FIELDS = frozenset(
    {
        "value",  # for CheckBox
    }
)

# Fields that exist only in v0.9 and should be stripped for v0.8
_V09_ONLY_FIELDS: dict[str, frozenset[str]] = {
    "Divider": frozenset({"axis"}),
    "ChoicePicker": frozenset({"displayStyle", "filterable"}),
}

# Per-component field renames: v0.9 field name → v0.8 field name
_FIELD_RENAMES: dict[str, dict[str, str]] = {
    "Text": {"variant": "usageHint"},
    "Image": {"variant": "usageHint"},
    "TextField": {"value": "text", "variant": "textFieldType"},
    "Row": {"justify": "distribution", "align": "alignment"},
    "Column": {"justify": "distribution", "align": "alignment"},
    "List": {"align": "alignment"},
    "Slider": {"min": "minValue", "max": "maxValue"},
    "Tabs": {"tabs": "tabItems"},
    "Modal": {"trigger": "entryPointChild", "content": "contentChild"},
}

# Component type renames
_COMPONENT_TYPE_RENAMES = {
    "ChoicePicker": "MultipleChoice",
}

# Fields that hold children (need explicitList wrapping)
_CHILD_LIST_FIELDS = frozenset({"children"})

# Fields that hold a single child ref (no wrapping needed)
_CHILD_REF_FIELDS = frozenset({"child", "trigger", "content", "entryPointChild", "contentChild"})

# Components where "value" is a number (not string)
_NUMERIC_VALUE_COMPONENTS = frozenset({"Slider"})

# Components where "value" is a boolean
_BOOLEAN_VALUE_COMPONENTS = frozenset({"CheckBox"})


def _convert_component(comp: dict) -> dict:
    """Convert a v0.9 flat component to v0.8 nested wrapper format.

    v0.9: {"id": "x", "component": "Text", "text": "Hello", "variant": "h1"}
    v0.8: {"id": "x", "component": {"Text": {"text": {"literalString": "Hello"}, "usageHint": "h1"}}}
    """
    comp_type = comp["component"]
    v08_comp_type = _COMPONENT_TYPE_RENAMES.get(comp_type, comp_type)
    renames = _FIELD_RENAMES.get(comp_type, {})
    strip_fields = _V09_ONLY_FIELDS.get(comp_type, frozenset())

    # Separate envelope fields from component-specific fields
    inner: dict[str, Any] = {}

    for key, value in comp.items():
        if key in ("id", "component", "weight"):
            continue
        if key in strip_fields:
            continue

        # Apply field renames
        v08_key = renames.get(key, key)

        # Convert values based on field type and component
        converted = _convert_field_value(key, value, comp_type)
        if converted is not None:
            inner[v08_key] = converted

    # Handle Button variant → primary boolean
    if comp_type == "Button" and "variant" in comp:
        variant = comp["variant"]
        inner.pop("variant", None)
        if variant == "primary":
            inner["primary"] = True

    result: dict[str, Any] = {"id": comp["id"]}
    if "weight" in comp:
        result["weight"] = comp["weight"]
    result["component"] = {v08_comp_type: inner}

    return result


def _convert_field_value(field: str, value: Any, comp_type: str) -> Any:
    """Convert a field value to v0.8 format."""
    # Action fields
    if field == "action":
        return _convert_action(value)

    # Children list fields
    if field in _CHILD_LIST_FIELDS:
        return _convert_children(value)

    # Tab items (list of {title, child})
    if field == "tabs":
        return [_convert_tab_item(t) for t in value]

    # Dynamic value fields — wrap in typed literals
    if field in _DYNAMIC_STRING_FIELDS:
        if comp_type in _NUMERIC_VALUE_COMPONENTS and field == "value":
            return _wrap_dynamic_number(value)
        if comp_type in _BOOLEAN_VALUE_COMPONENTS and field == "value":
            return _wrap_dynamic_boolean(value)
        return _wrap_dynamic_string(value)

    # Checks (validation) — v0.8 has no checks, silently drop
    if field == "checks":
        return None

    # Options for ChoicePicker — pass through
    return value


def _convert_tab_item(tab: dict) -> dict:
    """Convert a v0.9 tab to v0.8 tab item."""
    result: dict[str, Any] = {}
    if "title" in tab:
        result["title"] = _wrap_dynamic_string(tab["title"])
    if "child" in tab:
        result["child"] = tab["child"]
    return result


# ---------------------------------------------------------------------------
# Dynamic value wrapping
# ---------------------------------------------------------------------------


def _wrap_dynamic_string(value: Any) -> Any:
    """Wrap a v0.9 dynamic string value in v0.8 typed wrapper."""
    if isinstance(value, str):
        return {"literalString": value}
    if isinstance(value, dict):
        if "path" in value:
            return {"path": value["path"]}
        if "functionCall" in value:
            raise ValueError("FunctionCall not supported in v0.8 export")
        return value
    return value


def _wrap_dynamic_number(value: Any) -> Any:
    """Wrap a v0.9 dynamic number value in v0.8 typed wrapper."""
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return {"literalNumber": value}
    if isinstance(value, dict):
        if "path" in value:
            return {"path": value["path"]}
        if "functionCall" in value:
            raise ValueError("FunctionCall not supported in v0.8 export")
        return value
    return value


def _wrap_dynamic_boolean(value: Any) -> Any:
    """Wrap a v0.9 dynamic boolean value in v0.8 typed wrapper."""
    if isinstance(value, bool):
        return {"literalBoolean": value}
    if isinstance(value, dict):
        if "path" in value:
            return {"path": value["path"]}
        if "functionCall" in value:
            raise ValueError("FunctionCall not supported in v0.8 export")
        return value
    return value


# ---------------------------------------------------------------------------
# Action conversion
# ---------------------------------------------------------------------------


def _convert_action(action: dict) -> dict:
    """Convert a v0.9 action to v0.8 format.

    v0.9: {"event": {"name": "submit", "context": {"key": "val"}}}
    v0.8: {"name": "submit", "context": [{"key": "key", "value": "val"}]}

    FunctionAction (v0.9 only) raises ValueError.
    """
    if "functionCall" in action:
        raise ValueError("FunctionAction not supported in v0.8 export")

    event = action.get("event", action)
    result: dict[str, Any] = {"name": event["name"]}

    context = event.get("context")
    if context is not None:
        if isinstance(context, dict):
            result["context"] = [{"key": k, "value": _wrap_context_value(v)} for k, v in context.items()]
        elif isinstance(context, list):
            result["context"] = context
        else:
            result["context"] = []
    else:
        result["context"] = []

    return result


def _wrap_context_value(value: Any) -> Any:
    """Wrap an action context value for v0.8."""
    if isinstance(value, str):
        return {"literalString": value}
    if isinstance(value, dict) and "path" in value:
        return {"path": value["path"]}
    return value


# ---------------------------------------------------------------------------
# Children conversion
# ---------------------------------------------------------------------------


def _convert_children(children: Any) -> dict:
    """Convert v0.9 children to v0.8 format.

    v0.9: ["id1", "id2"] or {"componentId": "...", "path": "/..."}
    v0.8: {"explicitList": ["id1", "id2"]} or {"template": {"componentId": "...", "dataBinding": "/..."}}
    """
    if isinstance(children, list):
        return {"explicitList": children}

    if isinstance(children, dict) and "componentId" in children:
        return {
            "template": {
                "componentId": children["componentId"],
                "dataBinding": children["path"],
            },
        }

    return {"explicitList": children}
