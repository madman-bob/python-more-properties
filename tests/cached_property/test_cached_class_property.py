from unittest.mock import Mock

from more_properties import cached_class_property
from tests.class_property.test_class_property import TestClassProperty


class TestCachedClassProperty(TestClassProperty):
    class_property = cached_class_property

    def test_cached_class_property_basic(self):
        m = Mock()

        class Foo:
            name = "Foo"

            @self.class_property
            def identifier(cls):
                """Object identifier"""
                m(cls)
                return cls.name.lower()

        with self.subTest("Value cached"):
            for _ in range(3):
                self.assertEqual("foo", Foo.identifier)
                self.assertEqual("foo", Foo().identifier)

            m.assert_called_once_with(Foo)

        with self.subTest("Cache is per class"):
            m.reset_mock()

            class Bar(Foo):
                name = "Bar"

            for _ in range(3):
                self.assertEqual("foo", Foo.identifier)
                self.assertEqual("bar", Bar.identifier)

            m.assert_called_once_with(Bar)


del TestClassProperty
