from dataclasses import dataclass
from typing import Optional
from unittest.mock import Mock

from more_properties import cached_property
from tests.test_property import TestProperty


class TestCachedProperty(TestProperty):
    property = cached_property

    def test_cached_property_basic(self):
        m = Mock()

        @dataclass
        class Index:
            i: Optional[int] = None

            @self.property
            def i1(self):
                """1 based index"""
                m(self)
                return self.i + 1 if self.i is not None else None

        index = Index(0)

        with self.subTest("Value cached"):
            self.assertEqual(1, index.i1)
            self.assertEqual(1, index.i1)
            self.assertEqual(1, index.i1)

            m.assert_called_once_with(index)

        with self.subTest("Cache is per object"):
            m.reset_mock()

            another_index = Index(10)

            for _ in range(3):
                self.assertEqual(1, index.i1)
                self.assertEqual(11, another_index.i1)

            m.assert_called_once_with(another_index)


del TestProperty
