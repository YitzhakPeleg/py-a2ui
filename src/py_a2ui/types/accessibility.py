from pydantic import BaseModel, ConfigDict


class AccessibilityAttributes(BaseModel):
    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    label: str | None = None
    description: str | None = None
