from typing import TypeVar

from more_properties.util_properties import WrappedProperty

__all__ = [
    "ClassProperty",
    "class_property",
    "StaticProperty",
    "static_property",
]

OT = TypeVar("OT", contravariant=True)  # Owner Type
VT = TypeVar("VT")  # Value Type


class ClassProperty(WrappedProperty[OT, VT]):
    wrapper = classmethod

    def __post_init__(self) -> None:
        fget = self.__dict__["fget"]

        if isinstance(fget, self.wrapper):
            fget.__doc__ = fget.__func__.__doc__

        super().__post_init__()


class StaticProperty(ClassProperty[OT, VT]):
    wrapper = staticmethod


class_property = ClassProperty
static_property = StaticProperty
