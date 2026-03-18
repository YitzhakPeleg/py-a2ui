"""E-commerce product card with data binding.

Demonstrates:
- Nested component composition
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
        Card(
            id="product_card",
            child=Column(
                children=[
                    Image(url=DataBinding(path="/product/imageUrl"), variant="largeFeature", fit="cover"),
                    Text(text=format_string("${name}"), variant="h3"),
                    Text(text=format_currency("USD", decimals=2)),
                    Row(
                        children=[
                            Button(
                                child=Text(text="Add to Cart"),
                                variant="primary",
                                action=EventAction(
                                    event_name="add_to_cart",
                                    context={"productId": DataBinding(path="/product/id")},
                                ),
                            ),
                            Button(
                                child=Text(text="View Details"),
                                variant="borderless",
                                action=FunctionAction(function_call=open_url("https://shop.example.com/product")),
                            ),
                        ]
                    ),
                ]
            ),
        ),
    ],
)

if __name__ == "__main__":
    msg.print_tree()
    print()
    print(msg.export_json(indent=2))
