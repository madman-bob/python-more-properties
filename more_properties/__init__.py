from more_properties.class_property import class_property, static_property
from more_properties.property import property

__all__ = [
    "property",
    "class_property",
    "classproperty",
    "static_property",
    "staticproperty",
]

# Providing aliases for consistency with classmethod and staticmethod
classproperty = class_property
staticproperty = static_property
