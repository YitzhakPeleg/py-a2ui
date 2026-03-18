"""Analytics dashboard with dynamic data.

Demonstrates:
- Multiple server messages (CreateSurface + UpdateComponents + UpdateDataModel)
- Tabs for dashboard sections
- List with DynamicChildTemplate for data-driven children
- format_number(), format_date(), pluralize() for display formatting
- Modal for drill-down details
- DataBinding for live values
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
components = UpdateComponentsMessage(
    surface_id="dashboard",
    components=[
        # -- Top-level layout --
        Column(id="root", children=["title", "stats_row", "content_tabs"]),
        Text(id="title", text="Analytics Dashboard", variant="h1"),
        # -- Stats summary row --
        Row(id="stats_row", children=["total_users_card", "active_sessions_card", "revenue_card"]),
        Card(id="total_users_card", child="total_users_text"),
        Text(id="total_users_text", text=format_number(grouping=True), variant="h2"),
        Card(id="active_sessions_card", child="active_sessions_text"),
        Text(
            id="active_sessions_text",
            text=pluralize(one="session", other="sessions"),
            variant="h2",
        ),
        Card(id="revenue_card", child="revenue_text"),
        Text(id="revenue_text", text=DataBinding(path="/stats/revenue"), variant="h2"),
        # -- Tabbed content --
        Tabs(
            id="content_tabs",
            tabs=[
                Tab(title="Recent Events", child="events_section"),
                Tab(title="Top Pages", child="pages_section"),
            ],
        ),
        # --- Events tab: dynamic list ---
        Column(id="events_section", children=["events_list"]),
        List(
            id="events_list",
            children=DynamicChildTemplate(component_id="event_row", path="/events"),
        ),
        Row(id="event_row", children=["event_name", "event_time"]),
        Text(id="event_name", text=DataBinding(path="/name")),
        Text(id="event_time", text=format_date("%b %d, %H:%M")),
        # --- Pages tab with detail modal ---
        Column(id="pages_section", children=["pages_list"]),
        List(
            id="pages_list",
            children=DynamicChildTemplate(component_id="page_row", path="/pages"),
        ),
        Row(id="page_row", children=["page_path", "page_views", "page_detail_modal"]),
        Text(id="page_path", text=DataBinding(path="/path")),
        Text(id="page_views", text=format_number(grouping=True)),
        # -- Modal for page details --
        Modal(id="page_detail_modal", trigger="detail_btn", content="detail_content"),
        Button(
            id="detail_btn",
            child="detail_btn_label",
            variant="borderless",
            action=EventAction(event_name="open_detail"),
        ),
        Text(id="detail_btn_label", text="Details"),
        Column(id="detail_content", children=["detail_title", "detail_body"]),
        Text(id="detail_title", text=DataBinding(path="/path"), variant="h3"),
        Text(id="detail_body", text="Detailed analytics for this page."),
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

    messages = [
        create.model_dump(by_alias=True, exclude_none=True),
        components.model_dump(by_alias=True, exclude_none=True),
        data.model_dump(by_alias=True, exclude_none=True),
    ]
    print(json.dumps(messages, indent=2))
