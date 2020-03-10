from itertools import product
from unittest import TestCase

from more_properties import static_property


class TestStaticProperty(TestCase):
    static_property = static_property

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
                self.assertEqual("Initial value", cls.var)
                self.assertEqual("Initial value", cls().var)
            else:
                with self.assertRaisesRegex(AttributeError, "unreadable attribute"):
                    cls.var

                with self.assertRaisesRegex(AttributeError, "unreadable attribute"):
                    cls().var

        with self.subTest("Setter"):
            if has_setter:
                cls().var = "New value"
                self.assertEqual("New value", cls.var_cache)
            else:
                with self.assertRaisesRegex(AttributeError, "can't set attribute"):
                    cls().var = "New value"

        with self.subTest("Deleter"):
            if has_deleter:
                del cls().var
                self.assertEqual(None, cls.var_cache)
            else:
                with self.assertRaisesRegex(AttributeError, "can't delete attribute"):
                    del cls().var

        with self.subTest("Docstring"):
            self.assertEqual(
                "Object identifier" if has_docstring else None,
                cls.__dict__.get("var").__doc__,
            )

    def test_static_property_basic(self):
        class Foo:
            var_cache = "Initial value"

            @self.static_property
            def var():
                """Object identifier"""
                return Foo.var_cache

            @var.setter
            def var(value):
                Foo.var_cache = value

            @var.deleter
            def var():
                Foo.var_cache = None

        with self.subTest(cls=Foo):
            self.check_class(
                Foo,
                has_getter=True,
                has_setter=True,
                has_deleter=True,
                has_docstring=True,
            )

        class Bar(Foo):
            pass

        with self.subTest("Subclass shares value forwards"):
            Foo().var = "Another value"
            self.assertEqual("Another value", Bar.var)

        with self.subTest("Subclass shares value backwards"):
            Bar().var = "Yet another value"
            self.assertEqual("Yet another value", Foo.var)

    def test_static_property_inline_definition(self):
        class Foo:
            var_cache = "Initial value"

            @staticmethod
            def get_var():
                return Foo.var_cache

            @staticmethod
            def set_var(value):
                Foo.var_cache = value

            @staticmethod
            def del_var():
                Foo.var_cache = None

            var = self.static_property(get_var, set_var, del_var, "Object identifier")

        self.check_class(
            Foo, has_getter=True, has_setter=True, has_deleter=True, has_docstring=True,
        )

    def test_static_property_missing_components(self):
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
                    var_cache = "Initial value"

                    @staticmethod
                    def get_var():
                        return Foo.var_cache

                    @staticmethod
                    def set_var(value):
                        Foo.var_cache = value

                    @staticmethod
                    def del_var():
                        Foo.var_cache = None

                    var = self.static_property(
                        fget=get_var if has_getter else None,
                        fset=set_var if has_setter else None,
                        fdel=del_var if has_deleter else None,
                        doc="Object identifier" if has_docstring else None,
                    )

                self.check_class(
                    Foo, has_getter, has_setter, has_deleter, has_docstring
                )

    def test_static_property_docstring_priority(self):
        class Foo:
            var_cache = "Initial value"

            @staticmethod
            def get_var():
                """Incorrect docstring"""
                return Foo.var_cache

            var = self.static_property(get_var, doc="Object identifier")

        self.check_class(Foo, has_getter=True, has_docstring=True)
