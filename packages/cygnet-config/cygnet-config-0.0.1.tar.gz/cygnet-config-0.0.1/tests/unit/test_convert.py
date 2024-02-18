import math
import typing as t
from dataclasses import dataclass
from pathlib import Path

import pytest
from attrs import define
from cattrs.errors import IterableValidationError, StructureHandlerNotFoundError
from config import register
from config.convert import (
    Converter,
)
from config.utils import save


@register
@define
class MockAttrs:
    a: str
    b: int


@define
class MockCallable:
    a: str
    b: int

    def __call__(self, c: int) -> int:
        return c + self.b


@dataclass
class MockDataClass:
    a: str
    b: int


class MockClass:
    def __init__(self, a: str, b: int):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"MockClass(a={self.a}, b={self.b})"


class MockBareClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f"MockBareClass(a={self.a}, b={self.b})"


def mock_function(a: int, b: str):
    ...


class MockAnnotated:
    def __init__(
        self,
        hello,
        foo: int,
        bar: str = "test",
        numbers: t.Optional[t.List[float]] = None,
        container: t.Optional[t.Dict[str, int]] = None,
    ):
        self.hello = hello
        self.foo = foo
        self.bar = bar
        self.numbers = numbers or []
        self.container = container or {}


class MyProtocol(t.Protocol):
    pass


class MyComplexClass:
    def __init__(self, a: MockAttrs, b: MyProtocol, c: t.Callable | None = None):
        self.a = a
        self.b = b
        self.c = c


class TestConverter:
    def test_deprioritized_hook_tested_last(self):
        c = Converter(add_class_hook=False, add_protocol_hook=False)
        c.register_deprioritized_structure_hook_func(
            lambda _: True, lambda d, cl: cl(a=d["a"], b=d["b"] + 1)
        )
        data = {"a": "a", "b": 2}
        assert c.structure(data, MockAttrs) == MockAttrs(**data)
        assert c.structure(data, MockDataClass) == MockDataClass(**data)
        out = c.structure(data, MockBareClass)
        assert out.a == "a"
        assert out.b == 3

    def test_deprioritized_hook_preserves_fallback(self):
        c = Converter(add_class_hook=False, add_protocol_hook=False)
        c.register_deprioritized_structure_hook_func(
            lambda cl: getattr(cl, "custom", False),
            lambda d, cl: cl(a=d["a"], b=d["b"] + 1),
        )
        data = {"a": "a", "b": 2}
        with pytest.raises(StructureHandlerNotFoundError):
            c.structure(data, MockBareClass)

    def test_deprioritized_hook_does_not_clobber(self):
        c = Converter(add_class_hook=False, add_protocol_hook=False)
        c.register_deprioritized_structure_hook_func(
            lambda _: True, lambda d, cl: cl(a=d["a"], b=d["b"] + 1)
        )
        c.register_deprioritized_structure_hook_func(
            lambda cl: getattr(cl, "custom", False),
            lambda d, cl: cl(a=d["a"], b=d["b"] + 1),
        )
        data = {"a": "a", "b": 2}
        out = c.structure(data, MockBareClass)
        assert out.a == "a"
        assert out.b == 3

    def test_structure_handles_optional_types_by_passthrough(self):
        c = Converter()
        source = {"__type__": MockAttrs, "a": "hello", "b": 2}
        result = c.structure(source, MyProtocol | None)
        assert result == MockAttrs(a="hello", b=2)
        result = c.structure(None, MyProtocol | None)
        assert result is None
        data = {"a": "a", "b": 2}
        result = c.structure(data, MockBareClass | None)
        assert result.a == "a"
        assert result.b == 2
        result = c.structure(None, MockBareClass | None)
        assert result is None
        result = c.structure("tests.unit.test_convert.mock_function", t.Callable | None)
        assert result == mock_function
        result = c.structure(None, t.Callable | None)
        assert result is None

    def test_structure_recursively_builds_classes(self):
        source = {
            "a": {"a": "a", "b": 1},
            "b": {
                "__type__": "tests.unit.test_convert.MyComplexClass",
                "a": {"a": "a2", "b": 2},
                "b": {
                    "__type__": "tests.unit.test_convert.MockAttrs",
                    "a": "a3",
                    "b": 3,
                },
            },
            "c": "tests.unit.test_convert.mock_function",
        }
        result = Converter().structure(source, MyComplexClass)
        assert result.a == MockAttrs(a="a", b=1)
        assert isinstance(result.b, MyComplexClass)
        assert result.b.a == MockAttrs(a="a2", b=2)
        assert result.b.b == MockAttrs(a="a3", b=3)


