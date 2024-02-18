from config import registry

from .hello import foo, goo


class TestRegistry:
    def test_hello_functions_are_registered(self):
        assert registry["foo"] == foo
        assert registry["buzz"] == goo
