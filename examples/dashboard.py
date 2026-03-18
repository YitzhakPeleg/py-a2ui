"""Analytics dashboard with dynamic data.

Demonstrates:
- Multiple server messages (CreateSurface + UpdateComponents + UpdateDataModel)
- Nested component composition with export_json()
- Tabs for dashboard sections
- List with DynamicChildTemplate for data-driven children
- format_number(), format_date(), pluralize() for display formatting
- Modal for drill-down details
- DataBinding for live values

Note: DynamicChildTemplate targets (event_row, page_row) must be defined
as separate top-level components with explicit IDs, since the template
references them by string ID at runtime.
"""

from py_a2ui import (
    Button,
    Card,
    Column,
    CreateSurfaceMessage,
    DataBinding,
    DynamicChildTemplate,
    EventAction,
    List,
    Modal,
    Row,
    Tab,
    Tabs,
    Text,
    UpdateComponentsMessage,
    UpdateDataModelMessage,
    format_date,
    format_number,
    pluralize,
)

# Step 1: Create the surface
create = CreateSurfaceMessage(
    surface_id="dashboard",
    catalog_id="analytics",
    send_data_model=True,
)

# Step 2: Send component tree
# Main nested tree + flat template components for DynamicChildTemplate
components = UpdateComponentsMessage(
    surface_id="dashboard",
    components=[
        # -- Main nested tree --
        Column(id="root", children=[
            Text(text="Analytics Dashboard", variant="h1"),
            Row(children=[
                Card(child=Text(text=format_number(grouping=True), variant="h2")),
                Card(child=Text(text=pluralize(one="session", other="sessions"), variant="h2")),
                Card(child=Text(text=DataBinding(path="/stats/revenue"), variant="h2")),
            ]),
            Tabs(tabs=[
                Tab(
                    title="Recent Events",
                    child=Column(children=[
                        List(children=DynamicChildTemplate(component_id="event_row", path="/events")),
                    ]),
                ),
                Tab(
                    title="Top Pages",
                    child=Column(children=[
                        List(children=DynamicChildTemplate(component_id="page_row", path="/pages")),
                    ]),
                ),
            ]),
        ]),
        # -- Template components for DynamicChildTemplate (require explicit IDs) --
        Row(id="event_row", children=["event_name", "event_time"]),
        Text(id="event_name", text=DataBinding(path="/name")),
        Text(id="event_time", text=format_date("%b %d, %H:%M")),
        Row(id="page_row", children=["page_path", "page_views", "page_detail_modal"]),
        Text(id="page_path", text=DataBinding(path="/path")),
        Text(id="page_views", text=format_number(grouping=True)),
        Modal(
            id="page_detail_modal",
            trigger=Button(
                child=Text(text="Details"),
                variant="borderless",
                action=EventAction(event_name="open_detail"),
            ),
            content=Column(children=[
                Text(text=DataBinding(path="/path"), variant="h3"),
                Text(text="Detailed analytics for this page."),
            ]),
        ),
    ],
)

# Step 3: Populate data model
data = UpdateDataModelMessage(
    surface_id="dashboard",
    value={
        "stats": {"totalUsers": 12483, "activeSessions": 342, "revenue": "$48,291"},
        "events": [
            {"name": "Page View", "time": "2026-03-18T10:30:00Z"},
            {"name": "Sign Up", "time": "2026-03-18T10:28:00Z"},
            {"name": "Purchase", "time": "2026-03-18T10:25:00Z"},
        ],
        "pages": [
            {"path": "/home", "views": 8432},
            {"path": "/pricing", "views": 3210},
            {"path": "/docs", "views": 2876},
        ],
    },
)

if __name__ == "__main__":
    import json

    components.print_tree()
    print()

    messages = [
        create.model_dump(by_alias=True, exclude_none=True),
        components.export(),
        data.model_dump(by_alias=True, exclude_none=True),
    ]
    print(json.dumps(messages, indent=2))
