from unittest.mock import Mock

from more_properties import cached_static_property
from tests.class_property.test_static_property import TestStaticProperty


class TestCachedStaticProperty(TestStaticProperty):
    static_property = cached_static_property

    def test_cached_static_property_basic(self):
        m = Mock()

        class Foo:
            var_cache = "Value"

            @self.static_property
            def var():
                """Object identifier"""
                m()
                return Foo.var_cache

        with self.subTest("Value cached"):
            for _ in range(3):
                self.assertEqual("Value", Foo.var)
                self.assertEqual("Value", Foo().var)

            m.assert_called_once_with()

        with self.subTest("Cache is shared"):
            m.reset_mock()

            class Bar(Foo):
                var_cache = "Another value"

            for _ in range(3):
                self.assertEqual("Value", Foo.var)
                self.assertEqual("Value", Bar.var)

            m.assert_not_called()


del TestStaticProperty