class TestConverter_structure_annotated_class:
    def test_raises_if_missing_required_param(self):
        with pytest.raises(TypeError):
            Converter().structure_annotated_class(
                {"foo": 5, "bar": "bar"}, MockAnnotated
            )

    def test_class_initialized_with_given_parameters(self):
        params = {"hello": "there", "foo": 5, "bar": "bar"}
        out = Converter().structure_annotated_class(params, MockAnnotated)
        assert isinstance(out, MockAnnotated)
        assert out.hello == "there"
        assert out.foo == 5
        assert out.bar == "bar"

    def test_raises_for_type_mismatch(self):
        with pytest.raises(ValueError):
            Converter().structure_annotated_class(
                {"hello": "there", "foo": "not an int"}, MockAnnotated
            )

    def test_coerces_args_to_annotated_types(self):
        c = Converter().structure_annotated_class(
            {"hello": "there", "foo": "3"}, MockAnnotated
        )
        assert c.foo == 3

    def test_coerces_list_types(self):
        c = Converter().structure_annotated_class(
            {"hello": "there", "foo": 3, "numbers": ["1", 2.3, "4"]}, MockAnnotated
        )
        assert c.numbers == [1.0, 2.3, 4]
        with pytest.raises(IterableValidationError):
            Converter().structure_annotated_class(
                {"hello": "there", "foo": 3, "numbers": [1, 2.3, "x"]}, MockAnnotated
            )

    def test_validates_dict_types(self):
        c = Converter().structure_annotated_class(
            {"hello": "there", "foo": 3, "container": {"a": 1, "b": "2"}}, MockAnnotated
        )
        assert c.container == {"a": 1, "b": 2}
        with pytest.raises(IterableValidationError):
            c = Converter().structure_annotated_class(
                {"hello": "there", "foo": 3, "container": {"a": "x", "b": 2}},
                MockAnnotated,
            )

    def test_validates_kwargs(self):
        class KWargClass:
            def __init__(self, foo: float, **kwargs: int):
                self.foo = foo
                self.kwargs = kwargs

        c = Converter().structure_annotated_class(
            {"foo": 2.3, "bar": 3, "baz": 2.2}, KWargClass
        )
        assert c.foo == 2.3
        assert c.kwargs == {"bar": 3, "baz": 2}

        with pytest.raises(ValueError):
            Converter().structure_annotated_class(
                {"foo": 2.3, "bar": "not an int"}, KWargClass
            )

    def test_recursively_validates_classes(self):
        class DeepClass:
            def __init__(self, foo: MockAnnotated):
                self.foo = foo

        c = Converter().structure_annotated_class(
            {"foo": {"hello": "there", "foo": 3}}, DeepClass
        )
        assert c.foo.hello == "there"
        assert c.foo.foo == 3

    def test_string_matching_path_to_file_is_loaded_as_params(self, tmp_path):
        config_path = tmp_path / "config.yaml"
        params = {"hello": "there", "foo": 3}
        save(params, config_path)
        c = Converter().structure_annotated_class(str(config_path), MockAnnotated)
        assert isinstance(c, MockAnnotated)
        assert c.hello == "there"
        assert c.foo == 3

    def test_string_types_not_checked_for_config_file_loading(self, tmp_path):
        config_path = tmp_path / "config.yaml"
        params = {"hello": "there", "foo": 3}
        save(params, config_path)
        c = Converter().structure_annotated_class(str(config_path), str)
        assert c == str(config_path)

    def test_Path_types_not_checked_for_config_file_loading(self, tmp_path):
        config_path = tmp_path / "config.yaml"
        params = {"hello": "there", "foo": 3}
        save(params, config_path)
        c = Converter().structure_annotated_class(str(config_path), Path)
        assert c == config_path


