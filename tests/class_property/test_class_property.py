from itertools import product
from unittest import TestCase

from more_properties import class_property


class TestClassProperty(TestCase):
    def check_class(
        self,
        cls,
        has_getter=False,
        has_setter=False,
        has_deleter=False,
        has_docstring=False,
    ):
        with self.subTest("Getter"):
            if has_getter:
                self.assertEqual(cls.name.lower(), cls.identifier)
                self.assertEqual(cls.name.lower(), cls().identifier)
            else:
                with self.assertRaisesRegex(AttributeError, "unreadable attribute"):
                    cls.identifier

                with self.assertRaisesRegex(AttributeError, "unreadable attribute"):
                    cls().identifier

        with self.subTest("Setter"):
            if has_setter:
                cls().identifier = "doohickey"
                self.assertEqual("Doohickey", cls.name)
            else:
                with self.assertRaisesRegex(AttributeError, "can't set attribute"):
                    cls().identifier = "doohickey"

        with self.subTest("Deleter"):
            if has_deleter:
                del cls().identifier
                self.assertEqual(None, cls.name)
            else:
                with self.assertRaisesRegex(AttributeError, "can't delete attribute"):
                    del cls().identifier

        with self.subTest("Docstring"):
            self.assertEqual(
                "Object identifier" if has_docstring else None,
                cls.__dict__.get("identifier").__doc__,
            )

    def test_class_property_basic(self):
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

        with self.subTest(cls=Foo):
            self.check_class(
                Foo,
                has_getter=True,
                has_setter=True,
                has_deleter=True,
                has_docstring=True,
            )

        class Bar(Foo):
            name = "Bar"

        with self.subTest(cls=Bar):
            self.check_class(
                Bar,
                has_getter=True,
                has_setter=True,
                has_deleter=True,
                has_docstring=False,  # Incorrect, but don't have canonical way of getting docstring
            )

    def test_class_property_inline_definition(self):
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
                get_identifier, set_identifier, del_identifier, "Object identifier"
            )

        self.check_class(
            Foo, has_getter=True, has_setter=True, has_deleter=True, has_docstring=True,
        )

    def test_class_property_missing_components(self):
        for has_getter, has_setter, has_deleter, has_docstring in product(
            [False, True], repeat=4
        ):
            with self.subTest(
                has_getter=has_getter,
                has_setter=has_setter,
                has_deleter=has_deleter,
                has_docstring=has_docstring,
            ):

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
                        fget=get_identifier if has_getter else None,
                        fset=set_identifier if has_setter else None,
                        fdel=del_identifier if has_deleter else None,
                        doc="Object identifier" if has_docstring else None,
                    )

                self.check_class(
                    Foo, has_getter, has_setter, has_deleter, has_docstring
                )

    def test_class_property_docstring_priority(self):
        class Foo:
            name = "Foo"

            @classmethod
            def get_identifier(cls):
                """Incorrect docstring"""
                return cls.name.lower()

            identifier = class_property(get_identifier, doc="Object identifier")

        self.check_class(Foo, has_getter=True, has_docstring=True)
