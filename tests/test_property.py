from dataclasses import dataclass
from itertools import product
from typing import Optional
from unittest import TestCase

from more_properties import property


class TestProperty(TestCase):
    property = property

    def check_class(
        self,
        cls,
        has_getter=False,
        has_setter=False,
        has_deleter=False,
        has_docstring=False,
    ):
        with self.subTest("Getter"):
            index = cls(10)

            if has_getter:
                self.assertEqual(11, index.i1)
            else:
                with self.assertRaisesRegex(AttributeError, "unreadable attribute"):
                    index.i1

        with self.subTest("Setter"):
            index = cls(10)

            if has_setter:
                index.i1 = 20
                self.assertEqual(19, index.i)
            else:
                with self.assertRaisesRegex(AttributeError, "can't set attribute"):
                    index.i1 = 20

        with self.subTest("Deleter"):
            index = cls(10)

            if has_deleter:
                del index.i1
                self.assertEqual(None, index.i)
            else:
                with self.assertRaisesRegex(AttributeError, "can't delete attribute"):
                    del index.i1

        with self.subTest("Docstring"):
            self.assertEqual(
                "1 based index" if has_docstring else None, cls.__dict__["i1"].__doc__
            )

    def test_property_basic(self):
        @dataclass
        class Index:
            i: Optional[int] = None

            @self.property
            def i1(self):
                """1 based index"""
                return self.i + 1 if self.i is not None else None

            @i1.setter
            def i1(self, value):
                self.i = value - 1 if value is not None else None

            @i1.deleter
            def i1(self):
                self.i = None

        self.check_class(
            Index,
            has_getter=True,
            has_setter=True,
            has_deleter=True,
            has_docstring=True,
        )

    def test_property_inline_definition(self):
        @dataclass
        class Index:
            i: Optional[int] = None

            def get_i1(self):
                return self.i + 1 if self.i is not None else None

            def set_i1(self, value):
                self.i = value - 1 if value is not None else None

            def del_i1(self):
                self.i = None

            i1 = self.property(get_i1, set_i1, del_i1, "1 based index")

        self.check_class(
            Index,
            has_getter=True,
            has_setter=True,
            has_deleter=True,
            has_docstring=True,
        )

    def test_property_missing_components(self):
        for has_getter, has_setter, has_deleter, has_docstring in product(
            [False, True], repeat=4
        ):
            with self.subTest(
                has_getter=has_getter,
                has_setter=has_setter,
                has_deleter=has_deleter,
                has_docstring=has_docstring,
            ):

                @dataclass
                class Index:
                    i: Optional[int] = None

                    def get_i1(self):
                        return self.i + 1 if self.i is not None else None

                    def set_i1(self, value):
                        self.i = value - 1 if value is not None else None

                    def del_i1(self):
                        self.i = None

                    i1 = self.property(
                        fget=get_i1 if has_getter else None,
                        fset=set_i1 if has_setter else None,
                        fdel=del_i1 if has_deleter else None,
                        doc="1 based index" if has_docstring else None,
                    )

                self.check_class(
                    Index, has_getter, has_setter, has_deleter, has_docstring
                )

    def test_property_docstring_priority(self):
        @dataclass
        class Index:
            i: Optional[int] = None

            def get_i1(self):
                """Incorrect docstring"""
                return self.i + 1 if self.i is not None else None

            i1 = self.property(get_i1, doc="1 based index")

        self.check_class(Index, has_getter=True, has_docstring=True)