def my_test_func(*, foo: int, bar: str = "test"):
    pass


my_constant = "hello"


class TestConverter_structure_callable:
    def test_instantiates_function_from_importable_string(self):
        f = Converter().structure_callable("math.sqrt", t.Callable[[float], float])
        assert f == math.sqrt

    def test_instantiates_callable_class_from_source_dict(self):
        source = {"__type__": MockCallable, "a": "foo", "b": 1}
        m = Converter().structure_callable(source, t.Callable)
        assert m == MockCallable(a="foo", b=1)

    def test_raises_if_instantiates_noncallable_class(self):
        source = {"__type__": MockAttrs, "a": "foo", "b": 1}
        with pytest.raises(ValueError):
            Converter().structure_callable(source, t.Callable)

    def test_raises_if_structured_object_is_not_callable(self):
        with pytest.raises(ValueError):
            Converter().structure_callable(
                "tests.unit.test_convert.my_constant", t.Callable[[float], float]
            )


class TestConverter_structure_protocol:
    def test_instantiates_class_given_by_type(self):
        c = Converter().structure_protocol(
            {"a": "a", "b": 2, "__type__": MockAttrs}, t.Protocol
        )
        assert c == MockAttrs(a="a", b=2)

    def test_can_specify_type_field(self):
        c = Converter(type_field="--type").structure_protocol(
            {"a": "a", "b": 2, "--type": MockAttrs}, t.Protocol
        )
        assert c == MockAttrs(a="a", b=2)

    def test_dispatches_source_string(self):
        c = Converter().structure_protocol(
            {"__type__": "tests.unit.test_convert.MockAttrs", "a": "a", "b": 2},
            t.Protocol,
        )
        assert c == MockAttrs(a="a", b=2)

    def test_dispatches_from_registry_if_possible(self):
        c = Converter().structure_protocol(
            {"__type__": "MockAttrs", "a": "hello", "b": 1}, t.Protocol
        )
        assert c == MockAttrs(a="hello", b=1)

    def test_validates_class_satisfies_protocol(self):
        @t.runtime_checkable
        class MyProtocol(t.Protocol):
            def custom_func(self, a, b):
                ...

        @define
        class MockMyProtocalAttrs:
            a: str
            b: int

            def custom_func(self, a, b):
                pass

        c = Converter().structure_protocol(
            {"a": "a", "b": 2, "__type__": MockMyProtocalAttrs}, MyProtocol
        )
        assert c == MockMyProtocalAttrs(a="a", b=2)

        with pytest.raises(ValueError):
            Converter().structure_protocol(
                {"a": "a", "b": 2, "__type__": MockAttrs}, MyProtocol
            )

    def test_dispatchable_string_is_used_as_source(self):
        class MyCallback(t.Protocol):
            def __call__(self, a, b):
                ...

        c = Converter().structure_protocol(
            "tests.unit.test_convert.mock_function", MyCallback
        )
        assert c == mock_function

    def test_string_matching_path_to_file_is_loaded_as_params(self, tmp_path):
        config_path = tmp_path / "config.yaml"
        params = {
            "a": "a",
            "b": 2,
            "__type__": "tests.unit.test_convert.MockAttrs",
        }
        save(params, config_path)
        c = Converter().structure_protocol(str(config_path), t.Protocol)
        print(c)
        assert c == MockAttrs(a="a", b=2)
