"""E-commerce product card with data binding.

Demonstrates:
- DataBinding for dynamic values from the data model
- format_currency() and format_string() function helpers
- Image component with variant
- Row layout for action buttons
- open_url() for navigation
- FunctionAction for triggering built-in functions
"""

from py_a2ui import (
    Button,
    Card,
    Column,
    DataBinding,
    EventAction,
    FunctionAction,
    Image,
    Row,
    Text,
    UpdateComponentsMessage,
    format_currency,
    format_string,
    open_url,
)

msg = UpdateComponentsMessage(
    surface_id="product",
    components=[
        # -- Layout --
        Card(id="product_card", child="card_content"),
        Column(id="card_content", children=["product_image", "product_title", "product_price", "actions_row"]),
        # -- Product info (data-bound) --
        Image(id="product_image", url=DataBinding(path="/product/imageUrl"), variant="largeFeature", fit="cover"),
        Text(
            id="product_title",
            text=format_string("${name}"),
            variant="h3",
        ),
        Text(
            id="product_price",
            text=format_currency("USD", decimals=2),
            variant="body",
        ),
        # -- Action buttons --
        Row(id="actions_row", children=["add_to_cart_btn", "details_btn"]),
        Button(
            id="add_to_cart_btn",
            child="add_to_cart_label",
            variant="primary",
            action=EventAction(event_name="add_to_cart", context={"productId": DataBinding(path="/product/id")}),
        ),
        Text(id="add_to_cart_label", text="Add to Cart"),
        Button(
            id="details_btn",
            child="details_label",
            variant="borderless",
            action=FunctionAction(function_call=open_url("https://shop.example.com/product")),
        ),
        Text(id="details_label", text="View Details"),
    ],
)

if __name__ == "__main__":
    print(msg.model_dump_json(by_alias=True, exclude_none=True, indent=2))
