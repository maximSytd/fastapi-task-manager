import enum
import typing


class StrEnumAsDict(typing.TypedDict):
    """Typed dict for enum that have value and label."""

    value: str
    label: str


class TranslatableStrEnum(enum.StrEnum):
    """StrEnum with fastapi-babel translation support."""

    def __new__(cls, value: str, label):
        obj = str.new(cls, value)
        obj._value_ = value
        obj.label = label
        return obj

    @property
    def text(self) -> str:
        """Return and translate label."""
        return str(self.label)

    @classmethod
    def choices(cls):
        """Return enum choices (value, label)."""
        return [(item.value, str(item.label)) for item in cls]

    def as_dict(self) -> StrEnumAsDict:
        """Return value and label as dict."""
        return {"value": self.value, "label": str(self.label)}