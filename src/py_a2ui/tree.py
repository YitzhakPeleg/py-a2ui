"""Rich tree visualization for A2UI component trees."""

from rich.console import Console
from rich.markup import escape
from rich.tree import Tree

from py_a2ui.types.base import ComponentCommon


def build_tree(components: list[ComponentCommon], label: str = "Surface") -> Tree:
    """Build a Rich Tree from nested components."""
    root = Tree(f"[bold]{label}[/bold]")
    counter = _Counter()
    for comp in components:
        _add_node(root, comp, counter)
    return root


class _Counter:
    def __init__(self) -> None:
        self.value: int = 1

    def next_id(self, component: ComponentCommon) -> str:
        if component.id is not None:
            return component.id
        cid = f"{component.component.lower()}_{self.value}"
        self.value += 1
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
        elif isinstance(child, str):
            node.add(f"[dim]{child!s}[/dim]")


def _format_label(comp: ComponentCommon, cid: str) -> str:
    """Format: ComponentType "text" [variant] -> action (id)"""
    parts = [f"[bold cyan]{comp.component}[/bold cyan]"]

    # Text content
    text = getattr(comp, "text", None)
    if isinstance(text, str) and text:
        display = text[:30] + "..." if len(text) > 30 else text
        parts.append(f'[green]"{display}"[/green]')

    # Variant
    variant = getattr(comp, "variant", None)
    if variant is not None:
        # Show variant if it differs from the default
        field_info = type(comp).model_fields.get("variant")
        if field_info is not None and variant != field_info.default:
            parts.append(f"[yellow]\\[{escape(str(variant))}][/yellow]")

    # Action
    action = getattr(comp, "action", None)
    if action is not None:
        event_name = getattr(action, "event_name", None)
        if event_name:
            parts.append(f"[magenta]-> {event_name}[/magenta]")

    # ID
    parts.append(f"[dim]({cid})[/dim]")

    return " ".join(parts)


def _get_children(component: ComponentCommon) -> list:
    """Extract child components/refs from a component."""
    children: list = []

    # Check for children (Column, Row, List)
    child_list = getattr(component, "children", None)
    if isinstance(child_list, list):
        children.extend(child_list)

    # Check for child (Card, Button)
    child = getattr(component, "child", None)
    if child is not None:
        children.append(child)

    # Check for trigger/content (Modal)
    trigger = getattr(component, "trigger", None)
    if trigger is not None:
        children.append(trigger)
    content = getattr(component, "content", None)
    if content is not None:
        children.append(content)

    # Check for tabs (Tabs)
    tabs = getattr(component, "tabs", None)
    if tabs is not None:
        for tab in tabs:
            tab_child = getattr(tab, "child", None)
            if tab_child is not None:
                children.append(tab_child)

    return children


def print_tree(components: list[ComponentCommon], label: str = "Surface") -> None:
    """Print a visual tree of the component hierarchy to the console."""
    tree = build_tree(components, label=label)
    Console().print(tree)
