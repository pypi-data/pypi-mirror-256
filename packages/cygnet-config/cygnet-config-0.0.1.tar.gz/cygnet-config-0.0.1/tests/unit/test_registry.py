import pytest
from config import register
from config._registry import Registry


@pytest.fixture
def registry():
    return Registry()


class TestRegistry:
    def test_has_dict_api(self):
        registry = Registry()
        assert isinstance(registry, dict)

    def test_getting_missing_item_raises(self):
        registry = Registry()
        registry.register_missing("MyFoo", missing_library="foo_library")
        with pytest.raises(ValueError) as error:
            registry["MyFoo"]
            assert "foo_library" in error.msg

    def test_missing_registry_has_priority(self):
        registry = Registry()
        registry.register_missing("MyFoo", missing_library="foo_library")
        registry["MyFoo"] = lambda x: x
        with pytest.raises(ValueError) as error:
            registry["MyFoo"]
            assert "foo_library" in error.msg

    def test_missing_item_considered_in_registry(self):
        registry = Registry()
        registry.register_missing("MyFoo", missing_library="foo_library")
        assert "MyFoo" in registry


class TestRegistryAPI:
    def test_register_adds_function_to_registry(self, registry):
        @register(registry=registry)
        def foo(X, y):
            return "foo", X

        assert registry["foo"] == foo

    def test_can_override_function_name(self, registry):
        @register(name="bar", registry=registry)
        def foo(X, y):
            return X, y

        assert registry["bar"] == foo
        assert foo.__name__ == "bar"

    def test_can_register_using_function_call(self, registry):
        def foo(X=None, y=3):
            return X, y

        register(foo, registry=registry)
        assert registry["foo"] == foo
        register(foo, name="zoo", bar="hello, {}".format, registry=registry)
        assert registry["zoo"].bar("world") == "hello, world"
        assert registry["zoo"] == foo

    def test_can_set_attributes_using_kwargs(self, registry):
        @register(bar=123, buzz=lambda x: x + 1, registry=registry)
        def foo(X, y):
            return X, y

        assert registry["foo"].bar == 123
        assert registry["foo"].buzz(4) == 5
