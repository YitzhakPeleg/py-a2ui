"""Rich tree visualization for A2UI component trees."""

from rich.console import Console
from rich.markup import escape
from rich.tree import Tree

from py_a2ui._registry import CHILD_FIELDS, generate_id
from py_a2ui.types.base import ComponentCommon
from py_a2ui.types.children import DynamicChildTemplate


def build_tree(components: list[ComponentCommon], label: str = "Surface") -> Tree:
    """Build a Rich Tree from nested components."""
    root = Tree(f"[bold]{escape(label)}[/bold]")
    counter = _Counter()
    for comp in components:
        _add_node(root, comp, counter)
    return root


class _Counter:
    def __init__(self) -> None:
        self.value: int = 1

    def next_id(self, component: ComponentCommon) -> str:
        cid, self.value = generate_id(component, self.value)
        return cid


def _add_node(parent: Tree, component: ComponentCommon, counter: _Counter) -> None:
    """Recursively add a component and its children to the tree."""
    cid = counter.next_id(component)
    label = _format_label(component, cid)
    node = parent.add(label)

    children = _get_children(component)
    for child in children:
        if isinstance(child, ComponentCommon):
            _add_node(node, child, counter)
        elif isinstance(child, DynamicChildTemplate):
            node.add(f"[dim italic]template: {escape(child.component_id)} \\[{escape(child.path)}][/dim italic]")
        elif isinstance(child, str):
            node.add(f"[dim]{escape(str(child))}[/dim]")


def _format_label(comp: ComponentCommon, cid: str) -> str:
    """Format: ComponentType "text" [variant] -> action (id)"""
    parts = [f"[bold cyan]{escape(comp.component)}[/bold cyan]"]

    # Text content
    text = getattr(comp, "text", None)
    if isinstance(text, str) and text:
        display = text[:30] + "..." if len(text) > 30 else text
        parts.append(f'[green]"{escape(display)}"[/green]')

    # Variant
    variant = getattr(comp, "variant", None)
    if variant is not None:
        # Show variant if it differs from the default
        field_info = type(comp).model_fields.get("variant")
        if field_info is not None and variant != field_info.default:
            parts.append(f"[yellow]\\[{escape(str(variant))}][/yellow]")

    # Action — show EventAction event name or FunctionAction function name
    action = getattr(comp, "action", None)
    if action is not None:
        event_name = getattr(action, "event_name", None)
        if event_name:
            parts.append(f"[magenta]-> {escape(str(event_name))}[/magenta]")
        else:
            fn_call = getattr(action, "function_call", None)
            if fn_call is not None:
                parts.append(f"[magenta]-> fn:{escape(fn_call.call)}[/magenta]")

    # ID
    parts.append(f"[dim]({escape(cid)})[/dim]")

    return " ".join(parts)


def _get_children(component: ComponentCommon) -> list:
    """Extract child components/refs from a component using the shared registry."""
    children: list = []
    comp_type = component.component
    child_fields = CHILD_FIELDS.get(comp_type, [])

    for field_name, field_type in child_fields:
        value = getattr(component, field_name, None)
        if value is None:
            continue

        if field_type == "single":
            children.append(value)

        elif field_type == "list":
            if isinstance(value, list):
                children.extend(value)
            elif isinstance(value, DynamicChildTemplate):
                children.append(value)

        elif field_type == "tab_list":
            for tab in value:
                tab_child = getattr(tab, "child", None)
                if tab_child is not None:
                    children.append(tab_child)

    return children


def print_tree(components: list[ComponentCommon], label: str = "Surface") -> None:
    """Print a visual tree of the component hierarchy to the console."""
    tree = build_tree(components, label=label)
    Console().print(tree)
