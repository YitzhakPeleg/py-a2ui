from py_a2ui.actions.function_call import FunctionCall, ReturnType
from py_a2ui.types.dynamic import DynamicBoolean


def and_(*conditions: DynamicBoolean) -> FunctionCall:
    """Logical AND on two or more boolean values."""
    return FunctionCall(call="and", args={"values": list(conditions)}, return_type=ReturnType.BOOLEAN)


def or_(*conditions: DynamicBoolean) -> FunctionCall:
    """Logical OR on two or more boolean values."""
    return FunctionCall(call="or", args={"values": list(conditions)}, return_type=ReturnType.BOOLEAN)


def not_(condition: DynamicBoolean) -> FunctionCall:
    """Logical NOT on a boolean value."""
    return FunctionCall(call="not", args={"value": condition}, return_type=ReturnType.BOOLEAN)
