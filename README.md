# `more_properties`

A collection of `property` variants.

## Basic Usage

Variants behave mostly as the built-in `property`, except where noted.

Given the following class,

```python
from more_properties import property, class_property, static_property


class Parrot:
    @property
    def name(self):
        return "Fred"

    @class_property
    def order(cls):
        return Psittaciformes

    @static_property
    def planet():
        return Earth
```

the properties may be accessed like so:

```pycon
>>> Parrot().name
'Fred'
>>> Parrot.order
<class 'Psittaciformes'>
>>> Parrot.planet
<class 'Earth'>
```

## Setters/Deleters

Setters and deleters are defined in the same way as the built-in `property`.
Either with the decorator method

```python
from more_properties import class_property


class Foo:
    name = "Foo"

    @class_property
    def identifier(cls):
        """Object identifier"""
        return cls.name.lower()

    @identifier.setter
    def identifier(cls, value):
        cls.name = value.title()

    @identifier.deleter
    def identifier(cls):
        cls.name = None
```

or the inline method

```python
from more_properties import class_property


class Foo:
    name = "Foo"

    @classmethod
    def get_identifier(cls):
        return cls.name.lower()

    @classmethod
    def set_identifier(cls, value):
        cls.name = value.title()

    @classmethod
    def del_identifier(cls):
        cls.name = None

    identifier = class_property(
        get_identifier,
        set_identifier,
        del_identifier,
        "Object identifier"
    )
```

## Reference

### `property`

A modified version of the built-in [`property`](https://docs.python.org/3/library/functions.html#property).

Always behaves as a
[data descriptor](https://docs.python.org/3/howto/descriptor.html#descriptor-protocol),
regardless of which (if any) of getter, setter, and deleter are set.

Behaviour when accessed on a class, is undefined.

### `class_property`

A `property` for classes.
Both `cls.x` and `instance.x` call the getter with the class.
Setting `instance.x` calls the setter with the class and value.
Deleting `instance.x` call the deleter with the class only.

```python
from more_properties import class_property


class Foo:
    @class_property
    def identifier(cls):
        """Class identifier"""
        return cls.__name__.lower()


class Bar(Foo):
    pass
```

```pycon
>>> Foo.identifier
'foo'
>>> Foo().identifier
'foo'
```

```pycon
>>> Bar.identifier
'bar'
>>> Bar().identifier
'bar'
```

`classproperty` provided as a synonym, for consistency with `classmethod`.

<aside class="warning">
    <p>
        Due to the
        <a href="https://docs.python.org/3/reference/datamodel.html#object.__set__">Python data model</a>,
        using the setters/deleters on <em>classes</em> may not work as intended.
    </p>
    <p>
        Getters always work as intended, and using setters/deleters on <em>instances</em> work as intended.
    </p>
</aside>

### `static_property`

A `property` independent of its accessor.
Both `cls.x` and `instance.x` call the getter with no parameters.
Setting `instance.x` calls the setter with the value only.
Deleting `instance.x` call the deleter with no parameters.

```python
from more_properties import static_property


x = "bar"

class Foo:
    @static_property
    def val():
        return x
```

```pycon
>>> Foo.val
'bar'
>>> Foo().val
'bar'
```

`staticproperty` provided as a synonym, for consistency with `staticmethod`.

<aside class="warning">
    <p>
        Due to the
        <a href="https://docs.python.org/3/reference/datamodel.html#object.__set__">Python data model</a>,
        using the setters/deleters on <em>classes</em> may not work as intended.
    </p>
    <p>
        Getters always work as intended, and using setters/deleters on <em>instances</em> work as intended.
    </p>
</aside>

### `cached_property`
### `cached_class_property`
### `cached_static_property`

Variants of `property`, `class_property`, and `static_property`, respectively.

They are each used in the same way as the originals,
but cache the value of the getters.

```python
from dataclasses import dataclass

from more_properties import cached_property


@dataclass
class Foo:
    x: int

    @cached_property
    def y(self):
        print("Doing work")
        return self.x + 1
```

```pycon
>>> bar = Foo(1)
>>> bar.y
Doing work
2
>>> bar.y
2
```

If the setters/deleters are defined,
then the cache is cleared before they are called.

Further, the cache may be explicitly cleared through the `clear_cache` method,
exposed only during class creation.

```python
@dataclass
class Foo:
    x: int

    @cached_property
    def y(self):
        print("Doing work")
        return self.x + 1

    y_clear_cache = y.clear_cache
```

```pycon
>>> bar = Foo(1)
>>> bar.y
Doing work
2
>>> bar.y
2
>>> bar.y_clear_cache()
>>> bar.y
Doing work
2
```

## Installation

Install and update using the standard Python package manager [pip](https://pip.pypa.io/en/stable/):

```bash
pip install more_properties
```